const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

export async function fetchLatestRoi(sourceId = "default") {
  const response = await fetch(`${API_BASE_URL}/roi/latest?source_id=${encodeURIComponent(sourceId)}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch ROI: ${response.status}`);
  }
  return response.json();
}

