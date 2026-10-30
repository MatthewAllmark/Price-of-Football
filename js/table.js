// Sortable + filterable price table. No dependencies.
(function () {
  var table = document.getElementById('prices'); if (!table) return;
  var tbody = table.tBodies[0], buttons = table.querySelectorAll('thead button');
  var q = document.getElementById('q'), complete = document.getElementById('complete'), league = document.getElementById('league');
  var count = document.getElementById('count'), empty = document.getElementById('empty');
  var rowsAll = Array.prototype.slice.call(tbody.rows);
  function val(row, k) {
    var c = row.children[k], v = c.getAttribute('data-v');
    if (k === 0) return (v || '').toLowerCase();
    return v === '' || v === null ? null : parseFloat(v);
  }
  buttons.forEach(function (b) {
    b.addEventListener('click', function () {
      var k = +b.dataset.k, dir = b.getAttribute('aria-sort') === 'ascending' ? 'descending' : 'ascending';
      buttons.forEach(function (o) { o.removeAttribute('aria-sort'); o.parentNode.removeAttribute('aria-sort'); });
      b.setAttribute('aria-sort', dir); b.parentNode.setAttribute('aria-sort', dir);
      var rows = rowsAll.slice(), m = dir === 'ascending' ? 1 : -1;
      rows.sort(function (a, c) {
        var x = val(a, k), y = val(c, k);
        if (x === null && y === null) return 0;
        if (x === null) return 1; if (y === null) return -1;   // blanks always last, whichever direction
        return (x < y ? -1 : x > y ? 1 : 0) * m;
      });
      rows.forEach(function (r) { tbody.appendChild(r); });
    });
  });
  function filter() {
    var s = (q.value || '').trim().toLowerCase(), lg = league ? league.value : '', shown = 0;
    rowsAll.forEach(function (r) {
      var ok = !s || r.getAttribute('data-name').indexOf(s) > -1 || (r.getAttribute('data-ground') || '').indexOf(s) > -1;
      if (ok && lg) ok = r.getAttribute('data-league') === lg;
      // "matchday prices" = a cheapest or a dearest matchday figure (columns 4 and 5)
      if (ok && complete.checked) ok = r.children[4].getAttribute('data-v') !== '' || r.children[5].getAttribute('data-v') !== '';
      r.hidden = !ok; if (ok) shown++;
    });
    if (count) count.textContent = shown === rowsAll.length ? 'Showing all ' + shown + ' clubs' : 'Showing ' + shown + ' of ' + rowsAll.length + ' clubs';
    if (empty) empty.hidden = shown !== 0;
  }
  q.addEventListener('input', filter); complete.addEventListener('change', filter);
  if (league) {
    league.addEventListener('change', function () {
      var p = new URLSearchParams(location.search);
      if (league.value) p.set('league', league.value); else p.delete('league');
      var qs = p.toString();
      history.replaceState(null, '', location.pathname + (qs ? '?' + qs : '') + (league.value ? '#t-h' : ''));
      filter();
    });
    var want = new URLSearchParams(location.search).get('league');
    if (want && league.querySelector('option[value="' + want.replace(/[^a-z-]/g, '') + '"]')) league.value = want;
  }
  var reset = document.getElementById('reset');
  if (reset) reset.addEventListener('click', function () {
    q.value = ''; complete.checked = false;
    if (league) { league.value = ''; history.replaceState(null, '', location.pathname); }
    filter();
  });
  filter();   // also applies any values the browser restored on back/forward
})();
