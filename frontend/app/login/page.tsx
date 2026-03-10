'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import { message } from 'antd'; // Utilisation d'Ant Design pour les alertes

const LoginPage = () => {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({ email: '', password: '' });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Remplacez l'URL par celle de votre API Django
      const response = await axios.post('http://127.0.0.1:8000/api/token/', {
        username: formData.email, // Django utilise souvent 'username' pour l'email dans JWT
        password: formData.password
      });

      if (response.data.access) {
        localStorage.setItem('token', response.data.access);
        message.success('Connexion réussie !');
        router.push('/dashboard');
      }
    } catch (error) {
      message.error('Identifiants invalides. Veuillez réessayer.');
      console.error('Erreur login:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6">
      <div className="flex w-full max-w-5xl bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-200">
        
        {/* Section Visuelle (Gauche) */}
        <div className="hidden lg:flex lg:w-1/2 bg-primary p-12 flex-col justify-between text-white relative">
          <div className="relative z-10">
            <h1 className="text-4xl font-bold leading-tight">ECORYS 224</h1>
            <p className="mt-4 text-primary-content/80 text-lg">
              La plateforme moderne pour la gestion de votre établissement scolaire.
            </p>
          </div>
          <div className="relative z-10">
            <p className="text-sm opacity-70">© 2026 BEAVOGUI - Tous droits réservés.</p>
          </div>
          {/* Décoration abstraite */}
          <div className="absolute -bottom-20 -left-20 w-80 h-80 bg-white/10 rounded-full blur-3xl"></div>
        </div>

        {/* Section Formulaire (Droite) */}
        <div className="w-full lg:w-1/2 p-10 md:p-16">
          <div className="text-center lg:text-left mb-10">
            <h2 className="text-3xl font-extrabold text-slate-800">Bienvenue 👋</h2>
            <p className="text-slate-500 mt-2 text-sm">Veuillez entrer vos accès pour continuer.</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="form-control">
              <label className="label">
                <span className="label-text font-bold text-slate-700">Adresse Email</span>
              </label>
              <input
                type="email"
                placeholder="nom@ecole.com"
                className="input input-bordered w-full h-12 focus:border-primary transition-all bg-slate-50"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                required
              />
            </div>

            <div className="form-control">
              <label className="label">
                <span className="label-text font-bold text-slate-700">Mot de passe</span>
              </label>
              <input
                type="password"
                placeholder="••••••••"
                className="input input-bordered w-full h-12 focus:border-primary transition-all bg-slate-50"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                required
              />
              <div className="flex justify-end mt-2">
                <a href="#" className="text-sm text-primary font-semibold hover:underline">Mot de passe oublié ?</a>
              </div>
            </div>

            <button 
              type="submit" 
              className={`btn btn-primary w-full h-12 text-white shadow-lg shadow-primary/20 ${loading ? 'loading' : ''}`}
              disabled={loading}
            >
              {loading ? 'Vérification...' : 'Se connecter'}
            </button>
          </form>
        </div>

      </div>
    </div>
  );
};

export default LoginPage;