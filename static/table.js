class ClueTable {
	constructor(canvas, ctx, nColumns, nRows, columnSize, rowSize, colorEven, colorOdd, lineColor, headerVisible, width, height, isTutorial, readOnly = false) {
		this.canvas = canvas;
		this.ctx = ctx;
		this.nColumns = nColumns;
		this.nRows = nRows;
		this.columnSize = columnSize;
		this.rowSize = rowSize;
		this.colorEven = colorEven;
		this.colorOdd = colorOdd;
		this.lineColor = lineColor;
		this.headerVisible = headerVisible;
		this.width = width;
		this.height = height;
		this.isTutorial = isTutorial;
		this.readOnly = readOnly;
		this.data = [...Array(nColumns)].map(() => Array(nRows).fill(""));
		this.extra = [...Array(nColumns)].map(() => Array(nRows).fill(""));
	}

	draw() {
		this.ctx.fillStyle = this.colorEven;
		this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
		let startColumn = this.nRows === 1 ? 0 : 1;
		for (let i = startColumn; i < this.nColumns; i++) {
			for (let j = 0; j < this.nRows; j++) {
				this.clearCell(i, j);
				this.data[i][j] = "";
			}
		}
	}

	clearCell(column, row) {
		this.ctx.clearRect(
			this.columnSize * column,
			this.rowSize * row,
			this.columnSize,
			this.rowSize
		);
		this.data[column][row] = null;
		let backgroundColor = row % 2 === 0 ? this.colorEven : this.colorOdd;
		if (this.headerVisible && row === 0) backgroundColor = this.colorEven;
		else if (this.headerVisible) backgroundColor = row % 2 === 0 ? this.colorOdd : this.colorEven;
		this.ctx.fillStyle = backgroundColor;
		this.ctx.fillRect(
			this.columnSize * column,
			this.rowSize * row,
			this.columnSize,
			this.rowSize
		);
		this.ctx.strokeStyle = this.lineColor;
		this.ctx.beginPath();
		this.ctx.moveTo(this.columnSize * column, this.rowSize * row);
		this.ctx.lineTo(this.columnSize * (column + 1), this.rowSize * row);
		this.ctx.lineTo(this.columnSize * (column + 1), this.rowSize * (row + 1));
		this.ctx.lineTo(this.columnSize * column, this.rowSize * (row + 1));
		this.ctx.closePath();
		this.ctx.stroke();
	}

	fillCell(text, size, color, column, row) {
		this.ctx.font = "bold " + size + "px Raleway";
		this.ctx.textAlign = "center";
		this.ctx.fillStyle = color;
		if (text && typeof(text) === "object") {
			this.ctx.drawImage(
				text,
				this.columnSize * column + this.columnSize / 2 - text.width / 5,
				this.rowSize * row / 2 + this.rowSize / 1.8 - text.height / 4,
				text.width / 2.5,
				text.height / 2.5
			);
		} else {
			this.ctx.fillText(
				text,
				this.columnSize * column + this.columnSize / 2,
				this.rowSize * row + this.rowSize / 1.5
			);
		}
		this.data[column][row] = text;
	}

	renderTextInColumn(text, size, color, column) {
		this.ctx.font = "bold " + size + "px Raleway";
		this.ctx.textAlign = "center";
		this.ctx.fillStyle = color;
		const textX = this.columnSize * column + this.columnSize / 2;
		const textY = this.height / 2 + size / 3;
		if (text && typeof(text) === "object") {
			this.ctx.drawImage(
				text,
				textX - size / 2,
				textY - size / 1.2,
				text.width / 2.5,
				text.height / 2.5
			);
		} else this.ctx.fillText(text, textX, textY);
	}

	crossCell(size, color, column, row) {
		this.ctx.strokeStyle = color;
		this.ctx.lineWidth = size;
		this.ctx.beginPath();
		this.ctx.moveTo(this.columnSize * column + 3, this.rowSize * row + 3);
		this.ctx.lineTo(
			this.columnSize * (column + 1) - 3,
			this.rowSize * (row + 1) - 3
		);
		this.ctx.moveTo(
			this.columnSize * (column + 1) - 3,
			this.rowSize * row + 3
		);
		this.ctx.lineTo(
			this.columnSize * column + 3,
			this.rowSize * (row + 1) - 3
		);
		this.ctx.stroke();
		this.extra[column][row] = "crossed";
	}

	findPosition(x, y) {
		//console.log(x, y);
		const rect = this.canvas.getBoundingClientRect()
		x = this.height * x / rect.height;
		y = this.width * y / rect.width;
		return [Math.trunc(x / this.columnSize), Math.trunc(y / this.rowSize)];
	}
}

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
	document.getElementById("locations-small").style.height = '25vh';
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

	createCluesTable("kitchen:tutorial-0", "kitchen:tutorial-0", 7, tutorialData.timeOffset, true, true);
	createCluesTable("bedroom:tutorial-0", "bedroom:tutorial-0", 7, tutorialData.timeOffset, false, true);
	createCluesTable("dining room:tutorial-0", "dining room:tutorial-0", 7, tutorialData.timeOffset, false, true);
	createCluesTable("bathroom:tutorial-0", "bathroom:tutorial-0", 7, tutorialData.timeOffset, false, true);

	createCluesTable("bedroom:tutorial-1", "bedroom:tutorial-1", 7, tutorialData.timeOffset, true, true);

	createCluesTable("kitchen:tutorial-2", "kitchen:tutorial-2", 7, tutorialData.timeOffset, true, true);
	createCluesTable("dining room:tutorial-2", "dining room:tutorial-2", 7, tutorialData.timeOffset, false, true);
	createCluesTable("bathroom:tutorial-2", "bathroom:tutorial-2", 7, tutorialData.timeOffset, false, true);

	createCluesTable("dining room:tutorial-3", "dining room:tutorial-3", 7, tutorialData.timeOffset, true, true);

	createCluesTable("kitchen:tutorial-4", "kitchen:tutorial-4", 7, tutorialData.timeOffset, true, true);
	createCluesTable("bedroom:tutorial-4", "bedroom:tutorial-4", 7, tutorialData.timeOffset, false, true);
	createCluesTable("dining room:tutorial-4", "dining room:tutorial-4", 7, tutorialData.timeOffset, false, true);
	createCluesTable("bathroom:tutorial-4", "bathroom:tutorial-4", 7, tutorialData.timeOffset, false, true);

	createCluesTable("kitchen:tutorial-5", "kitchen:tutorial-5", 7, tutorialData.timeOffset, true, true);
	createCluesTable("bedroom:tutorial-5", "bedroom:tutorial-5", 7, tutorialData.timeOffset, false, true);
	createCluesTable("dining room:tutorial-5", "dining room:tutorial-5", 7, tutorialData.timeOffset, false, true);
	createCluesTable("bathroom:tutorial-5", "bathroom:tutorial-5", 7, tutorialData.timeOffset, false, true);

	createCluesTable("kitchen:tutorial-6", "kitchen:tutorial-6", 7, tutorialData.timeOffset, true, true);
	createCluesTable("bedroom:tutorial-6", "bedroom:tutorial-6", 7, tutorialData.timeOffset, false, true);
	createCluesTable("dining room:tutorial-6", "dining room:tutorial-6", 7, tutorialData.timeOffset, false, true);
	createCluesTable("bathroom:tutorial-6", "bathroom:tutorial-6", 7, tutorialData.timeOffset, false, true);

	createCluesTable("kitchen:tutorial-7", "kitchen:tutorial-7", 7, tutorialData.timeOffset, true, true);


	createCluesTable("kitchen:tutorial-final", "kitchen:tutorial-final", 7, tutorialData.timeOffset, true, true);
	createCluesTable("bedroom:tutorial-final", "bedroom:tutorial-final", 7, tutorialData.timeOffset, false, true);
	createCluesTable("dining room:tutorial-final", "dining room:tutorial-final", 7, tutorialData.timeOffset, false, true);
	createCluesTable("bathroom:tutorial-final", "bathroom:tutorial-final", 7, tutorialData.timeOffset, false, true);

	tables.get("kitchen:tutorial-final").readOnly = true;
	tables.get("bedroom:tutorial-final").readOnly = true;
	tables.get("dining room:tutorial-final").readOnly = true;
	tables.get("bathroom:tutorial-final").readOnly = true;

	createCluesTableWeapons("weapons");
	createCluesTableWeapons("weapons:tutorial-0");
	createCluesTableWeapons("weapons:tutorial-final");
	tables.get("weapons:tutorial-final").crossCell(3, '#770000', 2, 0);
	tables.get("weapons:tutorial-final").readOnly = true;
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

	var tableColorEven = "#888888";
	var tableColorOdd = "#777777";
	var tableLineColor = "#FFFFFF";
	if (isKindle) {
		tableColorEven = "#FFFFFF";
		tableColorOdd = "#FFFFFF";
		tableLineColor = "#000000";
	}
	let table = new ClueTable(
		c, ctx, nColumns, nRows, columnSize, rowSize,
		tableColorEven, tableColorOdd, tableLineColor, false, width, height, isTutorial
	);
	tables.set(name, table);
	table.draw();

	weapons = Object.keys(weaponMap);
	for (var i = 0; i < weapons.length; i++) {
		var placeIcon = getEmoji(locationIcons[weaponMap[weapons[i]]]);
		var weaponIcon = getEmoji(weaponIcons[weapons[i]]);
		if (isKindle)
			table.fillCell(weaponIcon, columnSize / 6, "#000000", i, 0);
		else
			table.fillCell(
				weaponIcon + " " + placeIcon,
				columnSize / 6,
				"#000000",
				i,
				0
			);
	}
}

