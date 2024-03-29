function googleTranslateElementInit() {
	new google.translate.TranslateElement({pageLanguage: 'en'}, 'google_translate_element');
}

// Create a new onchange event and trigger it
const triggerEvent = (element,eventName) =>{
	const event = new Event(eventName, {'bubbles': true});
	element.dispatchEvent(event);
};

function checkIfWebsiteShouldBeTranslated(force) {
	language = window.navigator.language;
	language = language.split("-")[0];
	console.log(language);
	if (force || (sessionStorage.getItem("language") === null && language != "en")) {
		let modal = new bootstrap.Modal(document.getElementById('languageSelector'), {});
		modal.show();
	}
}

function keepInEnglish() {
	sessionStorage.setItem("language", "");
	var goog_te_combo = document.getElementsByClassName("goog-te-combo")[0];
	goog_te_combo.value = "en";
	triggerEvent(document.querySelector('.goog-te-combo'), 'change');
}

function translateContent(language) {
	var goog_te_combo = document.getElementsByClassName("goog-te-combo")[0];
	console.log(goog_te_combo);
	goog_te_combo.value = language;
	console.log(goog_te_combo.value);
	sessionStorage.setItem("language", goog_te_combo.value)

	// HACK: for some reason, this needs to be executed twice
	triggerEvent(goog_te_combo, 'change');
	goog_te_combo.value = language;
	triggerEvent(goog_te_combo, 'change');
}

checkIfWebsiteShouldBeTranslated(false);