import axios from "axios";

const api = axios.create({
  baseURL: "/api"
});

export async function authGoogle() {
  const res = await api.get('/auth/google/');
  return res.data;
}

export async function getUserProfile() {
  const res = await api.get('/auth/user/me');
  return res.data;
}

export async function logoutUser() {
  const res = await api.post('/auth/user/logout');
  return res.data;
}

