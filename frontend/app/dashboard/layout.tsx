"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard, Users, GraduationCap, FileText, BookOpen,
  ShieldAlert, CreditCard, Bell, School, HandCoins,
  ClipboardCheck, LogOut, Menu, X, History,
  UserCircle, Loader2
} from "lucide-react";
import { useAuth } from "@/hooks/useAuth";

const menuGroups = [
  {
    title: "Général",
    items: [
      { name: "Vue d'ensemble", href: "/dashboard", icon: LayoutDashboard , roles: ["DEV", "ADMIN", "STAFF"] },
      { name: "Notifications", href: "/dashboard/notifications", icon: Bell, roles: ["DEV", "ADMIN", "STAFF", "PARENT"] },
    ]
  },
  {
    title: "Scolarité",
    items: [
      { name: "Eleves", href: "/dashboard/student", icon: Users, roles: ["DEV", "ADMIN", "STAFF"] },
      { name: "Inscriptions", href: "/dashboard/enrollment", icon: GraduationCap, roles: ["DEV", "ADMIN", "STAFF"] },
      { name: "Classes & École", href: "/dashboard/school", icon: School, roles: ["DEV", "ADMIN", "STAFF"] },
      { name: "Matières", href: "/dashboard/schedule", icon: BookOpen, roles: ["DEV", "ADMIN", "STAFF"]  },
      { name: "Notes & Bulletins", href: "/dashboard/grading", icon: FileText , roles: ["DEV", "ADMIN", "STAFF", "PARENT"] },
      { name: "Discipline", href: "/dashboard/discipline", icon: ShieldAlert , roles: ["DEV", "ADMIN", "STAFF", "PARENT"] },
      { name: "Paiements", href: "/dashboard/paiements", icon: HandCoins, roles: ["DEV", "ADMIN", "STAFF", "PARENT"] },
      { name: "Enfants", href: "/dashboard/children", icon: UserCircle, roles: ["DEV", "ADMIN", "PARENT"] },
    ]
  },
  {
    title: "Administration",
    items: [
      { name: "Utilisateurs", href: "/dashboard/accounts", icon: Users, roles: ["DEV", "ADMIN"] },
      { name: "Personnel & RH", href: "/dashboard/people", icon: ClipboardCheck, roles: ["DEV", "ADMIN", "STAFF"] },
      { name: "Facturation", href: "/dashboard/billing", icon: CreditCard, roles: ["DEV", "ADMIN"] },
      { name: "Logs & Audit", href: "/dashboard/audit", icon: History, roles: ["DEV"] },
    ]
  }
];

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const pathname = usePathname();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const filteredMenu = menuGroups
    .map((group) => ({
      ...group,
      items: group.items.filter((item) => !item.roles || (user && item.roles.includes(user.role))),
    }))
    .filter((group) => group.items.length > 0);

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950">
      {/* Mobile Sidebar Overlay */}
      <div className={`fixed inset-0 z-40 lg:hidden ${sidebarOpen ? "block" : "hidden"}`}>
        <div className="fixed inset-0 bg-zinc-900/80 backdrop-blur-sm" onClick={() => setSidebarOpen(false)} />
        <div className="fixed inset-y-0 left-0 w-64 bg-white dark:bg-zinc-900 p-6 shadow-xl">
          <div className="mb-8 flex items-center justify-between">
            <span className="text-xl font-bold tracking-tight">ECORYS-224</span>
            <button onClick={() => setSidebarOpen(false)}><X size={24} /></button>
          </div>

          <nav className="space-y-2">
            {filteredMenu.map((group) => (
              <div key={group.title}>
                <h3 className="mb-2 px-4 text-xs font-semibold uppercase tracking-wider text-zinc-400">
                  {group.title}
                </h3>
                <div className="space-y-1">
                  {group.items.map((item) => (
                    <Link
                      key={item.name}
                      href={item.href}
                      onClick={() => setSidebarOpen(false)}
                      className={`flex items-center gap-3 rounded-xl px-4 py-2.5 text-sm font-medium transition-all ${
                        pathname === item.href
                          ? "bg-zinc-900 text-white shadow-md dark:bg-zinc-50 dark:text-zinc-950"
                          : "text-zinc-500 hover:bg-zinc-100 hover:text-zinc-950 dark:hover:bg-zinc-800 dark:hover:text-zinc-200"
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
        <div className="flex flex-grow flex-col overflow-y-auto p-6">
          <div className="mb-8 flex items-center gap-3 px-2">
            <img src="/eco1.png" alt="Logo" className="h-10 w-10 rounded-full object-cover" />
            <span className="text-lg font-bold tracking-tight dark:text-white">GESTION SCOLAIRE</span>
          </div>

          <nav className="flex-1 space-y-8">
            {filteredMenu.map((group) => (
              <div key={group.title}>
                <h3 className="mb-2 px-4 text-xs font-semibold uppercase tracking-wider text-zinc-400">
                  {group.title}
                </h3>
                <div className="space-y-1">
                  {group.items.map((item) => (
                    <Link
                      key={item.name}
                      href={item.href}
                      className={`flex items-center gap-3 rounded-xl px-4 py-2.5 text-sm font-medium transition-all ${
                        pathname === item.href
                          ? "bg-zinc-900 text-white shadow-md dark:bg-zinc-50 dark:text-zinc-950"
                          : "text-zinc-500 hover:bg-zinc-100 hover:text-zinc-950 dark:hover:bg-zinc-800 dark:hover:text-zinc-200"
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

          <div className="mt-10 border-t border-zinc-100 pt-4 dark:border-zinc-800">
            <button className="flex w-full items-center gap-3 rounded-xl px-4 py-2.5 text-sm font-medium text-red-500 transition-colors hover:bg-red-50 dark:hover:bg-red-900/10">
              <LogOut size={18} /> Déconnexion
            </button>
          </div>
        </div>
      </aside>

      <div className="flex min-h-screen flex-col lg:pl-72">
        <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-zinc-200 bg-white/80 px-6 backdrop-blur-md dark:border-zinc-800 dark:bg-zinc-900/80">
          <button className="lg:hidden" onClick={() => setSidebarOpen(true)}><Menu size={24} /></button>

          <div className="ml-auto flex items-center gap-4">
            <button className="relative rounded-full p-2 text-zinc-500 transition-colors hover:bg-zinc-100 dark:hover:bg-zinc-800">
              <Bell size={20} />
              <span className="absolute right-2 top-2 h-2 w-2 rounded-full border-2 border-white bg-red-500 dark:border-zinc-900" />
            </button>

            <div className="mx-2 h-8 w-px bg-zinc-200 dark:border-zinc-800" />

            {loading ? (
              <Loader2 className="h-5 w-5 animate-spin text-zinc-400" />
            ) : (
              <div className="flex items-center gap-3">
                <div className="hidden text-right sm:block">
                  <p className="text-sm font-bold leading-none text-zinc-950 dark:text-white">
                    {user?.first_name} {user?.last_name}
                  </p>
                  <p className="mt-1 text-[10px] font-medium uppercase text-zinc-500">
                    {user?.role} • {user?.contact}
                  </p>
                </div>
                <div className="flex h-10 w-10 items-center justify-center overflow-hidden rounded-full border border-zinc-200 bg-zinc-100 dark:border-zinc-700">
                  {user?.photo ? (
                    <img src={user.photo} alt="Profil" className="h-full w-full object-cover" />
                  ) : (
                    <UserCircle className="h-6 w-6 text-zinc-400" />
                  )}
                </div>
              </div>
            )}
          </div>
        </header>

        <main className="flex-grow p-6 lg:p-8">{children}</main>
      </div>
    </div>
  );
}