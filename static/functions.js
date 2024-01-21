var ua = navigator.userAgent;
var isKindle = /Kindle/i.test(ua);
var emoji = null;
if (isKindle) {
	emoji = new EmojiConvertor();
	emoji.img_sets['google'].path = 'images/emoji-data/img-google-64/';
	emoji.img_set = 'google';
	emoji.text_mode = false;
	document.body.innerHTML = emoji.replace_unified(document.body.innerHTML);
	document.getElementById("locations-big").src = "images/locations_big.png";
	document.getElementById("locations-small").src = "images/locations_small.png";
}

function getEmoji(input) {
	if (emoji) {
		input = emoji.replace_unified(input);
		const parser = new DOMParser();
		htmlDoc = parser.parseFromString(input, 'text/html');
		codepoint = htmlDoc.getElementsByTagName("span")[0].dataset["codepoints"];
		console.log(codepoint);
		return document.getElementById(codepoint);
	} else
		return input;
}

function getCurrentDate() {
	var options = {  weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour12: false };
	return String(new Date().toLocaleTimeString('en-us', options)).split(" at")[0];
}

function getTableData() {
	var data = [];
	for (let i = 0; i < tables.length; i++) {
		data[i] = []
		for (let row = 0; row < tables[i].getRows().length; row++) {
			for (col = 1; col < tables[i].getRow(row).getCells().length; col++) {
				value = tables[i].getRow(row).getCells()[col].getValue();
				data[i].push([row, col, value]);
			}
		}
	}
	return data;
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
}

document.getElementById("span-today").innerHTML = getCurrentDate();
var tries = 0;
var maxClue = 1;
var crossClue = new Array(data.additionalClues.length).fill(false);
var currentClue = 0;
revealAnotherClue(0);

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
	element.src = "images/" + name + ".jpg";
	let modal = new bootstrap.Modal(document.getElementById('portraitModal'), {});
	modal.show();
}

function revealAnotherClue(offset) {
	if (currentClue == 0 && offset < 0)
		return;

	if (currentClue == data.additionalClues.length - 1 && offset > 0)
		return;

	currentClue = currentClue + offset;
	maxClue = Math.max(maxClue, currentClue);
	element = document.getElementById("clue-text");
	element.innerHTML = data.additionalClues[currentClue];
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
	element.innerHTML = "Clue #" + (currentClue + 1).toString();

	document.getElementById("previous-clue-button").disabled = (currentClue == 0);
	document.getElementById("next-clue-button").disabled = (currentClue == data.additionalClues.length - 1);
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
	let numberClues = data.additionalClues.length;
	viewedPercentage = 100 * maxClue / numberClues;
	rank = ""
	if (viewedPercentage ==  0 && tries == 0) {
		rank += "<b>clairvoyant</b> 🧙";
		rank += "<br><i>Next time try guessing the lotto</i>!"
	} else if (viewedPercentage <= 50 && tries == 0) {
		rank += "<b>super sleuth</b> 🕵️";
		rank += "<br><i>Your deductive abilities are remarkable !</i>"
	} else if (viewedPercentage <= 60 && tries == 0) {
		rank += "<b>seasoned P.I</b> 🕵️";
		rank += "<br><i>Good job indeed !</i>"
	} else if (viewedPercentage <= 70 && tries == 0) {
		rank += "<b>amateur gumshoe!</b> 👮";
		rank += "<br><i>Keep sharpening your deductive skills!</i>"
	} else if (viewedPercentage <= 80 && tries == 0) {
		rank += "<b>absent minded!</b> 🤷";
		rank += "<br><i>Keep sharpening your deductive skills!</i>"
	} else {
		rank += "<b>barely conscious</b> 🧟"
		rank += "<br><i>Congratulations on a job.. done!</i>"
	}

	return rank;
}

var places = new Map();
places.set("bedroom", getEmoji(data.representationsMap["bedroom"]));
places.set("dining room", getEmoji(data.representationsMap["dining room"]));
places.set("kitchen", getEmoji(data.representationsMap["kitchen"]));
places.set("bathroom", getEmoji(data.representationsMap["bathroom"]));

var tables = new Map();

