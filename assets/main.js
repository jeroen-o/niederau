// Niederau.nl — kleine interacties, geen externe afhankelijkheden
(function () {
  // Mobiel menu
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a[href^="#"]')) {
        nav.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // Zomer/winter-tabs in de sectie Seizoenen
  var tabs = document.querySelectorAll('.season-switch [role="tab"]');
  function show(id) {
    tabs.forEach(function (t) {
      var on = t.getAttribute('aria-controls') === id;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
  }
  if (tabs.length) {
    tabs.forEach(function (t) {
      t.addEventListener('click', function () { show(t.getAttribute('aria-controls')); });
    });
  }

  // Seizoen staat al op <html data-season> (inline script in de head).
  var root = document.documentElement;
  function applySeason(season) {
    root.setAttribute('data-season', season);
    if (tabs.length) show(season === 'winter' ? 'p-winter' : 'p-summer');
  }
  applySeason(root.getAttribute('data-season') || 'summer');

  var toggle = document.querySelector('.season-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      applySeason(root.getAttribute('data-season') === 'winter' ? 'summer' : 'winter');
    });
  }

  // Jaartal in de footer
  var now = new Date().getFullYear();
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = now; });
})();
