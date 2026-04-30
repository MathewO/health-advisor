// Bump on every dashboard change so old caches are evicted on next load.
const CACHE_VERSION = 'mybody-2026-04-30a';

const APP_SHELL = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './apple-touch-icon.png',
  'https://cdn.jsdelivr.net/npm/chart.js@4.4.2/dist/chart.umd.min.js'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_VERSION)
      .then(cache => cache.addAll(APP_SHELL))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(k => k !== CACHE_VERSION).map(k => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

// Allow the page to query the active SW version (used by the footer indicator).
self.addEventListener('message', e => {
  if (e.data && e.data.type === 'GET_VERSION') {
    e.ports[0] && e.ports[0].postMessage({ version: CACHE_VERSION });
  }
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);

  // GitHub API: never cache. Always network with offline fallback.
  if (url.hostname === 'api.github.com') {
    e.respondWith(
      fetch(e.request).catch(() =>
        new Response(JSON.stringify({ error: 'offline' }), {
          status: 503,
          headers: { 'Content-Type': 'application/json' }
        })
      )
    );
    return;
  }

  // Network-first for content that changes: HTML pages, JS, JSON, Markdown logs.
  // Falls back to cache only when network is unreachable (true offline).
  const isFreshAlways =
    e.request.mode === 'navigate' ||
    /\.(html|js|json|md|csv)$/i.test(url.pathname);

  if (isFreshAlways) {
    e.respondWith(
      fetch(e.request)
        .then(resp => {
          if (resp && resp.ok && resp.type === 'basic') {
            const clone = resp.clone();
            caches.open(CACHE_VERSION).then(c => c.put(e.request, clone));
          }
          return resp;
        })
        .catch(() =>
          caches.match(e.request).then(c => c || caches.match('./index.html'))
        )
    );
    return;
  }

  // Cache-first for static binary assets (icons, fonts, CDN libs).
  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(resp => {
        if (resp && resp.ok) {
          const clone = resp.clone();
          caches.open(CACHE_VERSION).then(c => c.put(e.request, clone));
        }
        return resp;
      });
    })
  );
});
