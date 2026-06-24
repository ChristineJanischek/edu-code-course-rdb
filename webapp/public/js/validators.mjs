const ALLOWED_CONTENT_TYPES = new Set(["text", "code", "summary", "translation", "transcript"]);

function normalizeText(value) {
  return String(value ?? "").trim();
}

export function normalizeSubmissionForm(formElement) {
  const formData = new FormData(formElement);
  return {
    learner_alias: normalizeText(formData.get("student_id")),
    task_id: normalizeText(formData.get("task_id")),
    response_text: normalizeText(formData.get("content")),
    response_kind: normalizeText(formData.get("content_type")) || "text",
    source_context: normalizeText(formData.get("source")) || "webapp",
    status: "submitted",
  };
}

export function validateSubmissionPayload(payload) {
  const issues = [];

  if (!payload.learner_alias) {
    issues.push("Schüler-ID fehlt.");
  } else if (payload.learner_alias.length > 80) {
    issues.push("Schüler-ID ist zu lang.");
  }

  if (!payload.task_id) {
    issues.push("Aufgaben-ID fehlt.");
  } else if (payload.task_id.length > 120) {
    issues.push("Aufgaben-ID ist zu lang.");
  }

  if (!payload.response_text) {
    issues.push("Antwort fehlt.");
  } else if (payload.response_text.length > 12000) {
    issues.push("Antwort ist zu lang.");
  }

  if (!ALLOWED_CONTENT_TYPES.has(payload.response_kind)) {
    issues.push("Inhaltstyp ist nicht erlaubt.");
  }

  return issues;
}
