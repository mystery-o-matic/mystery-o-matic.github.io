function getCurrentDate() {
	var options = {  weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour12: false };
	return String(new Date().toLocaleDateString(getLanguage(), options));
}

function showPage(page) {
	data = getTableData();
	document.getElementById("home").style.display = "none";
	document.getElementById("about").style.display = "none";
	document.getElementById("how-to-play").style.display = "none";
	document.getElementById("sleuth-o-meter").style.display = "none";
	document.getElementById(page).style.display = "block";

	for (let i = 0; i < tables.length; i++) {
		tables[i].redraw(true);
		for (let j = 0; j < data[i].length; j++) {
			[row, col, value] = data[i][j];
			tables[i].getRow(row).getCells()[col].setValue(value);
		}
	}

	if (page != "home") {
		document.getElementById("home-button").style.removeProperty("display");
		document.getElementById("switch-theme-button").style.display = "none";
		document.getElementById("translate-button").style.display = "none";
	} else {
		document.getElementById("home-button").style.display = "none";
		document.getElementById("switch-theme-button").style.removeProperty("display");
		document.getElementById("translate-button").style.removeProperty("display");
	}
}

document.getElementById("span-today").innerHTML = getCurrentDate();
var tries = 0;
var maxClue = 1;
var clues = [];
var crossClue = [];
var currentClue = 0;

function selectClues(withLies) {
	var element;

	element = document.getElementById("selection-clues-box");
	element.style.display = "none";

	element = document.getElementById("clues-box");
	element.style.removeProperty("display");

	element = document.getElementById("clues-buttons");
	element.style.removeProperty("display");

	language = getLanguage();
	clues = withLies ? data.additionalCluesWithLies[language] : data.additionalClues[language];
	new Array(clues.length).fill(false);
	revealAnotherClue(0);
}

function autosaveLocalNotebook() {
	var editorKey = 'story-notebook';
	var editor = document.getElementById(editorKey);
	var cache = localStorage.getItem(editorKey);

	var newValue = editor.value;
	if (cache != newValue) {
		cache = newValue;
		localStorage.setItem(editorKey, cache);
	}
}

function setLocalNotepad() {
	var editorKey = 'story-notebook';
	var editor = document.getElementById(editorKey);
	var cache = localStorage.getItem(editorKey);

	if (cache) {
		editor.value = cache;
	}
	editor.addEventListener('input', autosaveLocalNotebook);
}

setLocalNotepad();

function openModal(name) {
	let element = document.getElementById('portraitImage');
	element.src = "../images/" + name + ".jpg";
	let modal = new bootstrap.Modal(document.getElementById('portraitModal'), {});
	modal.show();
}

function revealAnotherClue(offset) {
	if (currentClue == 0 && offset < 0)
		return;

	if (currentClue == clues.length - 1 && offset > 0)
		return;

	currentClue = currentClue + offset;
	maxClue = Math.max(maxClue, currentClue);
	element = document.getElementById("clue-text");
	element.innerHTML = clues[currentClue];
	if (emoji) {
		element.innerHTML = emoji.replace_unified(element.innerHTML);
	}
	changeClueStrikeout(crossClue[currentClue], element);

	var currentTheme = document.querySelector("html").getAttribute("data-bs-theme");
	var usingLightTheme = currentTheme == "light";
	var links = element.children;
	for(let i = 0; i < links.length; i++) {
		if(links[i].href && !links[i].classList.contains("sticky-notes")) {
			toggleLinkTheme(!usingLightTheme, links[i]);
		}
	}

	element = document.getElementById("clue-title");
	language = getLanguage();
	switch (language) {
		case "en":
			element.innerHTML = "Clue";
			break;
		case "es":
			element.innerHTML = "Pista";
			break;
	}
	element.innerHTML += " #" + (currentClue + 1).toString();

	document.getElementById("previous-clue-button").disabled = (currentClue == 0);
	document.getElementById("next-clue-button").disabled = (currentClue == clues.length - 1);
}

function toggleClueStrikeout(element) {
	if (element.style.textDecoration == "line-through") {
		element.style.textDecoration = "none";
	} else
		element.style.textDecoration = "line-through";

	crossClue[currentClue] = element.style.textDecoration == "line-through";
}

function changeClueStrikeout(strike, element) {
	if (strike)
		element.style.textDecoration = "line-through";
	else
		element.style.textDecoration = "none";
}

function computeRank() {
	let numberClues = clues.length;
	viewedPercentage = 100 * maxClue / numberClues;
	if (viewedPercentage ==  0 && tries == 0) {
		rankIndex = "clairvoyant";
	} else if (viewedPercentage <= 65 && tries == 0) {
		rankIndex = "super sleuth";
	} else if (viewedPercentage <= 75 && tries == 0) {
		rankIndex = "seasoned P.I";
	} else if (viewedPercentage <= 85 && tries == 0) {
		rankIndex = "amateur gumshoe";
	} else if (viewedPercentage <= 95 && tries == 0) {
		rankIndex = "absent minded";
	} else {
		rankIndex = "barely conscious";
	}

	language = getLanguage();
	rank = rankStrings[language][rankIndex].rank;
	rank += rankStrings[language][rankIndex].message;

	return rank;
}

async function hash(message) {
	const msgUint8 = new TextEncoder().encode(message); // encode as (utf-8) Uint8Array
	const hashBuffer = await crypto.subtle.digest("SHA-256", msgUint8); // hash the message
	const hashArray = Array.from(new Uint8Array(hashBuffer)); // convert buffer to byte array
	const hashHex = hashArray
	.map((b) => b.toString(16).padStart(2, "0"))
	.join(""); // convert bytes to hex string
	return hashHex;
}

function checkAccusation() {
	input = "";
	let who = document.getElementById("who-selector").value;
	let how = document.getElementById("how-selector").value;
	let when = document.getElementById("when-selector").value;
	if (who == "" || how == "" || when == "") {
		alert("You accusation is incomplete detective!");
		return;
	}

	input = input + who + "-";
	input = input + how + "-";
	input = input + when;

	hash(input).then((result) => {
		if (result == data.correctAnswer) {
			rank = computeRank();
			document.getElementById("accusation-lose").style.display = "none";
			document.getElementById("accusation-win-message").innerHTML += " " + rank;
			document.getElementById("accusation-win").style.display = "block";
			document.getElementById("accusation-win").scrollIntoView();
			document.getElementById("accusation-button").disabled = true;

			storyClue = document.getElementById("story-clue").textContent;
			document.getElementById("story-notebook").value += "\n" + getCurrentDate() + ":\n" + storyClue + "\n";
		} else {
			document.getElementById("accusation-lose").style.display = "block";
			document.getElementById("accusation-lose").scrollIntoView();
			tries += 1;
		}
	});
}

function toggleLinkTheme(usingLightTheme, element) {
	element.classList.remove(usingLightTheme ? "link-dark" : "link-light");
	element.classList.add(usingLightTheme ? "link-light" : "link-dark");
}

function switchTheme() {
	var currentTheme = document.querySelector("html").getAttribute("data-bs-theme");
	document.querySelector("html").setAttribute("data-bs-theme", currentTheme == "light" ? "dark" : "light");
	var usingLightTheme = currentTheme == "light";
	var links = document.getElementsByTagName("a");
	for(let i = 0; i < links.length; i++) {
		if(links[i].href && !links[i].classList.contains("sticky-notes")) {
			toggleLinkTheme(usingLightTheme, links[i]);
		}
	}
	document.getElementById("logoImage").src = usingLightTheme ? "../images/logo_dark.png" : "../images/logo_light.png"
}

if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
	switchTheme()
}
