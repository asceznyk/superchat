import axios from "axios";

const api = axios.create({
  baseURL: "/api"
});

export async function getRoot() {
  const res = await api.get('/');
  return res.data;
}


