"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    // Mock authentication: navigate to dashboard on submit
    router.push("/dashboard");
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 dark:bg-black">
      <div className="w-full max-w-sm rounded-2xl bg-white p-8 shadow-md dark:bg-zinc-900">
        <h1 className="mb-6 text-2xl font-bold text-zinc-900 dark:text-zinc-50">
          Connexion
        </h1>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div className="flex flex-col gap-1">
            <label
              htmlFor="phone"
              className="text-sm font-medium text-zinc-700 dark:text-zinc-300"
            >
              Téléphone (contact)
            </label>
            <input
              id="phone"
              type="tel"
              placeholder="Ex: 624000000"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              required
              className="rounded-lg border border-zinc-300 px-4 py-2 text-zinc-900 focus:outline-none focus:ring-2 focus:ring-zinc-500 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-50"
            />
          </div>
          <div className="flex flex-col gap-1">
            <label
              htmlFor="password"
              className="text-sm font-medium text-zinc-700 dark:text-zinc-300"
            >
              Mot de passe
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="rounded-lg border border-zinc-300 px-4 py-2 text-zinc-900 focus:outline-none focus:ring-2 focus:ring-zinc-500 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-50"
            />
          </div>
          <button
            type="submit"
            className="mt-2 rounded-lg bg-zinc-900 px-4 py-2 font-semibold text-white transition-colors hover:bg-zinc-700 dark:bg-zinc-50 dark:text-zinc-900 dark:hover:bg-zinc-200"
          >
            Se connecter
          </button>
        </form>
      </div>
    </div>
  );
}
