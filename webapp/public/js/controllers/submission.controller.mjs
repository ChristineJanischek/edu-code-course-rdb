import { ApiClient } from "../api-client.mjs";
import { renderStatus, withRetry } from "../error-handler.mjs";
import { SubmissionModel } from "../models/submission.model.mjs";
import { SubmissionView } from "../views/submission.view.mjs";

class SubmissionController {
  constructor(formElement, statusElement, apiClient) {
    this.formElement = formElement;
    this.model = new SubmissionModel(formElement);
    this.view = new SubmissionView(formElement, statusElement);
    this.apiClient = apiClient;
  }

  bind() {
    if (!this.formElement) {
      return;
    }

    this.formElement.addEventListener("submit", (event) => this.submit(event));
  }

  async submit(event) {
    event.preventDefault();

    const payload = this.model.createPayload();
    const issues = this.model.validate(payload);
    if (issues.length > 0) {
      this.view.setStatus(issues.join(" "), "error");
      return;
    }

    this.view.setStatus("Sende Abgabe...", "warning");

    try {
      const response = await withRetry(() => this.apiClient.postJson("/api/v1/submissions", payload));
      const submission = response?.submission || {};

      this.view.setStatus(
        `Abgabe gespeichert: ${submission.learner_alias || payload.learner_alias} / ${submission.task_id || payload.task_id}`,
        "success"
      );
      this.view.resetFormDefaults();
    } catch (error) {
      renderStatus(this.view.statusElement, error);
    }
  }
}

export function initSubmissionController() {
  const apiBaseUrl = window.SUBMISSION_API_BASE_URL || window.PYTHON_API_URL || "/api-proxy.php";
  const apiClient = new ApiClient(apiBaseUrl, { timeoutMs: 10000 });

  new SubmissionController(
    document.getElementById("submissionForm"),
    document.getElementById("submissionStatus"),
    apiClient
  ).bind();
}
