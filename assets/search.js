/* Zoeken over de hele site: laadt bij eerste gebruik de index van de huidige taal (assets/search-xx.json). */
(function () {
  'use strict';
  var input = document.getElementById('q');
  var list = document.getElementById('q-res');
  var pop = list && list.parentNode;
  var chips = pop && pop.querySelector('.q-f');
  var filter = 'all', lastQ = '';
  var status = document.getElementById('q-st');
  if (!input || !list) return;
  var lang = (document.documentElement.lang || 'nl').slice(0, 2);
  var L = {
    nl: { all: 'Alles', none: 'Geen resultaten voor', n1: 'resultaat', nn: 'resultaten', more: 'Meer resultaten: verfijn je zoekopdracht',
      kinds: { act: 'Activiteit', place: 'Plaats', region: 'Regio', guide: 'Gids', event: 'Agenda', other: 'Pagina', home: 'Home', 'act-hub': 'Overzicht', 'place-hub': 'Overzicht', 'region-hub': 'Overzicht', 'guide-hub': 'Overzicht', 'event-hub': 'Overzicht' } },
    en: { all: 'All', none: 'No results for', n1: 'result', nn: 'results', more: 'More results: refine your search',
      kinds: { act: 'Activity', place: 'Place', region: 'Region', guide: 'Guide', event: 'Event', other: 'Page', home: 'Home', 'act-hub': 'Overview', 'place-hub': 'Overview', 'region-hub': 'Overview', 'guide-hub': 'Overview', 'event-hub': 'Overview' } },
    de: { all: 'Alle', none: 'Keine Ergebnisse für', n1: 'Ergebnis', nn: 'Ergebnisse', more: 'Weitere Ergebnisse: Suche verfeinern',
      kinds: { act: 'Aktivität', place: 'Ort', region: 'Region', guide: 'Ratgeber', event: 'Termin', other: 'Seite', home: 'Start', 'act-hub': 'Übersicht', 'place-hub': 'Übersicht', 'region-hub': 'Übersicht', 'guide-hub': 'Übersicht', 'event-hub': 'Übersicht' } }
  }[lang] || null;
  if (!L) L = { all: 'Alles', none: 'Geen resultaten voor', n1: 'resultaat', nn: 'resultaten', more: '', kinds: {} };
  var scriptSrc = (document.currentScript && document.currentScript.src) || '';
  var base = scriptSrc ? scriptSrc.replace(/search\.js.*$/, '') : '/assets/';
  var data = null, loading = false, active = -1, shown = [];

  function norm(s) {
    return (s || '').toLowerCase().replace(/ß/g, 'ss').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, ' ').trim();
  }

  var SYN = {
    nl: { rodelen: ['rodelbaan', 'sleeen'], rodel: ['rodelbaan', 'sleeen'], sleeen: ['rodelbaan', 'rodelen'], skien: ['ski', 'skipiste', 'pistes'], skiën: ['ski', 'skipiste', 'pistes'], wandelen: ['wandelroute', 'wandeltocht', 'hike'], zwemmen: ['zwembad', 'openluchtbad', 'bad'], zwembad: ['zwemmen', 'openluchtbad'], fietsen: ['e-bike', 'mountainbike', 'fietsroute'], kinderen: ['gezin', 'familie', 'kids'], regen: ['regendag', 'binnen'], eten: ['restaurant', 'hut', 'alm'], restaurant: ['eten', 'hut', 'alm'], golfen: ['golfbaan', 'golfclub'], hotel: ['verblijf', 'wastlhof'], slapen: ['verblijf', 'hotel'], sneeuw: ['winter', 'ski'], paardrijden: ['paard', 'manege'], vissen: ['forel', 'hengelen'] },
    en: { sledding: ['toboggan', 'rodel', 'sled'], tobogganing: ['rodel', 'toboggan'], skiing: ['ski', 'slopes', 'pistes'], hiking: ['walking', 'hike', 'trail'], walking: ['hiking', 'hike'], swimming: ['pool', 'swim', 'lido'], pool: ['swimming', 'swim'], cycling: ['bike', 'e-bike', 'cycle'], biking: ['mountain bike', 'e-bike', 'cycling'], kids: ['children', 'family'], children: ['family', 'kids'], rain: ['rainy', 'indoors'], food: ['restaurant', 'hut', 'alm'], eating: ['restaurant', 'hut'], restaurant: ['food', 'hut', 'alm'], golfing: ['golf course', 'golf club'], hotel: ['stay', 'wastlhof'], snow: ['winter', 'ski'], fishing: ['trout', 'fish'], horse: ['riding', 'stables'] },
    de: { rodeln: ['rodelbahn', 'schlitten'], rodel: ['rodelbahn', 'rodeln'], schlitten: ['rodelbahn', 'rodeln'], skifahren: ['ski', 'piste', 'pisten'], wandern: ['wanderweg', 'wanderung', 'hike'], schwimmen: ['schwimmbad', 'freibad', 'bad'], schwimmbad: ['schwimmen', 'freibad'], radfahren: ['fahrrad', 'e-bike', 'mountainbike'], kinder: ['familie', 'kids'], regen: ['regentag', 'drinnen'], essen: ['restaurant', 'hutte', 'alm'], restaurant: ['essen', 'huette', 'alm'], golfen: ['golfplatz', 'golfclub'], hotel: ['unterkunft', 'wastlhof'], schnee: ['winter', 'ski'], angeln: ['forelle', 'fischen'], reiten: ['pferd', 'reitstall'] }
  };
  var SYNL = {};
  Object.keys((SYN[lang] || SYN.nl)).forEach(function (k) { SYNL[norm(k)] = SYN[lang] ? SYN[lang][k] : SYN.nl[k]; });
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
  function tokHit(r, t) {
    if (r.tn.indexOf(t) === 0 || r.tn.indexOf(' ' + t) > -1) return 12;
    if (r.tn.indexOf(t) > -1) return 8;
    if (r.hn.indexOf(' ' + t) > -1 || r.hn.indexOf(t) === 0) return 5;
    if (r.dn.indexOf(t) > -1) return 4;
    if (r.hn.indexOf(t) > -1) return 3;
    if (r.xn.indexOf(t) > -1) return 1;
    return 0;
  }
  function score(r, toks, phrase) {
    var s = 0;
    for (var i = 0; i < toks.length; i++) {
      var hit = tokHit(r, toks[i]);
      var alts = SYNL[toks[i]];
      if (alts) for (var a = 0; a < alts.length; a++) { var h2 = Math.floor(tokHit(r, norm(alts[a])) * 0.8); if (h2 > hit) hit = h2; }
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
  function close() { pop.hidden = true; input.setAttribute('aria-expanded', 'false'); input.removeAttribute('aria-activedescendant'); active = -1; }
  var GROUPS = ['all', 'act', 'place', 'guide', 'event', 'other'];
  function groupOf(k) { return k.replace('-hub', '') === 'region' ? 'place' : (k === 'home' ? 'other' : k.replace('-hub', '')); }
  function render(q) {
    lastQ = q;
    var phrase = norm(q), toks = phrase.split(' ').filter(Boolean);
    if (!toks.length) { close(); status.textContent = ''; return; }
    var res = [];
    for (var i = 0; i < data.length; i++) { var s = score(data[i], toks, phrase); if (s) res.push([s, data[i]]); }
    res.sort(function (a, b) { return b[0] - a[0] || a[1].t.localeCompare(b[1].t); });
    var counts = { all: res.length };
    res.forEach(function (x) { var g = groupOf(x[1].k); counts[g] = (counts[g] || 0) + 1; });
    if (filter !== 'all' && !counts[filter]) filter = 'all';
    var vis = filter === 'all' ? res : res.filter(function (x) { return groupOf(x[1].k) === filter; });
    shown = vis.slice(0, 8).map(function (x) { return x[1]; });
    var chtml = '';
    GROUPS.forEach(function (g) {
      if (g !== 'all' && !counts[g]) return;
      var label = g === 'all' ? L.all : (L.kinds[g] || g);
      chtml += '<button type="button" class="q-chip' + (g === filter ? ' q-chip-on' : '') + '" data-g="' + g + '" aria-pressed="' + (g === filter) + '">' + esc(label) + ' <span>' + (counts[g] || 0) + '</span></button>';
    });
    chips.innerHTML = res.length ? chtml : '';
    var html = '';
    if (!shown.length) html = '<li class="q-none" role="presentation">' + L.none + ' “' + esc(q.trim()) + '”</li>';
    shown.forEach(function (r, i) {
      html += '<li role="option" id="q-o' + i + '"><a href="' + esc(r.u) + '"><span class="q-t">' + esc(r.t) + '</span><span class="q-k">' + esc(L.kinds[r.k] || '') + '</span>' +
        (r.d ? '<span class="q-d">' + esc(r.d.length > 110 ? r.d.slice(0, 107).replace(/\s+\S*$/, '') + '…' : r.d) + '</span>' : '') + '</a></li>';
    });
    if (vis.length > 8) html += '<li class="q-more" role="presentation">' + L.more + ' (' + vis.length + ')</li>';
    list.innerHTML = html; pop.hidden = false; active = -1;
    input.setAttribute('aria-expanded', 'true'); input.removeAttribute('aria-activedescendant');
    status.textContent = res.length ? res.length + ' ' + (res.length === 1 ? L.n1 : L.nn) : L.none + ' ' + q.trim();
  }
  if (chips) chips.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('.q-chip');
    if (!b) return;
    filter = b.getAttribute('data-g'); render(lastQ || input.value);
    var again = chips.querySelector('[data-g="' + filter + '"]'); if (again) again.focus();
  });
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
    if (e.key === 'ArrowDown') { e.preventDefault(); if (pop.hidden) render(input.value); else move(1); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
    else if (e.key === 'Enter') {
      var a = list.querySelector('.q-on a') || (shown.length && !pop.hidden ? list.querySelector('[role=option] a') : null);
      if (a) { e.preventDefault(); window.location.href = a.getAttribute('href'); }
    } else if (e.key === 'Escape') { if (!pop.hidden) { close(); } else { input.value = ''; } }
  });
  var sbtn = document.querySelector('.search-btn');
  if (sbtn) sbtn.addEventListener('click', function () {
    var mb = document.querySelector('.menu-btn');
    if (mb && mb.getAttribute('aria-expanded') === 'true') mb.click();
    window.scrollTo({ top: 0, behavior: 'smooth' });
    input.focus({ preventScroll: true });
    input.select();
  });
  var barEl = input.closest('.searchbar');
  document.addEventListener('click', function (e) {
    var path = e.composedPath ? e.composedPath() : [];
    if (path.indexOf(barEl) === -1 && !(e.target.closest && e.target.closest('.searchbar'))) close();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && !/^(INPUT|TEXTAREA|SELECT)$/.test((document.activeElement || {}).tagName || '')) { e.preventDefault(); input.focus(); }
  });
})();
