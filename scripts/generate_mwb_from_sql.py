#!/usr/bin/env python3
"""Generate native Workbench-style .mwb archives from SQL structure dumps.

The script is intentionally self-contained and avoids any dependency on
MySQL Workbench itself. It parses the existing *_struktur_*.sql dumps,
builds a compact Workbench model tree, and writes a .mwb archive that
contains the required native container entries.
"""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import re
import shutil
import tempfile
import uuid
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass, field


DEFAULT_INPUT_DIR = pathlib.Path("generated/klassenarbeiten")
DEFAULT_OUTPUT_GUIDE = DEFAULT_INPUT_DIR / "WORKBENCH-MWB-WORKFLOW.md"
DEFAULT_REFERENCE_ARCHIVE = pathlib.Path(
    "uploads/pruefungsaufgaben-und-erwartungshorizonte-fuer-ki-training/mwb-dateien/betreuung.mwb"
)
WORKBENCH_MODEL_VERSION = "1.4.4"
WORKBENCH_GRT_FORMAT = "2.0"
WORKBENCH_DOC_TYPE = "MySQL Workbench Model"
WORKBENCH_CHARSET = "utf8"
WORKBENCH_COLLATION = "utf8_general_ci"
UUID_NAMESPACE = uuid.UUID("0d04b8f0-59a9-4c64-b0a6-cc8f8be4fd50")


@dataclass(frozen=True)
class ColumnSpec:
    name: str
    sql_type: str
    nullable: bool = True
    primary_key: bool = False
    unique: bool = False
    auto_increment: bool = False
    default_value: str | None = None


@dataclass(frozen=True)
class ForeignKeySpec:
    name: str
    columns: list[str]
    referenced_table: str
    referenced_columns: list[str]
    update_rule: str = "RESTRICT"
    delete_rule: str = "RESTRICT"


@dataclass(frozen=True)
class IndexSpec:
    name: str
    columns: list[str]
    unique: bool = False
    primary: bool = False


@dataclass
class TableSpec:
    name: str
    columns: list[ColumnSpec] = field(default_factory=list)
    foreign_keys: list[ForeignKeySpec] = field(default_factory=list)
    indexes: list[IndexSpec] = field(default_factory=list)

    def ensure_covering_indexes(self) -> None:
        existing = {tuple(index.columns): index for index in self.indexes}

        primary_columns = [column.name for column in self.columns if column.primary_key]
        if primary_columns and tuple(primary_columns) not in existing:
            self.indexes.insert(0, IndexSpec(name="PRIMARY", columns=primary_columns, unique=True, primary=True))

        for fk in self.foreign_keys:
            key = tuple(fk.columns)
            if key not in existing:
                index_name = f"{fk.name}_idx"
                self.indexes.append(IndexSpec(name=index_name, columns=list(fk.columns)))


@dataclass(frozen=True)
class SqlModel:
    source_sql: pathlib.Path
    database_name: str
    schema_name: str
    tables: list[TableSpec]


CREATE_TABLE_RE = re.compile(r"^CREATE\s+TABLE(?:\s+IF\s+NOT\s+EXISTS)?\s+`?([^`\s(]+)`?\s*\($", re.IGNORECASE)
CREATE_DATABASE_RE = re.compile(r"^CREATE\s+(?:DATABASE|SCHEMA)(?:\s+IF\s+NOT\s+EXISTS)?\s+`?([^`;\s]+)`?", re.IGNORECASE)
USE_RE = re.compile(r"^USE\s+`?([^`;\s]+)`?;?$", re.IGNORECASE)
PRIMARY_KEY_RE = re.compile(r"^PRIMARY\s+KEY\s*\((?P<columns>[^)]+)\)$", re.IGNORECASE)
UNIQUE_KEY_RE = re.compile(
    r"^UNIQUE\s+(?:KEY|INDEX)?\s*`?(?P<name>[^`(\s]+)?`?\s*\((?P<columns>[^)]+)\)$",
    re.IGNORECASE,
)
KEY_RE = re.compile(r"^(?:KEY|INDEX)\s+`?(?P<name>[^`(\s]+)`?\s*\((?P<columns>[^)]+)\)$", re.IGNORECASE)
FOREIGN_KEY_RE = re.compile(
    r"^CONSTRAINT\s+`?(?P<name>[^`\s]+)`?\s+FOREIGN\s+KEY\s*\((?P<columns>[^)]+)\)\s+REFERENCES\s+`?(?P<table>[^`\s(]+)`?\s*\((?P<ref_columns>[^)]+)\)(?P<actions>.*)$",
    re.IGNORECASE,
)
COLUMN_RE = re.compile(
    r"^`?(?P<name>[^`\s(]+)`?\s+(?P<type>[A-Za-z0-9_]+(?:\([^)]*\))?)(?P<rest>.*)$",
    re.IGNORECASE,
)
DEFAULT_RE = re.compile(r"\bDEFAULT\s+(?P<value>(?:'[^']*')|(?:\S+))", re.IGNORECASE)


