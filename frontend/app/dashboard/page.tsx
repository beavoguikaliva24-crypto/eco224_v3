export default function DashboardPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-zinc-50 dark:bg-black">
      <div className="rounded-2xl bg-white p-8 shadow-md dark:bg-zinc-900">
        <h1 className="text-2xl font-bold text-zinc-900 dark:text-zinc-50">
          Dashboard
        </h1>
        <p className="mt-2 text-zinc-600 dark:text-zinc-400">
          Bienvenue sur le tableau de bord.
        </p>
      </div>
    </div>
  );
}
