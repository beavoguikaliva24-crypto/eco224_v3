import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
// import 'antd/dist/reset.css'; // Cette ligne n'est plus nécessaire avec la méthode ci-dessous
import StyledComponentsRegistry from "@/lib/AntdRegistry";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Ecole 224 - Gestion Scolaire",
  description: "Plateforme de gestion scolaire complète",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
return (
      <html lang="fr">
        <body className={inter.className}>
          <StyledComponentsRegistry>{children}</StyledComponentsRegistry>
        </body>
      </html>
    );
} // <-- Le fichier doit s'arrêter exactement ici