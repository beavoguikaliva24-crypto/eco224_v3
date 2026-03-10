import { useState, useEffect } from 'react';
import axios from 'axios';

export function useAuth() {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const token = localStorage.getItem('access');
        if (!token) {
          setLoading(false);
          return;
        }

        const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";
        
        // On appelle l'endpoint de profil (ajustez selon votre vue Django)
        // Si vous n'avez pas d'endpoint /me/, utilisez /api/users/{id}/
        const response = await axios.get(`${baseUrl}/api/users/me/`, {
          headers: { Authorization: `Bearer ${token}` }
        });

        setUser(response.data);
      } catch (error) {
        console.error("Erreur de récupération utilisateur", error);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  return { user, loading };
}