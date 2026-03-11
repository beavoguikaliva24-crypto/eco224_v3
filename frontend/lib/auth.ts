import Cookies from "js-cookie";

const ACCESS_KEY = "access";
const REFRESH_KEY = "refresh";
const ROLE_KEY = "user_role";

export function setTokens(access: string, refresh: string, role?: string) {
  // Stockage en Cookie pour le Middleware (Serveur)
  Cookies.set(ACCESS_KEY, access, { expires: 7, path: '/', sameSite: 'lax' });
  if (role) Cookies.set(ROLE_KEY, role, { expires: 7, path: '/' });

  // Optionnel : Garder le localStorage pour vos scripts clients existants
  localStorage.setItem(ACCESS_KEY, access);
  localStorage.setItem(REFRESH_KEY, refresh);
  if (role) localStorage.setItem(ROLE_KEY, role);
}

export function clearTokens() {
  Cookies.remove(ACCESS_KEY, { path: '/' });
  Cookies.remove(ROLE_KEY, { path: '/' });
  localStorage.removeItem(ACCESS_KEY);
  localStorage.removeItem(REFRESH_KEY);
  localStorage.removeItem(ROLE_KEY);
}