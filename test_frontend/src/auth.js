import api from './api';

const TOKEN_KEY = 'access_token';

export const login = async (email, password) => {
  const response = await api.post('user/token', { email, password });
  const token = response.data.access;
  localStorage.setItem(TOKEN_KEY, token);
  api.defaults.headers['Authorization'] = `Bearer ${token}`;
};

export const logout = () => {
  localStorage.removeItem(TOKEN_KEY);
  delete api.defaults.headers.common['Authorization'];
};

export const getToken = () => {
  return localStorage.getItem(TOKEN_KEY);
};

export const isAuthenticated = () => {
  const token = getToken();
  return !!token;
};