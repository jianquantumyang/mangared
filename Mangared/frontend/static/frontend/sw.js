// service-worker.js

// Устанавливаем кэш
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open('my-cache').then(cache => {
      
    })
  );
});

// Перехватываем запросы и ищем их в кэше
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
