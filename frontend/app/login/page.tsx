"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Lock, Phone, Loader2, Eye, EyeOff } from "lucide-react";
import axios from "axios";

export default function LoginPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({ phone: "", password: "" });
  
  // AJOUT DE CET ÉTAT POUR CORRIGER L'ERREUR
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      // Utilisation de la variable d'environnement du fichier .env.local
      const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "http://10.15.8.179:8000" || "http://beapc:8000";
      
      const response = await axios.post(`${baseUrl}/api/token/`, {
        contact: formData.phone,
        password: formData.password,
      });

      localStorage.setItem("access", response.data.access);
      localStorage.setItem("refresh", response.data.refresh);
      router.push("/dashboard");
    } catch (err: any) {
      if (!err.response) {
        setError("Le serveur est injoignable. Vérifiez votre connexion ou l'adresse API.");
      } else {
        setError("Identifiants incorrects.");
      }
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-300 px-4 py-6 dark:bg-zinc-950">
      
      {/* Conteneur Principal - Deux colonnes sur desktop */}
      <div className="flex w-full max-w-6xl overflow-hidden rounded-[2rem] border border-zinc-600 bg-white shadow-2xl shadow-zinc-200/50 dark:border-zinc-800 dark:bg-zinc-900 dark:shadow-none">
        
        {/* --- Colonne de gauche : Formulaire (max-w-xl pour un formulaire compact) --- */}
        <div className="flex w-full items-center justify-center p-8 sm:p-12 md:p-16 lg:max-w-xl lg:p-20">

          {/* IMAGE D'ARRIÈRE-PLAN SUBTILE POUR LE FORMULAIRE */}
          <div className="absolute inset-0 z-0">
            <img
              src="https://images.unsplash.com/photo-1579547621113-e4bb2a19bdd6?q=80&w=1600&auto=format&fit=crop" // Image abstraite subtile
              alt="Texture d'arrière-plan du formulaire"
              className="h-full w-full object-cover opacity-30 dark:opacity-10" // Opacité réduite pour la subtilité
            />
             <div className="absolute inset-0 bg-white/50 dark:bg-zinc-950/70" /> {/* Overlay pour la lisibilité */}
          </div>
          
          <div className="w-full max-w-sm space-y-10 z-10 relative">
            
            {/* Header du formulaire */}
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
                
                {/* Champ Téléphone */}
                <div className="space-y-2">
                  <label htmlFor="phone" className="text-sm font-medium text-zinc-800 dark:text-zinc-200">
                    Téléphone (contact)
                  </label>
                  {error && (
                    <p className="text-sm text-red-500">{error}</p>
                  )}
                  <div className="relative">
                    <Phone className="absolute left-4 top-3.5 h-5 w-5 text-zinc-400" />
                    <input
                      id="phone"
                      type="tel"
                      placeholder="624 00 00 00"
                      required
                      className="flex h-12 w-full rounded-xl border border-zinc-200 bg-white px-12 py-3 text-sm ring-offset-white transition-all focus:border-zinc-300 focus:outline-none focus:ring-2 focus:ring-zinc-950 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 dark:border-zinc-700 dark:bg-zinc-950 dark:ring-offset-zinc-950 dark:focus:ring-zinc-300"
                      onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    />
                  </div>
                </div>

                {/* Champ Mot de passe */}
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
                      className="flex h-12 w-full rounded-xl border border-zinc-200 bg-white px-12 py-3 text-sm ring-offset-white transition-all focus:border-zinc-300 focus:outline-none focus:ring-2 focus:ring-zinc-950 focus:ring-offset-2 dark:border-zinc-700 dark:bg-zinc-950 dark:focus:ring-zinc-300"
                      onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-4 top-3.5 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200"
                      aria-label={showPassword ? "Masquer le mot de passe" : "Afficher le mot de passe"}
                    >
                      {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                    </button>
                  </div>
                </div>
              </div>

              {/* Bouton de Soumission */}
              <button
                type="submit"
                disabled={isLoading}
                className="inline-flex h-12 w-full items-center justify-center whitespace-nowrap rounded-xl bg-zinc-950 px-6 py-3 text-sm font-semibold text-zinc-50 transition-colors hover:bg-zinc-900/90 focus:outline-none focus:ring-2 focus:ring-zinc-950 focus:ring-offset-2 disabled:pointer-events-none disabled:opacity-60 dark:bg-zinc-50 dark:text-zinc-950 dark:hover:bg-zinc-100/90"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                    Authentification en cours...
                  </>
                ) : (
                  "Se connecter à mon compte"
                )}
              </button>
            </form>

              {/* Footer du formulaire */}
            <p className="text-center text-sm text-zinc-600 dark:text-zinc-400 lg:text-left">
              Vous n&apos;avez pas encore de compte ?{" "}
              <a href="#" className="font-semibold text-zinc-950 underline-offset-4 hover:underline dark:text-zinc-50">
                S&apos;inscrire gratuitement
              </a>
            </p>
          </div>
        </div>

        {/* --- Colonne de droite : Image et Message (cachée sur mobile) --- */}
        <div className="relative hidden flex-1 lg:block">
          
          {/* Image d'arrière-plan avec overlay pour la lisibilité */}
          <div className="absolute inset-0">
            <img
              src="https://images.unsplash.com/photo-1557682250-33bd709cbe85?q=80&w=1600&auto=format&fit=crop" // Remplacez par votre image locale ou URL
              alt="Visual décoratif d'arrière-plan"
              className="h-full w-full object-cover"
            />
            {/* Gradient Overlay pour améliorer le contraste du texte */}
            <div className="absolute inset-0 bg-gradient-to-t from-zinc-950/90 via-zinc-950/50 to-transparent" />
          </div>

          {/* Contenu textuel sur l'image */}
          <div className="relative flex h-full flex-col justify-end p-6">
            <div className="max-w-xl space-y-2">
              {/* Message Principal */}
              <h2 className="text-4xl font-extrabold tracking-tighter text-white">
                Gérez votre etablissement, <br />
                simplement.
              </h2>
              {/* Sous-message */}
              <p className="text-lg text-zinc-200">
                Accédez à votre tableau de bord centralisé pour suivre vos ventes, vos clients et vos stocks en temps réel.
              </p>
              
              {/* Optionnel: Un petit badge/logo de marque */}
              <div className="absolute top-12 left-16 flex items-center gap-3">
                 <div className="w-35 h-35 rounded-full bg-white/10 backdrop-blur-sm border border-white/20 flex items-center justify-center">
                    <span className="text-white font-bold text-xl rounded-full">
                      <img src="/eco1.png" alt="Logo" className="w-34 h-34 rounded-full"/>
                    </span>
                    
                 </div>
                 <span className="text-white font-semibold text-xl tracking-tight">GESTION SCOLAIRE</span>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}