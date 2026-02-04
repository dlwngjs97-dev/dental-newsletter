/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'www.dailydental.co.kr',
      },
      {
        protocol: 'https',
        hostname: 'www.dentalnews.or.kr',
      },
      {
        protocol: 'https',
        hostname: 'www.dentalarirang.com',
      },
    ],
  },
}

module.exports = nextConfig
