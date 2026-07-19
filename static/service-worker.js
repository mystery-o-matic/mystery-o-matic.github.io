const CACHE_NAME = "mystery-o-matic-offline-v1";
const LANGUAGES = ["en", "es", "ru"];
const LANGUAGE_ASSETS = LANGUAGES.flatMap(function (language) {
	return [
		"/" + language + "/",
		"/" + language + "/manifest.webmanifest",
		"/" + language + "/locations_big.svg",
		"/" + language + "/locations_big.png",
		"/" + language + "/locations_small.svg",
		"/" + language + "/locations_small.png",
		"/" + language + "/locations_tutorial.svg",
		"/" + language + "/locations_tutorial_small.svg",
		"/" + language + "/locations_tutorial_highlighted.svg",
		"/" + language + "/locations_tutorial_highlighted_bathroom.svg",
		"/" + language + "/locations_tutorial_highlighted_bedroom.svg",
		"/" + language + "/locations_tutorial_highlighted_dining_room.svg"
	];
});
const CORE_ASSETS = [
	"/",
	"/index.html",
	"/data.js",
	"/tutorialData.js",
	"/table.js",
	"/translation.js",
	"/functions.js",
	"/sleuth-o-meter.js",
	"/tutorial-nav.js",
	"/emoji.css",
	"/emoji.js",
	"/css/main.css",
	"/css/sticky-notes.css",
	"/css/sleuth-o-meter.css",
	"/images/apple-touch-icon.png",
	"/images/favicon-16x16.png",
	"/images/favicon-32x32.png",
	"/images/favicon.ico",
	"/images/icon-192.png",
	"/images/icon-512.png",
	"/images/icon-512-maskable.png",
	"/images/logo_dark.png",
	"/images/logo_light.png",
	"/images/preview.jpg",
	"/images/sleuth-o-meter.png"
].concat(LANGUAGE_ASSETS);

self.addEventListener("install", function (event) {
	event.waitUntil(
		cacheCoreAssets().then(function () {
			return self.skipWaiting();
		})
	);
});

self.addEventListener("activate", function (event) {
	event.waitUntil(self.clients.claim());
});

self.addEventListener("fetch", function (event) {
	if (event.request.method !== "GET") {
		return;
	}

	var url = new URL(event.request.url);

	if (event.request.headers.get("X-Mystery-Refresh-Preflight") === "1") {
		event.respondWith(fetch(event.request));
		return;
	}

	if (isAnalyticsRequest(url)) {
		return;
	}

	if (isGeneratedMysteryAsset(url)) {
		event.respondWith(networkFirst(
			event.request,
			[new Request(new URL(url.pathname, self.location.origin).toString())],
			requestWithoutSearch(event.request)
		));
		return;
	}

	if (isSameOrigin(url) && url.searchParams.has("mystery-update-check")) {
		event.respondWith(fetch(event.request));
		return;
	}

	if (event.request.mode === "navigate") {
		event.respondWith(networkFirst(event.request, getNavigationFallbacks(url)));
		return;
	}

	if (isMysteryDataRequest(url)) {
		event.respondWith(networkFirst(
			event.request,
			[new Request(new URL("/data.js", self.location.origin).toString())],
			requestWithoutSearch(event.request)
		));
		return;
	}

	if (isAppShellAsset(url)) {
		event.respondWith(networkFirst(
			event.request,
			[new Request(new URL(url.pathname, self.location.origin).toString())],
			requestWithoutSearch(event.request)
		));
		return;
	}

	if (isSameOrigin(url)) {
		event.respondWith(staleWhileRevalidate(event.request, requestWithoutSearch(event.request)));
		return;
	}

	event.respondWith(staleWhileRevalidate(event.request, event.request));
});

async function cacheCoreAssets() {
	var cache = await caches.open(CACHE_NAME);
	await Promise.allSettled(
		CORE_ASSETS.map(function (asset) {
			return cache.add(new Request(asset, { cache: "reload" }));
		})
	);
}

function isSameOrigin(url) {
	return url.origin === self.location.origin;
}

function isMysteryDataRequest(url) {
	return isSameOrigin(url) && url.pathname === "/data.js";
}

function isGeneratedMysteryAsset(url) {
	return isSameOrigin(url) && /^\/(en|es|ru)\/locations_(big|small)\.(svg|png)$/.test(url.pathname);
}

function isAppShellAsset(url) {
	if (!isSameOrigin(url)) {
		return false;
	}

	return [
		"/functions.js",
		"/sleuth-o-meter.js",
		"/table.js",
		"/translation.js",
		"/tutorialData.js",
		"/tutorial-nav.js",
		"/emoji.js",
		"/emoji.css",
		"/css/main.css",
		"/css/sticky-notes.css",
		"/css/sleuth-o-meter.css"
	].indexOf(url.pathname) !== -1;
}

function isAnalyticsRequest(url) {
	return [
		"googletagmanager.com",
		"google-analytics.com",
		"stats.g.doubleclick.net"
	].some(function (host) {
		return url.hostname === host || url.hostname.endsWith("." + host);
	});
}

function requestWithoutSearch(request) {
	var url = new URL(request.url);
	if (!isSameOrigin(url)) {
		return request;
	}
	url.search = "";
	return new Request(url.toString());
}

function getNavigationFallbacks(url) {
	var pathname = url.pathname;
	var fallbacks = [requestWithoutSearch(new Request(url.toString()))];

	if (!pathname.endsWith("/")) {
		fallbacks.push(new Request(new URL(pathname + "/", self.location.origin).toString()));
	}

	var languageMatch = pathname.match(/^\/(en|es|ru)(?:\/|$)/);
	if (languageMatch) {
		fallbacks.push(new Request(new URL("/" + languageMatch[1] + "/", self.location.origin).toString()));
	}

	fallbacks.push(new Request(new URL("/en/", self.location.origin).toString()));
	fallbacks.push(new Request(new URL("/index.html", self.location.origin).toString()));
	fallbacks.push(new Request(new URL("/", self.location.origin).toString()));
	return fallbacks;
}

async function networkFirst(request, fallbacks, cacheRequest) {
	var cache = await caches.open(CACHE_NAME);
	var key = cacheRequest || requestWithoutSearch(request);

	try {
		var response = await fetchFresh(request);
		if (canCache(response)) {
			try {
				await cache.put(key, response.clone());
			} catch (cacheErr) {}
		}
		return response;
	} catch (err) {
		var cached = await cache.match(key);
		if (cached) {
			return cached;
		}

		for (var i = 0; i < fallbacks.length; i++) {
			cached = await cache.match(fallbacks[i], { ignoreSearch: true });
			if (cached) {
				return cached;
			}
		}

		throw err;
	}
}

function fetchFresh(request) {
	try {
		return fetch(new Request(request, { cache: "reload" }));
	} catch (err) {
		return fetch(request);
	}
}

async function staleWhileRevalidate(request, cacheRequest) {
	var cache = await caches.open(CACHE_NAME);
	var key = cacheRequest || request;
	var cached = await cache.match(key, { ignoreSearch: true });
	var fetched = fetch(request).then(function (response) {
		if (canCache(response)) {
			cache.put(key, response.clone()).catch(function () {});
		}
		return response;
	}).catch(function () {
		return null;
	});

	if (cached) {
		return cached;
	}

	var response = await fetched;
	if (response) {
		return response;
	}

	throw new Error("No cached response available");
}

function canCache(response) {
	return response && (response.ok || response.type === "opaque");
}