def normalize_identifier(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_]+", "_", value.strip().lower())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned or "model"


def deterministic_uuid(*parts: str) -> str:
    return "{" + str(uuid.uuid5(UUID_NAMESPACE, "::".join(parts))).upper() + "}"


def split_identifiers(value: str) -> list[str]:
    return [part.strip().strip("`") for part in value.split(",") if part.strip()]


def parse_sql_dump(path: pathlib.Path) -> SqlModel:
    database_name = path.stem
    schema_name = database_name.split("_struktur_")[0]
    tables: list[TableSpec] = []

    lines = path.read_text(encoding="utf-8").splitlines()
    current_table_name: str | None = None
    current_table_lines: list[str] = []

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("--"):
            continue

        create_database_match = CREATE_DATABASE_RE.match(line)
        if create_database_match:
            database_name = create_database_match.group(1).strip("`")
            continue

        use_match = USE_RE.match(line)
        if use_match:
            database_name = use_match.group(1).strip("`")
            continue

        if current_table_name is None:
            table_match = CREATE_TABLE_RE.match(line)
            if table_match:
                current_table_name = table_match.group(1).strip("`")
                current_table_lines = []
            continue

        if line.startswith(")"):
            tables.append(parse_table(current_table_name, current_table_lines))
            current_table_name = None
            current_table_lines = []
            continue

        current_table_lines.append(line.rstrip(","))

    if current_table_name is not None:
        tables.append(parse_table(current_table_name, current_table_lines))

    for table in tables:
        table.ensure_covering_indexes()

    return SqlModel(
        source_sql=path,
        database_name=database_name,
        schema_name=normalize_identifier(schema_name),
        tables=tables,
    )


