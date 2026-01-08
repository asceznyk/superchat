import api, { unwrap, setLogoutHandler } from '@/api/setup'

export const authGoogle = (cpath:string) => unwrap(
  api.get(`/auth/google/?cpath=${cpath}`)
);

export const getUserProfile = () => unwrap(api.get('/auth/user/me'));

export const logoutUser = () => unwrap(api.post('/auth/user/logout'));

setLogoutHandler(() => {
  logoutUser();
})


