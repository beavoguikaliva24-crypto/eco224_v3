import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// On utilise les mêmes routes que votre sidebar
const ROLE_PERMISSIONS: Record<string, string[]> = {
  '/dashboard/accounts': ['DEV', 'ADMIN'],
  '/dashboard/billing': ['DEV', 'ADMIN'],
  '/dashboard/audit': ['DEV'],
  '/dashboard/enrollment': ['DEV', 'ADMIN', 'STAFF'],
  '/dashboard/people': ['DEV', 'ADMIN', 'STAFF'],
  '/dashboard/student': ['DEV', 'ADMIN', 'STAFF'],
};

export function middleware(request: NextRequest) {
  const token = request.cookies.get('access')?.value;
  // On s'assure de lire exactement 'user_role'
  const userRole = request.cookies.get('user_role')?.value;
  const { pathname } = request.nextUrl;

  // 1. Protection : Pas de token = Redirection login
  if (!token && pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // 2. Protection : Rôle manquant ou non autorisé
  if (pathname.startsWith('/dashboard')) {
    for (const [route, allowedRoles] of Object.entries(ROLE_PERMISSIONS)) {
      if (pathname.startsWith(route)) {
        if (!userRole || !allowedRoles.includes(userRole)) {
          // On redirige vers la racine du dashboard si pas de permission
          return NextResponse.redirect(new URL('/dashboard', request.url));
        }
      }
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*'],
};