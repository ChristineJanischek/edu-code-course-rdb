#!/usr/bin/env python3
"""
XML-Struktogramm Validator

Validiert XML-definierte Struktogramme gegen XSD-Schema.
Wird verwendet in Pre-Commit Hooks und GitHub Actions.

Usage:
    python struktogramm_xml_validator.py path/to/file.xml
    python struktogramm_xml_validator.py struktogramme/xml_definitions/ --all
    python struktogramm_xml_validator.py --dry-run
"""

import sys
import os
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Tuple, List, Dict
import argparse


class XSDValidationError(Exception):
    """Raised when XSD validation fails."""
    pass


class StruktogrammXMLValidator:
    """Validates XML Struktogramm files against XSD schema."""
    
    def __init__(self, schema_path: str = None):
        """
        Initialize validator with optional custom schema path.
        
        Args:
            schema_path: Path to custom XSD schema. If None, uses default location.
        """
        if schema_path is None:
            # Auto-discover schema
            current_dir = Path(__file__).parent.parent
            schema_path = current_dir / "xml_schemas" / "struktogramm.xsd"
        
        self.schema_path = Path(schema_path)
        if not self.schema_path.exists():
            raise FileNotFoundError(f"Schema nicht gefunden: {self.schema_path}")
        
        self.schema_tree = ET.parse(str(self.schema_path))
        self.schema_root = self.schema_tree.getroot()
        self.errors = []
        self.warnings = []
    
    def validate_file(
        self,
        file_path: str,
        fix_types: bool = False,
    ) -> Tuple[bool, List[str], List[str]]:
        """
        Validate single XML file.
        
        Args:
            file_path: Path to XML file to validate
            
        Returns:
            Tuple of (is_valid, list_of_error_messages, list_of_warnings)
        """
        self.errors = []
        self.warnings = []
        
        file_path = Path(file_path)
        
        if not file_path.exists():
            return False, [f"Datei existiert nicht: {file_path}"], []
        
        if not file_path.suffix.lower() == ".xml":
            return False, [f"Keine XML-Datei: {file_path}"], []
        
        try:
            tree = ET.parse(str(file_path))
            root = tree.getroot()
        except ET.ParseError as e:
            return False, [f"XML Parse Error (Zeile {e.position[0]}): {e.msg}"], []
        except Exception as e:
            return False, [f"Fehler beim Lesen: {str(e)}"], []
        
        # Typ-Attribute prüfen/setzen
        typ_changed = self._check_typ_attributes(root, fix_types)
        if fix_types and typ_changed:
            ET.indent(tree, space="  ", level=0)
            tree.write(file_path, encoding="utf-8", xml_declaration=True)

        # Validate against XSD (manual checks since Python has no built-in XSD validator)
        errors = self._validate_against_schema(root, file_path)
        
        if errors:
            return False, errors, self.warnings
        
        return True, [], self.warnings
    
    def _validate_against_schema(self, root: ET.Element, file_path: Path) -> List[str]:
        """
        Manually validate XML against XSD rules.
        
        Args:
            root: Root XML element
            file_path: Path to file (for error messages)
            
        Returns:
            List of validation errors
        """
        errors = []
        
        # Check root element
        if root.tag != "struktogramm":
            errors.append(f"Fehler: Root-Element muss 'struktogramm' sein, nicht '{root.tag}'")
            return errors
        
        # Check metadata exists
        metadata = root.find("metadata")
        if metadata is None:
            errors.append("Fehler: <metadata> Element ist erforderlich")
            return errors
        
        # Check required metadata fields
        required_metadata = ["titel", "level", "kategorie"]
        for field in required_metadata:
            if metadata.find(field) is None:
                errors.append(f"Fehler: <metadata><{field}> ist erforderlich")
        
        # Check level enum
        level_elem = metadata.find("level")
        if level_elem is not None and level_elem.text:
            if level_elem.text not in ["L1", "L2", "L3"]:
                errors.append(
                    f"Fehler: Level muss L1, L2 oder L3 sein, nicht '{level_elem.text}'"
                )
        
        # Check content exists
        content = root.find("inhalt")
        if content is None:
            errors.append("Fehler: <inhalt> Element ist erforderlich")
            return errors
        
        if len(content) == 0:
            errors.append("Fehler: <inhalt> darf nicht leer sein")
        
        # Validate content structure
        content_errors = self._validate_content_structure(content, file_path)
        errors.extend(content_errors)
        
        return errors

    def _check_typ_attributes(self, root: ET.Element, fix_types: bool) -> bool:
        """Prueft fehlende typ-Attribute und kann sie automatisch setzen."""
        changed = False
        for elem in root.iter():
            if elem.tag not in {"prozess", "eingabe", "ausgabe", "rueckgabe"}:
                continue
            if elem.get("typ"):
                continue
            text = elem.text.strip() if elem.text else ""
            inferred = self._infer_typ_attr(elem.tag, text)
            if inferred:
                self.warnings.append(
                    f"Warnung: typ-Attribut fehlt bei <{elem.tag}> (empfohlen: '{inferred}')"
                )
                if fix_types:
                    elem.set("typ", inferred)
                    changed = True
            else:
                self.warnings.append(
                    f"Warnung: typ-Attribut fehlt bei <{elem.tag}> (konnte nicht abgeleitet werden)"
                )
        return changed

    def _infer_typ_attr(self, tag: str, text: str) -> str:
        """Leitet typ-Attribute aus Tag und Text ab."""
        if tag == "ausgabe":
            return "ausgabe"
        if tag == "rueckgabe":
            return "rueckgabe"
        if tag == "eingabe":
            if " als " in text:
                return "deklaration_und_einlesen"
            return "einlesen"
        if tag == "prozess":
            if " als " in text and "=" in text:
                return "deklaration_und_initialisierung"
            if " als " in text:
                return "deklaration"
            if "=" in text:
                return "zuweisung"
            return "default"
        return "default"
    
    def _validate_content_structure(
        self, 
        element: ET.Element, 
        file_path: Path,
        depth: int = 0,
        path: str = "inhalt"
    ) -> List[str]:
        """
        Recursively validate content structure.
        
        Args:
            element: Element to validate
            file_path: Path to file (for error messages)
            depth: Current recursion depth
            path: Current path for error messages
            
        Returns:
            List of validation errors
        """
        errors = []
        
        # Check max depth
        if depth > 4:
            errors.append(
                f"Warnung: Struktur zu tief verschachtelt (Ebene {depth}) bei {path}"
            )
        
        # Valid element types
        valid_elements = {
            "prozess", "eingabe", "ausgabe", "rueckgabe",
            "wenn", "wiederhole", "zaehle"
        }
        
        for i, child in enumerate(element):
            child_path = f"{path}/{child.tag}[{i}]"
            
            if child.tag not in valid_elements:
                errors.append(
                    f"Fehler: Ungültiger Element-Typ '{child.tag}' in {path}"
                )
                continue
            
            # Validate specific element types
            if child.tag in ["prozess", "ausgabe", "rueckgabe"]:
                if not child.text or not child.text.strip():
                    errors.append(f"Fehler: {child.tag} darf nicht leer sein ({child_path})")
            
            elif child.tag == "eingabe":
                if not child.text or not child.text.strip():
                    errors.append(f"Fehler: eingabe darf nicht leer sein ({child_path})")
            
            elif child.tag == "wenn":
                # If statement must have bedingung and dann
                if child.find("bedingung") is None:
                    errors.append(f"Fehler: <wenn> muss <bedingung> haben ({child_path})")
                if child.find("dann") is None:
                    errors.append(f"Fehler: <wenn> muss <dann> haben ({child_path})")
                
                # Validate nested content
                for subcond in child:
                    if subcond.tag in ["dann", "sonst"]:
                        subcond_errors = self._validate_content_structure(
                            subcond, file_path, depth + 1, f"{child_path}/{subcond.tag}"
                        )
                        errors.extend(subcond_errors)
            
            elif child.tag == "wiederhole":
                # While loop must have bedingung and inhalt
                if child.find("bedingung") is None:
                    errors.append(f"Fehler: <wiederhole> muss <bedingung> haben ({child_path})")
                if child.find("inhalt") is None:
                    errors.append(f"Fehler: <wiederhole> muss <inhalt> haben ({child_path})")
                
                # Validate nested content
                inhalt = child.find("inhalt")
                if inhalt is not None:
                    subcond_errors = self._validate_content_structure(
                        inhalt, file_path, depth + 1, f"{child_path}/inhalt"
                    )
                    errors.extend(subcond_errors)
            
            elif child.tag == "zaehle":
                # For loop must have variable, von, bis, and inhalt
                required_zaehle = ["variable", "von", "bis", "inhalt"]
                for req in required_zaehle:
                    if child.find(req) is None:
                        errors.append(
                            f"Fehler: <zaehle> muss <{req}> haben ({child_path})"
                        )
                
                # Validate nested content
                inhalt = child.find("inhalt")
                if inhalt is not None:
                    subcond_errors = self._validate_content_structure(
                        inhalt, file_path, depth + 1, f"{child_path}/inhalt"
                    )
                    errors.extend(subcond_errors)
        
        return errors
    
    def validate_directory(
        self,
        directory: str,
        fix_types: bool = False,
    ) -> Dict[str, Tuple[bool, List[str], List[str]]]:
        """
        Validate all XML files in directory.
        
        Args:
            directory: Path to directory containing .xml files
            
        Returns:
            Dict mapping file paths to (is_valid, error_list) tuples
        """
        directory = Path(directory)
        results = {}
        
        if not directory.is_dir():
            return {directory: (False, [f"Nicht existendes Verzeichnis: {directory}"], [])}
        
        xml_files = list(directory.rglob("*.xml"))
        
        if not xml_files:
            return {directory: (False, ["Keine .xml Dateien gefunden"], [])}
        
        for xml_file in xml_files:
            is_valid, errors, warnings = self.validate_file(str(xml_file), fix_types=fix_types)
            results[xml_file] = (is_valid, errors, warnings)
        
        return results