def parse_table(name: str, lines: list[str]) -> TableSpec:
    columns: list[ColumnSpec] = []
    foreign_keys: list[ForeignKeySpec] = []
    indexes: list[IndexSpec] = []
    primary_key_columns: list[str] = []

    for line in lines:
        if not line:
            continue

        primary_match = PRIMARY_KEY_RE.match(line)
        if primary_match:
            primary_key_columns = split_identifiers(primary_match.group("columns"))
            continue

        fk_match = FOREIGN_KEY_RE.match(line)
        if fk_match:
            actions = fk_match.group("actions") or ""
            foreign_keys.append(
                ForeignKeySpec(
                    name=fk_match.group("name").strip("`"),
                    columns=split_identifiers(fk_match.group("columns")),
                    referenced_table=fk_match.group("table").strip("`"),
                    referenced_columns=split_identifiers(fk_match.group("ref_columns")),
                    update_rule=_extract_rule(actions, "UPDATE") or "RESTRICT",
                    delete_rule=_extract_rule(actions, "DELETE") or "RESTRICT",
                )
            )
            continue

        unique_match = UNIQUE_KEY_RE.match(line)
        if unique_match:
            unique_name = unique_match.group("name")
            columns_in_index = split_identifiers(unique_match.group("columns"))
            indexes.append(
                IndexSpec(
                    name=unique_name.strip("`") if unique_name else f"uq_{name}_{'_'.join(columns_in_index)}",
                    columns=columns_in_index,
                    unique=True,
                )
            )
            continue

        key_match = KEY_RE.match(line)
        if key_match:
            indexes.append(
                IndexSpec(
                    name=key_match.group("name").strip("`"),
                    columns=split_identifiers(key_match.group("columns")),
                )
            )
            continue

        column_match = COLUMN_RE.match(line)
        if column_match:
            column_name = column_match.group("name").strip("`")
            column_type = column_match.group("type").upper()
            rest = column_match.group("rest") or ""
            is_primary = "PRIMARY KEY" in rest.upper()
            is_unique = "UNIQUE" in rest.upper() and not is_primary
            is_not_null = "NOT NULL" in rest.upper() or is_primary
            auto_increment = "AUTO_INCREMENT" in rest.upper()
            default_match = DEFAULT_RE.search(rest)
            default_value = default_match.group("value") if default_match else None

            columns.append(
                ColumnSpec(
                    name=column_name,
                    sql_type=column_type,
                    nullable=not is_not_null,
                    primary_key=is_primary,
                    unique=is_unique,
                    auto_increment=auto_increment,
                    default_value=default_value,
                )
            )
            if is_primary and column_name not in primary_key_columns:
                primary_key_columns.append(column_name)

    if primary_key_columns:
        primary_names = set(primary_key_columns)
        columns = [
            ColumnSpec(
                name=column.name,
                sql_type=column.sql_type,
                nullable=column.nullable,
                primary_key=column.name in primary_names,
                unique=column.unique,
                auto_increment=column.auto_increment,
                default_value=column.default_value,
            )
            for column in columns
        ]

    table = TableSpec(name=name, columns=columns, foreign_keys=foreign_keys, indexes=indexes)
    if primary_key_columns:
        table.indexes.insert(0, IndexSpec(name="PRIMARY", columns=primary_key_columns, unique=True, primary=True))
    return table


def _extract_rule(actions: str, keyword: str) -> str | None:
    match = re.search(rf"ON\s+{keyword}\s+(CASCADE|RESTRICT|SET\s+NULL|NO\s+ACTION)", actions, re.IGNORECASE)
    if not match:
        return None
    return re.sub(r"\s+", " ", match.group(1).upper())


