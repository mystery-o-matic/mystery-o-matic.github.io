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

hideClues();
document.getElementById("span-today").innerHTML = getCurrentDate();
var tries = 0;
var currentClue = 1;
var maxClue = 1;

function openModal(name) {
	let element = document.getElementById('portraitImage');
	element.src = "images/" + name + ".jpg";
	let modal = new bootstrap.Modal(document.getElementById('portraitModal'), {});
	modal.show();
}

function hideClues() {
	let i = 2;
	while (true) {
		element = document.getElementById("clue-" + i)
		if (element == null)
			break;

		element.style.display = "none"
		i = i + 1
	}
	document.getElementById("previous-clue-button").disabled = true;
}

function revealAnotherClue(offset) {
	if (currentClue == 1 && offset < 0)
		return;

	if (currentClue == document.getElementById("clues").children.length && offset > 0)
		return;

	element = document.getElementById("clue-" + currentClue);
	element.style.display = "none"

	currentClue = currentClue + offset;
	maxClue = Math.max(maxClue, currentClue);
	element = document.getElementById("clue-" + currentClue);
	element.style.display = "block";

	document.getElementById("previous-clue-button").disabled = (currentClue == 1);
	document.getElementById("next-clue-button").disabled = (currentClue == document.getElementById("clues").children.length);
}

function toggleClueStrikeout(element) {
	if (element.style.textDecoration == "line-through") {
		element.style.textDecoration = "none";
	} else
		element.style.textDecoration = "line-through";
}

function clueWasViewed(element) {
	return element.textContent.includes("👀")
}

function computeRank() {
	let numberClues = document.getElementById("clues").children.length;
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

function markedAsViewed(element) {
	if (!clueWasViewed(element))
		element.textContent += "👀";
}

var places = new Map();
places.set("bedroom", "🛏️");
places.set("living room", "🛋️");
places.set("kitchen", "🍲");
places.set("bathroom", "🚽");

var tables = new Map();

function createTables() {
	createCluesTable("bedroom", data.numIntervals, data.timeOffset, true, false);
	createCluesTable("kitchen", data.numIntervals, data.timeOffset, false, false);
	createCluesTable("living room", data.numIntervals, data.timeOffset, false, false);
	createCluesTable("bathroom", data.numIntervals, data.timeOffset, false, false);
	createCluesTable("kitchen-tutorial", 6, data.timeOffset, true, true);
	createCluesTable("bathroom-tutorial", 6, data.timeOffset, false, true);
}

createTables();

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
	table.ctx.fillText(text, table.columnSize * column + table.columnSize / 2, table.rowSize * row + table.rowSize / 1.8);
	table.data[column][row] = text;
}

function createCluesTable(name, nColumns, timeOffset, headerVisible, isTutorial) {
	var rowNames = []
	if (isTutorial) {
		rowNames = rowNames.concat(['alice', 'bob']);
	} else {
		rowNames = rowNames.concat(data.suspectNames);
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
	var titles = ["🕰️"];
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
		} else {
			document.getElementById("accusation-lose").style.display = "block";
			document.getElementById("accusation-lose").scrollIntoView();
			tries += 1;
		}
	});
}

function switchTheme() {
	var currentTheme = document.querySelector("html").getAttribute("data-bs-theme");
	document.querySelector("html").setAttribute("data-bs-theme", currentTheme == "light" ? "dark" : "light");

	var links = document.getElementsByTagName("a");
	for(let i = 0; i < links.length; i++) {
		if(links[i].href && !links[i].classList.contains("sticky-notes")) {
			links[i].classList.remove(currentTheme == "light" ? "link-dark" : "link-light");
			links[i].classList.add(currentTheme == "light" ? "link-light" : "link-dark");
		}
	}
}