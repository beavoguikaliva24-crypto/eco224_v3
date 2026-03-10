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

        // Utilise l'URL de votre .env.local ou localhost par défaut
        const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";
        
        // L'URL correspond à votre configuration router.register(r"users", UserViewSet)
        const response = await axios.get(`${baseUrl}/api/accounts/users/me/`, {
          headers: { Authorization: `Bearer ${token}` }
        });

        setUser(response.data);
      } catch (error) {
        console.error("Session expirée ou erreur serveur");
        localStorage.removeItem('access');
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  return { user, loading };
}