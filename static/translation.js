rankStringsEN = {
	"clairvoyant": {
		"rank": "<b>clairvoyant</b> 🧙",
		"message": "<i>Phenomenal! Would you try guessing the lottery numbers for me?</i>"
	},
	"super sleuth": {
		"rank": "<b>super sleuth</b> 🕵️",
		"message": "<i>Outstanding! I bet you could solve any cold case!</i>"
	},
	"seasoned P.I": {
		"rank": "<b>seasoned P.I</b> 🕵️",
		"message": "<i>Impressive! I bet you never misplace your keys.</i>"
	},
	"amateur gumshoe": {
		"rank": "<b>amateur gumshoe</b> 👮",
		"message": "<i>Well done! Keep sharpening your deductive skills!</i>"
	},
	"absent minded": {
		"rank": "<b>absent minded</b> 🤷",
		"message": "<i>Keep it up! There's (a lot of) room for improvement, though.</i>"
	},
	"barely conscious": {
		"rank": "<b>barely conscious</b> 🧟",
		"message": "<i>Fair enough! Congratulations on a job... done.</i>"
	}
}

rankStringsES = {
	"clairvoyant": {
		"rank": "<b>clarividente</b> 🧙",
		"message": "<i>¡Fenomenal! ¿Podrías intentar adivinar los números de la lotería por mí?</i>"
	},
	"super sleuth": {
		"rank": "<b>super detective</b> 🕵️",
		"message": "<i>¡Excelente! ¡Apuesto a que podrías resolver cualquier caso!</i>"
	},
	"seasoned P.I": {
		"rank": "<b>investigador experimentado</b> 🕵️",
		"message": "<i>¡Impresionante! Apuesto a que nunca pierdes las llaves.</i>"
	},
	"amateur gumshoe": {
		"rank": "<b>sabueso novato</b> 👮",
		"message": "<i>¡Bien hecho! ¡Sigue perfeccionando tus habilidades deductivas!</i>"
	},
	"absent minded": {
		"rank": "<b>despistado</b> 🤷",
		"message": "<i>¡Sigue así! Aunque hay (mucho) margen de mejora.</i>"
	},
	"barely conscious": {
		"rank": "<b>semiconsciente</b> 🧟",
		"message": "<i>¡Está bien! Felicitaciones por un trabajo... hecho.</i>"
	}
}

rankStrings = {
	"en": rankStringsEN,
	"es": rankStringsES
}

function getLanguage() {
	return sessionStorage.getItem("language") || "en";
}

function checkIfWebsiteShouldBeTranslated(force) {
	language = window.navigator.language;
	language = language.split("-")[0];
	console.log(language);
	if (force || (sessionStorage.getItem("language") === null && language != "en")) {
		let modal = new bootstrap.Modal(document.getElementById('languageSelector'), {});
		modal.show();
	}
}

checkIfWebsiteShouldBeTranslated(false);
