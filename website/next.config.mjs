const basePath = process.env.BASE_PATH || '';

const nextConfig = {
  reactStrictMode: true,
  images: {
    unoptimized: true,
  },
  output: 'export',
  trailingSlash: true,

  basePath: basePath,
  assetPrefix: basePath,
};

export default nextConfig;
