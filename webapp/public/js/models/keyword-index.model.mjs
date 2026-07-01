export class KeywordIndexModel {
  constructor(items = []) {
    this.items = items;
    this.candidates = this.items.map((item) => {
      const link = item.querySelector("a");
      return {
        title: (item.dataset.title || link?.textContent || "").trim(),
        topic: (item.dataset.topic || "").trim(),
        href: (link?.getAttribute("href") || "").trim(),
      };
    }).filter((candidate) => candidate.title && candidate.href);
  }

  filterByTerm(rawTerm) {
    const term = String(rawTerm || "").trim().toLowerCase();

    return this.items.map((item) => {
      const title = (item.dataset.title || "").toLowerCase();
      const topic = (item.dataset.topic || "").toLowerCase();
      return term === "" || title.includes(term) || topic.includes(term);
    });
  }

  buildKeywordPayload(rawTerm) {
    return {
      search_term: String(rawTerm || "").trim(),
      language: "de",
      topic: "relationale-datenbanken",
      candidates: this.candidates,
    };
  }

  visibilityByHref(results) {
    const resultHrefs = new Set(
      Array.isArray(results)
        ? results.map((entry) => String(entry?.href || "").trim()).filter(Boolean)
        : []
    );

    if (resultHrefs.size === 0) {
      return this.items.map(() => false);
    }

    return this.items.map((item) => {
      const href = item.querySelector("a")?.getAttribute("href") || "";
      return resultHrefs.has(href.trim());
    });
  }
}
