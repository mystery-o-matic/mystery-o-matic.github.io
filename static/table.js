var ua = navigator.userAgent;
var isKindle = /Kindle/i.test(ua);
var isMobile = /Mobi/i.test(ua);

var emoji = null;

if (isKindle) {
	emoji = new EmojiConvertor();
	emoji.img_sets['google'].path = '../images/emoji-data/img-google-64/';
	emoji.img_set = 'google';
	emoji.text_mode = false;
	document.body.innerHTML = emoji.replace_unified(document.body.innerHTML);
	document.getElementById("locations-big").src = "locations_big.png";
	document.getElementById("locations-big").style.height = 'auto';
	document.getElementById("locations-small").src = "locations_small.png";
	document.getElementById("locations-small").style.height = '10vh';
}

function preload_image(url) {
	let img = new Image();
	console.log("preloading: " + url)
	img.src = url;
	return img;
}

function getEmoji(input) {
	if (emoji) {
		input = emoji.replace_unified(input);
		const parser = new DOMParser();
		htmlDoc = parser.parseFromString(input, 'text/html');
		codepoint = htmlDoc.getElementsByTagName("span")[0].dataset["codepoints"];
		return preload_image("../images/emoji-data/img-google-64/" + codepoint + ".png");
	} else
		return input;
}

var tables = new Map();
var places = new Map();

