// Festival budget calculator. Festival prices come from window.FESTS (sourced data); everything else is user input.
(function () {
  var F = window.FESTS || [], $ = function (id) { return document.getElementById(id); };
  var sel = $('fest');
  F.forEach(function (f, i) { var o = document.createElement('option'); o.value = i; o.textContent = f.name + ' (£' + f.ticket + ')'; sel.appendChild(o); });
  function num(id) { var v = parseFloat($(id).value); return isNaN(v) || v < 0 ? 0 : v; }
  function gbp(v) { return '£' + v.toLocaleString('en-GB', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
  function load() {
    var f = F[+sel.value]; if (!f) return;
    $('ticket').value = f.ticket; $('days').value = f.days; $('parking').value = f.parking || 0;
    $('feenote').textContent = f.fees === 'included' ? 'This ticket price already includes the booking fee.' :
      f.fees === 'extra' ? 'The festival says booking fees are added on top. Enter them above if you know them.' :
      'The festival page does not say whether booking fees are included.';
    calc();
  }
  function calc() {
    var n = Math.max(1, Math.round(num('people'))), t = num('ticket'), fee = num('fee'), park = num('parking') / n,
        tr = num('travel'), food = num('food') * Math.max(1, num('days')), oth = num('other');
    var total = t + fee + park + tr + food + oth;
    $('total').textContent = gbp(total);
    var items = [['Ticket', t], ['Booking fee', fee], ['Parking share', park], ['Travel', tr], ['Food and drink', food], ['Other', oth]];
    $('breakdown').innerHTML = items.filter(function (x) { return x[1] > 0; }).map(function (x) { return '<li>' + x[0] + ': ' + gbp(x[1]) + '</li>'; }).join('');
  }
  sel.addEventListener('change', load);
  ['people', 'ticket', 'fee', 'parking', 'travel', 'food', 'days', 'other'].forEach(function (id) { $(id).addEventListener('input', calc); });
  load();
})();
