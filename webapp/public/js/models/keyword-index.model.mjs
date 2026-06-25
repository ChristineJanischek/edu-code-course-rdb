export class KeywordIndexModel {
  constructor(items = []) {
    this.items = items;
  }

  filterByTerm(rawTerm) {
    const term = String(rawTerm || "").trim().toLowerCase();

    return this.items.map((item) => {
      const title = (item.dataset.title || "").toLowerCase();
      const topic = (item.dataset.topic || "").toLowerCase();
      return term === "" || title.includes(term) || topic.includes(term);
    });
  }
}
