import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Ecole-224 | Connexion',
  description: 'Plateforme de gestion scolaire',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  // data-theme est l'attribut que DaisyUI utilise pour appliquer un thème
  return (
    <html lang="fr" data-theme="light">
      <body className={inter.className}>{children}</body>
    </html>
  );
}