def build_document_xml(model: SqlModel) -> bytes:
    root = ET.Element(
        "data",
        {
            "grt_format": WORKBENCH_GRT_FORMAT,
            "document_type": WORKBENCH_DOC_TYPE,
            "version": WORKBENCH_MODEL_VERSION,
        },
    )

    document = add_object(root, "workbench.Document", deterministic_uuid(model.schema_name, "document"))
    info = add_object(document, "app.DocumentInfo", deterministic_uuid(model.schema_name, "info"), key="info")
    add_string(info, "caption", model.schema_name)
    add_string(info, "title", f"{model.schema_name} model")
    add_string(info, "notes", f"Generated from {model.source_sql.name}")

    physical_models = add_object(
        document,
        "workbench.physical.Model",
        deterministic_uuid(model.schema_name, "physical-model"),
        key="physicalModels",
    )
    add_string(physical_models, "name", model.schema_name)
    add_string(physical_models, "modelType", "physical")

    catalog = add_object(physical_models, "db.mysql.Catalog", deterministic_uuid(model.schema_name, "catalog"), key="catalog")
    schemata = add_container(catalog, "schemata", "db.mysql.Schema")
    schema = add_object(schemata, "db.mysql.Schema", deterministic_uuid(model.schema_name, "schema"))
    add_string(schema, "name", model.schema_name)
    add_string(schema, "defaultCharacterSetName", WORKBENCH_CHARSET)
    add_string(schema, "defaultCollationName", WORKBENCH_COLLATION)

    tables_container = add_container(schema, "tables", "db.mysql.Table")
    for table in model.tables:
        table_obj = add_object(tables_container, "db.mysql.Table", deterministic_uuid(model.schema_name, "table", table.name))
        add_string(table_obj, "name", table.name)
        add_string(table_obj, "engine", "InnoDB")
        add_string(table_obj, "comment", "")

        columns_container = add_container(table_obj, "columns", "db.mysql.Column")
        for column in table.columns:
            column_obj = add_object(
                columns_container,
                "db.mysql.Column",
                deterministic_uuid(model.schema_name, "column", table.name, column.name),
            )
            add_string(column_obj, "name", column.name)
            add_string(column_obj, "simpleType", column.sql_type)
            add_bool(column_obj, "isNotNull", not column.nullable)
            add_bool(column_obj, "autoIncrement", column.auto_increment)
            if column.default_value is not None:
                add_string(column_obj, "defaultValue", column.default_value)
            add_bool(column_obj, "isPrimary", column.primary_key)
            add_bool(column_obj, "isUnique", column.unique)

        foreign_keys_container = add_container(table_obj, "foreignKeys", "db.mysql.ForeignKey")
        for fk in table.foreign_keys:
            fk_obj = add_object(
                foreign_keys_container,
                "db.mysql.ForeignKey",
                deterministic_uuid(model.schema_name, "fk", table.name, fk.name),
            )
            add_string(fk_obj, "name", fk.name)
            add_string(fk_obj, "referencedTable", fk.referenced_table)
            add_string(fk_obj, "referencedTableSchema", model.schema_name)
            add_string(fk_obj, "updateRule", fk.update_rule)
            add_string(fk_obj, "deleteRule", fk.delete_rule)
            fk_columns = add_container(fk_obj, "columns", "db.mysql.ForeignKeyColumn")
            for source_column, target_column in zip(fk.columns, fk.referenced_columns):
                fk_column = add_object(
                    fk_columns,
                    "db.mysql.ForeignKeyColumn",
                    deterministic_uuid(model.schema_name, "fk-column", table.name, fk.name, source_column, target_column),
                )
                add_string(fk_column, "name", source_column)
                add_string(fk_column, "referencedColumn", target_column)

        indices_container = add_container(table_obj, "indices", "db.mysql.Index")
        for index in table.indexes:
            index_obj = add_object(
                indices_container,
                "db.mysql.Index",
                deterministic_uuid(model.schema_name, "index", table.name, index.name),
            )
            add_string(index_obj, "name", index.name)
            add_bool(index_obj, "isPrimary", index.primary)
            add_bool(index_obj, "unique", index.unique)
            index_columns = add_container(index_obj, "columns", "db.mysql.IndexColumn")
            for column_name in index.columns:
                index_column = add_object(
                    index_columns,
                    "db.mysql.IndexColumn",
                    deterministic_uuid(model.schema_name, "index-column", table.name, index.name, column_name),
                )
                add_string(index_column, "name", column_name)

    indent_xml(root)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def add_object(parent: ET.Element, struct_name: str, object_id: str, key: str | None = None) -> ET.Element:
    attributes = {"type": "object", "struct-name": struct_name, "id": object_id}
    if key is not None:
        attributes["key"] = key
    return ET.SubElement(parent, "value", attributes)


def add_container(parent: ET.Element, key: str, content_struct_name: str) -> ET.Element:
    return ET.SubElement(parent, "value", {"key": key, "content-struct-name": content_struct_name})


def add_string(parent: ET.Element, key: str, value: str) -> ET.Element:
    element = ET.SubElement(parent, "value", {"type": "string", "key": key})
    element.text = value
    return element


def add_bool(parent: ET.Element, key: str, value: bool) -> ET.Element:
    element = ET.SubElement(parent, "value", {"type": "bool", "key": key})
    element.text = "true" if value else "false"
    return element


def indent_xml(element: ET.Element, level: int = 0) -> None:
    indent = "\n" + level * "  "
    if len(element):
        if not element.text or not element.text.strip():
            element.text = indent + "  "
        for child in element:
            indent_xml(child, level + 1)
        if not element[-1].tail or not element[-1].tail.strip():
            element[-1].tail = indent
    if level and (not element.tail or not element.tail.strip()):
        element.tail = indent


