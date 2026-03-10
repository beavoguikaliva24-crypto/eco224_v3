"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useVisibleMenuGroups } from "./sidebar-menu";

type SidebarProps = {
  mobile?: boolean;
  onNavigate?: () => void;
};

export default function Sidebar({ mobile = false, onNavigate }: SidebarProps) {
  const pathname = usePathname();
  const groups = useVisibleMenuGroups();

  return (
    <aside className={mobile ? "w-64 p-4" : "w-72 p-6 border-r border-zinc-200"}>
      {groups.map((group) => (
        <div key={group.title} className="mb-6">
          <h3 className="mb-2 text-xs font-bold uppercase tracking-wider text-zinc-400">{group.title}</h3>
          <nav className="space-y-1">
            {group.items.map((item) => {
              const isActive = pathname === item.href || pathname.startsWith(item.href + "/");
              const Icon = item.icon as React.ComponentType<{ className?: string }>;

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={onNavigate}
                  className={`flex items-center gap-3 rounded-xl px-3 py-2 text-sm transition ${
                    isActive
                      ? "bg-zinc-900 text-white"
                      : "text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900"
                  }`}
                >
                  {Icon ? <Icon className="h-4 w-4" /> : null}
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </nav>
        </div>
      ))}
    </aside>
  );
}