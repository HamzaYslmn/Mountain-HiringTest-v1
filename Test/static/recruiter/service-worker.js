const CACHE_NAME = 'recruiter-cache';
const urlsToCache = [
    '/static/styles.css',
    '/static/scripts.js',
    '/static/icons/favicon.ico',
    '/static/icons/favicon_256.png',
    '/static/icons/favicon_512.png'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request);
            })
    );
});
