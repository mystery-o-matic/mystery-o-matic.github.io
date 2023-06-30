function getCurrentDate() {
	var options = {  weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour12: false };
	return String(new Date().toLocaleTimeString('en-us', options)).split(" at")[0];
}

document.getElementById("span-today").innerHTML = getCurrentDate();

function openModal(name) {
	let element = document.getElementById('portraitImage');
	element.src = "images/" + name + ".jpg";
	let modal = new bootstrap.Modal(document.getElementById('portraitModal'), {});
	modal.show();
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
	let viewed = 0;
	let i = 1;
	while (true) {
		element = document.getElementById("panelsStayOpen-collapse-" + i)
		if (element == null)
			break;

		if (clueWasViewed(element.parentElement))
			viewed = viewed + 1;

		i = i + 1
	}
	viewedPercentage = 100 * viewed / i;
	rank = ""
	if (viewedPercentage == 0)
		rank = "Sleuth level: clairvoyant!";
	else if (viewedPercentage <= 25)
		rank = "Sleuth level: chief inspector!";
	else if (viewedPercentage <= 50)
		rank = "Sleuth level: senior detective!";
	else if (viewedPercentage <= 75)
		rank = "Sleuth level: sub-inspector!";
	else {
		rank = "Sleuth level: constable"
		rank = rank + "\nCongratulations on a job.. done!"
	}

	return rank;
}

function markedAsViewed(element) {
	if (!clueWasViewed(element))
		element.textContent += "👀";
}

//create Tabulator on DOM element with id "example-table"
var tables = [];
tables.push(createCluesTable("bedroom", nColumns, timeOffset, true));
tables.push(createCluesTable("kitchen", nColumns, timeOffset, false));
tables.push(createCluesTable("living", nColumns, timeOffset, false));
tables.push(createCluesTable("bathroom", nColumns, timeOffset, false));

function createCluesTable(name, nColumns, timeOffset, headerVisible) {
  var date = new Date(null);
  date.setSeconds(timeOffset);
  var columns = [ //Define Table Columns
  {title:"", field:"name", headerSort:false, hozAlign:"center", vertAlign:"center", resizable: false},
  ];
  var title;
  for (let i = 0; i < nColumns; i++) {
    title = date.toISOString().substr(11, 5);
	columns.push({title:title, width: 45, headerSort:false, hozAlign:"center", vertAlign:"center", resizable:false});
	date.setSeconds(60 * 15);
  }

  var tabledata = [];
  for (let i = 0; i < suspectNames.length; i++) {
	tabledata.push({id: i, name: suspectNames[i]});
  }

  var table = new Tabulator("#clues-table-" + name, {
	renderVertical:"basic",
	layout:"fitDataTable",
	headerVisible: headerVisible,
	data:tabledata, //assign data to table
	columns: columns,
  });

  table.on("cellClick", function(e, cell){
	if (cell.getColumn().getField() == "name")
		return;
    if (cell.getValue() == undefined)
		cell.setValue("✓")
	else if (cell.getValue() == "✓")
		cell.setValue("✗")
	else if (cell.getValue() == "✗")
		cell.setValue("?")
	else
		cell.setValue(null)
  });
  return table;
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

function checkAccusation(solution) {
	input = "";
	input = input + document.getElementById("who-selector").value + "-";
	input = input + document.getElementById("how-selector").value + "-";
	input = input + document.getElementById("when-selector").value;

	hash(input).then((result) => {
		if (result == solution) {
			rank = computeRank();
			alert("Correct answer!\n" + rank);
		} else
			alert("Incorrect answer!");
	});
}