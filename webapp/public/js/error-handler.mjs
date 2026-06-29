import { ApiError } from "./api-client.mjs";

export function sanitizeStudentFacingMessage(message) {
  const normalized = String(message || "");
  return normalized
    .replace(/^\s*#{1,6}\s*CTX-GOV\b.*$/gim, "")
    .replace(/^\s*CTX-GOV\s*:\s*.*$/gim, "")
    .replace(/\bCTX-GOV\b[^\r\n]*/gi, "")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

export function classifyError(error) {
  if (error instanceof ApiError) {
    if (error.code === "REQUEST_TIMEOUT" || error.code === "NETWORK_ERROR") {
      return {
        headline: "Netzwerkproblem",
        message: error.message,
        retryable: true,
      };
    }

    if (error.status >= 500) {
      return {
        headline: "Serverfehler",
        message: error.message,
        retryable: true,
      };
    }

    return {
      headline: "Ungültige Eingabe",
      message: error.message,
      retryable: false,
    };
  }

  return {
    headline: "Unerwarteter Fehler",
    message: error?.message || "Unbekannter Fehler",
    retryable: false,
  };
}

export async function withRetry(operation, { attempts = 3, baseDelayMs = 300 } = {}) {
  let lastError;

  for (let attempt = 1; attempt <= attempts; attempt += 1) {
    try {
      return await operation();
    } catch (error) {
      lastError = error;
      const info = classifyError(error);
      if (!info.retryable || attempt === attempts) {
        break;
      }
      await new Promise((resolve) => window.setTimeout(resolve, baseDelayMs * attempt));
    }
  }

  throw lastError;
}

export function renderStatus(targetElement, error) {
  const info = classifyError(error);
  const message = sanitizeStudentFacingMessage(`${info.headline}: ${info.message}`) || "Fehler bei der Anfrage.";
  targetElement.textContent = message;
  targetElement.dataset.state = info.retryable ? "warning" : "error";
  targetElement.closest(".feedback-box")?.setAttribute("data-state", info.retryable ? "warning" : "error");
}
