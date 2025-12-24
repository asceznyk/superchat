import axios from "axios";

const api = axios.create({
  baseurl: "/api"
});

export async function authGoogle() {
  const res = await axios.get('/api/auth/google/');
  return res.data;
}

