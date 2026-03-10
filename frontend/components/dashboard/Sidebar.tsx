const userRole = (typeof window !== "undefined" ? Cookies.get("user_role") : undefined) as string | undefined;

const visibleGroups = menuGroups
  .map((group) => ({
    ...group,
    items: group.items.filter((item) => !item.roles || (userRole && item.roles.includes(userRole))),
  }))
  .filter((g) => g.items.length > 0);