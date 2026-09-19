/**
 * SmartClass - Módulo de Comunicação com a API RESTful
 */

const API_BASE_URL = window.API_BASE_URL || (
  window.location.port === '5000'
    ? '/api/v1'
    : (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:5000/api/v1'
        : `${window.location.origin}/api/v1`)
);

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
