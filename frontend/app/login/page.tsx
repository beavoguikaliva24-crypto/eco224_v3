'use client';

import { useRouter } from 'next/navigation';

const LoginPage = () => {
  const router = useRouter();

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    console.log('Tentative de connexion...');
    // Logique d'authentification à ajouter ici
    // Pour l'instant, on redirige vers le tableau de bord
    router.push('/dashboard');
  };

  return (
    <div className="flex min-h-screen">
      {/* --- Volet Gauche (Image et Marque) --- */}
      <div className="hidden w-1/2 flex-col items-center justify-center bg-primary text-primary-content lg:flex">
        <div className="text-center">
          <h1 className="mb-4 text-5xl font-bold">ECOLE-224</h1>
          <p className="text-xl">Votre plateforme de gestion scolaire unifiée.</p>
        </div>
      </div>

      {/* --- Volet Droit (Formulaire de connexion) --- */}
      <div className="flex w-full items-center justify-center bg-base-100 p-8 lg:w-1/2">
        <div className="w-full max-w-md">
          <h2 className="mb-2 text-3xl font-bold">Bienvenue 👋</h2>
          <p className="mb-8 text-base-content/70">Veuillez entrer vos accès pour continuer.</p>

          <form onSubmit={handleSubmit}>
            <div className="form-control w-full">
              <label className="label">
                <span className="label-text">Adresse Email</span>
              </label>
              <input
                type="email"
                placeholder="nom@exemple.com"
                className="input input-bordered w-full"
                defaultValue="nom@ecole.com"
                required
              />
            </div>
            <div className="form-control mt-4 w-full">
              <label className="label">
                <span className="label-text">Mot de passe</span>
              </label>
              <input
                type="password"
                placeholder="********"
                className="input input-bordered w-full"
                defaultValue="password"
                required
              />
              <label className="label">
                <a href="#" className="link-hover link label-text-alt">
                  Mot de passe oublié ?
                </a>
              </label>
            </div>
            <div className="form-control mt-6">
              <button type="submit" className="btn btn-primary">
                Se connecter
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;