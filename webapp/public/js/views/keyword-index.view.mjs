export class KeywordIndexView {
  constructor(items = [], statusElement = null) {
    this.items = items;
    this.statusElement = statusElement;
  }

  render(visibilityMap) {
    this.items.forEach((item, index) => {
      item.hidden = !Boolean(visibilityMap[index]);
      item.removeAttribute("data-score");
      item.removeAttribute("title");
    });
  }

  renderRanked(visibilityMap, rankedResults = [], statusText = "") {
    const byHref = new Map(
      rankedResults
        .map((entry) => {
          const href = String(entry?.href || "").trim();
          if (!href) {
            return null;
          }

          return [href, entry];
        })
        .filter(Boolean)
    );

    this.items.forEach((item, index) => {
      const isVisible = Boolean(visibilityMap[index]);
      item.hidden = !isVisible;

      const href = item.querySelector("a")?.getAttribute("href") || "";
      const ranked = byHref.get(href.trim());
      if (!ranked) {
        item.removeAttribute("data-score");
        item.removeAttribute("title");
        return;
      }

      item.dataset.score = String(ranked.score ?? "");
      item.title = String(ranked.rationale || "");
    });

    if (this.statusElement) {
      this.statusElement.textContent = statusText;
    }
  }

  renderStatus(message) {
    if (this.statusElement) {
      this.statusElement.textContent = message;
    }
  }
}
