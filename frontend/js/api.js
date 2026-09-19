function getApiBaseUrl() {
  if (window.API_BASE_URL) return window.API_BASE_URL;
  const origin = window.location.origin;
  const pathname = window.location.pathname;
  const basePath = pathname.startsWith('/smartclass') ? '/smartclass/api/v1' : '/api/v1';

  if (window.location.port === '5000' || (!origin.includes('localhost:3000') && !origin.includes('127.0.0.1:3000'))) {
    return `${origin}${basePath}`;
  }
  return 'http://localhost:5000/api/v1';
}

const API_BASE_URL = getApiBaseUrl();

export async function checkApiHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: "GET",
      headers: { "Accept": "application/json" }
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    console.warn("API Health Check falhou:", error.message);
    throw error;
  }
}

export async function fetchRecentReadings(limit = 100) {
  try {
    const response = await fetch(`${API_BASE_URL}/medicoes/recent?limit=${limit}`, {
      method: "GET",
      headers: { "Accept": "application/json" }
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const result = await response.json();
    return result.data || [];
  } catch (error) {
    console.error("Erro ao buscar medições recentes:", error.message);
    throw error;
  }
}

export async function sendTelemetryReading(payload) {
  try {
    const response = await fetch(`${API_BASE_URL}/medicoes`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
      },
      body: JSON.stringify(payload)
    });
    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.message || `Erro HTTP ${response.status}`);
    }
    return result;
  } catch (error) {
    console.error("Erro ao enviar medição:", error.message);
    throw error;
  }
}
