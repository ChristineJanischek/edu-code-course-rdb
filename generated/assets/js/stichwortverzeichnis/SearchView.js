export class SearchView {
  constructor(rows, statusElement, noResultsElement) {
    this.rows = Array.isArray(rows) ? rows : [];
    this.statusElement = statusElement;
    this.noResultsElement = noResultsElement;
  }

  render(filterResult) {
    const { matches, visibleCount, totalCount } = filterResult;

    this.rows.forEach((row, index) => {
      const isVisible = Boolean(matches[index]);
      row.style.display = isVisible ? "" : "none";
    });

    if (this.noResultsElement) {
      this.noResultsElement.hidden = visibleCount !== 0;
    }

    if (this.statusElement) {
      this.statusElement.textContent = `${visibleCount} von ${totalCount} Eintraegen sichtbar.`;
    }
  }
}
