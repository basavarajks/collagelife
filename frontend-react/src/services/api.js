import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
});

apiClient.interceptors.request.use((config) => {
  const token = window.sessionStorage.getItem('sdms_auth_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export const authApi = {
  login: (payload) => apiClient.post('/auth/login', payload),
  logout: () => apiClient.post('/auth/logout'),
  me: () => apiClient.get('/auth/me'),
  changePassword: (payload) => apiClient.post('/auth/change-password', payload),
  forgotPassword: (payload) => apiClient.post('/auth/forgot-password', payload),
  getProtectedExample: () => apiClient.get('/api/protected'),
};

export function getApiErrorMessage(error) {
  if (error.response?.data?.error?.message) return error.response.data.error.message;
  if (error.code === 'ECONNABORTED') return 'Request timed out. Please retry.';
  if (error.message === 'Network Error') return 'Backend unavailable. Start Flask and verify VITE_API_BASE_URL.';
  return 'Unexpected error. Please try again.';
}

export { API_BASE_URL };
