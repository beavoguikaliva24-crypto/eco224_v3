import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server'; // Correction de l'import type

const ROLE_PERMISSIONS: Record<string, string[]> = {
  '/dashboard/accounts': ['DEV', 'ADMIN'],
  '/dashboard/billing': ['DEV', 'ADMIN'],
  '/dashboard/audit': ['DEV'],
  '/dashboard/enrollment': ['DEV', 'ADMIN', 'STAFF'],
  '/dashboard/people': ['DEV', 'ADMIN', 'STAFF'],
  '/dashboard/student': ['DEV', 'ADMIN', 'STAFF'], // Route ajoutée
};

export function middleware(request: NextRequest) {
  const token = request.cookies.get('access')?.value;
  // On utilise une seule variable constante pour éviter le ReferenceError
  const currentUserRole = request.cookies.get('user_role')?.value;
  const { pathname } = request.nextUrl;

  // 1. Redirection si pas de token
  if (!token && pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // 2. Vérification des permissions
  if (pathname.startsWith('/dashboard')) {
    for (const [route, allowedRoles] of Object.entries(ROLE_PERMISSIONS)) {
      if (pathname.startsWith(route)) {
        // Correction de la condition qui causait l'erreur
        if (!currentUserRole || !allowedRoles.includes(currentUserRole)) {
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