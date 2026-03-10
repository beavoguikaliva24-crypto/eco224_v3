"use client";
import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const router = useRouter();

    return (
        <div className="min-h-screen bg-slate-100 flex items-center justify-center p-4">
            <div className="max-w-md w-full bg-white rounded-xl shadow-lg p-8">
                <h2 className="text-3xl font-bold text-center text-slate-800 mb-8">Eco224</h2>
                
                {error && <p className="bg-red-100 text-red-600 p-3 rounded-lg mb-4 text-sm text-center">{error}</p>}
                
                <form className="space-y-6">
                    <div>
                        <label className="block text-sm font-medium text-slate-700">Utilisateur</label>
                        <input type="text" required value={username} onChange={(e) => setUsername(e.target.value)}
                            className="mt-1 w-full px-4 py-2 border border-slate-300 rounded-lg outline-none focus:ring-2 focus:ring-blue-500" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-slate-700">Mot de passe</label>
                        <input type="password" required value={password} onChange={(e) => setPassword(e.target.value)}
                            className="mt-1 w-full px-4 py-2 border border-slate-300 rounded-lg outline-none focus:ring-2 focus:ring-blue-500" />
                    </div>
                    <button type="submit" disabled={loading}
                        className="w-full bg-blue-600 text-white py-2 rounded-lg font-semibold hover:bg-blue-700 transition disabled:bg-slate-400">
                        {loading ? 'Connexion...' : 'Se connecter'}
                    </button>
                </form>
            </div>
        </div>
    );
}