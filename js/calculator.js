// Away day cost calculator. Prefills from window.POF_CLUBS (built from data/clubs.json)
// and shows a short away-day box from window.POF_AWAY (built from data/away_guide.json).
(function () {
  var D = window.POF_CLUBS || {}, A = window.POF_AWAY || {}, $ = function (id) { return document.getElementById(id); };
  function esc(t) { return String(t == null ? '' : t).replace(/[&<>"']/g, function (ch) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]; }); }
  // "Your away day at X" box: away end, nearest station + walk, top 3 pubs, link to the club page.
  function awayBox(slug) {
    var box = $('awaybox'); if (!box) return;
    var c = D[slug], a = A[slug];
    if (!c || !a) { box.hidden = true; box.innerHTML = ''; return; }
    var h = '<h2>Your away day at ' + esc(c.ground) + '</h2><dl class="away-facts">';
    if (a.stand) h += '<div><dt>Away end</dt><dd>' + esc(a.stand) + '</dd></div>';
    if (a.station) h += '<div><dt>Nearest station</dt><dd>' + esc(a.station.name) + (a.station.walk ? ' — ' + esc(a.station.walk) : '') + '</dd></div>';
    h += '</dl>';
    if (a.pubs && a.pubs.length) {
      h += '<p class="away-pubs-h">Away-friendly pubs</p><ul>' + a.pubs.map(function (p) {
        return '<li>' + (p.maps ? '<a href="' + esc(p.maps) + '" target="_blank" rel="noopener">' + esc(p.name) + '</a>' : esc(p.name)) + '</li>';
      }).join('') + '</ul>';
    }
    h += '<p class="small">Pub policies change, so check before you travel. Colours rules may apply.</p>';
    h += '<p><a class="btn" href="clubs/' + encodeURIComponent(slug) + '.html#away-guide">Full away day guide for ' + esc(c.name) + ' →</a></p>';
    box.innerHTML = h; box.hidden = false;
  }
  var club = $('club'), ids = ['ticket', 'pint', 'pints', 'pie', 'prog', 'rail'];
  function num(id) { var v = parseFloat($(id).value); return isNaN(v) || v < 0 ? 0 : v; }
  function gbp(v) { return '£' + v.toFixed(2); }
  function fill() {
    var c = D[club.value], miss = [];
    if (!c) {
      // "Choose a club…" selected: clear the prefilled prices and the URL, keep the user's rail fare and pint count.
      ['ticket', 'pint', 'pie', 'prog'].forEach(function (id) { $(id).value = ''; });
      $('missing').textContent = '';
      history.replaceState(null, '', location.pathname);
      awayBox(''); calc(); return;
    }
    // £30 cap applies to Premier League grounds only; elsewhere use the home club's away price or leave blank.
    var a = c.away_ticket != null ? c.away_ticket : (c.pl ? 30 : null);
    $('ticket').value = a != null ? a.toFixed(2) : '';
    if (a == null) miss.push('away ticket');
    [['pint', 'pint'], ['pie', 'pie'], ['prog', 'programme']].forEach(function (p) {
      var v = c[p[1]]; $(p[0]).value = v != null ? v.toFixed(2) : '';
      if (v == null) miss.push(p[1]);
    });
    var list = miss.length > 1 ? miss.slice(0, -1).join(', ') + ' or ' + miss[miss.length - 1] : miss[0];
    $('missing').textContent = miss.length ? 'No reliable ' + list + ' price for ' + c.ground + ' yet — we leave it blank rather than guess. Type your own if you know it.' : '';
    history.replaceState(null, '', '?club=' + encodeURIComponent(club.value));
    awayBox(club.value);
    calc();
  }
  function calc() {
    var n = num('pints'), t = num('ticket'), pint = num('pint') * n, pie = num('pie'), prog = num('prog'), rail = num('rail');
    $('total').textContent = gbp(t + pint + pie + prog + rail);
    var items = [['Away ticket', t], ['Pints (' + n + ')', pint], ['Pie', pie], ['Programme', prog]];
    if (rail) items.push(['Rail fare', rail]);
    $('breakdown').innerHTML = items.map(function (i) { return '<li>' + i[0] + ': ' + gbp(i[1]) + '</li>'; }).join('');
  }
  club.addEventListener('change', fill);
  ids.forEach(function (id) { $(id).addEventListener('input', calc); });
  var want = new URLSearchParams(location.search).get('club');
  if (want && D[want]) { club.value = want; fill(); }
  else if (club.value && D[club.value]) fill();   // value restored by the browser on back/forward
  else calc();
})();
