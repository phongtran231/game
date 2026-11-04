// Minimal service worker: makes COIN-OPX installable as an app. It deliberately has no fetch
// handler and caches nothing, so ROMs, cores and app bundles always come from the network/disk
// paths the app already manages (and COOP/COEP headers are never altered).
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (event) => event.waitUntil(self.clients.claim()));
