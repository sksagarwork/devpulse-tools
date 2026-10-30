// CryptoCalc Pro Service Worker (Offline Cache Engine)
const CACHE_NAME = 'cryptocalc-pro-v1';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './eth-gas-calculator.html',
  './crypto-sip-calculator.html',
  './impermanent-loss-calculator.html',
  './crypto-tax-calculator.html',
  './staking-yield-calculator.html',
  './dca-crypto-calculator.html',
  './liquidation-price-calculator.html',
  './crypto-profit-calculator.html',
  './css/style.css',
  './js/common.js',
  './favicon.svg',
  './manifest.json',
  './og-image.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  // Navigation requests: Network first with cache fallback
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request).catch(() => caches.match(event.request) || caches.match('./index.html'))
    );
    return;
  }
  // Static assets: Cache first with network fallback
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) return cachedResponse;
      return fetch(event.request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return networkResponse;
      });
    }).catch(() => {
      // Offline fallback
      return caches.match(event.request);
    })
  );
});
