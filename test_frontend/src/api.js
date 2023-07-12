import axios from 'axios';
import dotenv from 'dotenv';
dotenv.config();

const access = localStorage.getItem('access_token');
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL | 'http://localhost:8000/api/',
  headers: {
    'Content-Type': 'application/json',
    Authorization: access ? `Bearer ${access}` : '',
  },
});

export default api;