"use client";

import { useEffect, useState } from "react";
import { Users, Phone, School, UserCircle, Loader2, AlertCircle } from "lucide-react";
import { getAccessToken } from "@/lib/auth";
import { apiFetch, ApiError } from "@/lib/api";

type Child = {
  id: number;
  first_name?: string; // si backend mappe depuis prenom1
  last_name?: string;  // si backend mappe depuis nom
  prenom1?: string;    // fallback direct Student
  nom?: string;        // fallback direct Student
  matricule?: string;
  classe?: string | null;
  photo?: string | null;
  contact?: string;
  school_name?: string;
  date_naissance?: string;
  lieu_naissance?: string;
};

type ChildrenResponse = { results?: Child[] } | Child[];

function normalizeChild(raw: Child): Child {
  return {
    ...raw,
    first_name: raw.first_name ?? raw.prenom1 ?? "",
    last_name: raw.last_name ?? raw.nom ?? "",
    classe: raw.classe ?? null,
  };
}

export default function ChildrenPage() {
  const [children, setChildren] = useState<Child[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchChildren = async () => {
      setLoading(true);
      setError("");

      try {
        const token = getAccessToken();
        if (!token) {
          setError("Session invalide. Veuillez vous reconnecter.");
          return;
        }

        // Endpoint backend confirmé
        const data = await apiFetch<ChildrenResponse>("/api/children/", { token });
        const list = Array.isArray(data) ? data : (data.results ?? []);
        setChildren(list.map(normalizeChild));
      } catch (err) {
        if (err instanceof ApiError) {
          if (err.status === 403) {
            setError("Accès refusé. Cette page est réservée aux parents.");
          } else if (err.status === 404) {
            setError("Endpoint /api/children/ introuvable côté serveur.");
          } else {
            setError("Impossible de charger la liste des enfants.");
          }
        } else {
          setError("Une erreur inattendue est survenue.");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchChildren();
  }, []);

  return (
    <section className="space-y-6">
      <header>
        <h1 className="text-3xl font-extrabold tracking-tight text-zinc-950 dark:text-zinc-50">
          Mes enfants
        </h1>
        <p className="mt-1 text-zinc-600 dark:text-zinc-400">
          Consultez les informations scolaires de vos enfants.
        </p>
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
          {children.map((child) => (
            <article key={child.id} className="rounded-2xl border border-zinc-200 bg-white p-5">
              <div className="mb-4 flex items-center gap-3">
                <div className="h-12 w-12 overflow-hidden rounded-full border border-zinc-200 bg-zinc-100">
                  {child.photo ? (
                    <img
                      src={child.photo}
                      alt={`${child.first_name} ${child.last_name}`}
                      className="h-full w-full object-cover"
                    />
                  ) : (
                    <div className="flex h-full w-full items-center justify-center">
                      <UserCircle className="h-7 w-7 text-zinc-400" />
                    </div>
                  )}
                </div>
                <div>
                  <h2 className="text-base font-bold">
                    {child.first_name} {child.last_name}
                  </h2>
                  <p className="text-xs uppercase text-zinc-500">
                    {child.matricule || "Matricule non défini"}
                  </p>
                </div>
              </div>

              <div className="space-y-2 text-sm text-zinc-600">
                <p className="flex items-center gap-2">
                  <School className="h-4 w-4" />
                  Classe: <b>{child.classe || "—"}</b>
                </p>
                <p className="flex items-center gap-2">
                  <Phone className="h-4 w-4" />
                  Contact: <b>{child.contact || "—"}</b>
                </p>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}