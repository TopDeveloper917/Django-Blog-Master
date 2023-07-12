import axios from 'axios';

const access = localStorage.getItem('access_token');
const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
  headers: {
    'Content-Type': 'application/json',
    Authorization: access ? `Bearer ${access}` : '',
  },
});

export default api;