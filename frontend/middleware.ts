// ✅ Importez tout de next/server
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// Définition des accès basés sur vos modèles Django
const ROLE_ACCESS: Record<string, string[]> = {
  '/dashboard/accounts': ['DEV', 'ADMIN'],
  '/dashboard/billing': ['DEV', 'ADMIN'],
  '/dashboard/audit': ['DEV'],
  '/dashboard/enrollment': ['DEV', 'ADMIN', 'STAFF'],
};

export function middleware(request: NextRequest) {
  const token = request.cookies.get('access')?.value;
  const userRole = request.cookies.get('user_role')?.value;
  const { pathname } = request.nextUrl;

  // Protection : redirection vers login si pas de token
  if (!token && pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Protection par rôle
  if (pathname.startsWith('/dashboard')) {
    for (const [route, allowedRoles] of Object.entries(ROLE_ACCESS)) {
      if (pathname.startsWith(route) && userRole && !allowedRoles.includes(userRole)) {
        // Redirection vers l'accueil du dashboard si le rôle est insuffisant
        return NextResponse.redirect(new URL('/dashboard', request.url));
      }
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*'],
};