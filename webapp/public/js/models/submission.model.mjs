import { normalizeSubmissionForm, validateSubmissionPayload } from "../validators.mjs";

export class SubmissionModel {
  constructor(formElement) {
    this.formElement = formElement;
  }

  createPayload() {
    return normalizeSubmissionForm(this.formElement);
  }

  validate(payload) {
    return validateSubmissionPayload(payload);
  }
}
