import { ApiClient } from "../api-client.mjs";
import { renderStatus, withRetry } from "../error-handler.mjs";
import { KeywordIndexModel } from "../models/keyword-index.model.mjs";
import { KeywordIndexView } from "../views/keyword-index.view.mjs";

class KeywordIndexController {
  constructor(searchForm, searchInput, searchButton, listElement, statusElement, apiClient) {
    const items = listElement ? Array.from(listElement.querySelectorAll("li")) : [];
    this.searchForm = searchForm;
    this.searchInput = searchInput;
    this.searchButton = searchButton;
    this.statusElement = statusElement;
    this.apiClient = apiClient;
    this.model = new KeywordIndexModel(items);
    this.view = new KeywordIndexView(items, statusElement);
    this.searchDebounceId = null;
  }

  bind() {
    if (!this.searchInput) {
      return;
    }

    this.searchForm?.addEventListener("submit", (event) => {
      event.preventDefault();
      this.searchNow();
    });
    this.searchInput.addEventListener("input", () => this.onInputChanged());
    this.searchButton?.addEventListener("click", () => this.searchNow());
    this.update();
  }

  onInputChanged() {
    if (this.searchDebounceId) {
      window.clearTimeout(this.searchDebounceId);
    }

    this.searchDebounceId = window.setTimeout(() => {
      this.update();
    }, 260);
  }

  searchNow() {
    if (this.searchDebounceId) {
      window.clearTimeout(this.searchDebounceId);
      this.searchDebounceId = null;
    }

    this.view.renderStatus("Suche gestartet...");
    this.update();
  }

  async update() {
    const term = this.searchInput.value;
    const visibilityMap = this.model.filterByTerm(term);
    this.view.render(visibilityMap);

    const normalizedTerm = String(term || "").trim();
    if (normalizedTerm.length < 1) {
      this.view.renderStatus("Lokale Stichwortsuche aktiv.");
      return;
    }

    try {
      this.view.renderStatus("LLM-Suche läuft...");
      const payload = this.model.buildKeywordPayload(normalizedTerm);
      const response = await withRetry(() => this.apiClient.postJson("/api/v1/assistant/keyword-search", payload), {
        attempts: 2,
        baseDelayMs: 220,
      });

      const ranked = Array.isArray(response?.results) ? response.results : [];
      if (ranked.length === 0) {
        this.view.render(visibilityMap);
        this.view.renderStatus(response?.summary || "Keine LLM-Treffer. Lokaler Index bleibt aktiv.");
        return;
      }

      const rankedVisibility = this.model.visibilityByHref(ranked);
      this.view.renderRanked(rankedVisibility, ranked, response?.summary || "LLM-Treffer geladen.");
    } catch (error) {
      if (this.statusElement) {
        renderStatus(this.statusElement, error);
      }
      this.view.render(visibilityMap);
    }
  }
}

export function initKeywordIndexController() {
  const apiBaseUrl = window.PYTHON_API_URL || "/api-proxy.php";
  const apiClient = new ApiClient(apiBaseUrl, { timeoutMs: 12000 });

  const controller = new KeywordIndexController(
    document.getElementById("keywordSearchForm"),
    document.getElementById("keywordSearch"),
    document.getElementById("keywordSearchButton"),
    document.getElementById("keywordList"),
    document.getElementById("keywordStatus"),
    apiClient
  );
  controller.bind();
}
