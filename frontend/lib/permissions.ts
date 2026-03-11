export type AppRole = "DEV" | "ADMIN" | "STAFF" | "TEACHER" | "STUDENT" | "PARENT";

export type MenuItem = {
  name: string;
  href: string;
  icon?: unknown;
  roles?: AppRole[];
};

export type MenuGroup = {
  title: string;
  items: MenuItem[];
};

/**
 * Autorisations côté routing (middleware) :
 * chaque route dashboard protégée + rôles autorisés
 */
export const ROUTE_ACCESS: Record<string, AppRole[]> = {
  "/dashboard/enrollment": ["DEV", "ADMIN", "STAFF"],
  "/dashboard/school": ["DEV", "ADMIN", "STAFF", "TEACHER"],
  "/dashboard/schedule": ["DEV", "ADMIN", "STAFF", "TEACHER", "STUDENT"],
  "/dashboard/grading": ["DEV", "ADMIN", "STAFF", "TEACHER", "STUDENT", "PARENT"],
  "/dashboard/discipline": ["DEV", "ADMIN", "STAFF", "TEACHER", "PARENT"],
  "/dashboard/paiements": ["DEV", "ADMIN", "STAFF", "PARENT"],
  "/dashboard/children": ["DEV", "ADMIN", "STAFF", "PARENT"],
  "/dashboard/accounts": ["DEV", "ADMIN"],
  "/dashboard/people": ["DEV", "ADMIN", "STAFF"],
  "/dashboard/billing": ["DEV", "ADMIN"],
  "/dashboard/audit": ["DEV"],
  "/dashboard/student": ["DEV", "ADMIN", "STAFF", ],
  
};