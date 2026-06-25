import { SearchModel } from "./SearchModel.js";
import { SearchView } from "./SearchView.js";

class SearchController {
  constructor(inputElement, model, view) {
    this.inputElement = inputElement;
    this.model = model;
    this.view = view;
  }

  bind() {
    if (!this.inputElement) {
      return;
    }

    this.inputElement.addEventListener("input", () => {
      this.applyFilter();
    });

    this.applyFilter();
  }

  applyFilter() {
    const result = this.model.filterByQuery(this.inputElement.value);
    this.view.render(result);
  }
}

(function initStichwortSuche() {
  const input = document.getElementById("stichwortSuche");
  const table = document.querySelector("table");
  const status = document.getElementById("suchStatus");
  const noResults = document.getElementById("suchKeineTreffer");

  if (!input || !table || !status || !noResults) {
    return;
  }

  const rows = Array.from(table.querySelectorAll("tbody tr"));
  const model = new SearchModel(rows);
  const view = new SearchView(rows, status, noResults);
  const controller = new SearchController(input, model, view);

  controller.bind();
})();
