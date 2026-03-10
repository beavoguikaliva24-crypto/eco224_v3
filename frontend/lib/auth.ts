"use client";

import { apiFetch } from "./api";
import Cookies from "js-cookie";

const ACCESS_KEY = "eco224_access";
const REFRESH_KEY = "eco224_refresh";

export function setTokens(access: string, refresh: string) {
  localStorage.setItem(ACCESS_KEY, access);
  localStorage.setItem(REFRESH_KEY, refresh);
}

export async function login(contact: string, password: string) {
  const data = await apiFetch<{ access: string; refresh: string }>("/api/token/", {
    method: "POST",
    body: JSON.stringify({ contact, password }),
  });

  setTokens(data.access, data.refresh);
  Cookies.set("access", data.access, { expires: 7 });

  // Important: récupérer le profil réel
  const me = await apiFetch<{ role: string; full_name?: string; contact?: string }>("/api/me/", {
    token: data.access,
  });

  Cookies.set("user_role", me.role, { expires: 7 });
  localStorage.setItem("eco224_me", JSON.stringify(me));

  return { ...data, user: me };
}