def print_validation_results(results: Dict, verbose: bool = False) -> int:
    """
    Print validation results in human-readable format.
    
    Args:
        results: Dict from validate_file or validate_directory
        verbose: Print additional details
        
    Returns:
        Exit code (0 = all valid, 1 = errors found)
    """
    total = len(results)
    valid = sum(1 for is_valid, *_ in results.values() if is_valid)
    invalid = total - valid
    warning_count = sum(len(warnings) for _, _, warnings in results.values())
    
    print(f"\n{'=' * 70}")
    print(f"📋 XML-Struktogramm Validierung")
    print(f"{'=' * 70}")
    print(f"Gesamt: {total} | ✅ Gültig: {valid} | ❌ Fehler: {invalid} | ⚠️ Warnungen: {warning_count}")
    print(f"{'=' * 70}\n")
    
    if invalid > 0:
        print("❌ FEHLER GEFUNDEN:\n")
        for file_path, (is_valid, errors, _) in results.items():
            if not is_valid:
                print(f"📄 {file_path}")
                for error in errors:
                    print(f"   ⚠️  {error}")
                print()
    else:
        print("✅ ALLE DATEIEN GÜLTIG!")

    if warning_count > 0 and verbose:
        print("⚠️  WARNUNGEN:")
        for file_path, (_, _, warnings) in results.items():
            if warnings:
                print(f"📄 {file_path}")
                for warning in warnings:
                    print(f"   ⚠️  {warning}")
                print()
    
    print(f"{'=' * 70}\n")
    
    return 1 if invalid > 0 else 0


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Validiert XML-Struktogramme gegen XSD-Schema"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Pfad zur .xml Datei oder zum Verzeichnis (default: aktuelles Verz.)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Alle .xml Dateien in Verzeichnis validieren"
    )
    parser.add_argument(
        "--schema",
        help="Pfad zu benutzerdefiniertem XSD Schema"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Nur Beispiel-Validierungen durchführen"
    )
    parser.add_argument(
        "--fix-types",
        action="store_true",
        help="Fehlende typ-Attribute automatisch setzen"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Ausführliche Ausgabe"
    )
    
    args = parser.parse_args()
    
    # Initialize validator
    try:
        validator = StruktogrammXMLValidator(schema_path=args.schema)
    except FileNotFoundError as e:
        print(f"❌ Fehler: {e}")
        return 1
    
    # Dry-run mode
    if args.dry_run:
        print("\n🧪 DRY-RUN MODE - Beispiele werden validiert\n")
        
        # Create test XML
        test_xml = """<?xml version="1.0" encoding="UTF-8"?>
<struktogramm>
  <metadata>
    <titel>Test Array-Summe</titel>
    <level>L1</level>
    <kategorie>Schleifen</kategorie>
  </metadata>
  <inhalt>
    <prozess>summe = 0</prozess>
  </inhalt>
</struktogramm>
"""
        
        # Write to temp file
        temp_path = Path("/tmp/test_struktogramm.xml")
        temp_path.write_text(test_xml)
        
        # Validate
        is_valid, errors, warnings = validator.validate_file(str(temp_path))
        results = {temp_path: (is_valid, errors, warnings)}
        
        temp_path.unlink()  # Cleanup
        
        return print_validation_results(results, verbose=args.verbose)
    
    # Normal mode
    path = Path(args.path)
    
    if path.is_file():
        is_valid, errors, warnings = validator.validate_file(str(path), fix_types=args.fix_types)
        results = {path: (is_valid, errors, warnings)}
    elif path.is_dir() or args.all:
        results = validator.validate_directory(str(path), fix_types=args.fix_types)
    else:
        print(f"❌ Pfad nicht existiert: {path}")
        return 1
    
    return print_validation_results(results, verbose=args.verbose)


if __name__ == "__main__":
    sys.exit(main())
