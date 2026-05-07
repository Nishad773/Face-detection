import { API_BASE_URL } from "../config";

export async function fetchLatestRoi(sessionId) {
  const response = await fetch(`${API_BASE_URL}/roi/latest?session_id=${encodeURIComponent(sessionId)}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch ROI: ${response.status}`);
  }
  return response.json();
}
