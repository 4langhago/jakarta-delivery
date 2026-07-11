// K-Food Jakarta 서비스워커: 오프라인에서도 마지막 방문 화면 표시
const CACHE = 'kfood-v1';
const ASSETS = ['./index.html', './manifest.json', './icon-192.png', './icon-512.png'];

self.addEventListener('install', (e) => {
    e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)));
    self.skipWaiting();
});

self.addEventListener('activate', (e) => {
    e.waitUntil(
        caches.keys().then((keys) =>
            Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
        ).then(() => self.clients.claim())
    );
});

// 네트워크 우선, 실패 시 캐시 (항상 최신 메뉴/연락처를 보여주기 위함)
self.addEventListener('fetch', (e) => {
    if (e.request.method !== 'GET') return;
    e.respondWith(
        fetch(e.request)
            .then((res) => {
                if (res.ok && new URL(e.request.url).origin === location.origin) {
                    const clone = res.clone();
                    caches.open(CACHE).then((c) => c.put(e.request, clone));
                }
                return res;
            })
            .catch(() => caches.match(e.request, { ignoreSearch: true }))
    );
});
