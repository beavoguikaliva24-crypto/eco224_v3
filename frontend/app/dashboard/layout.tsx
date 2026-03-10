import Link from 'next/link';
import {
  ChartBarIcon,
  UserGroupIcon,
  UsersIcon,
  BookOpenIcon,
  Cog6ToothIcon,
  ArrowRightStartOnRectangleIcon,
  Bars3Icon,
} from '@heroicons/react/24/outline';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="drawer lg:drawer-open">
      <input id="my-drawer-2" type="checkbox" className="drawer-toggle" />
      
      {/* Contenu de la Page (inclut le header) */}
      <div className="drawer-content flex flex-col">
        {/* En-tête (Header) */}
        <div className="navbar sticky top-0 z-30 w-full bg-base-100/80 shadow-sm backdrop-blur">
          <div className="flex-none lg:hidden">
            <label htmlFor="my-drawer-2" aria-label="open sidebar" className="btn btn-square btn-ghost">
              <Bars3Icon className="h-6 w-6" />
            </label>
          </div>
          <div className="flex-1">
            <Link href="/dashboard" className="btn btn-ghost text-xl">
              Tableau de Bord
            </Link>
          </div>
          <div className="flex-none">
            <div className="dropdown dropdown-end">
              <label tabIndex={0} className="btn btn-ghost btn-circle avatar">
                <div className="w-10 rounded-full">
                  {/* Remplacez par l'avatar de l'utilisateur */}
                  <img
                    alt="Avatar de l'utilisateur"
                    src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.jpg"
                  />
                </div>
              </label>
              <ul tabIndex={0} className="menu menu-sm dropdown-content z-[1] mt-3 w-52 rounded-box bg-base-100 p-2 shadow">
                <li><a className="justify-between">Profil</a></li>
                <li><a>Paramètres</a></li>
                <li><Link href="/login">Déconnexion</Link></li>
              </ul>
            </div>
          </div>
        </div>
        
        {/* Contenu Principal */}
        <main className="flex-1 p-4 lg:p-8 bg-base-200">
          {children}
        </main>
      </div>

      {/* Barre Latérale (Sidebar) */}
      <div className="drawer-side">
        <label htmlFor="my-drawer-2" aria-label="close sidebar" className="drawer-overlay"></label>
        <ul className="menu min-h-full w-64 bg-base-100 p-4 text-base-content">
          <li className="text-xl font-bold p-4">ECOLE-224</li>
          <li><Link href="/dashboard"><ChartBarIcon className="h-5 w-5" /> Tableau de bord</Link></li>
          <li><Link href="/dashboard/students"><UsersIcon className="h-5 w-5" /> Élèves</Link></li>
          <li><Link href="/dashboard/teachers"><UserGroupIcon className="h-5 w-5" /> Enseignants</Link></li>
          <li><Link href="/dashboard/courses"><BookOpenIcon className="h-5 w-5" /> Matières</Link></li>
          <li><Link href="/dashboard/settings"><Cog6ToothIcon className="h-5 w-5" /> Paramètres</Link></li>
          <li className="mt-auto"><Link href="/login"><ArrowRightStartOnRectangleIcon className="h-5 w-5" /> Déconnexion</Link></li>
        </ul>
      </div>
    </div>
  );
}