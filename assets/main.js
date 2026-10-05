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

  // Fotogalerij met lightbox
  var items = Array.prototype.slice.call(document.querySelectorAll('.g-item'));
  var lb = document.querySelector('.lightbox');
  if (items.length && lb && lb.showModal) {
    var lbImg = lb.querySelector('img');
    var lbCap = lb.querySelector('figcaption');
    var cur = 0;
    var open = function (i) {
      cur = (i + items.length) % items.length;
      var im = items[cur].querySelector('img');
      lbImg.src = items[cur].href;
      lbImg.alt = im.alt;
      lbCap.textContent = im.alt;
    };
    items.forEach(function (a, i) {
      a.addEventListener('click', function (e) { e.preventDefault(); open(i); lb.showModal(); });
    });
    lb.querySelector('.lb-close').addEventListener('click', function () { lb.close(); });
    lb.querySelector('.lb-prev').addEventListener('click', function () { open(cur - 1); });
    lb.querySelector('.lb-next').addEventListener('click', function () { open(cur + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) lb.close(); });
    lb.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') open(cur - 1);
      if (e.key === 'ArrowRight') open(cur + 1);
    });
  }
})();
