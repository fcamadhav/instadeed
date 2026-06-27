import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  output: "standalone",
  assetPrefix: "/_landing",
};

export default nextConfig;