function createTables() {
	createCluesTable("bedroom", data.numIntervals, data.timeOffset, true, false);
	createCluesTable("kitchen", data.numIntervals, data.timeOffset, false, false);
	createCluesTable("dining room", data.numIntervals, data.timeOffset, false, false);
	createCluesTable("bathroom", data.numIntervals, data.timeOffset, false, false);
	createCluesTable("kitchen-tutorial", 6, data.timeOffset, true, true);
	createCluesTable("bathroom-tutorial", 6, data.timeOffset, false, true);
	createCluesTableWeapons();
}

function drawClueTable(table) {
	table.ctx.fillStyle = "#cccccc";
	table.ctx.fillRect(0, 0, table.canvas.width, table.canvas.height);

	table.ctx.strokeStyle = "white";
	for (let i = 0; i < table.nColumns + 1; i++) {
		table.ctx.moveTo(table.columnSize * i, 0);
		table.ctx.lineTo(table.columnSize * i, table.height);
		table.ctx.stroke();
	}

	for (let i = 0; i < table.nRows + 1; i++) {
		var start = table.columnSize;
		if (i == 0 || i == table.nRows) // Draw first and last line
			start = 0;

		table.ctx.moveTo(start, table.rowSize * i);
		table.ctx.lineTo(table.width, table.rowSize * i);
		table.ctx.stroke();
	}
}

function fillClueTable(text, size, color, column, row, table) {
	table.ctx.font = "bold " + size + "px Raleway";
	table.ctx.textAlign = "center";
	table.ctx.fillStyle = color;
	if (text && typeof(text) === "object") {
		console.log(text);
		table.ctx.drawImage(text, table.columnSize * column + table.columnSize / 2 - text.width / 2, table.rowSize * row + table.rowSize / 1.8 - text.height / 1.8);
	} else
		table.ctx.fillText(text, table.columnSize * column + table.columnSize / 2, table.rowSize * row + table.rowSize / 1.8);

	table.data[column][row] = text;
}

function createCluesTableWeapons() {
	var rowNames = []

	nColumns = 4;
	var nRows = rowNames.length + 1;
	var name = "weapons"
	var c = document.getElementById("clues-table-" + name);
	var width = c.width;
	var height = c.height;

	var columnSize = width / nColumns;
	var rowSize = height / nRows;

	var ctx = c.getContext("2d");

	var table = {
		canvas: c,
		ctx: ctx,
		nColumns: nColumns,
		nRows: nRows,
		columnSize: columnSize,
		rowSize: rowSize,
		headerVisible: false,
		width: width,
		height: height,
		data: [...Array(nColumns)].map(e => Array(nRows).fill("")),
		extra: [...Array(nColumns)].map(e => Array(nRows).fill("")),
		isTutorial: false,
	};

	tables.set(name, table);
	drawClueTable(table);

	var place;
	place = data.representationsMap[data.weaponsMap["poison"]];
	fillClueTable("⚗️ "+place, columnSize / 6, '#000000', 0, 0, table);
	table.extra[0][0] = "⚗️ "+place;
	place = data.representationsMap[data.weaponsMap["knife"]];
	fillClueTable("🔪 "+place, columnSize / 6, '#000000', 1, 0, table);
	table.extra[1][0] = "🔪 "+place;
	place = data.representationsMap[data.weaponsMap["pistol"]];
	fillClueTable("🔫 "+place, columnSize / 6, '#000000', 2, 0, table);
	table.extra[2][0] = "🔫 "+place;
	place = data.representationsMap[data.weaponsMap["rope"]];
	fillClueTable("🪢 "+place, columnSize / 6, '#000000', 3, 0, table);
	table.extra[3][0] = "🪢 "+place;
}


