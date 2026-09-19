/**
 * SmartClass - Módulo de Autenticação e Sessão do Operador
 */
const API_BASE_URL = window.location.port === '5000'
  ? ''
  : (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
      ? 'http://localhost:5000'
      : '');

export const AUTH_KEYS = {
  TOKEN: 'smartclass_auth_token',
  USER: 'smartclass_user',
  REMEMBER: 'smartclass_remember_login'
};

export async function loginUser(username, password, rememberMe = true) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username.trim(),
        password: password.trim()
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || 'Falha na autenticação.');
    }

    // Armazena no sessionStorage e/ou localStorage
    const storage = rememberMe ? localStorage : sessionStorage;
    storage.setItem(AUTH_KEYS.TOKEN, data.token);
    storage.setItem(AUTH_KEYS.USER, JSON.stringify(data.user));
    localStorage.setItem(AUTH_KEYS.REMEMBER, rememberMe ? 'true' : 'false');

    return {
      success: true,
      user: data.user,
      token: data.token
    };
  } catch (error) {
    return {
      success: false,
      message: error.message || 'Não foi possível conectar ao servidor de autenticação.'
    };
  }
}

export function getAuthUser() {
  const userStr = localStorage.getItem(AUTH_KEYS.USER) || sessionStorage.getItem(AUTH_KEYS.USER);
  if (!userStr) return null;
  try {
    return JSON.parse(userStr);
  } catch {
    return null;
  }
}

export function isAuthenticated() {
  const token = localStorage.getItem(AUTH_KEYS.TOKEN) || sessionStorage.getItem(AUTH_KEYS.TOKEN);
  return Boolean(token);
}

export function logoutUser() {
  localStorage.removeItem(AUTH_KEYS.TOKEN);
  localStorage.removeItem(AUTH_KEYS.USER);
  sessionStorage.removeItem(AUTH_KEYS.TOKEN);
  sessionStorage.removeItem(AUTH_KEYS.USER);
  
  // Redireciona para login
  window.location.href = 'login.html';
}
