import Cookies from "js-cookie";

const ACCESS_KEY = "access";
const REFRESH_KEY = "refresh";
const ROLE_KEY = "user_role";

/**
 * Récupère le token d'accès.
 * Indispensable pour les appels API dans vos pages (ex: liste des élèves).
 */
export function getAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return Cookies.get(ACCESS_KEY) || localStorage.getItem(ACCESS_KEY);
}

/**
 * Récupère le rôle de l'utilisateur (DEV, ADMIN, STAFF, etc.)
 */
export function getUserRole(): string | null {
  if (typeof window === "undefined") return null;
  return Cookies.get(ROLE_KEY) || localStorage.getItem(ROLE_KEY);
}

/**
 * Enregistre les jetons et le rôle.
 * Cette fonction doit être appelée dans votre page de Login.
 */
export function setTokens(access: string, refresh: string, role?: string) {
  // 1. Stockage en Cookies (Lecture possible par le Middleware Next.js)
  Cookies.set(ACCESS_KEY, access, { expires: 7, path: '/', sameSite: 'lax' });
  if (role) {
    Cookies.set(ROLE_KEY, role, { expires: 7, path: '/', sameSite: 'lax' });
  }

  // 2. Stockage en LocalStorage (Pour la persistance côté client uniquement)
  if (typeof window !== "undefined") {
    localStorage.setItem(ACCESS_KEY, access);
    localStorage.setItem(REFRESH_KEY, refresh);
    if (role) localStorage.setItem(ROLE_KEY, role);
  }
}

/**
 * Supprime toutes les données de session lors de la déconnexion.
 */
export function clearTokens() {
  Cookies.remove(ACCESS_KEY, { path: '/' });
  Cookies.remove(ROLE_KEY, { path: '/' });
  
  if (typeof window !== "undefined") {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
    localStorage.removeItem(ROLE_KEY);
  }
}