function createCluesTable(name, nColumns, timeOffset, headerVisible, isTutorial) {
	var rowNames = []
	if (isTutorial) {
		rowNames = rowNames.concat(['alice', 'bob']);
	} else {
		rowNames = rowNames.concat(data.characterNames);
	}

	nColumns = nColumns + 2;
	var nRows = rowNames.length;
	if (headerVisible)
		nRows = nRows + 1;

	var c = document.getElementById("clues-table-" + name);
	if (!headerVisible) {
		c.height = c.height - 40;
	}

	var width = c.width;
	var height = c.height;

	var columnSize = width / nColumns;
	var rowSize = height / nRows;

	var ctx = c.getContext("2d");

	var table = {
		canvas: c,
		ctx: ctx,
		nColumns: nColumns,
		nRows: nRows,
		columnSize: columnSize,
		rowSize: rowSize,
		headerVisible: headerVisible,
		width: width,
		height: height,
		data: [...Array(nColumns)].map(e => Array(nRows).fill("")),
		isTutorial: isTutorial,
	};

	tables.set(name, table);
	drawClueTable(table);

	var date = new Date(null);
	date.setSeconds(timeOffset);
	var titles = [getEmoji("🕰️")];
	for (let i = 0; i < nColumns; i++) {
	  title = date.toISOString().substr(11, 5);
	  titles.push(title);
	  date.setSeconds(60 * 15);
	}

	if (headerVisible) {
		for (let i = 0; i < nColumns - 1; i++) {
			fillClueTable(titles[i], columnSize / 3, '#000000', i + 1, 0, table);
			table.data[i + 1][0] = titles[i];
		}
	}
	var column;
	for (let i = 0; i < nRows; i++) {
		var column = i;
		if (headerVisible)
			column = column + 1;
		fillClueTable(rowNames[i], columnSize / 3, '#000000', 1, column, table);
		table.data[1][column] = rowNames[i];
	}
	var placeLabelPosition = 1;
	if (headerVisible)
		placeLabelPosition = placeLabelPosition + 1;

	fillClueTable(places.get(name.replace("-tutorial", "")), columnSize / 1.5, '#000000', 0, placeLabelPosition, table);
	table.data[0][0] = " ";
	table.data[0][1] = " ";
	table.data[0][2] = " ";
	table.data[0][3] = " ";
	table.data[0][placeLabelPosition] = places.get(name);

	if (!table.isTutorial) {
		var startRow = 0;
		if (headerVisible)
			startRow = 1
		for (let i = startRow; i < nRows; i++) {
			fillClueTable("✗", columnSize / 3, '#000000', nColumns - 1, i, table);
		}

		for (let i = startRow; i < startRow + rowNames.length; i++) {
			var character = rowNames[i - startRow];
			roomName = data.finalLocationsMap[character];
			var color = (character == data.victim) ? '#cc0000' : '#000000';
			if (roomName == name) {
				fillClueTable("█", columnSize / 3, '#cccccc', nColumns - 1, i, table);
				fillClueTable("✓", columnSize / 3, color, nColumns - 1, i, table);
			}
		}
	}

	return table;
}

function findPositionTable(table, x, y) {
	//console.log(x, y);
	const rect = table.canvas.getBoundingClientRect()
	x = table.height * x / rect.height;
	y = table.width * y / rect.width;
	return [Math.trunc(x / table.columnSize), Math.trunc(y / table.rowSize)];
}

function checkWeaponClicked(c, x, y) {
	var name = c.id.replace("clues-table-", "");
	var table = tables.get(name);
	var position = findPositionTable(table, x, y);
	var value = table.data[position[0]][position[1]];
	console.log(value);
	fillClueTable("█", table.columnSize / 2, '#cccccc', position[0], position[1], table);

	console.log(value);

	weapon = table.extra[position[0]][position[1]];
	fillClueTable(weapon, table.columnSize / 6, '#000000', position[0], position[1], table);

	if (value == "🚫") {
		// Nothing
	} else {
		fillClueTable("🚫", table.columnSize / 5, '#000000', position[0], position[1], table);
	}
}


function checkCellClicked(c, x, y) {
	var name = c.id.replace("clues-table-", "");
	var table = tables.get(name);
	var position = findPositionTable(table, x, y);
	//console.log(name);
	if (!table.isTutorial) {
		if (position[0] == table.nColumns - 1)
		return;
	}

	//console.log(table.data);
	var value = table.data[position[0]][position[1]];
    if (value == "")
		value = "✓";
	else if (value == "✓")
		value = "✗";
	else if (value == "✗")
		value = "?";
	else if (value == "?")
		value = "";
	else
		return;

	table.data[position[0]][position[1]] = value;
	fillClueTable("█", table.columnSize / 3, '#cccccc', position[0], position[1], table);
	fillClueTable(value, table.columnSize / 3, '#000000', position[0], position[1], table);
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

			storyClue = document.getElementById("story-clue").innerHTML.replace(/(<([^>]+)>)/ig, "\n");
			document.getElementById("story-notebook").value += "\n" + getCurrentDate() + ":\n" + storyClue;
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
	document.getElementById("logoImage").src = usingLightTheme ? "images/logo_dark.png" : "images/logo_light.png"
}

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

if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
	switchTheme()
}