function createTables() {
	locations = Object.keys(data.locationIcons)
	for (let i = 0; i < locations.length; i++) {
		roomName = locations[i]
		places.set(roomName, getEmoji(data.locationIcons[roomName]));
		createCluesTable("room"+i, roomName, data.numIntervals, data.timeOffset, i == 0, false);
	}

	locations = Object.keys(tutorialData.locationIcons)
	for (let i = 0; i < locations.length; i++) {
		roomName = locations[i]
		places.set(roomName, getEmoji(tutorialData.locationIcons[roomName]));
	}

	createCluesTable("kitchen:tutorial-1", "kitchen:tutorial-1", 6, tutorialData.timeOffset, true, true);
	createCluesTable("bathroom:tutorial-1", "bathroom:tutorial-1", 6, tutorialData.timeOffset, false, true);
	createCluesTable("kitchen:tutorial-2", "kitchen:tutorial-2", 6, tutorialData.timeOffset, true, true);
	createCluesTable("bathroom:tutorial-2", "bathroom:tutorial-2", 6, tutorialData.timeOffset, false, true);
	createCluesTableWeapons("weapons");
	createCluesTableWeapons("weapons:tutorial-1");
	createCluesTableWeapons("weapons:tutorial-2");
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

function drawClueTable(table) {
	table.ctx.fillStyle = table.colorEven;
	table.ctx.fillRect(0, 0, table.canvas.width, table.canvas.height);

	for (let i = 1; i < table.nColumns; i++) {
		for (let j = 0; j < table.nRows; j++) {
			clearClueTable(i, j, table);
			table.data[i][j] = "";
		}
	}
}

function clearClueTable(column, row, table) {
	// This function clears a cell and redraws the border lines
	table.ctx.clearRect(table.columnSize * column, table.rowSize * row, table.columnSize, table.rowSize);
	table.data[column][row] = null;

	// Determine the background color based on the row number
	var backgroundColor = row % 2 === 0 ? table.colorEven : table.colorOdd;
	if (table.headerVisible && row === 0)
		backgroundColor = table.colorEven;
	else if (table.headerVisible)
		backgroundColor = row % 2 === 0 ? table.colorOdd : table.colorEven;

	table.ctx.fillStyle = backgroundColor;
	table.ctx.fillRect(table.columnSize * column, table.rowSize * row, table.columnSize, table.rowSize);

	table.ctx.strokeStyle = table.lineColor;
	table.ctx.beginPath();
	table.ctx.moveTo(table.columnSize * column, table.rowSize * row);
	table.ctx.lineTo(table.columnSize * (column + 1), table.rowSize * row);
	table.ctx.lineTo(table.columnSize * (column + 1), table.rowSize * (row + 1));
	table.ctx.lineTo(table.columnSize * column, table.rowSize * (row + 1));
	table.ctx.closePath();
	table.ctx.stroke();
}

function fillClueTable(text, size, color, column, row, table) {
	table.ctx.font = "bold " + size + "px Raleway";
	table.ctx.textAlign = "center";
	table.ctx.fillStyle = color;
	if (text && typeof(text) === "object") {
		console.log(text);
		table.ctx.drawImage(text, table.columnSize * column + table.columnSize / 2 - text.width / 5, table.rowSize * row / 2 + table.rowSize / 1.8 - text.height / 4, text.width / 2.5, text.height / 2.5);
	} else
		table.ctx.fillText(text, table.columnSize * column + table.columnSize / 2, table.rowSize * row + table.rowSize / 1.5);

	table.data[column][row] = text;
}

function renderTextInColumn(text, size, color, column, table) {
	table.ctx.font = "bold " + size + "px Raleway";
	table.ctx.textAlign = "center";
	table.ctx.fillStyle = color;

	const textX = table.columnSize * column + table.columnSize / 2;
	const textY = table.height / 2 + size / 3;

	if (text && typeof(text) === "object") {
		console.log(text);
		table.ctx.drawImage(text, textX - size / 2, textY - size / 1.2, text.width / 2.5, text.height / 2.5);
	} else
		table.ctx.fillText(text, textX, textY);
}

function crossClueTable(size, color, column, row, table) {
	table.ctx.strokeStyle = color;
	table.ctx.lineWidth = size;
	table.ctx.beginPath();
	table.ctx.moveTo(table.columnSize * column + 3, table.rowSize * row + 3);
	table.ctx.lineTo(table.columnSize * (column + 1) - 3, table.rowSize * (row + 1) - 3);
	table.ctx.moveTo(table.columnSize * (column + 1) - 3, table.rowSize * row + 3);
	table.ctx.lineTo(table.columnSize * column + 3, table.rowSize * (row + 1) - 3);
	table.ctx.stroke();

	table.extra[column][row] = "crossed";
}

function createCluesTableWeapons(name) {
	var rowNames = []
	var isTutorial = name.includes("tutorial");

	var weaponMap = data.weaponMap;
	var weaponIcons = data.weaponIcons;
	var locationIcons = data.locationIcons;

	if (isTutorial) {
		weaponMap = tutorialData.weaponMap;
		weaponIcons = tutorialData.weaponIcons;
		locationIcons = tutorialData.locationIcons;
	}

	nColumns = Object.keys(weaponIcons).length;
	var nRows = rowNames.length + 1;

	var c = document.getElementById("clues-table-" + name);
	var ctx = c.getContext("2d");

	var width = Math.min(window.innerWidth * 0.92, c.width);
	var height = c.height;

	let ratio = window.devicePixelRatio;
	c.width = width * ratio;
	c.height = height * ratio;
	c.style.width = width + "px";
	c.style.height = height + "px";
	ctx.scale(ratio, ratio);
	c.style.display = 'inline';

	var columnSize = width / nColumns;
	var rowSize = height / nRows;

	var table = {
		canvas: c,
		ctx: ctx,
		nColumns: nColumns,
		nRows: nRows,
		columnSize: columnSize,
		rowSize: rowSize,
		colorEven: '#888888',
		colorOdd: '#777777',
		lineColor: '#FFFFFF',
		headerVisible: false,
		width: width,
		height: height,
		data: [...Array(nColumns)].map(e => Array(nRows).fill("")),
		extra: [...Array(nColumns)].map(e => Array(nRows).fill("")),
		isTutorial: isTutorial,
	};

	if (isKindle) {
		table.colorEven = '#FFFFFF';
		table.colorOdd = '#FFFFFF';
		table.lineColor = '#000000';
	}

	tables.set(name, table);
	drawClueTable(table);

	var placeIcon;
	var weaponIcon;

	weapons = Object.keys(weaponMap);
	for (var i = 0; i < weapons.length; i++) {
		placeIcon = getEmoji(locationIcons[weaponMap[weapons[i]]]);
		weaponIcon = getEmoji(weaponIcons[weapons[i]]);

		if (isKindle) // Kindle does not support rendering two emojis in the same cell
			fillClueTable(weaponIcon, columnSize / 6, '#000000', i, 0, table);
		else
			fillClueTable(weaponIcon + " " + placeIcon, columnSize / 6, '#000000', i, 0, table);
	}
}

function createCluesTable(room, name, nColumns, timeOffset, headerVisible, isTutorial) {
	var rowNames = []
	if (isTutorial) {
		rowNames = rowNames.concat(['alice', 'bob']);
	} else {
		rowNames = rowNames.concat(data.characterNames);
	}
	rowNames.sort();

	nColumns = nColumns + 2;
	var nRows = rowNames.length;
	if (headerVisible)
		nRows = nRows + 1;

	var c = document.getElementById("clues-table-" + room);
	var ctx = c.getContext("2d");
	var width = Math.min(window.innerWidth * 0.92, c.width);
	var height = c.height;

	let ratio = window.devicePixelRatio;
	c.width = width * ratio;
	c.height = height * ratio;
	c.style.width = width + "px";
	c.style.height = height + "px";
	c.style.display = 'inline';
	ctx.scale(ratio, ratio);

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
		colorEven: '#888888',
		colorOdd: '#777777',
		lineColor: '#FFFFFF',
		headerVisible: headerVisible,
		width: width,
		height: height,
		data: [...Array(nColumns)].map(e => Array(nRows).fill("")),
		isTutorial: isTutorial,
	};

	if (isKindle) {
		table.colorEven = '#EEEEEE';
		table.colorOdd = '#DDDDDD';
		table.lineColor = '#000000';
	}

	tables.set(room, table);
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
			fillClueTable(titles[i], columnSize / 3.3, '#000000', i + 1, 0, table);
			table.data[i + 1][0] = titles[i];
		}
	}
	var column;
	for (let i = 0; i < nRows; i++) {
		var column = i;
		if (headerVisible)
			column = column + 1;
		fillClueTable(rowNames[i], columnSize / 3.3, '#000000', 1, column, table);
		table.data[1][column] = rowNames[i];
	}
	var placeLabelPosition = 1;
	if (headerVisible)
		placeLabelPosition = placeLabelPosition + 1;

	name = name.split(":")[0];
	renderTextInColumn(places.get(name), columnSize / 1.5, '#000000', 0, table);
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
			roomName = data.locationMap[character];
			var color = (character == data.victim) ? '#cc0000' : '#000000';
			var symbol = (character == data.victim && isKindle) ? "☠︎" : "✓";
			if (roomName == name) {
				clearClueTable(nColumns - 1, i, table);
				fillClueTable(symbol, columnSize / 3, color, nColumns - 1, i, table);
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
	var value = table.extra[position[0]][position[1]];
	var weapon = table.data[position[0]][position[1]];

	clearClueTable(position[0], position[1], table);
	fillClueTable(weapon, table.columnSize / 6, '#000000', position[0], position[1], table);

	if (value == "crossed") {
		table.extra[position[0]][position[1]] = "";
	} else {
		crossClueTable(3, '#770000', position[0], position[1], table);
	}
}

