import axios from "axios";

const api = axios.create({
  baseURL: "/api",
});

export const unwrap = <T>(p: Promise<{ data: T }>) =>
  p.then(r => r.data);

let onLogout: (() => void)|null = null;
export const setLogoutHandler = (fn:() => void) => {
  onLogout = fn;
};

let isRefreshing = false;
let refreshPromise: Promise<void> | null = null;

api.interceptors.response.use(
  res => res,
  async error => {
    const original = error.config;
    if (error.response?.status !== 401) {
      return Promise.reject(error);
    }
    if (original._retry) {
      onLogout?.();
      return Promise.reject(error);
    }
    original._retry = true;
    if (!isRefreshing) {
      isRefreshing = true;
      refreshPromise = axios.post(
        "/api/auth/user/refresh",
        {},
        { withCredentials: true }
      ).finally(() => {
        isRefreshing = false;
      });
    }
    try {
      await refreshPromise;
      return api(original);
    } catch {
      onLogout?.();
      return Promise.reject(error);
    }
  }
);

export default api;

export async function fetchWithAuth(
  input:RequestInfo,
  init:RequestInit={}
): Promise<Response> {
  const res = await fetch(input, {
    credentials: "include",
    ...init,
  });
  if (res.status !== 401) return res;
  const refresh = await fetch("/api/auth/user/refresh", {
    method: "POST",
    credentials: "include",
  });
  if (!refresh.ok) {
    await fetch("/api/auth/user/logout", { method: "POST" });
    throw new Error("Unauthorized");
  }
  return fetch(input, {
    credentials: "include",
    ...init,
  });
}

