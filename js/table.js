// Sortable + filterable price table. No dependencies.
(function () {
  var table = document.getElementById('prices'); if (!table) return;
  var tbody = table.tBodies[0], buttons = table.querySelectorAll('thead button');
  var q = document.getElementById('q'), complete = document.getElementById('complete');
  function val(row, k) {
    var c = row.children[k], v = c.getAttribute('data-v');
    if (k === 0) return v.toLowerCase();
    return v === '' ? null : parseFloat(v);
  }
  buttons.forEach(function (b) {
    b.addEventListener('click', function () {
      var k = +b.dataset.k, dir = b.getAttribute('aria-sort') === 'ascending' ? 'descending' : 'ascending';
      buttons.forEach(function (o) { o.removeAttribute('aria-sort'); });
      b.setAttribute('aria-sort', dir);
      var rows = Array.prototype.slice.call(tbody.rows), m = dir === 'ascending' ? 1 : -1;
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
    var s = (q.value || '').trim().toLowerCase();
    Array.prototype.forEach.call(tbody.rows, function (r) {
      var text = r.children[0].textContent.toLowerCase();
      var ok = !s || text.indexOf(s) > -1;
      if (ok && complete.checked) ok = r.children[4].getAttribute('data-v') !== '';
      r.hidden = !ok;
    });
  }
  q.addEventListener('input', filter); complete.addEventListener('change', filter);
})();
