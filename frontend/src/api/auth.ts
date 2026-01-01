import api, { unwrap, setLogoutHandler } from '@/api/setup'

export const authGoogle = () => unwrap(api.get('/auth/google/'));

export const getUserProfile = () => unwrap(api.get('/auth/user/me'));

export const logoutUser = () => unwrap(api.post("/auth/user/logout"));

setLogoutHandler(() => {
  logoutUser();
})


