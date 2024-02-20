var ua = navigator.userAgent;
var isKindle = /Kindle/i.test(ua);
var isMobile = /Mobi/i.test(ua);

var emoji = null;
var pixelRatio = window.devicePixelRatio;

if (isMobile)
	pixelRatio = 1;

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

var tables = new Map();
var places = new Map();

function createTables() {
    for (const location of Object.keys(data.locationIcons)) {
        places.set(location, getEmoji(data.locationIcons[location]));
        createCluesTable(location, data.numIntervals, data.timeOffset, location == "bedroom", false);
    }
    createCluesTable("kitchen-tutorial", 6, data.timeOffset, true, true);
    createCluesTable("bathroom-tutorial", 6, data.timeOffset, false, true);
    createCluesTableWeapons();
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
	table.ctx.fillStyle = backgroundColor;
	table.ctx.fillRect(table.columnSize * column, table.rowSize * row, table.columnSize, table.rowSize);

	table.ctx.strokeStyle = "white";
	table.ctx.beginPath();
	table.ctx.moveTo(table.columnSize * column, table.rowSize * row);
	table.ctx.lineTo(table.columnSize * (column + 1), table.rowSize * row);
	table.ctx.lineTo(table.columnSize * (column + 1), table.rowSize * (row + 1));
	table.ctx.lineTo(table.columnSize * column, table.rowSize * (row + 1));
	table.ctx.closePath();
	table.ctx.stroke();
}

function fillClueTable(text, size, color, column, row, table) {
	size = Math.ceil(size / pixelRatio * 1.2);
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

function createCluesTableWeapons() {
	var rowNames = []

	nColumns = Object.keys(data.weaponIcons).length;
	var nRows = rowNames.length + 1;
	var name = "weapons"
	var c = document.getElementById("clues-table-" + name);
	c.style.display = 'inline';
	c.height /= pixelRatio;

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
		colorEven: '#888888',
		colorOdd: '#777777',
		headerVisible: false,
		width: width,
		height: height,
		data: [...Array(nColumns)].map(e => Array(nRows).fill("")),
		extra: [...Array(nColumns)].map(e => Array(nRows).fill("")),
		isTutorial: false,
	};


	tables.set(name, table);
	drawClueTable(table);

	var placeIcon;
	var weaponIcon;
	weapons = Object.keys(data.weaponMap);
	for (var i = 0; i < weapons.length; i++) {
		placeIcon = getEmoji(data.locationIcons[data.weaponMap[weapons[i]]]);
		weaponIcon = getEmoji(data.weaponIcons[weapons[i]]);

		if (isKindle) // Kindle does not support rendering two emojis in the same cell
			fillClueTable(weaponIcon, columnSize / 6, '#000000', i, 0, table);
		else 
			fillClueTable(weaponIcon + " " + placeIcon, columnSize / 6, '#000000', i, 0, table);
	}
}

function createCluesTable(name, nColumns, timeOffset, headerVisible, isTutorial) {
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

	var c = document.getElementById("clues-table-" + name);
	c.style.display = 'inline';
	if (!headerVisible) {
		c.height = c.height - 40;
	}

	c.height /= pixelRatio;

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
		colorEven: '#888888',
		colorOdd: '#777777',
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
			roomName = data.locationMap[character];
			var color = (character == data.victim) ? '#cc0000' : '#000000';
			if (roomName == name) {
				clearClueTable(nColumns - 1, i, table);
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
	clearClueTable(position[0], position[1], table);
	fillClueTable(value, table.columnSize / 3, '#000000', position[0], position[1], table);
}