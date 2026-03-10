import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { ROUTE_ACCESS, type AppRole } from "@/lib/permissions";

export function middleware(request: NextRequest) {
  const token = request.cookies.get("access")?.value;
  const userRole = request.cookies.get("user_role")?.value as AppRole | undefined;
  const { pathname } = request.nextUrl;

  if (!token && pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  if (pathname.startsWith("/dashboard")) {
    for (const [route, allowedRoles] of Object.entries(ROUTE_ACCESS)) {
      if (pathname.startsWith(route)) {
        if (!userRole || !allowedRoles.includes(userRole)) {
          return NextResponse.redirect(new URL("/dashboard", request.url));
        }
      }
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*"],
};