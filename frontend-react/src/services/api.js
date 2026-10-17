import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false,
});

export const authApi = {
  async login(payload) {
    return apiClient.post('/auth/login', payload);
  },
  async forgotPassword(payload) {
    return apiClient.post('/auth/forgot-password', payload);
  },
  async getProtectedExample(token) {
    return apiClient.get('/api/protected', {
      headers: {
        Authorization: 'Bearer ' + token,
      },
    });
  },
};

export function getApiErrorMessage(error) {
  if (error.response?.data?.error?.message) {
    return error.response.data.error.message;
  }

  if (error.code === 'ECONNABORTED') {
    return 'Request timed out. Please retry.';
  }

  if (error.message === 'Network Error') {
    return 'Network or backend configuration error. Verify Flask server and VITE_API_BASE_URL.';
  }

  return 'Unexpected error. Please try again.';
}

export { API_BASE_URL };
