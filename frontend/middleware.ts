import { NextResponse } from 'next/server'; // Correction ici
import type { NextRequest } from 'next/request';

// On définit strictement qui a accès à quoi
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
  const role = request.cookies.get('user_role')?.value;
  const userRole = request.cookies.get('user_role')?.value;
  const { pathname } = request.nextUrl;

 

  // 1. Redirection vers login si accès au dashboard sans token
   // Si on tente d'accéder au dashboard sans cookie 'access'
  if (!token && pathname.startsWith('/dashboard')) {
    const loginUrl = new URL('/login', request.url);
    // On peut ajouter l'URL actuelle en paramètre pour y revenir après login
    loginUrl.searchParams.set('from', pathname);
    return NextResponse.redirect(loginUrl);
  }

  // 2. Vérification des permissions par URL
  if (pathname.startsWith('/dashboard')) {
    for (const [route, allowedRoles] of Object.entries(ROLE_PERMISSIONS)) {
      if (pathname.startsWith(route)) {
        if (!userRole || !allowedRoles.includes(userRole)) {
          // Si le rôle n'est pas autorisé (ex: PARENT sur /audit), 
          // on le renvoie vers l'accueil du dashboard
          return NextResponse.redirect(new URL('/dashboard', request.url));
        }
      }
    }
  }

  return NextResponse.next();
}

// On applique le middleware uniquement sur le dashboard
export const config = {
  matcher: ['/dashboard/:path*'],
};