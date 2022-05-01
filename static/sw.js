const cacheName =  "v3-m"
console.log("Running cache version "+cacheName)
const staticAssets = [
    "/static/js/bs-init.js",
    "/static/js/chart.min.js",
    "/static/js/flow.js",
    "/static/js/theme.js",
    "/static/img/Cyclone.png",
    "/static/img/CycloneTransparent.png",
    "/static/img/OpenLoop.png",
    "/static/img/OpenLoopBlack.png",
    "/static/bootstrap/css/bootstrap.min.css",
    "/static/bootstrap/js/bootstrap.min.js",
    "/",
    "/about"
]

self.addEventListener('install', async e => {
    const cache = await caches.open(cacheName);
    await cache.addAll(staticAssets);
    return self.skipWaiting();
});

self.addEventListener('activate', e => {
    self.clients.claim();
});

self.addEventListener('fetch', async e => {
    const req = e.request;
    const url = new URL(req.url);

    if (url.origin === location.origin) {
        e.respondWith(cacheFirst(req));
    } else {
        e.respondWith(networkAndCache(req));
    }
});

async function cacheFirst(req) {
    const cache = await caches.open(cacheName);
    const cached = await cache.match(req);
    return cached || fetch(req);
}

async function networkAndCache(req) {
    const cache = await caches.open(cacheName);
    try {
        const fresh = await fetch(req);
        await cache.put(req, fresh.clone());
        return fresh;
    } catch (e) {
        const cached = await cache.match(req);
        return cached;
    }
}