"use client";

import Cookies from "js-cookie";
import { useMemo } from "react";
import {
  LayoutDashboard,
  Bell,
  GraduationCap,
  School,
  BookOpen,
  FileText,
  ShieldAlert,
  HandCoins,
  UserCircle,
  Users,
  ClipboardCheck,
  CreditCard,
  History,
} from "lucide-react";
import type { AppRole, MenuGroup } from "@/lib/permissions";

// Menu source
const menuGroups: MenuGroup[] = [
  {
    title: "Général",
    items: [
      { name: "Vue d'ensemble", href: "/dashboard", icon: LayoutDashboard },
      { name: "Notifications", href: "/dashboard/notifications", icon: Bell },
    ],
  },
  {
    title: "Scolarité",
    items: [
      { name: "Inscriptions", href: "/dashboard/enrollment", icon: GraduationCap, roles: ["DEV", "ADMIN", "STAFF"] },
      { name: "Classes & École", href: "/dashboard/school", icon: School, roles: ["DEV", "ADMIN", "STAFF", "TEACHER"] },
      { name: "Matières", href: "/dashboard/schedule", icon: BookOpen, roles: ["DEV", "ADMIN", "STAFF", "TEACHER", "STUDENT"] },
      { name: "Notes & Examens", href: "/dashboard/grading", icon: FileText, roles: ["DEV", "ADMIN", "STAFF", "TEACHER", "STUDENT", "PARENT"] },
      { name: "Discipline", href: "/dashboard/discipline", icon: ShieldAlert, roles: ["DEV", "ADMIN", "STAFF", "TEACHER", "PARENT"] },
      { name: "Paiements", href: "/dashboard/paiements", icon: HandCoins, roles: ["DEV", "ADMIN", "STAFF", "PARENT"] },
      { name: "Enfants", href: "/dashboard/children", icon: UserCircle, roles: ["DEV", "ADMIN", "STAFF", "PARENT"] },
    ],
  },
  {
    title: "Administration",
    items: [
      { name: "Utilisateurs", href: "/dashboard/accounts", icon: Users, roles: ["DEV", "ADMIN"] },
      { name: "Personnel & RH", href: "/dashboard/people", icon: ClipboardCheck, roles: ["DEV", "ADMIN", "STAFF"] },
      { name: "Facturation", href: "/dashboard/billing", icon: CreditCard, roles: ["DEV", "ADMIN"] },
      { name: "Logs & Audit", href: "/dashboard/audit", icon: History, roles: ["DEV"] },
    ],
  },
];

export function useVisibleMenuGroups() {
  return useMemo(() => {
    const role = Cookies.get("user_role") as AppRole | undefined;

    return menuGroups
      .map((group) => ({
        ...group,
        items: group.items.filter((item) => !item.roles || (role ? item.roles.includes(role) : false)),
      }))
      .filter((group) => group.items.length > 0);
  }, []);
}