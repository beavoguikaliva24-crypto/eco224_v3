"use client";

import { Users, GraduationCap, Briefcase, TrendingUp } from "lucide-react";

const stats = [
  { label: "Total Élèves", value: "1,240", icon: GraduationCap, color: "bg-blue-500" },
  { label: "Enseignants", value: "48", icon: Briefcase, color: "bg-purple-500" },
  { label: "Utilisateurs", value: "12", icon: Users, color: "bg-zinc-900" },
  { label: "Taux de présence", value: "94%", icon: TrendingUp, color: "bg-emerald-500" },
];

export default function DashboardPage() {
  return (
    <div className="space-y-10">
      <div>
        <h1 className="text-3xl font-extrabold tracking-tight text-zinc-950 dark:text-zinc-50">Tableau de bord</h1>
        <p className="text-zinc-500 mt-1">Voici ce qui se passe dans votre établissement aujourd'hui.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <div key={stat.label} className="group relative overflow-hidden rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-6 transition-all hover:shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-zinc-500">{stat.label}</p>
                <p className="mt-2 text-3xl font-bold text-zinc-950 dark:text-zinc-50">{stat.value}</p>
              </div>
              <div className={`rounded-xl p-3 text-white ${stat.color}`}>
                <stat.icon size={24} />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Placeholder pour graphiques ou liste récente */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="rounded-3xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-8">
          <h3 className="text-lg font-bold mb-4">Activités récentes</h3>
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="flex items-center gap-4 p-3 rounded-xl bg-zinc-50 dark:bg-zinc-800/50">
                <div className="h-2 w-2 rounded-full bg-zinc-400" />
                <p className="text-sm text-zinc-600 dark:text-zinc-400">Nouvelle inscription enregistrée il y a 2h.</p>
              </div>
            ))}
          </div>
        </div>
        <div className="rounded-3xl border border-dashed border-zinc-300 dark:border-zinc-700 p-8 flex items-center justify-center">
          <p className="text-zinc-400 text-sm">Espace pour graphique de revenus/présence</p>
        </div>
      </div>
    </div>
  );
}