function createCluesTable(room, name, nColumns, timeOffset, headerVisible, isTutorial) {
	var completeName = name;
	var rowNames = data.characterNames;
	var victim = data.victim;
	var locationMap = data.locationMap;
	if (isTutorial) {
		rowNames = tutorialData.characterNames;
		victim = tutorialData.victim;
		locationMap = tutorialData.locationMap;
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

	var tableColorEven = "#888888";
	var tableColorOdd = "#777777";
	var tableLineColor = "#FFFFFF";
	if (isKindle) {
		tableColorEven = "#EEEEEE";
		tableColorOdd = "#DDDDDD";
		tableLineColor = "#000000";
	}

	let table = new ClueTable(
		c, ctx, nColumns, nRows, columnSize, rowSize,
		tableColorEven, tableColorOdd, tableLineColor,
		headerVisible, width, height, isTutorial
	);
	tables.set(room, table);
	table.draw();

	var date = new Date(null);
	date.setSeconds(timeOffset);
	var titles = [getEmoji("🕰️")];
	for (let i = 0; i < nColumns; i++) {
	  title = date.toISOString().substr(12, 4);
	  titles.push(title);
	  date.setSeconds(60 * 15);
	}

	if (headerVisible) {
		for (let i = 0; i < nColumns - 1; i++) {
			table.fillCell(titles[i], columnSize / 2.8, '#000000', i + 1, 0);
			table.data[i + 1][0] = titles[i];
		}
	}
	var column;
	for (let i = 0; i < nRows; i++) {
		var column = i;
		if (headerVisible)
			column = column + 1;
		table.fillCell(rowNames[i], columnSize / 3.0, '#000000', 1, column);
		table.data[1][column] = rowNames[i];
	}
	var placeLabelPosition = 1;
	if (headerVisible)
		placeLabelPosition = placeLabelPosition + 1;

	name = name.split(":")[0];
	table.renderTextInColumn(places.get(name), columnSize / 1.5, '#000000', 0);
	table.data[0][0] = " ";
	table.data[0][1] = " ";
	table.data[0][2] = " ";
	table.data[0][3] = " ";
	table.data[0][placeLabelPosition] = places.get(name);

	var startRow = 0;
	if (headerVisible)
		startRow = 1
	for (let i = startRow; i < nRows; i++) {
		table.fillCell("✗", columnSize / 2, '#000000', nColumns - 1, i);
	}

	for (let i = startRow; i < startRow + rowNames.length; i++) {
		var character = rowNames[i - startRow];
		roomName = locationMap[character];
		var color = (character == victim) ? '#cc0000' : '#000000';
		var symbol = (character == victim && isKindle) ? "☠︎" : "✓";
		if (roomName == name) {
			table.clearCell(nColumns - 1, i);
			table.fillCell(symbol, columnSize / 2, color, nColumns - 1, i);
		}
	}

	if (isTutorial && tutorialData.initialData[completeName] != undefined) {
		for (let i = 0; i < (headerVisible ? nRows - 1 : nRows); i++) {
			for (let j = 0; j < nColumns - 3; j++) {
				table.fillCell(tutorialData.initialData[completeName][i][j], columnSize / 3, '#000000', j + 2, headerVisible ? i + 1 : i);
			}
		}
	}

	return table;
}

function checkWeaponClicked(c, x, y) {
	var name = c.id.replace("clues-table-", "");
	var table = tables.get(name);
	if (table.readOnly)
		return;
	var position = table.findPosition(x, y);
	var value = table.extra[position[0]][position[1]];
	var weapon = table.data[position[0]][position[1]];

	table.clearCell(position[0], position[1]);
	table.fillCell(weapon, table.columnSize / 6, '#000000', position[0], position[1]);

	if (value == "crossed") {
		table.extra[position[0]][position[1]] = "";
	} else {
		table.crossCell(3, '#770000', position[0], position[1]);
	}
}

function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms))
}

