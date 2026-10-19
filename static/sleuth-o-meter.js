var sleuthRankExplanations = {
	"en": {
		"first-try": 'Solve the case on your <span class="sleuth-highlight">first try</span>, revealing <span class="sleuth-highlight">{range} of {total}</span> clues.',
		"up-to": 'at most {limit}',
		"barely-conscious": 'You revealed <span class="sleuth-highlight">more than {limit} of {total}</span> clues, or got the <span class="sleuth-highlight">suspect, weapon or time</span> wrong once.',
		"wrong-answer": 'You got the <span class="sleuth-highlight">suspect, weapon or time</span> wrong once.',
		"unused": 'This rank is not used for the current puzzle mode.'
	},
	"es": {
		"first-try": 'Resuelve el caso en tu <span class="sleuth-highlight">primer intento</span>, revelando <span class="sleuth-highlight">{range} de {total}</span> pistas.',
		"up-to": 'como máximo {limit}',
		"barely-conscious": 'Revelaste <span class="sleuth-highlight">más de {limit} de {total}</span> pistas, o fallaste <span class="sleuth-highlight">sospechoso, arma u hora</span> alguna vez.',
		"wrong-answer": 'Fallaste <span class="sleuth-highlight">sospechoso, arma u hora</span> alguna vez.',
		"unused": 'Este rango no se utiliza en el modo actual del misterio.'
	},
	"ru": {
		"first-try": 'Раскройте дело с <span class="sleuth-highlight">первой попытки</span>, открыв <span class="sleuth-highlight">{range} из {total}</span> подсказок.',
		"up-to": 'не более {limit}',
		"barely-conscious": 'Вы открыли <span class="sleuth-highlight">более {limit} из {total}</span> подсказок или ошиблись в <span class="sleuth-highlight">подозреваемом, оружии или времени</span>.',
		"wrong-answer": 'Вы ошиблись в <span class="sleuth-highlight">подозреваемом, оружии или времени</span>.',
		"unused": 'Это звание не используется в текущем режиме загадки.'
	}
};

function getSleuthRankExplanation(rank) {
	var strings = sleuthRankExplanations[getLanguage()] || sleuthRankExplanations.en;
	var limits = getCurrentRankLimits();
	var total = limits["barely-conscious"];
	var order = ["super-sleuth", "seasoned-pi", "amateur-gumshoe", "absent-minded"];
	var text;
	if (rank === "barely-conscious") {
		text = limits["absent-minded"] < total ? strings[rank] : strings["wrong-answer"];
		return text.replace("{limit}", limits["absent-minded"]).replace("{total}", total);
	}
	var index = order.indexOf(rank);
	var lower = index > 0 ? limits[order[index - 1]] + 1 : 1;
	var upper = limits[rank];
	if (index < 0 || lower > upper) return strings.unused;
	var range = index === 0 ? strings["up-to"].replace("{limit}", upper)
		: (lower === upper ? String(upper) : lower + "–" + upper);
	return strings["first-try"].replace("{range}", range).replace("{total}", total);
}

function updateSleuthRankExplanation(rank) {
	if (!rank) {
		var active = document.querySelector(".sleuth-rank-item.active-rank");
		if (!active) return;
		rank = active.getAttribute("data-rank");
	}
	document.getElementById("sleuth-rank-explanation").innerHTML = getSleuthRankExplanation(rank);
}

function alignSleuthMeter() {
	var items = document.getElementsByClassName("sleuth-rank-item");
	var first = items[0].getBoundingClientRect();
	var last = items[items.length - 1].getBoundingClientRect();
	var height = last.bottom - first.top;
	if (height <= 0) return; // section is hidden

	// Match the image height to the button list: the row centers both
	// columns vertically, so their tops and bottoms line up exactly.
	var img = document.getElementById("sleuth-o-meter-img");
	img.style.height = height + "px";
	img.style.width = "auto";
}

window.addEventListener("resize", alignSleuthMeter);
new MutationObserver(alignSleuthMeter)
	.observe(document.getElementById("sleuth-o-meter"), { attributes: true, attributeFilter: ["style"] });

function raiseSleuthMeter(item) {
	alignSleuthMeter();
	var mercury = document.getElementById("sleuth-o-meter-mercury");
	var items = document.getElementsByClassName("sleuth-rank-item");
	var first = items[0].getBoundingClientRect();
	var last = items[items.length - 1].getBoundingClientRect();
	var itemRect = item.getBoundingClientRect();
	var firstMiddle = first.top + first.height / 2;
	var lastMiddle = last.top + last.height / 2;
	var itemMiddle = itemRect.top + itemRect.height / 2;

	// Map the button position onto the scale: top button reaches the top
	// mark (2.5% of the image), bottom button stays at the mercury base (77%)
	var wrapper = mercury.parentElement.getBoundingClientRect();
	var scaleSpan = wrapper.height * (0.77 - 0.025);
	var fraction = (lastMiddle - itemMiddle) / (lastMiddle - firstMiddle);
	mercury.style.height = (fraction * scaleSpan) + "px";

	for (var i = 0; i < items.length; i++) {
		items[i].classList.remove("active-rank", "flash-rank");
	}
	item.classList.add("active-rank");
	// Restart the flash animation even when re-clicking the same item
	void item.offsetWidth;
	item.classList.add("flash-rank");

	updateSleuthRankExplanation(item.getAttribute("data-rank"));
}
