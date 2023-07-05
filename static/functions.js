function getCurrentDate() {
	var options = {  weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour12: false };
	return String(new Date().toLocaleTimeString('en-us', options)).split(" at")[0];
}

function showPage(page) {
	document.getElementById("home").style.display = "none";
	document.getElementById("about").style.display = "none";
	document.getElementById("how-to-play").style.display = "none";
	document.getElementById(page).style.display = "block";
}

hideClues();
document.getElementById("span-today").innerHTML = getCurrentDate();
var tries = 0;

function openModal(name) {
	let element = document.getElementById('portraitImage');
	element.src = "images/" + name + ".jpg";
	let modal = new bootstrap.Modal(document.getElementById('portraitModal'), {});
	modal.show();
}

function hideClues() {
	let i = 4;
	while (true) {
		element = document.getElementById("accordion-" + i)
		if (element == null)
			break;

		element.style.display = "none"
		i = i + 1
	}
}

function revealAnotherClue() {
	let i = 1;
	let revealed = false;
	while (true) {
		element = document.getElementById("accordion-" + i);
		console.log(element);
		if (element == null) {
			break;
		}
		if (element.style.display == "none") {
			element.style.display = "block";
			revealed = true;
			break;
		}
		i = i + 1
	}
	if (!revealed) {
		var button = document.getElementById("more-clues-button");
		button.innerText = "No more clues"
		button.disabled = true;
	}
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
	rank = "Sleuth-o-matic: "
	if (viewedPercentage ==  0 && tries == 0) {
		rank += "<b>clairvoyant</b> 🪄";
		rank += "<br><i>Next time try guessing the lotto</i>!"
	} else if (viewedPercentage <= 25 && tries == 0) {
		rank += "<b>chief inspector</b> 🕵️";
		rank += "<br><i>Your deductive abilities are remarkable !</i>"
	} else if (viewedPercentage <= 50 && tries == 0) {
		rank += "<b>senior detective</b> 🕵️";
		rank += "<br><i>Good job indeed !</i>"
	} else if (viewedPercentage <= 75 && tries == 0) {
		rank += "<b>sub-inspector!</b> 🕵️";
		rank += "<br><i>Keep sharpening your deductive skills!</i>"
	} else {
		rank += "<b>constable</b> 👮"
		rank += "<br><i>Congratulations on a job.. done!</i>"
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
		if (result == solution) {
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