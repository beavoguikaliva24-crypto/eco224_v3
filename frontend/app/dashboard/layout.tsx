"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  LayoutDashboard, Users, GraduationCap, FileText, BookOpen,
  ShieldAlert, CreditCard, Bell, School, HandCoins,
  ClipboardCheck, Settings, LogOut, Menu, X, History, 
  UserCircle
} from "lucide-react";

// On organise la navigation par sections pour plus de clarté
const menuGroups = [
  {
    title: "Général",
    items: [
      { name: "Vue d'ensemble", href: "/dashboard", icon: LayoutDashboard },
      { name: "Notifications", href: "/dashboard/notifications", icon: Bell },
    ]
  },
  {
    title: "Scolarité",
    items: [
      { name: "Inscriptions", href: "/dashboard/enrollment", icon: GraduationCap }, // enrollment app
      { name: "Classes & École", href: "/dashboard/school", icon: School }, // school app
      { name: "Matières", href: "/dashboard/schedule", icon: BookOpen }, // schedule app
      { name: "Notes & Examens", href: "/dashboard/grading", icon: FileText }, // grading app
      { name: "Discipline", href: "/dashboard/discipline", icon: ShieldAlert }, // discipline app
      { name: "Paiements", href: "/dashboard/paiements", icon: HandCoins}, // billing app
    ]
  },
  {
    title: "Administration",
    items: [
      { name: "Utilisateurs", href: "/dashboard/accounts", icon: Users }, // accounts app
      { name: "Personnel & RH", href: "/dashboard/people", icon: ClipboardCheck }, // people app
      { name: "Facturation", href: "/dashboard/billing", icon: CreditCard }, // billing app
      { name: "Logs & Audit", href: "/dashboard/audit", icon: History }, // audit app
    ]
  }
];

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const pathname = usePathname();

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950">
        {/* Mobile Sidebar Overlay */}
      <div className={`fixed inset-0 z-40 lg:hidden ${sidebarOpen ? "block" : "hidden"}`}>
        <div className="fixed inset-0 bg-zinc-900/80 backdrop-blur-sm" onClick={() => setSidebarOpen(false)} />
        <div className="fixed inset-y-0 left-0 w-64 bg-white dark:bg-zinc-900 p-6 shadow-xl">
          <div className="flex items-center justify-between mb-8">
            <span className="font-bold text-xl tracking-tight">ECORYS-224</span>
            <button onClick={() => setSidebarOpen(false)}><X size={24} /></button>
          </div>
          <nav className="space-y-2">
            {menuGroups.map((group) => (
              <div key={group.title}>
                <h3 className="px-4 text-xs font-semibold text-zinc-400 uppercase tracking-wider mb-2">
                  {group.title}
                </h3>
                <div className="space-y-1">
                  {group.items.map((item) => (
                    <Link
                      key={item.name}
                      href={item.href}
                      className={`flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-medium transition-all ${
                        pathname === item.href 
                        ? "bg-zinc-900 text-white shadow-md dark:bg-zinc-50 dark:text-zinc-950" 
                        : "text-zinc-500 hover:bg-zinc-100 dark:hover:bg-zinc-800 hover:text-zinc-950 dark:hover:text-zinc-200"
                      }`}
                    >
                      <item.icon size={18} />
                      {item.name}
                    </Link>
                  ))}
                </div>
              </div>
            ))}
          </nav>
        </div>
      </div>
      {/* Sidebar Desktop */}
      <aside className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-72 lg:flex-col border-r border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900">
        <div className="flex flex-col flex-grow p-6 overflow-y-auto">
          
          {/* Logo Section */}
          <div className="flex items-center gap-3 mb-8 px-2">
            <img src="/eco1.png" alt="Logo" className="h-10 w-10 rounded-full object-cover" />
            <span className="font-bold text-lg tracking-tight dark:text-white">GESTION SCOLAIRE</span>
          </div>

          {/* Navigation par Groupes */}
          <nav className="flex-1 space-y-8">
            {menuGroups.map((group) => (
              <div key={group.title}>
                <h3 className="px-4 text-xs font-semibold text-zinc-400 uppercase tracking-wider mb-2">
                  {group.title}
                </h3>
                <div className="space-y-1">
                  {group.items.map((item) => (
                    <Link
                      key={item.name}
                      href={item.href}
                      className={`flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-medium transition-all ${
                        pathname === item.href 
                        ? "bg-zinc-900 text-white shadow-md dark:bg-zinc-50 dark:text-zinc-950" 
                        : "text-zinc-500 hover:bg-zinc-100 dark:hover:bg-zinc-800 hover:text-zinc-950 dark:hover:text-zinc-200"
                      }`}
                    >
                      <item.icon size={18} />
                      {item.name}
                    </Link>
                  ))}
                </div>
              </div>
            ))}
          </nav>

          {/* Footer Sidebar */}
          <div className="mt-10 border-t border-zinc-100 dark:border-zinc-800 pt-4">
            <button className="flex w-full items-center gap-3 px-4 py-2.5 text-sm font-medium text-red-500 hover:bg-red-50 dark:hover:bg-red-900/10 rounded-xl transition-colors">
              <LogOut size={18} /> Déconnexion
            </button>
          </div>
        </div>
      </aside>

      {/* Reste du contenu (Header + Main) */}
      {/* Main Content Area */}
      <div className="lg:pl-72 flex flex-col min-h-screen">
        <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-zinc-200 dark:border-zinc-800 bg-white/80 dark:bg-zinc-900/80 backdrop-blur-md px-6">
          <button className="lg:hidden" onClick={() => setSidebarOpen(true)}><Menu size={24} /></button>
          <div className="ml-auto flex items-center gap-4">
            <button className="p-2 text-zinc-500 hover:bg-zinc-100 dark:hover:bg-zinc-800 rounded-full transition-colors relative">
              <Bell size={20} />
              <span className="absolute top-2 right-2 h-2 w-2 bg-red-500 rounded-full border-2 border-white dark:border-zinc-900" />
            </button>
            <div className="h-8 w-px bg-zinc-200 dark:border-zinc-800 mx-2" />
            <div className="flex items-center gap-3">
              <div className="text-right hidden sm:block">
                <p className="text-sm font-semibold dark:text-white text-zinc-950">Utilisateur</p>
                <p className="text-xs text-zinc-500">Administrateur</p>
              </div>
              <UserCircle size={32} className="text-zinc-400" />
            </div>
          </div>
        </header>

        <main className="p-6 lg:p-8 flex-grow">
          {children}
        </main>
      </div>
    </div>
  );
}