import { KeywordIndexModel } from "../models/keyword-index.model.mjs";
import { KeywordIndexView } from "../views/keyword-index.view.mjs";

class KeywordIndexController {
  constructor(searchInput, listElement) {
    const items = listElement ? Array.from(listElement.querySelectorAll("li")) : [];
    this.searchInput = searchInput;
    this.model = new KeywordIndexModel(items);
    this.view = new KeywordIndexView(items);
  }

  bind() {
    if (!this.searchInput) {
      return;
    }

    this.searchInput.addEventListener("input", () => this.update());
    this.update();
  }

  update() {
    const visibilityMap = this.model.filterByTerm(this.searchInput.value);
    this.view.render(visibilityMap);
  }
}

export function initKeywordIndexController() {
  const controller = new KeywordIndexController(
    document.getElementById("keywordSearch"),
    document.getElementById("keywordList")
  );
  controller.bind();
}
