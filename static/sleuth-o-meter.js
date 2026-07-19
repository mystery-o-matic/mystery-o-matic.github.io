var sleuthRankExplanations = {
	"en": {
		"super-sleuth": 'Accuse the right suspect on your <span class="sleuth-highlight">first try</span>, revealing <span class="sleuth-highlight">at most 65%</span> of the clues.',
		"seasoned-pi": 'Accuse the right suspect on your <span class="sleuth-highlight">first try</span>, revealing <span class="sleuth-highlight">at most 75%</span> of the clues.',
		"amateur-gumshoe": 'Accuse the right suspect on your <span class="sleuth-highlight">first try</span>, revealing <span class="sleuth-highlight">at most 85%</span> of the clues.',
		"absent-minded": 'Accuse the right suspect on your <span class="sleuth-highlight">first try</span>, revealing <span class="sleuth-highlight">at most 95%</span> of the clues.',
		"barely-conscious": 'You revealed <span class="sleuth-highlight">almost every clue</span>, or got the <span class="sleuth-highlight">suspect, weapon or time</span> wrong once.'
	},
	"es": {
		"super-sleuth": 'Acusa al sospechoso correcto en tu <span class="sleuth-highlight">primer intento</span>, revelando <span class="sleuth-highlight">como máximo el 65%</span> de las pistas.',
		"seasoned-pi": 'Acusa al sospechoso correcto en tu <span class="sleuth-highlight">primer intento</span>, revelando <span class="sleuth-highlight">como máximo el 75%</span> de las pistas.',
		"amateur-gumshoe": 'Acusa al sospechoso correcto en tu <span class="sleuth-highlight">primer intento</span>, revelando <span class="sleuth-highlight">como máximo el 85%</span> de las pistas.',
		"absent-minded": 'Acusa al sospechoso correcto en tu <span class="sleuth-highlight">primer intento</span>, revelando <span class="sleuth-highlight">como máximo el 95%</span> de las pistas.',
		"barely-conscious": 'Revelaste <span class="sleuth-highlight">casi todas las pistas</span>, o fallaste <span class="sleuth-highlight">sospechoso, arma u hora</span> alguna vez.'
	},
	"ru": {
		"super-sleuth": 'Обвините нужного подозреваемого с <span class="sleuth-highlight">первой попытки</span>, раскрыв <span class="sleuth-highlight">не более 65%</span> подсказок.',
		"seasoned-pi": 'Обвините нужного подозреваемого с <span class="sleuth-highlight">первой попытки</span>, раскрыв <span class="sleuth-highlight">не более 75%</span> подсказок.',
		"amateur-gumshoe": 'Обвините нужного подозреваемого с <span class="sleuth-highlight">первой попытки</span>, раскрыв <span class="sleuth-highlight">не более 85%</span> подсказок.',
		"absent-minded": 'Обвините нужного подозреваемого с <span class="sleuth-highlight">первой попытки</span>, раскрыв <span class="sleuth-highlight">не более 95%</span> подсказок.',
		"barely-conscious": 'Вы раскрыли <span class="sleuth-highlight">почти все подсказки</span> или ошиблись в <span class="sleuth-highlight">подозреваемом, оружии или времени</span>.'
	}
};

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

	var explanations = sleuthRankExplanations[getLanguage()] || sleuthRankExplanations["en"];
	var explanation = document.getElementById("sleuth-rank-explanation");
	explanation.innerHTML = explanations[item.getAttribute("data-rank")];
}
