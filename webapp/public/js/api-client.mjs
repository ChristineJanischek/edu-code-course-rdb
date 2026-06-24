export class ApiError extends Error {
  constructor(message, { status = 0, code = "API_ERROR", details = null, traceId = null } = {}) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
    this.details = details;
    this.traceId = traceId;
  }
}

function normalizeEnvelope(payload) {
  if (payload && typeof payload === "object" && ("success" in payload || "data" in payload || "error" in payload)) {
    if (payload.success === false) {
      const error = payload.error || {};
      return {
        success: false,
        error: {
          message: error.message || "API request failed",
          code: error.code || "API_ERROR",
          details: error.details ?? null,
        },
        meta: payload.meta || {},
      };
    }

    return {
      success: true,
      data: Object.prototype.hasOwnProperty.call(payload, "data") ? payload.data : payload,
      meta: payload.meta || {},
    };
  }

  return { success: true, data: payload, meta: {} };
}

async function parseResponse(response) {
  const contentType = response.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return normalizeEnvelope(await response.json());
  }

  return normalizeEnvelope({ raw: await response.text() });
}

export class ApiClient {
  constructor(baseUrl, { timeoutMs = 10000 } = {}) {
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.timeoutMs = timeoutMs;
  }

  buildUrl(path) {
    return `${this.baseUrl}${path.startsWith("/") ? path : `/${path}`}`;
  }

  async request(path, { method = "GET", headers = {}, body = undefined } = {}) {
    const controller = new AbortController();
    const timeoutId = window.setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const response = await fetch(this.buildUrl(path), {
        method,
        headers,
        body,
        signal: controller.signal,
      });

      const envelope = await parseResponse(response);
      const traceId = response.headers.get("X-Trace-Id") || envelope.meta?.trace_id || null;

      if (!response.ok || envelope.success === false) {
        const error = envelope.error || {};
        throw new ApiError(error.message || response.statusText || "API request failed", {
          status: response.status,
          code: error.code || "HTTP_ERROR",
          details: error.details ?? null,
          traceId,
        });
      }

      return envelope.data;
    } catch (error) {
      if (error.name === "AbortError") {
        throw new ApiError("Die Anfrage hat zu lange gedauert.", { code: "REQUEST_TIMEOUT" });
      }
      if (error instanceof ApiError) {
        throw error;
      }
      throw new ApiError(error.message || "Unerwarteter Netzwerkfehler", { code: "NETWORK_ERROR" });
    } finally {
      window.clearTimeout(timeoutId);
    }
  }

  get(path) {
    return this.request(path);
  }

  postJson(path, data) {
    return this.request(path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
  }
}
