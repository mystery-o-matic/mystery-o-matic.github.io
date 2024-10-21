rankStringsEN = {
	"clairvoyant": {
		"rank": "<b>clairvoyant</b> 🧙",
		"message": "<i>Next time try guessing the lotto</i>!"
	},
	"super sleuth": {
		"rank": "<b>super sleuth</b> 🕵️",
		"message": "<i>Your deductive abilities are remarkable !</i>"
	},
	"seasoned P.I": {
		"rank": "<b>seasoned P.I</b> 🕵️",
		"message": "<i>Good job indeed !</i>"
	},
	"amateur gumshoe": {
		"rank": "<b>amateur gumshoe!</b> 👮",
		"message": "<i>Keep sharpening your deductive skills!</i>"
	},
	"absent minded": {
		"rank": "<b>absent minded!</b> 🤷",
		"message": "<i>Keep sharpening your deductive skills!</i>"
	},
	"barely conscious": {
		"rank": "<b>barely conscious</b> 🧟",
		"message": "<i>Congratulations on a job.. done!</i>"
	}
}

rankStringsES = {
	"clairvoyant": {
		"rank": "<b>clarividente</b> 🧙",
		"message": "<i>¡La próxima vez intenta adivinar la lotería!</i>!"
	},
	"super sleuth": {
		"rank": "<b>super detective</b> 🕵️",
		"message": "<i>¡Tus habilidades deductivas son notables!</i>"
	},
	"seasoned P.I": {
		"rank": "<b>investigador experimentado</b> 🕵️",
		"message": "<i>¡Buen trabajo!</i>"
	},
	"amateur gumshoe": {
		"rank": "<b>sabueso novato!</b> 👮",
		"message": "<i>¡Sigue mejorando tus habilidades deductivas!</i>"
	},
	"absent minded": {
		"rank": "<b>despistado!</b> 🤷",
		"message": "<i>¡Sigue mejorando tus habilidades deductivas!</i>"
	},
	"barely conscious": {
		"rank": "<b>semiconsciente</b> 🧟",
		"message": "<i>¡Felicidades por un trabajo.. hecho!</i>"
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
