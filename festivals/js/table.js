// Sortable + filterable festival table. No dependencies.
(function () {
  var table = document.getElementById('prices'); if (!table) return;
  var tbody = table.tBodies[0], buttons = table.querySelectorAll('thead button');
  var $ = function (id) { return document.getElementById(id); };
  var q = $('q'), nation = $('nation'), region = $('region'), month = $('month'), camp = $('camp'), onsale = $('onsale'), priced = $('priced');
  var count = $('count'), empty = $('empty'), rowsAll = Array.prototype.slice.call(tbody.rows);
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
        if (x === null) return 1; if (y === null) return -1;   // blanks always last
        return (x < y ? -1 : x > y ? 1 : 0) * m;
      });
      rows.forEach(function (r) { tbody.appendChild(r); });
    });
  });
  function filter() {
    var s = (q.value || '').trim().toLowerCase(), shown = 0;
    rowsAll.forEach(function (r) {
      var ok = !s || r.getAttribute('data-name').indexOf(s) > -1;
      if (ok && nation.value) ok = r.getAttribute('data-nation') === nation.value;
      if (ok && region.value) ok = r.getAttribute('data-region') === region.value;
      if (ok && month.value) ok = r.getAttribute('data-month') === month.value;
      if (ok && camp.value) ok = r.getAttribute('data-camp') === camp.value;
      if (ok && onsale.checked) ok = r.getAttribute('data-status') === 'on_sale';
      if (ok && priced.checked) ok = r.children[4].getAttribute('data-v') !== '';
      r.hidden = !ok; if (ok) shown++;
    });
    count.textContent = shown === rowsAll.length ? 'Showing all ' + shown + ' festivals' : 'Showing ' + shown + ' of ' + rowsAll.length + ' festivals';
    empty.hidden = shown !== 0;
  }
  [q].forEach(function (el) { el.addEventListener('input', filter); });
  [nation, region, month, camp, onsale, priced].forEach(function (el) { el.addEventListener('change', filter); });
  $('reset').addEventListener('click', function () { q.value = ''; nation.value = ''; region.value = ''; month.value = ''; camp.value = ''; onsale.checked = false; priced.checked = false; filter(); });
  filter();
})();
