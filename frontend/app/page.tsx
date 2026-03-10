import { redirect } from 'next/navigation';

export default function Home() {
  // Redirige immédiatement vers la page de login
  redirect('/login');
}