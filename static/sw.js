const cacheName =  "v3-m1"
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
    "/static/fonts/fa-solid-900.ttf",
    "/static/fonts/fontawesome-webfont.svg",
    "/static/fonts/fontawesome5-overrides.min.css",
    "/static/fonts/FontAwesome.otf",
    "/static/fonts/fa-regular-400.svg",
    "/static/fonts/fa-regular-400.woff2",
    "/static/fonts/fa-solid-900.eot",
    "/static/fonts/fontawesome-all.min.css",
    "/static/fonts/fontawesome-webfont.woff2",
    "/static/fonts/fa-brands-400.svg",
    "/static/fonts/fa-regular-400.woff",
    "/static/fonts/fa-brands-400.eot",
    "/static/fonts/fa-solid-900.svg",
    "/static/fonts/fontawesome-webfont.ttf",
    "/static/fonts/font-awesome.min.css",
    "/static/fonts/fa-solid-900.woff",
    "/static/fonts/fa-regular-400.ttf",
    "/static/fonts/fontawesome-webfont.woff",
    "/static/fonts/fa-solid-900.woff2",
    "/static/fonts/fa-brands-400.woff2",
    "/static/fonts/fa-brands-400.woff",
    "/static/fonts/fa-brands-400.ttf",
    "/static/fonts/fontawesome-webfont.eot",
    "/static/fonts/fa-regular-400.eot",
    "/",
    "/about",
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