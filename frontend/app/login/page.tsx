"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { login } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();
  const [contact, setContact] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await login(contact, password);
      router.push("/");
    } catch (err: any) {
      setError("Connexion impossible. Vérifie le contact/mot de passe.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 420, margin: "60px auto", padding: 20 }}>
      <h1 style={{ fontSize: 24, marginBottom: 16 }}>Connexion</h1>

      <form onSubmit={onSubmit} style={{ display: "grid", gap: 12 }}>
        <label style={{ display: "grid", gap: 6 }}>
          Téléphone (contact)
          <input
            value={contact}
            onChange={(e) => setContact(e.target.value)}
            placeholder="Ex: 624000000"
            required
          />
        </label>

        <label style={{ display: "grid", gap: 6 }}>
          Mot de passe
          <input
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type="password"
            required
          />
        </label>

        <button type="submit" disabled={loading}>
          {loading ? "Connexion..." : "Se connecter"}
        </button>

        {error ? <p style={{ color: "crimson" }}>{error}</p> : null}
      </form>
    </div>
  );
}