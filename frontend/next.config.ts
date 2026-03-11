import type { NextConfig } from "next";
/** @type {import('next').NextConfig} */

const nextConfig: NextConfig = {
  /* config options here */
  logging: {
    fetches: {
      fullUrl: true,
    },
  },
  experimental: {
    // Autorise les requêtes de développement sur votre IP locale
    allowedDevOrigins: ["10.182.66.105:3000", "beapc:3000", "localhost:3000"]
  }
};

export default nextConfig;


