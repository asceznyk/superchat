import axios from "axios";

const api = axios.create({
  baseURL: "/api"
});

export async function authGoogle() {
  const res = await api.get('/auth/google/');
  return res.data;
}

