self.addEventListener('install', (e) => {
  console.log('[Service Worker] Install');
});

self.addEventListener('fetch', (e) => {
  // This can be empty, but the listener must exist for the "Add to Home Screen" prompt
  e.respondWith(fetch(e.request));
});