export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://beapc:8000";

export type Json = Record<string, unknown>;

export class ApiError extends Error {
  status: number;
  payload: unknown;
  constructor(message: string, status: number, payload: unknown) {
    super(message);
    this.status = status;
    this.payload = payload;
  }
}

export async function apiFetch<T>(
  path: string,
  opts: RequestInit & { token?: string } = {},
): Promise<T> {
  const url = `${API_BASE_URL}${path.startsWith("/") ? path : `/${path}`}`;
  const headers = new Headers(opts.headers);

  if (!headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  if (opts.token) {
    headers.set("Authorization", `Bearer ${opts.token}`);
  }

  const res = await fetch(url, { ...opts, headers });

  const contentType = res.headers.get("content-type") ?? "";
  const payload =
    contentType.includes("application/json") ? await res.json() : await res.text();

  if (!res.ok) {
    throw new ApiError("API request failed", res.status, payload);
  }
  return payload as T;
}