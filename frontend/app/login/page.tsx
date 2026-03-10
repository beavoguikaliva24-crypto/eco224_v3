"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Lock, Phone, Loader2, Eye, EyeOff } from "lucide-react";
import Cookies from "js-cookie";
import axios from "axios";
import { API_BASE_URL } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({ phone: "", password: "" });
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      await login(formData.phone.trim(), formData.password);
      router.push("/dashboard");
    } catch (err) {
      if (err instanceof ApiError) {
        if (err.status === 401) setError("Numéro ou mot de passe incorrect.");
        else if (err.status >= 500) setError("Erreur serveur, veuillez réessayer.");
        else setError("Connexion impossible. Vérifiez les informations saisies.");
      } else {
        setError("Une erreur inattendue est survenue.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-300 px-4 py-6 dark:bg-zinc-950">
      <div className="flex w-full max-w-6xl overflow-hidden rounded-[2rem] border border-zinc-600 bg-white shadow-2xl shadow-zinc-200/50 dark:border-zinc-800 dark:bg-zinc-900 dark:shadow-none">
        {/* Colonne Gauche - Formulaire */}
        <div className="flex w-full items-center justify-center p-8 sm:p-12 md:p-16 lg:max-w-xl lg:p-20">
          <div className="absolute inset-0 z-0">
            <img
              src="https://images.unsplash.com/photo-1579547621113-e4bb2a19bdd6?q=80&w=1600&auto=format&fit=crop"
              alt="Background"
              className="h-full w-full object-cover opacity-30 dark:opacity-10"
            />
            <div className="absolute inset-0 bg-white/50 dark:bg-zinc-950/70" />
          </div>

          <div className="relative z-10 w-full max-w-sm space-y-10">
            <div className="text-center lg:text-left">
              <h1 className="text-4xl font-extrabold tracking-tighter text-zinc-950 dark:text-zinc-50">
                Bienvenue
              </h1>
              <p className="mt-3 text-base text-zinc-600 dark:text-zinc-400">
                Connectez-vous à votre compte pour gérer vos activités.
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-4">
                <div className="space-y-2">
                  <label htmlFor="phone" className="text-sm font-medium text-zinc-800 dark:text-zinc-200">
                    Téléphone (contact)
                  </label>
                  {error && (
                    <p className="rounded-md bg-red-50 p-2 text-sm text-red-600 dark:bg-red-900/20 dark:text-red-400">
                      {error}
                    </p>
                  )}
                  <div className="relative">
                    <Phone className="absolute left-4 top-3.5 h-5 w-5 text-zinc-400" />
                    <input
                      id="phone"
                      type="tel"
                      placeholder="624 00 00 00"
                      required
                      value={formData.phone}
                      className="flex h-12 w-full rounded-xl border border-zinc-200 bg-white px-12 py-3 text-sm transition-all focus:border-zinc-950 focus:outline-none focus:ring-1 focus:ring-zinc-950 dark:border-zinc-700 dark:bg-zinc-950 dark:focus:border-zinc-300 dark:focus:ring-zinc-300"
                      onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <label htmlFor="password" className="text-sm font-medium text-zinc-800 dark:text-zinc-200">
                      Mot de passe
                    </label>
                    <a href="#" className="text-xs text-zinc-500 hover:text-zinc-950 hover:underline dark:hover:text-zinc-300">
                      Oublié ?
                    </a>
                  </div>
                  <div className="relative">
                    <Lock className="absolute left-4 top-3.5 h-5 w-5 text-zinc-400" />
                    <input
                      id="password"
                      type={showPassword ? "text" : "password"}
                      required
                      value={formData.password}
                      className="flex h-12 w-full rounded-xl border border-zinc-200 bg-white px-12 py-3 text-sm transition-all focus:border-zinc-950 focus:outline-none focus:ring-1 focus:ring-zinc-950 dark:border-zinc-700 dark:bg-zinc-950 dark:focus:border-zinc-300 dark:focus:ring-zinc-300"
                      onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-4 top-3.5 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200"
                    >
                      {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                    </button>
                  </div>
                </div>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="inline-flex h-12 w-full items-center justify-center rounded-xl bg-zinc-950 px-6 py-3 text-sm font-semibold text-zinc-50 transition-colors hover:bg-zinc-900/90 disabled:opacity-60 dark:bg-zinc-50 dark:text-zinc-950 dark:hover:bg-zinc-100/90"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                    Authentification...
                  </>
                ) : (
                  "Se connecter à mon compte"
                )}
              </button>
            </form>

            <p className="text-center text-sm text-zinc-600 dark:text-zinc-400 lg:text-left">
              Vous n&apos;avez pas encore de compte ?{" "}
              <a href="#" className="font-semibold text-zinc-950 underline-offset-4 hover:underline dark:text-zinc-50">
                S&apos;inscrire gratuitement
              </a>
            </p>
          </div>
        </div>

        {/* Colonne Droite - Image */}
        <div className="relative hidden flex-1 lg:block">
          <div className="absolute inset-0">
            <img
              src="https://images.unsplash.com/photo-1557682250-33bd709cbe85?q=80&w=1600&auto=format&fit=crop"
              alt="Visual décoratif"
              className="h-full w-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-zinc-950/90 via-zinc-950/50 to-transparent" />
          </div>
          <div className="relative flex h-full flex-col justify-end p-6">
            <div className="max-w-xl space-y-2">
              <h2 className="text-4xl font-extrabold tracking-tighter text-white">
                Gérez votre etablissement, <br />
                simplement.
              </h2>
              <p className="text-lg text-zinc-200">
                Accédez à votre tableau de bord centralisé pour suivre vos ventes, vos clients et vos stocks en temps réel.
              </p>
              <div className="absolute left-16 top-12 flex items-center gap-3">
                <div className="flex h-35 w-35 items-center justify-center rounded-full border border-white/20 bg-white/10 backdrop-blur-sm">
                  <span className="rounded-full text-xl font-bold text-white">
                    <img src="/eco1.png" alt="Logo" className="h-34 w-34 rounded-full" />
                  </span>
                </div>
                <span className="text-xl font-semibold tracking-tight text-white">GESTION SCOLAIRE</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}