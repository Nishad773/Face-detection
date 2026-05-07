function trimTrailingSlash(value) {
  return value.replace(/\/+$/, "");
}

function toWebSocketOrigin(httpOrigin) {
  if (httpOrigin.startsWith("https://")) {
    return `wss://${httpOrigin.slice("https://".length)}`;
  }
  if (httpOrigin.startsWith("http://")) {
    return `ws://${httpOrigin.slice("http://".length)}`;
  }
  return httpOrigin;
}

const backendOrigin = trimTrailingSlash(
  import.meta.env.VITE_BACKEND_ORIGIN ?? "http://localhost:8000",
);

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL
  ? trimTrailingSlash(import.meta.env.VITE_API_BASE_URL)
  : `${backendOrigin}/api/v1`;

export const INGEST_WS_URL = import.meta.env.VITE_WS_INGEST_URL
  ? trimTrailingSlash(import.meta.env.VITE_WS_INGEST_URL)
  : `${toWebSocketOrigin(backendOrigin)}/api/v1/ws/ingest`;

