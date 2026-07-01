import { ApiClient } from "../api-client.mjs";
import { renderStatus, withRetry } from "../error-handler.mjs";
import { AssistantModel } from "../models/assistant.model.mjs";
import { AssistantView } from "../views/assistant.view.mjs";

class AssistantController {
  constructor(formElement, statusElement, hintElement, continueButton, checkButton, editorElement, fileNameElement, apiClient) {
    this.formElement = formElement;
    this.apiClient = apiClient;
    this.model = new AssistantModel(formElement);
    this.view = new AssistantView(formElement, statusElement, hintElement);
    this.continueButton = continueButton;
    this.checkButton = checkButton;
    this.editorElement = editorElement;
    this.fileNameElement = fileNameElement;
  }

  bind() {
    if (!this.formElement) {
      return;
    }
    this.formElement.addEventListener("submit", (event) => this.submit(event));
    this.continueButton?.addEventListener("click", () => this.requestGuidance("continue"));
    this.checkButton?.addEventListener("click", () => this.requestGuidance("check"));
  }

  async submit(event) {
    event.preventDefault();

    const payload = this.model.createPayload();
    await this.sendPayload(payload, "Der Assistent erstellt einen Lernhinweis...");
  }

  async requestGuidance(mode) {
    const payload = this.model.createGuidedPayload(
      mode,
      this.editorElement?.value || "",
      this.fileNameElement?.value || ""
    );
    const statusText = mode === "check"
      ? "Der Assistent prüft deinen aktuellen Stand..."
      : "Der Assistent ermittelt den nächsten Lernschritt...";

    await this.sendPayload(payload, statusText);
  }

  async sendPayload(payload, loadingStatus) {
    const issues = this.model.validate(payload);
    if (issues.length > 0) {
      this.view.setStatus(issues.join(" "), "error");
      return;
    }

    this.view.setStatus(loadingStatus, "warning");

    try {
      const response = await withRetry(() => this.apiClient.postJson("/api/v1/assistant/hint", payload));
      this.view.renderHint(response);
      this.view.setStatus("Hinweis erfolgreich erstellt.", "success");
    } catch (error) {
      renderStatus(this.view.statusElement, error);
    }
  }
}

export function initAssistantController() {
  const apiBaseUrl = window.PYTHON_API_URL || "/api-proxy.php";
  const apiClient = new ApiClient(apiBaseUrl, { timeoutMs: 15000 });

  new AssistantController(
    document.getElementById("assistantHintForm"),
    document.getElementById("assistantHintStatus"),
    document.getElementById("assistantHintOutput"),
    document.getElementById("assistantContinueButton"),
    document.getElementById("assistantCheckButton"),
    document.getElementById("practiceEditor"),
    document.getElementById("practiceFileName"),
    apiClient
  ).bind();
}
