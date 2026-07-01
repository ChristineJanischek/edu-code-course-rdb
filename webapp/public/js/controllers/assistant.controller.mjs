import { ApiClient } from "../api-client.mjs";
import { renderStatus, withRetry } from "../error-handler.mjs";
import { AssistantModel } from "../models/assistant.model.mjs";
import { AssistantView } from "../views/assistant.view.mjs";

class AssistantController {
  constructor(formElement, statusElement, hintElement, apiClient) {
    this.formElement = formElement;
    this.apiClient = apiClient;
    this.model = new AssistantModel(formElement);
    this.view = new AssistantView(formElement, statusElement, hintElement);
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

    this.view.setStatus("Der Assistent erstellt einen Lernhinweis...", "warning");

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
    apiClient
  ).bind();
}
