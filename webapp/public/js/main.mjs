import { ApiClient } from "./api-client.mjs";
import { renderStatus, withRetry } from "./error-handler.mjs";
import { normalizeSubmissionForm, validateSubmissionPayload } from "./validators.mjs";

class KeywordIndexFilter {
  constructor(searchInput, listElement) {
    this.searchInput = searchInput;
    this.listElement = listElement;
  }

  filter() {
    const term = this.searchInput.value.trim().toLowerCase();
    const items = this.listElement.querySelectorAll("li");

    for (const item of items) {
      const title = item.dataset.title || "";
      const topic = item.dataset.topic || "";
      const isVisible = term === "" || title.includes(term) || topic.includes(term);
      item.hidden = !isVisible;
    }
  }

  bind() {
    this.searchInput?.addEventListener("input", () => this.filter());
  }
}

class ExerciseEvaluator {
  constructor(rootElement) {
    this.rootElement = rootElement;
    this.input = rootElement.querySelector(".exercise-input");
    this.button = rootElement.querySelector(".exercise-check");
    this.feedback = rootElement.querySelector(".feedback-box p");
    this.requiredTokens = (rootElement.dataset.checks || "")
      .split("|")
      .map((token) => token.trim())
      .filter(Boolean);
  }

  evaluate() {
    const answer = this.input.value.trim();
    if (!answer) {
      this.feedback.textContent =
        "Noch keine Lösung eingetragen. Beginne mit einem fachlich begruendeten ersten Entwurf und pruefe dann gezielt Schluesselwoerter oder Begruendungen.";
      return;
    }

    const normalizedAnswer = answer.toUpperCase();
    const missingTokens = this.requiredTokens.filter(
      (token) => !normalizedAnswer.includes(token.toUpperCase())
    );

    if (missingTokens.length === 0) {
      this.feedback.textContent =
        "Starke Grundlage. Die geforderten Kernbausteine sind vorhanden. Pruefe jetzt noch fachlich, ob deine JOIN-Bedingungen oder Begruendungen exakt zum Sachverhalt passen und keine unnoetigen Attribute mitschwingen.";
      return;
    }

    this.feedback.textContent = `Noch unvollstaendig: ${missingTokens.join(", ")}. Ergaenze diese Bausteine und verknuepfe sie mit einer fachlichen Begruendung. Arbeite schrittweise: erst Struktur, dann Präzision.`;
  }

  bind() {
    this.button?.addEventListener("click", () => this.evaluate());
  }
}

class SubmissionForm {
  constructor(formElement, statusElement, apiClient) {
    this.formElement = formElement;
    this.statusElement = statusElement;
    this.apiClient = apiClient;
  }

  setStatus(message, state = "success") {
    this.statusElement.textContent = message;
    this.statusElement.dataset.state = state;
    this.statusElement.closest(".feedback-box")?.setAttribute("data-state", state);
  }

  async submit(event) {
    event.preventDefault();

    const payload = normalizeSubmissionForm(this.formElement);
    const issues = validateSubmissionPayload(payload);
    if (issues.length > 0) {
      this.setStatus(issues.join(" "), "error");
      return;
    }

    this.setStatus("Sende Abgabe...", "warning");

    try {
      const response = await withRetry(() => this.apiClient.postJson("/api/v1/submissions", payload));
      const submission = response?.submission || {};

      this.setStatus(
        `Abgabe gespeichert: ${submission.learner_alias || payload.learner_alias} / ${submission.task_id || payload.task_id}`,
        "success"
      );

      this.formElement.reset();
      const sourceField = this.formElement.querySelector('input[name="source"]');
      const contentTypeField = this.formElement.querySelector('select[name="content_type"]');
      if (sourceField) {
        sourceField.value = "webapp";
      }
      if (contentTypeField) {
        contentTypeField.value = "text";
      }
    } catch (error) {
      renderStatus(this.statusElement, error);
    }
  }

  bind() {
    this.formElement?.addEventListener("submit", (event) => this.submit(event));
  }
}

const apiBaseUrl = window.SUBMISSION_API_BASE_URL || window.PYTHON_API_URL || "/api-proxy.php";
const apiClient = new ApiClient(apiBaseUrl, { timeoutMs: 10000 });

new SubmissionForm(
  document.getElementById("submissionForm"),
  document.getElementById("submissionStatus"),
  apiClient
).bind();

new KeywordIndexFilter(
  document.getElementById("keywordSearch"),
  document.getElementById("keywordList")
).bind();

for (const card of document.querySelectorAll(".exercise-card")) {
  new ExerciseEvaluator(card).bind();
}

const navToggle = document.querySelector(".nav-toggle");
const primaryNav = document.getElementById("primaryNav");

if (navToggle && primaryNav) {
  navToggle.addEventListener("click", () => {
    const isOpen = primaryNav.classList.toggle("is-open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });

  primaryNav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      if (window.innerWidth <= 900) {
        primaryNav.classList.remove("is-open");
        navToggle.setAttribute("aria-expanded", "false");
      }
    });
  });
}
