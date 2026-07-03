export class KeywordIndexView {
  constructor(items = [], statusElement = null, insightsElement = null) {
    this.items = items;
    this.statusElement = statusElement;
    this.insightsElement = insightsElement;
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

  renderInsights(insights = []) {
    if (!this.insightsElement) {
      return;
    }

    if (!Array.isArray(insights) || insights.length === 0) {
      this.insightsElement.hidden = true;
      this.insightsElement.replaceChildren();
      return;
    }

    const fragment = document.createDocumentFragment();
    insights.forEach((insight) => {
      const article = document.createElement("article");
      article.className = "keyword-insight-card";

      const eyebrow = document.createElement("p");
      eyebrow.className = "eyebrow";
      eyebrow.textContent = String(insight?.category || "Wissenskarte");
      article.appendChild(eyebrow);

      const heading = document.createElement("h3");
      heading.textContent = String(insight?.title || "Suchhilfe");
      article.appendChild(heading);

      const summary = document.createElement("p");
      summary.className = "muted";
      summary.textContent = String(insight?.summary || "");
      article.appendChild(summary);

      this.appendCodeBlock(article, "Syntax", insight?.syntax);
      this.appendCodeBlock(article, "SQL-Beispiel", insight?.example_sql);
      this.appendCodeBlock(article, "VIEW-Beispiel", insight?.example_view);

      const sourceLabel = String(insight?.source_label || "").trim();
      const sourceUrl = String(insight?.source_url || "").trim();
      if (sourceLabel || sourceUrl) {
        const sourceRow = document.createElement("p");
        sourceRow.className = "keyword-source";
        if (sourceUrl) {
          const link = document.createElement("a");
          link.href = sourceUrl;
          link.target = "_blank";
          link.rel = "noopener";
          link.textContent = sourceLabel || sourceUrl;
          sourceRow.append("Quelle: ", link);
        } else {
          sourceRow.textContent = `Quelle: ${sourceLabel}`;
        }
        article.appendChild(sourceRow);
      }

      fragment.appendChild(article);
    });

    this.insightsElement.hidden = false;
    this.insightsElement.replaceChildren(fragment);
  }

  appendCodeBlock(container, label, content) {
    const text = String(content || "").trim();
    if (!text) {
      return;
    }

    const block = document.createElement("section");
    block.className = "keyword-example-block";

    const heading = document.createElement("h4");
    heading.textContent = label;
    block.appendChild(heading);

    const pre = document.createElement("pre");
    const code = document.createElement("code");
    code.textContent = text;
    pre.appendChild(code);
    block.appendChild(pre);

    container.appendChild(block);
  }

  renderStatus(message) {
    if (this.statusElement) {
      this.statusElement.textContent = message;
    }
  }
}
