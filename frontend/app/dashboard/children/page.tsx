"use client";

import { useEffect, useState } from "react";
import { Users, Phone, UserCircle, Loader2, AlertCircle } from "lucide-react";
import { getAccessToken } from "@/lib/auth";
import { apiFetch, ApiError } from "@/lib/api";

type Child = {
  id: number;
  full_name: string;
  matricule: string;
  photo: string | null;
  classe: string;          // Correspond à get_classe
  annee_scolaire: string;  // Correspond à get_annee_scolaire
};

type ChildrenResponse = { results?: Child[] } | Child[];

function normalizeChild(raw: any): Child {
  return {
    id: raw.id,
    // Adaptation aux champs réels de ton Student model (prenom1, nom)
    full_name: raw.full_name || `${raw.prenom1 ?? ''} ${raw.nom ?? ''}`.trim() || "Nom inconnu",
    matricule: raw.matricule,
    photo: raw.photo,
    classe: raw.classe_label || raw.classe || "Non définie", 
    annee_scolaire: raw.annee_scolaire || "2023-2024",
  };
}
export default function ChildrenPage() {
  const [children, setChildren] = useState<Child[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    (async () => {
      setLoading(true);
      setError("");
      try {
        const token = getAccessToken();
        if (!token) {
          setError("Session invalide. Veuillez vous reconnecter.");
          return;
        }
        const data = await apiFetch<ChildrenResponse>("/api/people/children/", { token });
        const list = Array.isArray(data) ? data : (data.results ?? []);
        setChildren(list.map(normalizeChild));
      } catch (err) {
        if (err instanceof ApiError) {
        if (err.status === 401) setError("Session expirée ou token invalide. Veuillez vous reconnecter.");
        else if (err.status === 403) setError("Accès refusé.");
        else if (err.status === 404) setError("Route backend absente: /api/people/children/.");
        else setError("Impossible de charger la liste des enfants.");
        } else {
          setError("Une erreur inattendue est survenue.");
        }
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return (
    <section className="space-y-6">
      <header>
        <h1 className="text-3xl font-extrabold tracking-tight">Mes enfants</h1>
        <p className="mt-1 text-zinc-600">Consultez les informations scolaires de vos enfants.</p>
      </header>

      {loading && (
        <div className="flex items-center gap-2 rounded-xl border border-zinc-200 bg-white p-4">
          <Loader2 className="h-5 w-5 animate-spin text-zinc-500" />
          <span className="text-sm text-zinc-600">Chargement...</span>
        </div>
      )}

      {!loading && error && (
        <div className="flex items-start gap-2 rounded-xl border border-red-200 bg-red-50 p-4 text-red-700">
          <AlertCircle className="mt-0.5 h-5 w-5" />
          <p className="text-sm">{error}</p>
        </div>
      )}

      {!loading && !error && children.length === 0 && (
        <div className="rounded-2xl border border-dashed border-zinc-300 p-10 text-center">
          <Users className="mx-auto mb-3 h-8 w-8 text-zinc-400" />
          <p className="font-semibold text-zinc-700">Aucun enfant trouvé</p>
        </div>
      )}

      {!loading && !error && children.length > 0 && (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {children.map((child, index) => {
  const childKey =
    child.id ??
    child.matricule ??
    `${child.full_name || "child"}-${index}`;

  return (
            <article key={childKey} className="rounded-2xl border border-zinc-200 bg-white p-5">
              <div className="mb-4 flex items-center gap-3">
                <div className="h-12 w-12 overflow-hidden rounded-full border border-zinc-200 bg-zinc-100">
                  {child.photo ? (
                    <img src={child.photo} alt={child.full_name} className="h-full w-full object-cover" />
                  ) : (
                    <div className="flex h-full w-full items-center justify-center">
                      <UserCircle className="h-7 w-7 text-zinc-400" />
                    </div>
                  )}
                </div>
                <div>
                  <h2 className="text-base font-bold">{child.full_name}</h2>
                  <p className="text-xs uppercase text-zinc-500">{child.matricule || "Matricule non défini"}</p>
                </div>
              </div>
              <div className="space-y-2 text-sm text-zinc-600">
                <p>Classe: <b>{child.classe || "Non définie"}</b></p>
                <p>Année scolaire: <b>{child.annee_scolaire || "Non définie"}</b></p>
                </div>
            </article>
            );
            })}
        </div>
      )}
    </section>
  );
}