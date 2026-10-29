// Away day cost calculator. Prefills from window.POF_CLUBS (built from data/clubs.json).
(function () {
  var D = window.POF_CLUBS || {}, $ = function (id) { return document.getElementById(id); };
  var club = $('club'), ids = ['ticket', 'pint', 'pints', 'pie', 'prog', 'rail'];
  function num(id) { var v = parseFloat($(id).value); return isNaN(v) || v < 0 ? 0 : v; }
  function gbp(v) { return '£' + v.toFixed(2); }
  function fill() {
    var c = D[club.value]; var miss = [];
    if (c) {
      $('ticket').value = c.away_ticket != null ? c.away_ticket : 30;
      [['pint', 'pint'], ['pie', 'pie'], ['prog', 'programme']].forEach(function (p) {
        var v = c[p[1]]; $(p[0]).value = v != null ? v.toFixed(2) : '';
        if (v == null) miss.push(p[1]);
      });
      $('missing').textContent = miss.length ? 'No reliable ' + miss.join(' or ') + ' price for ' + c.ground + ' yet — type your own if you know it.' : '';
      history.replaceState(null, '', '?club=' + club.value);
    }
    calc();
  }
  function calc() {
    var t = num('ticket'), pint = num('pint') * num('pints'), pie = num('pie'), prog = num('prog'), rail = num('rail');
    var total = t + pint + pie + prog + rail;
    $('total').textContent = gbp(total);
    var items = [['Away ticket', t], ['Pints (' + num('pints') + ')', pint], ['Pie', pie], ['Programme', prog]];
    if (rail) items.push(['Rail fare', rail]);
    $('breakdown').innerHTML = items.map(function (i) { return '<li>' + i[0] + ': ' + gbp(i[1]) + '</li>'; }).join('');
  }
  club.addEventListener('change', fill);
  ids.forEach(function (id) { $(id).addEventListener('input', calc); });
  var m = location.search.match(/club=([a-z-]+)/);
  if (m && D[m[1]]) { club.value = m[1]; fill(); } else calc();
})();
