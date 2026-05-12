#!/usr/bin/env python3
"""Generate schema-based EERM PNG diagrams from separated SQL artifacts.

This utility scans for `*_struktur_*.sql` files (naming convention
KF-ROUTINE-010), checks for the matching `*_daten_*.sql`, parses tables and
foreign keys from the structure file, and renders a readable PNG
(`{systemname}_{year}.png`) suitable for classroom usage.
"""

from __future__ import annotations

import argparse
import heapq
import pathlib
import re
from dataclasses import dataclass, field

try:
    from PIL import Image, ImageDraw, ImageFont
except ModuleNotFoundError as exc:  # pragma: no cover - runtime dependency guard
    raise SystemExit(
        "ERROR Pillow ist nicht installiert. Bitte ausfuehren: "
        "pip install Pillow"
    ) from exc


CREATE_TABLE_RE = re.compile(
    r"CREATE\s+TABLE\s+`?(?P<name>[a-zA-Z0-9_]+)`?\s*\((?P<body>.*?)\)\s*;",
    re.IGNORECASE | re.DOTALL,
)
FK_RE = re.compile(
    r"FOREIGN\s+KEY\s*\(\s*`?(?P<source_col>[a-zA-Z0-9_]+)`?\s*\)\s*"
    r"REFERENCES\s+`?(?P<target_table>[a-zA-Z0-9_]+)`?\s*\(\s*`?(?P<target_col>[a-zA-Z0-9_]+)`?\s*\)",
    re.IGNORECASE,
)


@dataclass
class ForeignKey:
    source_table: str
    source_col: str
    target_table: str
    target_col: str


@dataclass
class TableModel:
    name: str
    columns: list[str] = field(default_factory=list)
    primary_keys: set[str] = field(default_factory=set)


@dataclass
class TableLayout:
    table: TableModel
    rect: tuple[int, int, int, int]
    column_y: dict[str, int]

    def row_y(self, column: str) -> int:
        if column in self.column_y:
            return self.column_y[column]
        # Fallback to first visible row center when a column is not visible.
        if self.column_y:
            return next(iter(self.column_y.values()))
        return (self.rect[1] + self.rect[3]) // 2


class SqlSchemaParser:
    """Extracts table and FK information from SQL dumps."""

    def parse(self, sql_text: str) -> tuple[list[TableModel], list[ForeignKey]]:
        tables: list[TableModel] = []
        fks: list[ForeignKey] = []

        for table_match in CREATE_TABLE_RE.finditer(sql_text):
            table_name = table_match.group("name")
            body = table_match.group("body")
            table = TableModel(name=table_name)

            for raw_line in body.splitlines():
                line = raw_line.strip().rstrip(",")
                if not line or line.startswith("--"):
                    continue

                upper = line.upper()
                if upper.startswith("PRIMARY KEY"):
                    for col in re.findall(r"`?([a-zA-Z0-9_]+)`?", line):
                        if col.lower() not in {"primary", "key"}:
                            table.primary_keys.add(col)
                    continue

                if "FOREIGN KEY" in upper:
                    fk_match = FK_RE.search(line)
                    if fk_match:
                        fks.append(
                            ForeignKey(
                                source_table=table_name,
                                source_col=fk_match.group("source_col"),
                                target_table=fk_match.group("target_table"),
                                target_col=fk_match.group("target_col"),
                            )
                        )
                    continue

                if upper.startswith(("UNIQUE", "KEY", "INDEX", "CONSTRAINT")):
                    continue

                col_match = re.match(r"`?([a-zA-Z0-9_]+)`?\s+", line)
                if col_match:
                    table.columns.append(col_match.group(1))

            tables.append(table)

        return tables, fks


