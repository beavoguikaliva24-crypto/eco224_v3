"use client";

import { apiFetch } from "./api";

const ACCESS_KEY = "eco224_access";
const REFRESH_KEY = "eco224_refresh";

export function getAccessToken() {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(ACCESS_KEY);
}

export function setTokens(access: string, refresh: string) {
  localStorage.setItem(ACCESS_KEY, access);
  localStorage.setItem(REFRESH_KEY, refresh);
}

export function clearTokens() {
  localStorage.removeItem(ACCESS_KEY);
  localStorage.removeItem(REFRESH_KEY);
}

export async function login(contact: string, password: string) {
  // SimpleJWT default expects USERNAME_FIELD; chez toi => contact
  const data = await apiFetch<{ access: string; refresh: string }>(
    "/api/token/",
    {
      method: "POST",
      body: JSON.stringify({ contact, password }),
    },
  );
  setTokens(data.access, data.refresh);
  return data;
}