async function checkCellClicked(c, x, y) {
	var name = c.id.replace("clues-table-", "");
	var table = tables.get(name);
	if (table.readOnly)
		return;
	var position = table.findPosition(x, y);
	//console.log(name);
	if (position[0] == table.nColumns - 1)
		return;

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
	table.clearCell(position[0], position[1]);
	table.fillCell(value, table.columnSize / 2, '#000000', position[0], position[1]);

	var highligthColor = '#2222FF'
	name = table.data[1][position[1]]
	table.clearCell(1, position[1]);
	table.fillCell(name, table.columnSize / 2.6, highligthColor, 1, position[1]);

	var ftable = tables.get("room0");
	var time = ftable.data[position[0]][0]
	if (!table.isTutorial) {
		ftable.clearCell(position[0], 0);
		ftable.fillCell(time, ftable.columnSize / 2.6, highligthColor, position[0], 0);
	}

	await sleep(300);

	// Restore cells in both tables
	table.clearCell(1, position[1]);
	table.fillCell(name, table.columnSize / 3.3, '#000000', 1, position[1]);

	if (!table.isTutorial) {
		ftable.clearCell(position[0], 0);
		ftable.fillCell(time, table.columnSize / 3.3, '#000000', position[0], 0);
	}
}

function clearTable(c) {
	for (const [tableName, table] of tables.entries()) {
		if (!tableName.includes(c))
			continue;

		if (table.nRows == 1) {
			for (let i = 0; i < table.nColumns; i++) {
				var weapon = table.data[i][0]
				table.clearCell(i, 0);
				table.fillCell(weapon, table.columnSize / 6, '#000000', i, 0);
				table.extra[i][0] = "";
			}
		} else {
			for (let i = 0; i < table.nColumns - 1; i++) {
				for (let j = 0; j < table.nRows; j++) {
					var value = table.data[i][j];
					if (value == "✓" || value == "✗" || value == "?") {
						table.clearCell(i, j);
						table.fillCell("", table.columnSize / 3, '#000000', i, j);
					}
				}
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
					table.clearCell(j, i);
					table.fillCell(value, table.columnSize / 3, '#02FF20', j, i);
				} else {
					if (value == "")
						value = "?";
					table.clearCell(j, i);
					table.fillCell(value, table.columnSize / 3, '#FF2020', j, i);
				}
			} else if (expectedValue == "?") {
				if (value == "?" || value == "") {
					//Nothing
				} else {
					table.clearCell(j, i, table);
					table.fillCell(value, table.columnSize / 3, '#FF2020', j, i);
				}
			}
		}
	}
}