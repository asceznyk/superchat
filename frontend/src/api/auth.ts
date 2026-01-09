import api, { unwrap, setLogoutHandler } from '@/api/setup'

export const authGoogle = (cpath:string) => unwrap(
  api.get(`/auth/google/?cpath=${cpath}`, null, { withCredentials: true })
);

export const getUserProfile = () => unwrap(
  api.get('/auth/user/me', null, { withCredentials: true })
);

export const getUserThreads = () => unwrap(
  api.get('/auth/user/threads', null, { withCredentials: true })
)

export const logoutUser = () => unwrap(
  api.post('/auth/user/logout', null, { withCredentials: true })
);

setLogoutHandler(() => {
  logoutUser();
})


