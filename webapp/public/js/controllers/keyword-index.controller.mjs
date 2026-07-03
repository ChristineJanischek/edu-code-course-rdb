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
    this.view = new KeywordIndexView(items, statusElement, document.getElementById("keywordInsights"));
    this.searchDebounceId = null;
    this.activeRequestId = 0;
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
      this.activeRequestId += 1;
      this.view.renderInsights([]);
      this.view.renderStatus("Lokale Stichwortsuche aktiv.");
      return;
    }

    const requestId = this.activeRequestId + 1;
    this.activeRequestId = requestId;

    try {
      this.view.renderStatus("LLM-Suche läuft...");
      const payload = this.model.buildKeywordPayload(normalizedTerm);
      const response = await withRetry(() => this.apiClient.postJson("/api/v1/assistant/keyword-search", payload), {
        attempts: 2,
        baseDelayMs: 220,
      });

      if (requestId !== this.activeRequestId) {
        return;
      }

      const ranked = Array.isArray(response?.results) ? response.results : [];
      const insights = Array.isArray(response?.insights) ? response.insights : [];
      const knowledgeSources = Array.isArray(response?.knowledge_sources) ? response.knowledge_sources : [];
      if (ranked.length === 0) {
        this.view.render(visibilityMap);
        this.view.renderInsights(insights);
        this.view.renderStatus(this.buildStatusText(normalizedTerm, [], response?.summary, insights, knowledgeSources));
        return;
      }

      const rankedVisibility = this.model.visibilityByHref(ranked);
      this.view.renderRanked(rankedVisibility, ranked, this.buildStatusText(normalizedTerm, ranked, response?.summary, insights, knowledgeSources));
      this.view.renderInsights(insights);
    } catch (error) {
      if (this.statusElement) {
        renderStatus(this.statusElement, error);
      }
      this.view.render(visibilityMap);
      this.view.renderInsights([]);
    }
  }

  buildStatusText(searchTerm, rankedResults = [], summaryText = "", insights = [], knowledgeSources = []) {
    const sourceSuffix = Array.isArray(knowledgeSources) && knowledgeSources.length > 0
      ? ` Quellen: ${knowledgeSources.join(" | ")}`
      : "";

    if ((!Array.isArray(rankedResults) || rankedResults.length === 0) && (!Array.isArray(insights) || insights.length === 0)) {
      const fallbackSummary = summaryText || "Keine LLM-Treffer. Lokaler Index bleibt aktiv.";
      return `Suche '${searchTerm}': ${fallbackSummary}${sourceSuffix}`;
    }

    const topTitles = rankedResults
      .slice(0, 3)
      .map((entry) => String(entry?.title || "").trim())
      .filter(Boolean)
      .join(" | ");

    const insightTitles = Array.isArray(insights)
      ? insights
        .slice(0, 2)
        .map((entry) => String(entry?.title || "").trim())
        .filter(Boolean)
        .join(" | ")
      : "";

    const prefix = summaryText || `${rankedResults.length} Treffer gefunden.`;
    const parts = [prefix];
    if (topTitles) {
      parts.push(`Top-Links: ${topTitles}`);
    }
    if (insightTitles) {
      parts.push(`Beispiele: ${insightTitles}`);
    }
    if (sourceSuffix) {
      parts.push(sourceSuffix.trim());
    }
    return `Suche '${searchTerm}': ${parts.join(" ")}`;
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