function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms))
}

async function checkCellClicked(c, x, y) {
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
	clearClueTable(position[0], position[1], table);
	fillClueTable(value, table.columnSize / 3, '#000000', position[0], position[1], table);

	var highligthColor = '#2222FF'
	name = table.data[1][position[1]]
	clearClueTable(1, position[1], table);
	fillClueTable(name, table.columnSize / 2.6, highligthColor, 1, position[1], table);

	var ftable = tables.get("room0");
	var time = ftable.data[position[0]][0]
	clearClueTable(position[0], 0, ftable);
	fillClueTable(time, ftable.columnSize / 2.6, highligthColor, position[0], 0, ftable);

	await sleep(300);

	// Restore cells in both tables
	clearClueTable(1, position[1], table);
	fillClueTable(name, table.columnSize / 3.3, '#000000', 1, position[1], table);

	clearClueTable(position[0], 0, ftable);
	fillClueTable(time, table.columnSize / 3.3, '#000000', position[0], 0, ftable);
}

function clearTable(c) {
	var name = c.replace("clues-table-", "");
	var table = tables.get(name);

	var data = tutorialData.expectedData[name];
	for (let i = 0; i < table.nColumns; i++) {
		for (let j = 0; j < table.nRows; j++) {
			var value = table.data[i][j];
			if (value == "✓" || value == "✗" || value == "?") {
				clearClueTable(i, j, table);
				fillClueTable("", table.columnSize / 3, '#000000', i, j, table);
			}
		}
	}
}

function checkTutorialTable(c) {
	var name = c.replace("clues-table-", "");
	var table = tables.get(name);

	var data = tutorialData.expectedData[name];

	for (let i = 0; i < data.length; i++) {
		console.log(data[i])
		for (let j = 0; j < data[i].length; j++) {
			var expectedValue = data[i][j];
			var value = table.data[j][i];

			if (expectedValue == "✓" || expectedValue == "✗") {
				if (value == expectedValue) {
					clearClueTable(j, i, table);
					fillClueTable(value, table.columnSize / 3, '#02FF20', j, i, table);
				} else {
					if (value == "")
						value = "?";
					clearClueTable(j, i, table);
					fillClueTable(value, table.columnSize / 3, '#FF2020', j, i, table);
				}
			} else if (expectedValue == "?") {
				if (value == "?" || value == "") {
					//Nothing
				} else {
					clearClueTable(j, i, table);
					fillClueTable(value, table.columnSize / 3, '#FF2020', j, i, table);
				}
			}
		}
	}
}