export class SubmissionView {
  constructor(formElement, statusElement) {
    this.formElement = formElement;
    this.statusElement = statusElement;
  }

  setStatus(message, state = "success") {
    if (!this.statusElement) {
      return;
    }

    this.statusElement.textContent = message;
    this.statusElement.dataset.state = state;
    this.statusElement.closest(".feedback-box")?.setAttribute("data-state", state);
  }

  resetFormDefaults() {
    if (!this.formElement) {
      return;
    }

    this.formElement.reset();
    const sourceField = this.formElement.querySelector('input[name="source"]');
    const contentTypeField = this.formElement.querySelector('select[name="content_type"]');

    if (sourceField) {
      sourceField.value = "webapp";
    }
    if (contentTypeField) {
      contentTypeField.value = "text";
    }
  }
}
