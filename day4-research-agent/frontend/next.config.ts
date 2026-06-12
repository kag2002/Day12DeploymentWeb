import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  allowedDevOrigins: [
    'wanting-discussions-psychology-inclusive.trycloudflare.com',
    'day-alpha-reflect-pieces.trycloudflare.com',
    '*.trycloudflare.com'
  ],
  async rewrites() {
    const backendUrl = process.env.BACKEND_URL || 'https://chatbotsearchweb-backend-production.up.railway.app';
    return [
      {
        source: '/api/:path*',
        destination: `${backendUrl}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
