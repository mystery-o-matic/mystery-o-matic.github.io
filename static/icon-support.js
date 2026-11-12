// Image icon mode also works on school computers without an emoji font.
var isEInk = /Kindle/i.test(navigator.userAgent);
var useImageIcons = false;
var emoji = null;
var iconImageCache = new Map();
var iconImagesReady = Promise.resolve();

function requiredEmoji(converter, text) {
	converter.init_unified();
	return Array.from(new Set(text.match(converter.rx_unified) || []));
}

function getEmoji(input) {
	if (!emoji) return input;
	var wrapper = document.createElement('span');
	wrapper.innerHTML = emoji.replace_unified(input);
	var image = wrapper.querySelector('img');
	if (!image) return input;
	var src = image.getAttribute('src');
	if (!iconImageCache.has(src)) {
		var loaded = new Image();
		loaded.alt = (image.getAttribute('title') || 'icon').replace(/_/g, ' ');
		loaded.src = src;
		iconImageCache.set(src, loaded);
	}
	return iconImageCache.get(src);
}

function replaceEmojiText(node) {
	if (!node.parentElement || node.parentElement.closest('script, style, textarea, option, .emoji')) return;
	var converted = emoji.replace_unified(node.nodeValue);
	if (converted === node.nodeValue) return;
	var wrapper = document.createElement('span');
	wrapper.innerHTML = converted;
	wrapper.querySelectorAll('img').forEach(function (image) {
		image.alt = image.title.replace(/_/g, ' ');
	});
	node.replaceWith.apply(node, Array.from(wrapper.childNodes));
}

function replaceEmojiInElement(element) {
	if (element.nodeType === 3) {
		replaceEmojiText(element);
		return;
	}
	var walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT);
	var nodes = [];
	while (walker.nextNode()) nodes.push(walker.currentNode);
	nodes.forEach(replaceEmojiText);
}

function initializeIconSupport() {
	if (isEInk) document.getElementById('switch-theme-button').style.display = 'none';
	useImageIcons = isEInk || new URLSearchParams(window.location.search).get('icons') === 'images';
	if (!useImageIcons) return;
	var converter = new EmojiConvertor();
	var text = document.body.textContent + JSON.stringify(data) + JSON.stringify(tutorialData) + '🕰️☠️';
	var glyphs = requiredEmoji(converter, text);
	emoji = converter;
	emoji.img_sets.google.path = '../images/emoji-data/img-google-64/';
	emoji.img_set = 'google';
	emoji.allow_native = false;
	emoji.replace_mode = 'img';
	emoji.include_title = true;
	replaceEmojiInElement(document.body);
	// Switch every map, including hidden tutorial maps, to its font-free copy.
	document.querySelectorAll('img[src]').forEach(function (image) {
		var src = image.getAttribute('src');
		if (/^locations_[\w]+\.svg$/.test(src)) {
			// PNG maps are rendered at 3x resolution; retain the SVG's display size.
			image.addEventListener('load', function () {
				image.style.width = (image.naturalWidth / 3) + 'px';
			}, { once: true });
			image.src = src.replace(/\.svg$/, '.png');
		}
	});
	iconImagesReady = Promise.all(glyphs.map(function (glyph) {
		var image = getEmoji(glyph);
		if (typeof image === 'string' || image.complete) return Promise.resolve();
		return new Promise(function (resolve) {
			image.addEventListener('load', resolve, { once: true });
			image.addEventListener('error', resolve, { once: true });
		});
	}));
	// Process new clues, profiles, solution steps and rank messages without
	// replacing the body or destroying existing listeners and form state.
	var observer = new MutationObserver(function (changes) {
		changes.forEach(function (change) {
			if (change.type === 'characterData') replaceEmojiText(change.target);
			else change.addedNodes.forEach(replaceEmojiInElement);
		});
	});
	observer.observe(document.body, { childList: true, characterData: true, subtree: true });
	// Keep offline image assets available for this mode without downloading
	// them for visitors using ordinary links.
	if ('serviceWorker' in navigator) {
		navigator.serviceWorker.ready.then(function (registration) {
			if (registration.active) registration.active.postMessage({ type: 'cache-image-icons' });
		}).catch(function () {});
	}
}
