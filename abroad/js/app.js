/* Matchday Abroad: filters, map and "near me" for the fixture list. No tracking, no third-party scripts. */
(function () {
  var list = document.getElementById('fx-list');
  if (!list) return;
  var cards = Array.prototype.slice.call(list.querySelectorAll('.fx'));
  var fCountry = document.getElementById('f-country'), fText = document.getElementById('f-text'),
      fFrom = document.getElementById('f-from'), fTo = document.getElementById('f-to'),
      fSort = document.getElementById('f-sort'), count = document.getElementById('fx-count'),
      empty = document.getElementById('fx-empty'), nearBtn = document.getElementById('near-me'),
      nearMsg = document.getElementById('near-msg'), resetBtn = document.getElementById('f-reset');
  var me = null;
  function km(a, b, c, d) {
    var R = 6371, r = Math.PI / 180, x = Math.sin((c - a) * r / 2), y = Math.sin((d - b) * r / 2);
    var h = x * x + Math.cos(a * r) * Math.cos(c * r) * y * y; return 2 * R * Math.asin(Math.sqrt(h));
  }
  function apply() {
    var c = fCountry.value, t = (fText.value || '').trim().toLowerCase(), a = fFrom.value, b = fTo.value, shown = 0;
    cards.forEach(function (el) {
      var ok = (!c || el.dataset.country === c) && (!t || el.dataset.text.indexOf(t) !== -1) &&
               (!a || el.dataset.date >= a) && (!b || el.dataset.date <= b);
      el.hidden = !ok; if (ok) shown++;
    });
    var s = fSort.value;
    var sorted = cards.slice().sort(function (x, y) {
      if (s === 'date') return x.dataset.date < y.dataset.date ? -1 : x.dataset.date > y.dataset.date ? 1 : (+y.dataset.score - +x.dataset.score);
      if (s === 'distance' && me) return (+x.dataset.km || 1e9) - (+y.dataset.km || 1e9);
      return (+y.dataset.score - +x.dataset.score) || (x.dataset.date < y.dataset.date ? -1 : 1);
    });
    sorted.forEach(function (el) { list.appendChild(el); });
    count.textContent = shown + ' of ' + cards.length + ' fixtures shown';
    empty.hidden = shown !== 0;
    if (window._fxMarkers) window._fxMarkers(c);
  }
  [fCountry, fText, fFrom, fTo, fSort].forEach(function (el) { el.addEventListener('input', apply); el.addEventListener('change', apply); });
  resetBtn.addEventListener('click', function () { fCountry.value = ''; fText.value = ''; fFrom.value = fFrom.min; fTo.value = fTo.max; fSort.value = 'score'; apply(); });
  nearBtn.addEventListener('click', function () {
    if (!navigator.geolocation) { nearMsg.textContent = 'Your browser does not support location.'; return; }
    nearMsg.textContent = 'Finding your location… (it stays in your browser and is never sent to us)';
    navigator.geolocation.getCurrentPosition(function (p) {
      me = [p.coords.latitude, p.coords.longitude];
      cards.forEach(function (el) {
        if (!el.dataset.lat) { el.dataset.km = ''; return; }
        var d = km(me[0], me[1], +el.dataset.lat, +el.dataset.lon); el.dataset.km = d.toFixed(1);
        var s = el.querySelector('.dist'); if (s) s.textContent = Math.round(d) + ' km from you · ';
      });
      var opt = fSort.querySelector('option[value=distance]'); opt.disabled = false; fSort.value = 'distance';
      nearMsg.textContent = 'Sorted by straight-line distance from you. Stadiums without published coordinates go last.';
      apply();
      if (window._fxMap) window._fxMap.setView(me, 8);
    }, function () { nearMsg.textContent = 'Location unavailable or permission denied. Use the filters instead.'; }, { timeout: 10000 });
  });
  // Map
  var mapEl = document.getElementById('map');
  if (mapEl && window.L) {
    var map = L.map(mapEl, { scrollWheelZoom: false }).setView([45, 8], 4);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' }).addTo(map);
    var groups = {};
    cards.forEach(function (el) {
      if (!el.dataset.lat) return;
      var k = el.dataset.home; if (!groups[k]) groups[k] = { lat: +el.dataset.lat, lon: +el.dataset.lon, country: el.dataset.country, name: el.dataset.homename, stadium: el.dataset.stadium, url: el.dataset.homeurl, items: [] };
      groups[k].items.push({ t: el.dataset.title, d: el.dataset.datelabel, s: el.dataset.score });
    });
    var markers = [];
    Object.keys(groups).forEach(function (k) {
      var g = groups[k]; var items = g.items.slice(0, 4).map(function (i) { return '<li>' + i.d + ': ' + i.t + ' <b>' + i.s + '</b></li>'; }).join('');
      var m = L.marker([g.lat, g.lon], { title: g.name }).bindPopup('<strong><a href="' + g.url + '">' + g.name + '</a></strong><br>' + g.stadium + '<ul style="padding-left:16px;margin:6px 0">' + items + '</ul>');
      m._country = g.country; m.addTo(map); markers.push(m);
    });
    window._fxMap = map;
    window._fxMarkers = function (c) { markers.forEach(function (m) { if (!c || m._country === c) { if (!map.hasLayer(m)) m.addTo(map); } else if (map.hasLayer(m)) map.removeLayer(m); }); };
    mapEl.setAttribute('data-ready', String(markers.length));
  }
  apply();
})();
