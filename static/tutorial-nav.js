// Tutorial pagination
var tutorialCurrentPage = 1;
var tutorialPages = [
	{ id: 'tut-welcome',     title: { en: '🕵️ Welcome Detective!',             es: '🕵️ ¡Bienvenido Detective!',              ru: '🕵️ Добро пожаловать, детектив!' } },
	{ id: 'tut-timeline',    title: { en: '🕗 Using the Timeline Board',        es: '🕗 Usando el tablero de cronología',      ru: '🕗 Использование доски хронологии' } },
	{ id: 'tut-first-clue',  title: { en: '🔎 Your First Clue',                es: '🔎 Tu primera pista',                     ru: '🔎 Ваша первая подсказка' } },
	{ id: 'tut-deductions',  title: { en: '🧠 Making Deductions',               es: '🧠 Haciendo deducciones',                 ru: '🧠 Выводы и дедукция' } },
	{ id: 'tut-movement',    title: { en: '🚶 Movement Rules',                  es: '🚶 Reglas de movimiento',                 ru: '🚶 Правила передвижения' } },
	{ id: 'tut-backtrack',   title: { en: '↩️ Backtracking',                    es: '↩️ Retrocediendo',                        ru: '↩️ Обратный след' } },
	{ id: 'tut-indirect',    title: { en: '💬 Indirect Clues',                  es: '💬 Pistas indirectas',                    ru: '💬 Косвенные улики' } },
	{ id: 'tut-time-death',  title: { en: '⌛ Determining Time of Death',       es: '⌛ Determinando la hora de la muerte',    ru: '⌛ Время смерти' } },
	{ id: 'tut-weapon',      title: { en: '🔪 Finding the smoking gun',         es: '🔪 Encontrando el arma homicida',         ru: '🔪 Орудие преступления' } },
	{ id: 'tut-solved',      title: { en: '🎓 Solving your first case',         es: '🎓 Resolviendo tu primer caso',           ru: '🎓 Решаем первое дело' } },
	{ id: 'tut-weapons-id',  title: { en: '🔫 Better identification of weapons', es: '🔫 Mejor identificación de armas',       ru: '🔫 Идентификация оружия' } },
	{ id: 'tut-liars',       title: { en: '🤥 Dealing with liars',              es: '🤥 Lidiando con mentirosos',              ru: '🤥 Работа с лжецами' } }
];
var tutorialTotalPages = tutorialPages.length;

function showTutorialPage(pageNum) {
	if (pageNum < 1 || pageNum > tutorialTotalPages) return;

	tutorialCurrentPage = pageNum;

	// Hide all tutorial pages
	var allPages = document.querySelectorAll('.tutorial-page');
	for (var i = 0; i < allPages.length; i++) {
		allPages[i].style.display = 'none';
	}

	// Show target page
	var targetId = tutorialPages[pageNum - 1].id;
	var targetEl = document.getElementById(targetId);
	if (targetEl) {
		targetEl.style.display = 'block';
	}

	// Ensure canvases on this page are visible
	redrawTutorialCanvases(targetEl);

	// Update sidebar active state
	var sidebarItems = document.querySelectorAll('.tutorial-sidebar-item');
	for (var i = 0; i < sidebarItems.length; i++) {
		sidebarItems[i].classList.remove('active');
		if (sidebarItems[i].getAttribute('data-page') === targetId) {
			sidebarItems[i].classList.add('active');
		}
	}

	// Update mobile step dots
	var dots = document.querySelectorAll('.tutorial-step-dot');
	for (var i = 0; i < dots.length; i++) {
		dots[i].classList.remove('active');
		if (dots[i].getAttribute('data-page') === targetId) {
			dots[i].classList.add('active');
		}
	}

	// Update mobile title
	var mobileTitle = document.getElementById('tutorial-mobile-title');
	if (mobileTitle) {
		var lang = typeof getLanguage === 'function' ? getLanguage() : 'en';
		var titles = tutorialPages[pageNum - 1].title;
		mobileTitle.textContent = titles[lang] || titles['en'];
	}

	// Update page indicator
	var indicator = document.getElementById('tut-page-indicator');
	if (indicator) {
		indicator.textContent = pageNum + ' / ' + tutorialTotalPages;
	}

	// Update prev/next button states
	document.getElementById('tut-prev').disabled = (pageNum === 1);
	var nextBtn = document.getElementById('tut-next');
	var lang = typeof getLanguage === 'function' ? getLanguage() : 'en';
	var labelNext = {'en': 'Next', 'es': 'Siguiente', 'ru': 'Далее'}[lang] || 'Next';
	var labelBack = {'en': 'Back to the puzzle', 'es': 'Volver al misterio', 'ru': 'Вернуться к загадке'}[lang] || 'Back to the puzzle';
	if (pageNum === tutorialTotalPages) {
		nextBtn.innerHTML = labelBack + ' &rarr;';
		nextBtn.disabled = false;
	} else {
		nextBtn.innerHTML = labelNext + ' &rarr;';
		nextBtn.disabled = false;
	}

	// Scroll to top of tutorial
	var howToPlay = document.getElementById('how-to-play');
	if (howToPlay) {
		howToPlay.scrollIntoView({ behavior: 'smooth', block: 'start' });
	}
}

function redrawTutorialCanvases(pageEl) {
	if (!pageEl) return;
	var canvases = pageEl.querySelectorAll('canvas');
	for (var i = 0; i < canvases.length; i++) {
		canvases[i].style.display = 'inline';
	}
}

function tutorialNext() {
	if (tutorialCurrentPage === tutorialTotalPages) {
		showPage('home');
	} else {
		showTutorialPage(tutorialCurrentPage + 1);
	}
}

function tutorialPrev() {
	showTutorialPage(tutorialCurrentPage - 1);
}

function tutorialGoTo(pageId) {
	for (var j = 0; j < tutorialPages.length; j++) {
		if (tutorialPages[j].id === pageId) {
			showTutorialPage(j + 1);
			break;
		}
	}
}

function toggleTutorialSidebar() {
	var sidebar = document.getElementById('tutorial-sidebar');
	if (sidebar) {
		sidebar.classList.toggle('collapsed');
	}
}

// Attach click handlers
document.addEventListener('DOMContentLoaded', function () {
	var sidebarItems = document.querySelectorAll('.tutorial-sidebar-item');
	for (var i = 0; i < sidebarItems.length; i++) {
		sidebarItems[i].addEventListener('click', function () {
			tutorialGoTo(this.getAttribute('data-page'));
		});
	}

	var dots = document.querySelectorAll('.tutorial-step-dot');
	for (var i = 0; i < dots.length; i++) {
		dots[i].addEventListener('click', function () {
			tutorialGoTo(this.getAttribute('data-page'));
		});
	}
});
