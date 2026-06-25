export class SearchModel {
  constructor(rows) {
    this.rows = Array.isArray(rows) ? rows : [];
  }

  normalize(value) {
    return String(value || "")
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");
  }

  filterByQuery(rawQuery) {
    const query = this.normalize(rawQuery).trim();
    const matches = this.rows.map((row) => {
      const rowText = this.normalize(row.innerText);
      return query === "" || rowText.includes(query);
    });

    const visibleCount = matches.reduce((count, current) => (current ? count + 1 : count), 0);

    return {
      matches,
      visibleCount,
      totalCount: this.rows.length,
    };
  }
}