class SchemaDiagramRenderer:
    """Renders readable entity-relationship diagrams from parsed SQL schema."""

    def __init__(
        self,
        strict_plus: bool = False,
        a4_portrait: bool = False,
        max_columns: int = 2,
    ) -> None:
        self._strict_plus = strict_plus
        self._a4_portrait = a4_portrait
        self._max_columns = max(1, max_columns)
        self._title_font = self._load_font(26, bold=True)
        self._header_font = self._load_font(20, bold=True)
        self._text_font = self._load_font(16)
        self._small_font = self._load_font(14)

    def render(self, tables: list[TableModel], fks: list[ForeignKey], output_path: pathlib.Path) -> None:
        if not tables:
            self._render_empty(output_path)
            return

        levels = self._compute_levels(tables, fks)
        rows_by_level = self._order_rows_by_dependencies(tables, fks, levels)
        if self._a4_portrait:
            rows_by_level = self._rebalance_rows_for_portrait_print(rows_by_level)

        row_count = len(rows_by_level)
        col_count = max(len(row) for row in rows_by_level.values())

        card_w = 440 if self._a4_portrait else (500 if self._strict_plus else 480)
        card_h_max = max(180, 80 + 24 * min(10, max(len(t.columns) for t in tables)))
        if self._a4_portrait:
            gap_x = 54
            gap_y = 74
            pad_x = 52
            pad_y = 96
        else:
            gap_x = 110 if self._strict_plus else 70
            gap_y = 100 if self._strict_plus else 60
            pad_x = 90 if self._strict_plus else 70
            pad_y = 110 if self._strict_plus else 90

        width = pad_x * 2 + col_count * card_w + (col_count - 1) * gap_x
        height = pad_y * 2 + row_count * card_h_max + (row_count - 1) * gap_y + 120

        image = Image.new("RGB", (width, height), (246, 248, 252))
        draw = ImageDraw.Draw(image)

        # title
        draw.text((pad_x, 26), "EERM-Referenzgrafik (SQL-Kontext)", fill=(20, 33, 61), font=self._title_font)

        table_map = {t.name: t for t in tables}
        layouts: dict[str, TableLayout] = {}
        level_positions = {lvl: idx for idx, lvl in enumerate(sorted(rows_by_level.keys()))}

        row_tops: dict[int, int] = {}
        row_bottoms: dict[int, int] = {}
        for level, row_tables in rows_by_level.items():
            row_index = level_positions[level]
            y = pad_y + row_index * (card_h_max + gap_y)
            row_tops[level] = y

            span_w = len(row_tables) * card_w + (len(row_tables) - 1) * gap_x
            start_x = (width - span_w) // 2
            row_max_bottom = y

            for col_index, table_name in enumerate(row_tables):
                table = table_map[table_name]
                x = start_x + col_index * (card_w + gap_x)
                h = self._table_height(table, card_h_max)
                rect = (x, y, x + card_w, y + h)
                layout = self._build_table_layout(table, rect)
                layouts[table.name] = layout
                row_max_bottom = max(row_max_bottom, rect[3])
                self._draw_table_card(draw, layout)

            row_bottoms[level] = row_max_bottom

        corridors: dict[tuple[int, int], int] = {}
        sorted_levels = sorted(rows_by_level.keys())
        for i in range(len(sorted_levels) - 1):
            upper = sorted_levels[i]
            lower = sorted_levels[i + 1]
            corridors[(upper, lower)] = (row_bottoms[upper] + row_tops[lower]) // 2

        # Pre-calculate input/output slots so FK lines leave/enter cards at distinct ports.
        outgoing: dict[str, list[ForeignKey]] = {t.name: [] for t in tables}
        incoming: dict[str, list[ForeignKey]] = {t.name: [] for t in tables}
        for fk in fks:
            if fk.source_table in layouts and fk.target_table in layouts:
                # Parent -> child for downward routing.
                outgoing[fk.target_table].append(fk)
                incoming[fk.source_table].append(fk)

        out_slot: dict[tuple[str, str, str], int] = {}
        in_slot: dict[tuple[str, str, str], int] = {}

        for table_name, edges in outgoing.items():
            edges.sort(
                key=lambda edge: (
                    layouts[edge.source_table].rect[0] + layouts[edge.source_table].rect[2]
                ) // 2
            )
            for idx, edge in enumerate(edges):
                out_slot[(edge.source_table, edge.target_table, edge.source_col)] = idx

        for table_name, edges in incoming.items():
            edges.sort(
                key=lambda edge: (
                    layouts[edge.target_table].rect[0] + layouts[edge.target_table].rect[2]
                ) // 2
            )
            for idx, edge in enumerate(edges):
                in_slot[(edge.source_table, edge.target_table, edge.source_col)] = idx

        # draw relationships after boxes
        lane_count: dict[tuple[int, int], int] = {}
        occupied_route_cells: set[tuple[int, int]] = set()
        ordered_fks = sorted(
            fks,
            key=lambda fk: (
                levels.get(fk.target_table, 0),
                levels.get(fk.source_table, 0),
                layouts[fk.target_table].row_y(fk.target_col) if fk.target_table in layouts else 0,
                layouts[fk.source_table].row_y(fk.source_col) if fk.source_table in layouts else 0,
                fk.target_table,
                fk.source_table,
                fk.source_col,
            ),
        )

        for fk in ordered_fks:
            if fk.source_table not in layouts or fk.target_table not in layouts:
                continue
            parent_level = levels[fk.target_table]
            child_level = levels[fk.source_table]
            level_key = (parent_level, child_level)
            lane = lane_count.get(level_key, 0)
            lane_count[level_key] = lane + 1

            self._draw_fk_line(
                draw=draw,
                parent_layout=layouts[fk.target_table],
                child_layout=layouts[fk.source_table],
                fk=fk,
                all_layouts=layouts,
                out_index=out_slot.get((fk.source_table, fk.target_table, fk.source_col), 0),
                out_total=max(1, len(outgoing[fk.target_table])),
                in_index=in_slot.get((fk.source_table, fk.target_table, fk.source_col), 0),
                in_total=max(1, len(incoming[fk.source_table])),
                lane=lane,
                occupied_route_cells=occupied_route_cells,
            )

        legend = "Legende: PK = Primärschlüssel, FK = Fremdschlüssel"
        draw.text((pad_x, height - 40), legend, fill=(62, 79, 109), font=self._small_font)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path, format="PNG", optimize=True)

    def _compute_levels(self, tables: list[TableModel], fks: list[ForeignKey]) -> dict[str, int]:
        """Assign levels so parent tables are above child tables."""
        levels = {t.name: 0 for t in tables}

        changed = True
        max_iter = len(tables) * 5
        while changed and max_iter > 0:
            changed = False
            max_iter -= 1
            for fk in fks:
                if fk.source_table not in levels or fk.target_table not in levels:
                    continue
                required = levels[fk.target_table] + 1
                if levels[fk.source_table] < required:
                    levels[fk.source_table] = required
                    changed = True

        return levels

    def _order_rows_by_dependencies(
        self,
        tables: list[TableModel],
        fks: list[ForeignKey],
        levels: dict[str, int],
    ) -> dict[int, list[str]]:
        rows: dict[int, list[str]] = {}
        for t in tables:
            rows.setdefault(levels[t.name], []).append(t.name)

        for level in rows:
            rows[level].sort()

        level_list = sorted(rows.keys())
        if len(level_list) <= 1:
            return rows

        # Build adjacency maps used by barycenter sweeps.
        parents_of: dict[str, list[str]] = {t.name: [] for t in tables}
        children_of: dict[str, list[str]] = {t.name: [] for t in tables}
        for fk in fks:
            if fk.source_table in parents_of and fk.target_table in parents_of:
                parents_of[fk.source_table].append(fk.target_table)
                children_of[fk.target_table].append(fk.source_table)

        # Iterative down/up sweeps similar to Sugiyama-style layering.
        sweep_rounds = 10 if self._strict_plus else 6
        for _ in range(sweep_rounds):
            # Downward sweep: children by parent barycenter.
            for idx in range(1, len(level_list)):
                prev_level = level_list[idx - 1]
                level = level_list[idx]
                prev_pos = {name: i for i, name in enumerate(rows[prev_level])}

                def down_score(name: str) -> tuple[float, str]:
                    related = [p for p in parents_of[name] if p in prev_pos]
                    if not related:
                        return (float("inf"), name)
                    avg = sum(prev_pos[p] for p in related) / len(related)
                    return (avg, name)

                rows[level].sort(key=down_score)

            # Upward sweep: parents by child barycenter.
            for idx in range(len(level_list) - 2, -1, -1):
                next_level = level_list[idx + 1]
                level = level_list[idx]
                next_pos = {name: i for i, name in enumerate(rows[next_level])}

                def up_score(name: str) -> tuple[float, str]:
                    related = [c for c in children_of[name] if c in next_pos]
                    if not related:
                        return (float("inf"), name)
                    avg = sum(next_pos[c] for c in related) / len(related)
                    return (avg, name)

                rows[level].sort(key=up_score)

        # Local adjacent swaps if they reduce crossings.
        swap_rounds = 5 if self._strict_plus else 3
        for _ in range(swap_rounds):
            improved = False
            for level in level_list:
                if len(rows[level]) <= 1:
                    continue
                i = 0
                while i < len(rows[level]) - 1:
                    base_score = self._crossing_score(rows, fks, levels)
                    rows[level][i], rows[level][i + 1] = rows[level][i + 1], rows[level][i]
                    new_score = self._crossing_score(rows, fks, levels)
                    if new_score < base_score:
                        improved = True
                        i += 1
                    else:
                        # revert
                        rows[level][i], rows[level][i + 1] = rows[level][i + 1], rows[level][i]
                        i += 1
            if not improved:
                break

        return rows

    def _rebalance_rows_for_portrait_print(self, rows: dict[int, list[str]]) -> dict[int, list[str]]:
        """Split broad rows into smaller chunks for A4 portrait readability.

        This keeps the general level order but caps side-by-side entity cards,
        so entity types appear more often under each other than next to each other.
        """
        rebalanced: dict[int, list[str]] = {}
        new_level = 0
        for level in sorted(rows.keys()):
            current = rows[level]
            for idx in range(0, len(current), self._max_columns):
                rebalanced[new_level] = current[idx : idx + self._max_columns]
                new_level += 1
        return rebalanced

    def _crossing_score(
        self,
        rows: dict[int, list[str]],
        fks: list[ForeignKey],
        levels: dict[str, int],
    ) -> int:
        total = 0
        level_list = sorted(rows.keys())
        for i in range(len(level_list) - 1):
            upper = level_list[i]
            lower = level_list[i + 1]
            upper_pos = {name: idx for idx, name in enumerate(rows[upper])}
            lower_pos = {name: idx for idx, name in enumerate(rows[lower])}

            edges: list[tuple[int, int]] = []
            for fk in fks:
                if fk.target_table not in upper_pos or fk.source_table not in lower_pos:
                    continue
                if levels[fk.target_table] != upper or levels[fk.source_table] != lower:
                    continue
                edges.append((upper_pos[fk.target_table], lower_pos[fk.source_table]))

            total += self._count_inversions(edges)
        return total

    def _count_inversions(self, edges: list[tuple[int, int]]) -> int:
        if len(edges) < 2:
            return 0
        inv = 0
        for i in range(len(edges)):
            a_u, a_l = edges[i]
            for j in range(i + 1, len(edges)):
                b_u, b_l = edges[j]
                if (a_u < b_u and a_l > b_l) or (a_u > b_u and a_l < b_l):
                    inv += 1
        return inv

    def _load_font(self, size: int, bold: bool = False) -> ImageFont.ImageFont:
        candidates = []
        if bold:
            candidates.extend([
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            ])
        else:
            candidates.extend([
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            ])
        for path in candidates:
            if pathlib.Path(path).exists():
                return ImageFont.truetype(path, size=size)
        return ImageFont.load_default()

    def _table_height(self, table: TableModel, max_h: int) -> int:
        visible_cols = min(10, len(table.columns))
        return min(max_h, 70 + visible_cols * 24 + 16)

    def _build_table_layout(self, table: TableModel, rect: tuple[int, int, int, int]) -> TableLayout:
        x1, y1, _x2, y2 = rect
        column_y: dict[str, int] = {}
        y = y1 + 58
        for col in table.columns[:10]:
            column_y[col] = y + 10
            y += 24
        return TableLayout(table=table, rect=rect, column_y=column_y)

    def _draw_table_card(self, draw: ImageDraw.ImageDraw, layout: TableLayout) -> None:
        table = layout.table
        x1, y1, x2, y2 = layout.rect
        draw.rounded_rectangle(layout.rect, radius=14, fill=(255, 255, 255), outline=(30, 68, 134), width=3)
        draw.rectangle((x1, y1, x2, y1 + 46), fill=(225, 237, 255), outline=(30, 68, 134), width=0)
        draw.text((x1 + 14, y1 + 10), table.name, fill=(18, 41, 82), font=self._header_font)

        y = y1 + 58
        for idx, col in enumerate(table.columns[:10]):
            label = f"PK {col}" if col in table.primary_keys else col
            draw.text((x1 + 14, y), label, fill=(44, 54, 74), font=self._text_font)
            if idx < min(9, len(table.columns) - 1):
                draw.line((x1 + 12, y + 22, x2 - 12, y + 22), fill=(236, 240, 247), width=1)
            y += 24

        if len(table.columns) > 10:
            draw.text((x1 + 14, y2 - 24), f"... +{len(table.columns) - 10} weitere", fill=(90, 102, 126), font=self._small_font)

    def _draw_fk_line(
        self,
        draw: ImageDraw.ImageDraw,
        parent_layout: TableLayout,
        child_layout: TableLayout,
        fk: ForeignKey,
        all_layouts: dict[str, TableLayout],
        out_index: int,
        out_total: int,
        in_index: int,
        in_total: int,
        lane: int,
        occupied_route_cells: set[tuple[int, int]],
    ) -> None:
        slot_gap = 22 if self._strict_plus else 16
        parent_rect = parent_layout.rect
        child_rect = child_layout.rect

        parent_y = parent_layout.row_y(fk.target_col)
        child_y = child_layout.row_y(fk.source_col)

        parent_on_left = ((parent_rect[0] + parent_rect[2]) // 2) <= ((child_rect[0] + child_rect[2]) // 2)
        overlap_left = max(parent_rect[0], child_rect[0])
        overlap_right = min(parent_rect[2], child_rect[2])
        stacked_vertical = parent_rect[3] < child_rect[1] and (overlap_right - overlap_left) >= 80

        vertical_mode = False
        start_marker: tuple[int, int]
        end_marker: tuple[int, int]

        if stacked_vertical:
            vertical_mode = True
            slot_gap_x = 18 if self._strict_plus else 12
            overlap_mid = (overlap_left + overlap_right) // 2
            sx = self._clamp(
                overlap_mid + int((out_index - (out_total - 1) / 2) * slot_gap_x),
                overlap_left + 12,
                overlap_right - 12,
            )
            ex = self._clamp(
                overlap_mid + int((in_index - (in_total - 1) / 2) * slot_gap_x),
                overlap_left + 12,
                overlap_right - 12,
            )
            sy_inner = parent_rect[3] - 10
            sy = parent_rect[3]
            ey = child_rect[1]
            ey_inner = child_rect[1] + 10
            start_marker = (sx, sy_inner)
            end_marker = (ex, ey_inner)
        elif parent_on_left:
            sx_inner = parent_rect[2] - 10
            sx = parent_rect[2]
            ex = child_rect[0]
            ex_inner = child_rect[0] + 10
            start_marker = (sx_inner, parent_y)
            end_marker = (ex_inner, child_y)
        else:
            sx_inner = parent_rect[0] + 10
            sx = parent_rect[0]
            ex = child_rect[2]
            ex_inner = child_rect[2] - 10
            start_marker = (sx_inner, parent_y)
            end_marker = (ex_inner, child_y)

        if not vertical_mode:
            sy = parent_y + int((out_index - (out_total - 1) / 2) * slot_gap)
            ey = child_y + int((in_index - (in_total - 1) / 2) * slot_gap)
            start_marker = (start_marker[0], sy)
            end_marker = (end_marker[0], ey)

        color = (88, 103, 133)
        width = 3

        start = (sx, sy)
        end = (ex, ey)
        route = self._route_around_tables(
            start=start,
            end=end,
            parent_name=parent_layout.table.name,
            child_name=child_layout.table.name,
            all_layouts=all_layouts,
            canvas_width=draw.im.size[0],
            canvas_height=draw.im.size[1],
            occupied_route_cells=occupied_route_cells,
        )
        if route is None:
            if vertical_mode:
                lane_y = ((parent_rect[3] + child_rect[1]) // 2) + lane * (16 if self._strict_plus else 12)
                points = [(sx, sy_inner), (sx, sy), (sx, lane_y), (ex, lane_y), (ex, ey), (ex, ey_inner)]
            elif parent_on_left and parent_rect[2] < child_rect[0]:
                lane_x = ((parent_rect[2] + child_rect[0]) // 2) + lane * (18 if self._strict_plus else 12)
                points = [(sx_inner, sy), (sx, sy), (lane_x, sy), (lane_x, ey), (ex, ey), (ex_inner, ey)]
            elif (not parent_on_left) and child_rect[2] < parent_rect[0]:
                lane_x = ((parent_rect[0] + child_rect[2]) // 2) - lane * (18 if self._strict_plus else 12)
                points = [(sx_inner, sy), (sx, sy), (lane_x, sy), (lane_x, ey), (ex, ey), (ex_inner, ey)]
            else:
                # Vertical overlap case: route via side bus outside both tables.
                if parent_on_left:
                    bus_x = max(parent_rect[2], child_rect[2]) + (56 if self._strict_plus else 34) + lane * (20 if self._strict_plus else 14)
                else:
                    bus_x = min(parent_rect[0], child_rect[0]) - (56 if self._strict_plus else 34) - lane * (20 if self._strict_plus else 14)
                bus_x = self._clamp(bus_x, 24, draw.im.size[0] - 24)
                points = [
                    (sx_inner, sy),
                    (sx, sy),
                    (bus_x, sy),
                    (bus_x, ey),
                    (ex, ey),
                    (ex_inner, ey),
                ]
        else:
            points, reserved_cells = route
            occupied_route_cells.update(reserved_cells)

        for p1, p2 in zip(points, points[1:]):
            draw.line((*p1, *p2), fill=color, width=width)

        # small arrow at child side for clearer direction to FK table (points to FK).
        if vertical_mode:
            draw.polygon([(ex, ey_inner), (ex - 6, ey_inner + 10), (ex + 6, ey_inner + 10)], fill=color)
        elif parent_on_left:
            draw.polygon([(ex_inner, ey), (ex_inner - 10, ey - 6), (ex_inner - 10, ey + 6)], fill=color)
        else:
            draw.polygon([(ex_inner, ey), (ex_inner + 10, ey - 6), (ex_inner + 10, ey + 6)], fill=color)

        # Cardinality markers: parent side = 1, child side = N
        if vertical_mode:
            draw.text((sx - 14, sy_inner - 14), "1", fill=(52, 64, 89), font=self._small_font)
            draw.text((ex - 14, ey_inner + 4), "N", fill=(52, 64, 89), font=self._small_font)
        elif parent_on_left:
            draw.text((sx_inner - 16, sy - 14), "1", fill=(52, 64, 89), font=self._small_font)
            draw.text((ex_inner + 4, ey - 14), "N", fill=(52, 64, 89), font=self._small_font)
        else:
            draw.text((sx_inner + 4, sy - 14), "1", fill=(52, 64, 89), font=self._small_font)
            draw.text((ex_inner - 16, ey - 14), "N", fill=(52, 64, 89), font=self._small_font)

        # Compact endpoint markers avoid text clutter in dense diagrams.
        draw.ellipse((start_marker[0] - 3, start_marker[1] - 3, start_marker[0] + 3, start_marker[1] + 3), fill=(44, 70, 121))
        draw.ellipse((end_marker[0] - 3, end_marker[1] - 3, end_marker[0] + 3, end_marker[1] + 3), fill=(44, 70, 121))

    def _route_around_tables(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        parent_name: str,
        child_name: str,
        all_layouts: dict[str, TableLayout],
        canvas_width: int,
        canvas_height: int,
        occupied_route_cells: set[tuple[int, int]],
    ) -> tuple[list[tuple[int, int]], set[tuple[int, int]]] | None:
        margin = 20 if self._strict_plus else 14
        cell_size = 14 if self._strict_plus else 12
        bounds = self._routing_bounds(all_layouts, canvas_width, canvas_height)

        blocked: set[tuple[int, int]] = set()
        for name, layout in all_layouts.items():
            if name in {parent_name, child_name}:
                continue
            blocked.update(self._rect_to_blocked_cells(layout.rect, bounds, cell_size, margin))

        start_cell = self._point_to_cell(start, bounds, cell_size)
        end_cell = self._point_to_cell(end, bounds, cell_size)
        blocked.update(occupied_route_cells)
        blocked.discard(start_cell)
        blocked.discard(end_cell)

        path_cells = self._a_star_path(start_cell, end_cell, blocked, bounds, cell_size)
        if path_cells is None:
            return None

        points = [start]
        for cell in path_cells[1:-1]:
            points.append(self._cell_to_point(cell, bounds, cell_size))
        points.append(end)
        compressed = self._compress_polyline(points)
        reserved_cells = set(path_cells[1:-1])
        return compressed, reserved_cells

    def _routing_bounds(
        self,
        all_layouts: dict[str, TableLayout],
        canvas_width: int,
        canvas_height: int,
    ) -> tuple[int, int, int, int]:
        if not all_layouts:
            return (20, 72, canvas_width - 20, canvas_height - 56)

        min_x = min(layout.rect[0] for layout in all_layouts.values())
        min_y = min(layout.rect[1] for layout in all_layouts.values())
        max_x = max(layout.rect[2] for layout in all_layouts.values())
        max_y = max(layout.rect[3] for layout in all_layouts.values())

        pad_x = 80 if self._strict_plus else 60
        pad_y_top = 36
        pad_y_bottom = 72 if self._strict_plus else 56

        left = self._clamp(min_x - pad_x, 20, canvas_width - 40)
        top = self._clamp(min_y - pad_y_top, 72, canvas_height - 80)
        right = self._clamp(max_x + pad_x, 40, canvas_width - 20)
        bottom = self._clamp(max_y + pad_y_bottom, 100, canvas_height - 56)

        if right <= left:
            left, right = 20, canvas_width - 20
        if bottom <= top:
            top, bottom = 72, canvas_height - 56
        return (left, top, right, bottom)

    def _clamp(self, value: int, low: int, high: int) -> int:
        if value < low:
            return low
        if value > high:
            return high
        return value

    def _a_star_path(
        self,
        start: tuple[int, int],
        goal: tuple[int, int],
        blocked: set[tuple[int, int]],
        bounds: tuple[int, int, int, int],
        cell_size: int,
    ) -> list[tuple[int, int]] | None:
        width_cells = max(1, ((bounds[2] - bounds[0]) // cell_size) + 1)
        height_cells = max(1, ((bounds[3] - bounds[1]) // cell_size) + 1)

        def heuristic(cell: tuple[int, int]) -> int:
            return (abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])) * 10

        def edge_penalty(cell: tuple[int, int]) -> int:
            x, y = cell
            penalty = 0
            if x <= 1 or x >= width_cells - 2:
                penalty += 6
            if y <= 1 or y >= height_cells - 2:
                penalty += 4
            return penalty

        open_heap: list[tuple[int, int, tuple[int, int]]] = []
        heapq.heappush(open_heap, (heuristic(start), 0, start))
        came_from: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
        g_score: dict[tuple[int, int], int] = {start: 0}
        visited: set[tuple[int, int]] = set()

        while open_heap:
            _priority, current_cost, current = heapq.heappop(open_heap)
            if current in visited:
                continue
            visited.add(current)
            if current == goal:
                break

            cx, cy = current
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx = cx + dx
                ny = cy + dy
                neighbor = (nx, ny)
                if nx < 0 or ny < 0 or nx >= width_cells or ny >= height_cells:
                    continue
                if neighbor in blocked:
                    continue

                tentative = current_cost + 10 + edge_penalty(neighbor)
                if tentative >= g_score.get(neighbor, 1_000_000_000):
                    continue

                came_from[neighbor] = current
                g_score[neighbor] = tentative
                heapq.heappush(open_heap, (tentative + heuristic(neighbor), tentative, neighbor))

        if goal not in came_from:
            return None

        path: list[tuple[int, int]] = []
        current: tuple[int, int] | None = goal
        while current is not None:
            path.append(current)
            current = came_from.get(current)
        path.reverse()
        return path

    def _point_to_cell(
        self,
        point: tuple[int, int],
        bounds: tuple[int, int, int, int],
        cell_size: int,
    ) -> tuple[int, int]:
        x = max(bounds[0], min(point[0], bounds[2])) - bounds[0]
        y = max(bounds[1], min(point[1], bounds[3])) - bounds[1]
        return (x // cell_size, y // cell_size)

    def _cell_to_point(
        self,
        cell: tuple[int, int],
        bounds: tuple[int, int, int, int],
        cell_size: int,
    ) -> tuple[int, int]:
        return (
            bounds[0] + cell[0] * cell_size + cell_size // 2,
            bounds[1] + cell[1] * cell_size + cell_size // 2,
        )

    def _rect_to_blocked_cells(
        self,
        rect: tuple[int, int, int, int],
        bounds: tuple[int, int, int, int],
        cell_size: int,
        margin: int,
    ) -> set[tuple[int, int]]:
        x1, y1, x2, y2 = rect
        x1 -= margin
        y1 -= margin
        x2 += margin
        y2 += margin

        left = max(bounds[0], x1)
        top = max(bounds[1], y1)
        right = min(bounds[2], x2)
        bottom = min(bounds[3], y2)
        if left >= right or top >= bottom:
            return set()

        left_cell = (left - bounds[0]) // cell_size
        right_cell = (right - bounds[0]) // cell_size
        top_cell = (top - bounds[1]) // cell_size
        bottom_cell = (bottom - bounds[1]) // cell_size

        blocked: set[tuple[int, int]] = set()
        for cell_x in range(left_cell, right_cell + 1):
            for cell_y in range(top_cell, bottom_cell + 1):
                blocked.add((cell_x, cell_y))
        return blocked

    def _compress_polyline(self, points: list[tuple[int, int]]) -> list[tuple[int, int]]:
        if len(points) <= 2:
            return points

        compressed = [points[0]]
        prev_dx = points[1][0] - points[0][0]
        prev_dy = points[1][1] - points[0][1]
        for index in range(2, len(points)):
            current_dx = points[index][0] - points[index - 1][0]
            current_dy = points[index][1] - points[index - 1][1]
            if current_dx == prev_dx and current_dy == prev_dy:
                continue
            compressed.append(points[index - 1])
            prev_dx = current_dx
            prev_dy = current_dy

        compressed.append(points[-1])
        return compressed

    def _render_empty(self, output_path: pathlib.Path) -> None:
        image = Image.new("RGB", (1400, 800), (247, 249, 253))
        draw = ImageDraw.Draw(image)
        draw.text((80, 80), "Keine Tabellen im SQL-Dump gefunden", fill=(80, 40, 40), font=self._title_font)
        draw.text((80, 130), "Bitte *_struktur_*.sql und *_daten_*.sql pruefen (KF-ROUTINE-010).", fill=(90, 95, 110), font=self._text_font)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path, format="PNG", optimize=True)


def find_struktur_files(input_dir: pathlib.Path) -> list[pathlib.Path]:
    """Find structure dump files matching the convention *_struktur_*.sql (KF-ROUTINE-010).
    
    Convention:
      {systemname}_struktur_{year}.sql  (paired with {systemname}_daten_{year}.sql)
    """
    return sorted(input_dir.rglob("*_struktur_*.sql"))


def find_daten_file(struktur_file: pathlib.Path) -> pathlib.Path | None:
    """Find corresponding data dump file for a structure file.
    
    Example:
      Input:  /path/stadtfahrradverleih_struktur_2025.sql
      Output: /path/stadtfahrradverleih_daten_2025.sql
    """
    name = struktur_file.stem  # e.g. 'stadtfahrradverleih_struktur_2025'
    parts = name.split("_struktur_")
    if len(parts) == 2:
        systemname, year = parts[0], parts[1]
        daten_file = struktur_file.parent / f"{systemname}_daten_{year}.sql"
        return daten_file if daten_file.exists() else None
    return None


def derive_png_path(struktur_file: pathlib.Path) -> pathlib.Path:
    """Derive the output PNG path from the structure filename.

    Convention (KF-ROUTINE-010):
      {systemname}_struktur_{year}.sql  ->  {systemname}_{year}.png
    """
    name = struktur_file.stem  # e.g. 'stadtfahrradverleih_struktur_2025'
    parts = name.split("_struktur_")
    if len(parts) == 2:
        systemname, year = parts[0], parts[1]
        return struktur_file.parent / f"{systemname}_{year}.png"
    # Fallback: replace .sql extension with .png
    return struktur_file.with_suffix(".png")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate PNG diagrams from *_struktur_*.sql files (KF-ROUTINE-010)."
    )
    parser.add_argument(
        "--input-dir",
        type=pathlib.Path,
        default=pathlib.Path("generated/klassenarbeiten"),
        help="Directory to scan recursively for *_struktur_*.sql files paired with *_daten_*.sql",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing PNG files",
    )
    parser.add_argument(
        "--strict-plus",
        action="store_true",
        help="Use a wider, more collision-averse layout with stronger spacing",
    )
    parser.add_argument(
        "--a4-portrait",
        action="store_true",
        help="Optimize diagram layout for A4 portrait printing (more vertical stacking)",
    )
    parser.add_argument(
        "--max-columns",
        type=int,
        default=2,
        help="Maximum number of entity cards side-by-side in A4 portrait mode",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.input_dir.exists():
        print(f"ERROR input directory does not exist: {args.input_dir}")
        return 2

    struktur_files = find_struktur_files(args.input_dir)
    if not struktur_files:
        print(f"INFO no *_struktur_*.sql files found in {args.input_dir}")
        return 0

    sql_parser = SqlSchemaParser()
    renderer = SchemaDiagramRenderer(
        strict_plus=args.strict_plus,
        a4_portrait=args.a4_portrait,
        max_columns=args.max_columns,
    )

    for struktur_file in struktur_files:
        daten_file = find_daten_file(struktur_file)
        if daten_file is None:
            print(f"WARN {struktur_file}: kein entsprechendes *_daten_*.sql file gefunden, ueberspringe...")
            continue

        png_file = derive_png_path(struktur_file)
        if png_file.exists() and not args.force:
            print(f"SKIP {png_file} (already exists)")
            continue

        struktur_text = struktur_file.read_text(encoding="utf-8")
        tables, fks = sql_parser.parse(struktur_text)
        renderer.render(tables, fks, png_file)
        print(f"OK   {png_file} (tables={len(tables)}, fks={len(fks)})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
