/** @type {import('next').NextConfig} */
module.exports = {
  // If you fetch/download files from FastAPI at :5000, this will forward those to the backend (for dev only)
  async rewrites() {
    return [
      {
        source: '/api/download/:path*',
        destination: 'http://localhost:5000/api/download/:path*',
      },
      // If you want to forward all "/api/fetch-data" as well (optional, but not needed if you hardcode :5000 in fetch):
      // {
      //   source: '/api/fetch-data',
      //   destination: 'http://localhost:5000/api/fetch-data',
      // },
    ];
  },

  // If you want to enable network device testing (the warning you saw), add:
  // allowedDevOrigins: ['localhost', '192.168.100.18'],
};
