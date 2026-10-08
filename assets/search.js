/* Zoeken over de hele site: laadt bij eerste gebruik de index van de huidige taal (assets/search-xx.json). */
(function () {
  'use strict';
  var input = document.getElementById('q');
  var list = document.getElementById('q-res');
  var status = document.getElementById('q-st');
  if (!input || !list) return;
  var lang = (document.documentElement.lang || 'nl').slice(0, 2);
  var L = {
    nl: { none: 'Geen resultaten voor', n1: 'resultaat', nn: 'resultaten', more: 'Meer resultaten: verfijn je zoekopdracht',
      kinds: { act: 'Activiteit', place: 'Plaats', region: 'Regio', guide: 'Gids', event: 'Agenda', other: 'Pagina', home: 'Home', 'act-hub': 'Overzicht', 'place-hub': 'Overzicht', 'region-hub': 'Overzicht', 'guide-hub': 'Overzicht', 'event-hub': 'Overzicht' } },
    en: { none: 'No results for', n1: 'result', nn: 'results', more: 'More results: refine your search',
      kinds: { act: 'Activity', place: 'Place', region: 'Region', guide: 'Guide', event: 'Event', other: 'Page', home: 'Home', 'act-hub': 'Overview', 'place-hub': 'Overview', 'region-hub': 'Overview', 'guide-hub': 'Overview', 'event-hub': 'Overview' } },
    de: { none: 'Keine Ergebnisse für', n1: 'Ergebnis', nn: 'Ergebnisse', more: 'Weitere Ergebnisse: Suche verfeinern',
      kinds: { act: 'Aktivität', place: 'Ort', region: 'Region', guide: 'Ratgeber', event: 'Termin', other: 'Seite', home: 'Start', 'act-hub': 'Übersicht', 'place-hub': 'Übersicht', 'region-hub': 'Übersicht', 'guide-hub': 'Übersicht', 'event-hub': 'Übersicht' } }
  }[lang] || null;
  if (!L) L = { none: 'Geen resultaten voor', n1: 'resultaat', nn: 'resultaten', more: '', kinds: {} };
  var scriptSrc = (document.currentScript && document.currentScript.src) || '';
  var base = scriptSrc ? scriptSrc.replace(/search\.js.*$/, '') : '/assets/';
  var data = null, loading = false, active = -1, shown = [];

  function norm(s) {
    return (s || '').toLowerCase().replace(/ß/g, 'ss').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, ' ').trim();
  }
  function load(cb) {
    if (data) return cb();
    if (loading) return;
    loading = true;
    var x = new XMLHttpRequest();
    x.open('GET', base + 'search-' + (L.n1 ? lang : 'nl') + '.json');
    x.onload = function () {
      try {
        data = JSON.parse(x.responseText).map(function (r) {
          return { t: r[0], u: r[1], k: r[2], d: r[3], tn: norm(r[0]), dn: norm(r[3]), hn: norm(r[4]), xn: norm(r[5]) };
        });
      } catch (e) { data = []; }
      loading = false; cb();
    };
    x.onerror = function () { loading = false; data = []; cb(); };
    x.send();
  }
  function score(r, toks, phrase) {
    var s = 0;
    for (var i = 0; i < toks.length; i++) {
      var t = toks[i], hit = 0;
      if (r.tn.indexOf(t) === 0 || r.tn.indexOf(' ' + t) > -1) hit = 12;
      else if (r.tn.indexOf(t) > -1) hit = 8;
      else if (r.hn.indexOf(' ' + t) > -1 || r.hn.indexOf(t) === 0) hit = 5;
      else if (r.dn.indexOf(t) > -1) hit = 4;
      else if (r.hn.indexOf(t) > -1) hit = 3;
      else if (r.xn.indexOf(t) > -1) hit = 1;
      if (!hit) return 0;
      s += hit;
    }
    if (r.tn.indexOf(phrase) > -1) s += 15;
    if (r.tn.indexOf(phrase) === 0) s += 8;
    if (r.k === 'other' && s) s += 3;
    if (r.k === 'act' || r.k === 'place') s += 1;
    return s;
  }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function close() { list.hidden = true; input.setAttribute('aria-expanded', 'false'); input.removeAttribute('aria-activedescendant'); active = -1; }
  function render(q) {
    var phrase = norm(q), toks = phrase.split(' ').filter(Boolean);
    if (!toks.length) { close(); status.textContent = ''; return; }
    var res = [];
    for (var i = 0; i < data.length; i++) { var s = score(data[i], toks, phrase); if (s) res.push([s, data[i]]); }
    res.sort(function (a, b) { return b[0] - a[0] || a[1].t.localeCompare(b[1].t); });
    shown = res.slice(0, 8).map(function (x) { return x[1]; });
    var html = '';
    if (!shown.length) html = '<li class="q-none" role="presentation">' + L.none + ' “' + esc(q.trim()) + '”</li>';
    shown.forEach(function (r, i) {
      html += '<li role="option" id="q-o' + i + '"><a href="' + esc(r.u) + '"><span class="q-t">' + esc(r.t) + '</span><span class="q-k">' + esc(L.kinds[r.k] || '') + '</span>' +
        (r.d ? '<span class="q-d">' + esc(r.d.length > 110 ? r.d.slice(0, 107).replace(/\s+\S*$/, '') + '…' : r.d) + '</span>' : '') + '</a></li>';
    });
    if (res.length > 8) html += '<li class="q-more" role="presentation">' + L.more + ' (' + res.length + ')</li>';
    list.innerHTML = html; list.hidden = false; active = -1;
    input.setAttribute('aria-expanded', 'true'); input.removeAttribute('aria-activedescendant');
    status.textContent = res.length ? res.length + ' ' + (res.length === 1 ? L.n1 : L.nn) : L.none + ' ' + q.trim();
  }
  function move(d) {
    var items = list.querySelectorAll('[role=option]');
    if (!items.length) return;
    if (active > -1) items[active].classList.remove('q-on');
    active = (active + d + items.length) % items.length;
    items[active].classList.add('q-on');
    input.setAttribute('aria-activedescendant', items[active].id);
    items[active].scrollIntoView({ block: 'nearest' });
  }
  input.addEventListener('input', function () { load(function () { render(input.value); }); });
  input.addEventListener('focus', function () { load(function () { if (input.value.trim()) render(input.value); }); });
  input.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowDown') { e.preventDefault(); if (list.hidden) render(input.value); else move(1); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
    else if (e.key === 'Enter') {
      var a = list.querySelector('.q-on a') || (shown.length && !list.hidden ? list.querySelector('[role=option] a') : null);
      if (a) { e.preventDefault(); window.location.href = a.getAttribute('href'); }
    } else if (e.key === 'Escape') { if (!list.hidden) { close(); } else { input.value = ''; } }
  });
  document.addEventListener('click', function (e) { if (!e.target.closest || !e.target.closest('.searchbar')) close(); });
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && !/^(INPUT|TEXTAREA|SELECT)$/.test((document.activeElement || {}).tagName || '')) { e.preventDefault(); input.focus(); }
  });
})();