def load_container_template(reference_archive: pathlib.Path) -> tuple[bytes, bytes]:
    if not reference_archive.is_file():
        raise FileNotFoundError(f"Reference archive not found: {reference_archive}")

    with zipfile.ZipFile(reference_archive) as archive:
        lock_bytes = archive.read("lock")
        data_db_bytes = archive.read("@db/data.db")

    return lock_bytes, data_db_bytes


def write_mwb_archive(output_path: pathlib.Path, document_xml: bytes, lock_bytes: bytes, data_db_bytes: bytes) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_zip_path = pathlib.Path(temp_file.name)

    try:
        with zipfile.ZipFile(temp_zip_path, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("document.mwb.xml", document_xml)
            archive.writestr("lock", lock_bytes)
            archive.writestr("@db/data.db", data_db_bytes)
        shutil.move(str(temp_zip_path), output_path)
    finally:
        if temp_zip_path.exists():
            temp_zip_path.unlink(missing_ok=True)


def build_workflow_guide(models: list[tuple[SqlModel, pathlib.Path]], output_path: pathlib.Path) -> None:
    lines: list[str] = []
    lines.append("# Workflow: MWB-Dateien direkt aus SQL erzeugen")
    lines.append("")
    lines.append("Diese Datei wurde automatisch erzeugt mit:")
    lines.append("")
    lines.append("`bash scripts/prepare-workbench-mwb.sh`")
    lines.append("")
    lines.append("Die Generierung laeuft ohne MySQL Workbench. Sie liest die SQL-Strukturdumps, baut daraus native MWB-Archive und verwendet fuer die Containerstruktur eine Referenzvorlage aus dem Repository.")
    lines.append("")
    lines.append("## 1) Erzeugte Modelle")
    lines.append("")
    lines.append("| System | Schema | Quelle | Ziel-.mwb |")
    lines.append("|---|---|---|---|")

    for model, output_path_for_model in models:
        lines.append(f"| {model.schema_name} | {model.database_name} | {model.source_sql.as_posix()} | {output_path_for_model.as_posix()} |")

    lines.append("")
    lines.append("## 2) Validierung")
    lines.append("")
    lines.append("Die erzeugten Archive enthalten intern `document.mwb.xml`, `lock` und `@db/data.db`.")
    lines.append("")
    lines.append("Beispielpruefung:")
    lines.append("")
    lines.append("`bash scripts/validate-mwb-native.sh`")
    lines.append("")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def generate_models(input_dir: pathlib.Path, output_guide: pathlib.Path, reference_archive: pathlib.Path, only_system: str | None, force: bool) -> list[pathlib.Path]:
    models: list[tuple[SqlModel, pathlib.Path]] = []
    lock_bytes, data_db_bytes = load_container_template(reference_archive)

    known_systems = {
        pathlib.Path(name).stem.split("_struktur_")[0]
        for name in [path.name for path in input_dir.glob("*_struktur_*.sql")]
    }

    for struct_sql in sorted(input_dir.glob("*_struktur_*.sql")):
        system_name, year = parse_system_name_and_year(struct_sql.name)
        if only_system and system_name != only_system:
            continue

        model = parse_sql_dump(struct_sql)
        output_path = input_dir / f"{system_name}_{year}.mwb"
        if output_path.exists() and not force:
            output_path.unlink()

        document_xml = build_document_xml(model)
        write_mwb_archive(output_path, document_xml, lock_bytes, data_db_bytes)
        models.append((model, output_path))

    for system_name, fallback in manual_fallback_models(input_dir).items():
        if system_name in known_systems:
            continue
        if only_system and system_name != only_system:
            continue

        output_path = input_dir / f"{system_name}_2025.mwb"
        if output_path.exists() and not force:
            output_path.unlink()

        document_xml = build_document_xml(fallback)
        write_mwb_archive(output_path, document_xml, lock_bytes, data_db_bytes)
        models.append((fallback, output_path))

    if not models:
        raise RuntimeError(f"No matching *_struktur_*.sql files found in {input_dir}")

    build_workflow_guide(models, output_guide)
    return [output_path for _, output_path in models]


def parse_system_name_and_year(filename: str) -> tuple[str, str]:
    base = filename[:-4] if filename.lower().endswith(".sql") else filename
    if "_struktur_" not in base:
        raise ValueError(f"Unsupported SQL structure filename: {filename}")
    system_name, year = base.split("_struktur_", 1)
    return system_name, year


def manual_fallback_models(input_dir: pathlib.Path) -> dict[str, SqlModel]:
    return {
        "kursplattform": SqlModel(
            source_sql=input_dir / "KA02_BG12_2025_2026_VERSION1_lsg.md",
            database_name="kursplattform",
            schema_name="kursplattform",
            tables=_kursplattform_tables(),
        ),
        "lernlabor": SqlModel(
            source_sql=input_dir / "KA02_BG12_2025_2026_VERSION2_lsg.md",
            database_name="lernlabor",
            schema_name="lernlabor",
            tables=_lernlabor_tables(),
        ),
        "startupwerkstatt": SqlModel(
            source_sql=input_dir / "KA02_BG12_2025_2026_VERSION3_lsg.md",
            database_name="startupwerkstatt",
            schema_name="startupwerkstatt",
            tables=_startupwerkstatt_tables(),
        ),
    }


def _table(name: str, columns: list[ColumnSpec], foreign_keys: list[ForeignKeySpec] | None = None, indexes: list[IndexSpec] | None = None) -> TableSpec:
    table = TableSpec(name=name, columns=columns, foreign_keys=foreign_keys or [], indexes=indexes or [])
    table.ensure_covering_indexes()
    return table


def _kursplattform_tables() -> list[TableSpec]:
    return [
        _table(
            "mitglieder",
            [
                ColumnSpec("mitglied_id", "INT", nullable=False, primary_key=True),
                ColumnSpec("vorname", "VARCHAR(80)", nullable=False),
                ColumnSpec("nachname", "VARCHAR(80)", nullable=False),
                ColumnSpec("email", "VARCHAR(120)", nullable=False, unique=True),
                ColumnSpec("aktiv", "TINYINT", nullable=False, default_value="1"),
            ],
        ),
        _table(
            "dozenten",
            [
                ColumnSpec("dozent_id", "INT", nullable=False, primary_key=True),
                ColumnSpec("vorname", "VARCHAR(80)", nullable=False),
                ColumnSpec("nachname", "VARCHAR(80)", nullable=False),
                ColumnSpec("fachgebiet", "VARCHAR(120)", nullable=False),
                ColumnSpec("aktiv", "TINYINT", nullable=False, default_value="1"),
            ],
        ),
        _table(
            "kurse",
            [
                ColumnSpec("kurs_id", "INT", nullable=False, primary_key=True),
                ColumnSpec("titel", "VARCHAR(120)", nullable=False),
                ColumnSpec("beschreibung", "VARCHAR(255)", nullable=False),
                ColumnSpec("kategorie", "VARCHAR(80)", nullable=False),
                ColumnSpec("max_teilnehmer", "INT", nullable=False),
            ],
        ),
        _table(
            "termine",
            [
                ColumnSpec("termin_id", "INT", nullable=False, primary_key=True),
                ColumnSpec("kurs_id", "INT", nullable=False),
                ColumnSpec("startzeit", "DATETIME", nullable=False),
                ColumnSpec("endzeit", "DATETIME", nullable=False),
                ColumnSpec("raum", "VARCHAR(80)", nullable=False),
                ColumnSpec("status", "VARCHAR(40)", nullable=False),
            ],
            [ForeignKeySpec("fk_termine_kurse", ["kurs_id"], "kurse", ["kurs_id"])],
        ),
        _table(
            "anmeldungen",
            [
                ColumnSpec("anmeldung_id", "INT", nullable=False, primary_key=True),
                ColumnSpec("mitglied_id", "INT", nullable=False),
                ColumnSpec("termin_id", "INT", nullable=False),
                ColumnSpec("angemeldet_am", "DATETIME", nullable=False),
                ColumnSpec("status", "VARCHAR(40)", nullable=False),
            ],
            [
                ForeignKeySpec("fk_anmeldungen_mitglieder", ["mitglied_id"], "mitglieder", ["mitglied_id"]),
                ForeignKeySpec("fk_anmeldungen_termine", ["termin_id"], "termine", ["termin_id"]),
            ],
        ),
        _table(
            "kurs_dozent",
            [
                ColumnSpec("kurs_id", "INT", nullable=False, primary_key=True),
                ColumnSpec("dozent_id", "INT", nullable=False, primary_key=True),
                ColumnSpec("rolle", "VARCHAR(40)", nullable=False),
            ],
            [
                ForeignKeySpec("fk_kurs_dozent_kurs", ["kurs_id"], "kurse", ["kurs_id"]),
                ForeignKeySpec("fk_kurs_dozent_dozent", ["dozent_id"], "dozenten", ["dozent_id"]),
            ],
        ),
    ]


def _lernlabor_tables() -> list[TableSpec]:
    return [
        _table(
            "lernende",
            [
                ColumnSpec("lernende_id", "INT", nullable=False, primary_key=True),
                ColumnSpec("vorname", "VARCHAR(80)", nullable=False),
                ColumnSpec("nachname", "VARCHAR(80)", nullable=False),
                ColumnSpec("teamname", "VARCHAR(80)", nullable=False),
            ],
        ),
        _table(
            "teams",
            [
                ColumnSpec("team_id", "INT", nullable=False, primary_key=True),
                ColumnSpec("name", "VARCHAR(100)", nullable=False),
                ColumnSpec("status", "VARCHAR(40)", nullable=False),
            ],
        ),
        _table(
            "geraete",
            [
                ColumnSpec("geraet_id", "INT", nullable=False, primary_key=True),
                ColumnSpec("bezeichnung", "VARCHAR(120)", nullable=False),
                ColumnSpec("raum", "VARCHAR(80)", nullable=False),
                ColumnSpec("status", "VARCHAR(40)", nullable=False),
            ],
        ),
        _table(
            "workshops",
            [
                ColumnSpec("workshop_id", "INT", nullable=False, primary_key=True),
                ColumnSpec("titel", "VARCHAR(120)", nullable=False),
                ColumnSpec("thema", "VARCHAR(120)", nullable=False),
                ColumnSpec("max_teamgroesse", "INT", nullable=False),
            ],
        ),
        _table(
            "slots",
            [
                ColumnSpec("slot_id", "INT", nullable=False, primary_key=True),
                ColumnSpec("workshop_id", "INT", nullable=False),
                ColumnSpec("geraet_id", "INT", nullable=False),
                ColumnSpec("startzeit", "DATETIME", nullable=False),
                ColumnSpec("endzeit", "DATETIME", nullable=False),
            ],
            [
                ForeignKeySpec("fk_slots_workshops", ["workshop_id"], "workshops", ["workshop_id"]),
                ForeignKeySpec("fk_slots_geraete", ["geraet_id"], "geraete", ["geraet_id"]),
            ],
        ),
        _table(
            "coachs",
            [
                ColumnSpec("coach_id", "INT", nullable=False, primary_key=True),
                ColumnSpec("vorname", "VARCHAR(80)", nullable=False),
                ColumnSpec("nachname", "VARCHAR(80)", nullable=False),
                ColumnSpec("fachgebiet", "VARCHAR(120)", nullable=False),
            ],
        ),
        _table(
            "coach_einsaetze",
            [
                ColumnSpec("coach_einsatz_id", "INT", nullable=False, primary_key=True),
                ColumnSpec("coach_id", "INT", nullable=False),
                ColumnSpec("team_id", "INT", nullable=False),
                ColumnSpec("slot_id", "INT", nullable=False),
            ],
            [
                ForeignKeySpec("fk_coach_einsaetze_coachs", ["coach_id"], "coachs", ["coach_id"]),
                ForeignKeySpec("fk_coach_einsaetze_teams", ["team_id"], "teams", ["team_id"]),
                ForeignKeySpec("fk_coach_einsaetze_slots", ["slot_id"], "slots", ["slot_id"]),
            ],
        ),
    ]


def _startupwerkstatt_tables() -> list[TableSpec]:
    return [
        _table(
            "teams",
            [
                ColumnSpec("team_id", "INT", nullable=False, primary_key=True),
                ColumnSpec("name", "VARCHAR(100)", nullable=False),
                ColumnSpec("projekt", "VARCHAR(150)", nullable=False),
            ],
        ),
        _table(
            "mentoren",
            [
                ColumnSpec("mentor_id", "INT", nullable=False, primary_key=True),
                ColumnSpec("vorname", "VARCHAR(80)", nullable=False),
                ColumnSpec("nachname", "VARCHAR(80)", nullable=False),
                ColumnSpec("fachgebiet", "VARCHAR(120)", nullable=False),
            ],
        ),
        _table(
            "termine",
            [
                ColumnSpec("termin_id", "INT", nullable=False, primary_key=True),
                ColumnSpec("datum", "DATE", nullable=False),
                ColumnSpec("ort", "VARCHAR(80)", nullable=False),
                ColumnSpec("mentor_id", "INT", nullable=False),
            ],
            [ForeignKeySpec("fk_termine_mentoren", ["mentor_id"], "mentoren", ["mentor_id"])],
        ),
        _table(
            "pitches",
            [
                ColumnSpec("pitch_id", "INT", nullable=False, primary_key=True),
                ColumnSpec("team_id", "INT", nullable=False),
                ColumnSpec("termin_id", "INT", nullable=False),
                ColumnSpec("titel", "VARCHAR(150)", nullable=False),
                ColumnSpec("status", "VARCHAR(40)", nullable=False),
            ],
            [
                ForeignKeySpec("fk_pitches_teams", ["team_id"], "teams", ["team_id"]),
                ForeignKeySpec("fk_pitches_termine", ["termin_id"], "termine", ["termin_id"]),
            ],
        ),
        _table(
            "mentor_team",
            [
                ColumnSpec("mentor_id", "INT", nullable=False, primary_key=True),
                ColumnSpec("team_id", "INT", nullable=False, primary_key=True),
                ColumnSpec("rolle", "VARCHAR(40)", nullable=False),
            ],
            [
                ForeignKeySpec("fk_mentor_team_mentoren", ["mentor_id"], "mentoren", ["mentor_id"]),
                ForeignKeySpec("fk_mentor_team_teams", ["team_id"], "teams", ["team_id"]),
            ],
        ),
        _table(
            "feedback",
            [
                ColumnSpec("feedback_id", "INT", nullable=False, primary_key=True),
                ColumnSpec("pitch_id", "INT", nullable=False),
                ColumnSpec("kommentar", "VARCHAR(255)", nullable=False),
            ],
            [ForeignKeySpec("fk_feedback_pitches", ["pitch_id"], "pitches", ["pitch_id"])],
        ),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate MWB archives from SQL structure dumps")
    parser.add_argument("--input-dir", default=str(DEFAULT_INPUT_DIR), help="Directory containing *_struktur_*.sql files")
    parser.add_argument("--output-guide", default=str(DEFAULT_OUTPUT_GUIDE), help="Path for the generated workflow guide")
    parser.add_argument("--reference-archive", default=str(DEFAULT_REFERENCE_ARCHIVE), help="Native reference archive used as container template")
    parser.add_argument("--only-system", default="", help="Generate only one system (e.g. stadtfahrradverleih)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing .mwb files")
    args = parser.parse_args()

    input_dir = pathlib.Path(args.input_dir)
    output_guide = pathlib.Path(args.output_guide)
    reference_archive = pathlib.Path(args.reference_archive)
    only_system = args.only_system.strip() or None

    generate_models(input_dir, output_guide, reference_archive, only_system, args.force)

    print(f"[mwb-generator] Fertig: {output_guide}")
    print(f"[mwb-generator] Zeit: {dt.datetime.now(dt.timezone.utc).isoformat()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
