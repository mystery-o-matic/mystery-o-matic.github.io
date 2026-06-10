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
		this.ctx.fillStyle = color;
		if (text && typeof(text) === "object") {
			if (Array.isArray(text)) {
				this._drawImages(text, size, column, row);
			} else {
				this._drawImage(text, size, column, row);
			}
		} else {
			this._fillText(text, size, color, column, row);
		}
		this.data[column][row] = text;
	}

	_fillText(text, size, color, column, row) {
        const centerX = this.columnSize * column + this.columnSize / 2;
        const centerY = this.rowSize * row + this.rowSize / 2;
        if (isIOS && hasColorEmoji(text) && drawEmojiCentered(this.ctx, text, size, centerX, centerY))
            return;
        this.ctx.font = "bold " + size + "px Raleway";
        this.ctx.textAlign = "center";
        this.ctx.textBaseline = "middle";
        this.ctx.fillStyle = color;
        this.ctx.fillText(text, centerX, centerY);
    }

	_drawImage(image, size, column, row) {
        const dHeight = size;
        const dWidth = image.width * (dHeight / image.height);
        const centerX = this.columnSize * column + this.columnSize / 2;
        const centerY = this.rowSize * row + this.rowSize / 2;
        const dx = centerX - dWidth / 2;
        const dy = centerY - dHeight / 2;
        this.ctx.drawImage(image, dx, dy, dWidth, dHeight);
    }

	_drawImages(images, size, column, row) {
        const dHeight = size;
        const dWidths = images.map(img => img.width * (dHeight / img.height));
        const totalWidth = dWidths.reduce((a, b) => a + b, 0);

        const centerX = this.columnSize * column + this.columnSize / 2;
        const centerY = this.rowSize * row + this.rowSize / 2;

        let currentX = centerX - totalWidth / 2;
        for (let i = 0; i < images.length; i++) {
            const img = images[i];
            const dWidth = dWidths[i];
            const dy = centerY - dHeight / 2;
            this.ctx.drawImage(img, currentX, dy, dWidth, dHeight);
            currentX += dWidth;
        }
    }

	renderTextInColumn(text, size, color, column) {
		this.ctx.strokeStyle = this.lineColor;
		this.ctx.beginPath();
		this.ctx.moveTo(this.columnSize * column, 0);
		this.ctx.lineTo(this.columnSize * (column + 1), 0);
		this.ctx.moveTo(this.columnSize * column, 0);
		this.ctx.lineTo(this.columnSize * column, this.height);
		this.ctx.moveTo(this.columnSize * column, this.height);
		this.ctx.lineTo(this.columnSize * (column + 1), this.height);
		this.ctx.stroke();

		this.ctx.font = "bold " + size + "px Raleway";
		this.ctx.textAlign = "center";
		this.ctx.fillStyle = color;
		const textX = this.columnSize * column + this.columnSize / 2;
		const textY = this.height / 2;
		if (text && typeof(text) === "object") {
			const dHeight = size;
			const dWidth = text.width * (dHeight / text.height);
			const centerX = textX;
			const centerY = this.height / 2;
			const dx = centerX - dWidth / 2;
			const dy = centerY - dHeight / 2;
			this.ctx.drawImage(
				text,
				dx,
				dy,
				dWidth,
				dHeight
			);
		} else {
			if (isIOS && hasColorEmoji(text) && drawEmojiCentered(this.ctx, text, size, textX, textY))
				return;
			this.ctx.textBaseline = "middle";
			this.ctx.fillText(text, textX, textY);
		}
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

// Extra function to get font sizes for different specialized tables

function getCluesFontSize(t) {
	return Math.min(t.rowSize, t.columnSize) / 1.2;
}

function getCluesHeaderFontSize(t) {
	return t.columnSize / 2.9;
}

function getCluesNameFontSize(t) {
	return t.columnSize / 3.3;
}

function getCluesIconFontSize(t) {
	return t.columnSize / 1.5;
}

function getWeaponFontSize(columSize) {
	return columSize / 6;
}

var ua = navigator.userAgent;
var isKindle = /Kindle/i.test(ua);
var isMobile = /Mobi/i.test(ua);
// iPadOS 13+ pretends to be a Mac, so also check for touch support
var isIOS = /iPad|iPhone|iPod/i.test(ua) || (/Macintosh/i.test(ua) && navigator.maxTouchPoints > 1);

var emoji = null;

if (isKindle) {
	emoji = new EmojiConvertor();
	emoji.img_sets['google'].path = '../images/emoji-data/img-google-64/';
	emoji.img_set = 'google';
	emoji.text_mode = false;
	document.body.innerHTML = emoji.replace_unified(document.body.innerHTML);
	document.getElementById("locations-big").src = "locations_big.png";
	document.getElementById("locations-big").style.height = 'auto';
	document.getElementById("switch-theme-button").style.display = "none";
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

// On iOS, WebKit places color emoji on a canvas using metrics that do not
// match the glyphs it actually paints, so centering them with
// textAlign/textBaseline lands them outside their cell (macOS is fine).
// Workaround: draw the emoji once on an offscreen canvas, locate the painted
// pixels and blit that box centered with drawImage, which is unaffected.
var emojiSpriteCache = new Map();

function hasColorEmoji(text) {
	return typeof text === "string" && /[\uD800-\uDFFF\uFE0F]/.test(text);
}

function getEmojiSprite(text, size) {
	var key = size + ":" + text;
	if (emojiSpriteCache.has(key))
		return emojiSpriteCache.get(key);

	var scale = window.devicePixelRatio || 1;
	// Margins are oversized on purpose, so the glyphs land inside the
	// offscreen canvas even when they are drawn off-position
	var units = Array.from(text).length + 4;
	var canvas = document.createElement("canvas");
	canvas.width = Math.ceil(units * size * scale);
	canvas.height = Math.ceil(4 * size * scale);
	var sprite = null;
	try {
		var ctx = canvas.getContext("2d", { willReadFrequently: true });
		ctx.scale(scale, scale);
		ctx.font = "bold " + size + "px Raleway";
		ctx.fillText(text, 2 * size, 2.5 * size);
		var pixels = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
		var minX = canvas.width, minY = canvas.height, maxX = -1, maxY = -1;
		for (var y = 0; y < canvas.height; y++) {
			for (var x = 0; x < canvas.width; x++) {
				if (pixels[(y * canvas.width + x) * 4 + 3] > 16) {
					if (x < minX) minX = x;
					if (x > maxX) maxX = x;
					if (y < minY) minY = y;
					if (y > maxY) maxY = y;
				}
			}
		}
		if (maxX >= 0)
			sprite = {
				canvas: canvas,
				x: minX,
				y: minY,
				width: maxX - minX + 1,
				height: maxY - minY + 1,
				scale: scale
			};
	} catch (e) {
		// getImageData can be unavailable (e.g. lockdown mode); keep using fillText
	}
	emojiSpriteCache.set(key, sprite);
	return sprite;
}

function drawEmojiCentered(ctx, text, size, centerX, centerY) {
	var sprite = getEmojiSprite(text, size);
	if (!sprite)
		return false;
	var width = sprite.width / sprite.scale;
	var height = sprite.height / sprite.scale;
	ctx.drawImage(
		sprite.canvas,
		sprite.x, sprite.y, sprite.width, sprite.height,
		centerX - width / 2, centerY - height / 2, width, height
	);
	return true;
}

var tables = new Map();
var places = new Map();

function createTables() {
	rooms = data.locationOrder
	for (let i = 0; i < rooms.length; i++) {
		roomName = rooms[i][1]
		places.set(roomName, getEmoji(data.locationIcons[roomName]));
		createCluesTable(rooms[i][0], roomName, data.numIntervals, data.timeOffset, i == 0, false);
	}

	locations = Object.keys(tutorialData.locationIcons)
	for (let i = 0; i < locations.length; i++) {
		roomName = locations[i]
		places.set(roomName, getEmoji(tutorialData.locationIcons[roomName]));
	}

	createCluesTableWeapons("weapons");

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

	createCluesTableWeapons("weapons:tutorial-0");
	createCluesTableWeapons("weapons:tutorial-1");
	createCluesTableWeapons("weapons:tutorial-final");
	tables.get("weapons:tutorial-final").crossCell(3, '#770000', 2, 0);
	tables.get("weapons:tutorial-final").readOnly = true;

	if (window.location.hash == "#how-to-play") {
		showPage("how-to-play");
		window.scrollTo(0, 0);
	}
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

	var tableColorEven = "#FFFFFF";
	var tableColorOdd = "#E8E8E8";
	var tableLineColor = "#000000";
	if (isKindle) {
		tableColorEven = "#FFFFFF";
		tableColorOdd = "#FFFFFF";
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
			table.fillCell([weaponIcon, placeIcon], getWeaponFontSize(columnSize), "#000000", i, 0);
		else
			table.fillCell(
				weaponIcon + " " + placeIcon,
				getWeaponFontSize(columnSize),
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

	var tableColorEven = "#FFFFFF";
	var tableColorOdd = "#E8E8E8";
	var tableLineColor = "#000000";
	if (isKindle) {
		tableColorEven = "#EEEEEE";
		tableColorOdd = "#DDDDDD";
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
			table.fillCell(titles[i], getCluesHeaderFontSize(table), '#000000', i + 1, 0);
			table.data[i + 1][0] = titles[i];
		}
	}
	var column;
	for (let i = 0; i < nRows; i++) {
		var column = i;
		if (headerVisible)
			column = column + 1;
		table.fillCell(rowNames[i], getCluesNameFontSize(table), '#000000', 1, column);
		table.data[1][column] = rowNames[i];
	}
	var placeLabelPosition = 1;
	if (headerVisible)
		placeLabelPosition = placeLabelPosition + 1;

	name = name.split(":")[0];
	table.renderTextInColumn(places.get(name), getCluesIconFontSize(table), '#000000', 0);
	table.data[0][0] = " ";
	table.data[0][1] = " ";
	table.data[0][2] = " ";
	table.data[0][3] = " ";
	table.data[0][placeLabelPosition] = places.get(name);

	var startRow = 0;
	if (headerVisible)
		startRow = 1
	for (let i = startRow; i < nRows; i++) {
		table.fillCell("✗", getCluesFontSize(table), '#000000', nColumns - 1, i);
	}

	for (let i = startRow; i < startRow + rowNames.length; i++) {
		var character = rowNames[i - startRow];
		roomName = locationMap[character];
		var color = (character == victim) ? '#cc0000' : '#000000';
		var symbol = (character == victim && isKindle) ? "☠︎" : "✓";
		if (roomName == name) {
			table.clearCell(nColumns - 1, i);
			table.fillCell(symbol, getCluesFontSize(table), color, nColumns - 1, i);
		}
	}

	if (isTutorial && tutorialData.initialData[completeName] != undefined) {
		for (let i = 0; i < (headerVisible ? nRows - 1 : nRows); i++) {
			for (let j = 0; j < nColumns - 3; j++) {
				table.fillCell(tutorialData.initialData[completeName][i][j], getCluesFontSize(table), '#444444', j + 2, headerVisible ? i + 1 : i);
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
	table.fillCell(weapon, getWeaponFontSize(table.columnSize), '#000000', position[0], position[1]);

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
	table.fillCell(value, getCluesFontSize(table), '#000000', position[0], position[1]);

	var highligthColor = '#2222FF'
	name = table.data[1][position[1]]
	table.clearCell(1, position[1]);
	table.fillCell(name, getCluesNameFontSize(table) * 1.08, highligthColor, 1, position[1]);

	firstRoom = data.locationOrder[0][0];
	var ftable = tables.get(firstRoom);
	var time = ftable.data[position[0]][0]
	if (!table.isTutorial) {
		ftable.clearCell(position[0], 0);
		ftable.fillCell(time, getCluesHeaderFontSize(ftable) * 1.08, highligthColor, position[0], 0);
	}

	await sleep(300);

	// Restore cells in both tables
	table.clearCell(1, position[1]);
	table.fillCell(name, getCluesNameFontSize(table), '#000000', 1, position[1]);

	if (!table.isTutorial) {
		ftable.clearCell(position[0], 0);
		ftable.fillCell(time, getCluesHeaderFontSize(table), '#000000', position[0], 0);
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
				table.fillCell(weapon, getWeaponFontSize(table.columnSize), '#000000', i, 0);
				table.extra[i][0] = "";
			}
		} else {
			for (let i = 0; i < table.nColumns - 1; i++) {
				for (let j = 0; j < table.nRows; j++) {
					var value = table.data[i][j];
					if (value == "✓" || value == "✗" || value == "?") {
						table.clearCell(i, j);
						table.fillCell("", getCluesFontSize(table), '#000000', i, j);
					}
				}
			}
		}

	}
}

function checkTutorialTable(c, d) {
	var expectedData = tutorialData.initialData[d.replace("clues-table-", "")];
	var name = c.replace("clues-table-", "");
	var initialData = tutorialData.initialData[name];
	console.log(initialData);
	var table = tables.get(name);

	for (let i = 0; i < expectedData.length; i++) {
		for (let j = 0; j < expectedData[i].length; j++) {
			var expectedValue = expectedData[i][j].trim();
			var ii = table.headerVisible ? i + 1 : i;
			var value = table.data[j + 2][ii];

			if (initialData != undefined && initialData[i][j] != "")
				continue

			if (expectedValue == "✓" || expectedValue == "✗") {
				if (value == expectedValue) {
					table.clearCell(j + 2, ii);
					table.fillCell(value, getCluesFontSize(table), '#06402b', j + 2, ii);
				} else {
					if (value == "")
						value = "?";
					table.clearCell(j + 2, ii);
					table.fillCell(value, getCluesFontSize(table), '#AA0000', j + 2, ii);
				}
			} else if (expectedValue == "") {
				if (value == "?" || value == "") {
					//Nothing
				} else {
					table.clearCell(j + 2, i + 1, table);
					table.fillCell(value, getCluesFontSize(table), '#AA0000', j + 2, ii);
				}
			}
		}
	}
}
