import Cookies from "js-cookie";

const ACCESS_KEY = "access";
const REFRESH_KEY = "refresh";
const ROLE_KEY = "user_role";

/**
 * Récupère le token d'accès.
 * On vérifie d'abord les cookies (pour le SSR/Middleware) 
 * puis le localStorage (fallback client).
 */
export function getAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return Cookies.get(ACCESS_KEY) || localStorage.getItem(ACCESS_KEY);
}

/**
 * Récupère le rôle de l'utilisateur.
 */
export function getUserRole(): string | null {
  if (typeof window === "undefined") return null;
  return Cookies.get(ROLE_KEY) || localStorage.getItem(ROLE_KEY);
}

/**
 * Enregistre les jetons et le rôle dans les Cookies ET le LocalStorage.
 * Le cookie est indispensable pour que le Middleware Next.js ne bloque pas l'accès.
 */
export function setTokens(access: string, refresh: string, role?: string) {
  // 1. Stockage en Cookies (indispensable pour le Middleware)
  Cookies.set(ACCESS_KEY, access, { expires: 7, path: '/', sameSite: 'lax' });
  if (role) {
    Cookies.set(ROLE_KEY, role, { expires: 7, path: '/', sameSite: 'lax' });
  }

  // 2. Stockage en LocalStorage (pour la persistance côté client)
  if (typeof window !== "undefined") {
    localStorage.setItem(ACCESS_KEY, access);
    localStorage.setItem(REFRESH_KEY, refresh);
    if (role) localStorage.setItem(ROLE_KEY, role);
  }
}

/**
 * Nettoie toutes les traces de session.
 */
export function clearTokens() {
  // Suppression des Cookies
  Cookies.remove(ACCESS_KEY, { path: '/' });
  Cookies.remove(ROLE_KEY, { path: '/' });

  // Suppression du LocalStorage
  if (typeof window !== "undefined") {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
    localStorage.removeItem(ROLE_KEY);
  }
}