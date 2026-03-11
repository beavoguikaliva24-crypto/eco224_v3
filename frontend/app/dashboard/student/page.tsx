"use client";

import React, { useEffect, useState } from "react";
import axios from "axios";
import { getAccessToken } from "@/lib/auth"; // Assurez-vous du chemin correct
import { User, Search, Filter, Loader2 } from "lucide-react";

interface Student {
  id: number;
  first_name: string;
  last_name: string;
  matricule: string;
  classe_name: string; // Selon votre modèle Django
}

export default function StudentListPage() {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        const token = getAccessToken();
        const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "http://beapc:8000";
        
        const response = await axios.get(`${baseUrl}/api/students/`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        setStudents(response.data);
      } catch (err) {
        setError("Impossible de charger la liste des élèves.");
      } finally {
        setLoading(false);
      }
    };

    fetchStudents();
  }, []);

  if (loading) return (
    <div className="flex h-64 items-center justify-center">
      <Loader2 className="h-8 w-8 animate-spin text-zinc-500" />
    </div>
  );

  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-zinc-950 dark:text-zinc-50">Liste des Élèves</h1>
        <button className="rounded-lg bg-zinc-950 px-4 py-2 text-sm font-medium text-white dark:bg-zinc-50 dark:text-zinc-950">
          + Nouvel Élève
        </button>
      </div>

      <div className="overflow-hidden rounded-xl border border-zinc-200 bg-white dark:border-zinc-800 dark:bg-zinc-900">
        <table className="w-full text-left text-sm">
          <thead className="bg-zinc-50 text-zinc-600 dark:bg-zinc-800/50 dark:text-zinc-400">
            <tr>
              <th className="px-6 py-3 font-medium">Matricule</th>
              <th className="px-6 py-3 font-medium">Nom complet</th>
              <th className="px-6 py-3 font-medium">Classe</th>
              <th className="px-6 py-3 font-medium text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-200 dark:divide-zinc-800">
            {students.map((student) => (
              <tr key={student.id} className="hover:bg-zinc-50 dark:hover:bg-zinc-800/30">
                <td className="px-6 py-4 font-mono text-xs">{student.matricule}</td>
                <td className="px-6 py-4 font-medium">{student.first_name} {student.last_name}</td>
                <td className="px-6 py-4">{student.classe_name}</td>
                <td className="px-6 py-4 text-right">
                  <button className="text-zinc-500 hover:text-zinc-950 dark:hover:text-zinc-50">Modifier</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {students.length === 0 && (
          <div className="p-12 text-center text-zinc-500">Aucun élève enregistré pour le moment.</div>
        )}
      </div>
    </div>
  );
}