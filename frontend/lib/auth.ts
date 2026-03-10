"use client";

import Cookies from "js-cookie";
import { apiFetch } from "./api";

const ACCESS_KEY = "eco224_access";
const REFRESH_KEY = "eco224_refresh";
const ME_KEY = "eco224_me";

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
  localStorage.removeItem(ME_KEY);
  Cookies.remove("access");
  Cookies.remove("user_role");
}

export async function login(contact: string, password: string) {
  const data = await apiFetch<{ access: string; refresh: string }>("/api/token/", {
    method: "POST",
    body: JSON.stringify({ contact, password }),
  });

  setTokens(data.access, data.refresh);
  Cookies.set("access", data.access, { expires: 7 });

  // Récupère le vrai user (et surtout le vrai rôle)
  // Assure-toi que ton backend expose /api/me/
  const me = await apiFetch<{ role: string; full_name?: string; contact?: string }>(
    "/api/me/",
    { token: data.access },
  );

  if (me?.role) {
    Cookies.set("user_role", me.role, { expires: 7 });
  }

  localStorage.setItem(ME_KEY, JSON.stringify(me));

  return { ...data, user: me };
}