/* Our own slide runner. Keys: arrows / space / page keys to move, N notes, F fullscreen, Home / End.
   Elements with data-step="1", "2", ... appear one by one before the next slide. The address #7 opens slide 7. */
(function () {
  var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
  var stage = document.getElementById('stage');
  var notes = document.getElementById('notes');
  var i = 0, s = 0;

  function fit() {
    stage.style.transform = 'scale(' + Math.min(window.innerWidth / 1280, window.innerHeight / 720) + ')';
  }
  function maxStep(sl) {
    var m = 0;
    sl.querySelectorAll('[data-step]').forEach(function (e) { m = Math.max(m, +e.getAttribute('data-step')); });
    return m;
  }
  function render() {
    slides.forEach(function (sl, k) { sl.classList.toggle('on', k === i); });
    slides[i].querySelectorAll('[data-step]').forEach(function (e) {
      e.classList.toggle('on', +e.getAttribute('data-step') <= s);
    });
    document.getElementById('bar').style.width = ((i + 1) / slides.length * 100) + '%';
    document.getElementById('count').textContent = (i + 1) + ' / ' + slides.length;
    var a = slides[i].querySelector('aside');
    notes.textContent = a ? a.textContent.replace(/\n\s+/g, '\n').trim() : '';
    try { history.replaceState(null, '', '#' + (i + 1)); } catch (e) { /* file:// in some browsers */ }
  }
  function next() {
    document.getElementById('help').classList.add('off');
    if (s < maxStep(slides[i])) { s++; }
    else if (i < slides.length - 1) { i++; s = 0; }
    render();
  }
  function prev() {
    if (s > 0) { s--; }
    else if (i > 0) { i--; s = maxStep(slides[i]); }
    render();
  }
  function go(n) { i = Math.max(0, Math.min(slides.length - 1, n)); s = 0; render(); }

  document.getElementById('next').onclick = next;
  document.getElementById('prev').onclick = prev;
  window.addEventListener('resize', fit);
  window.addEventListener('keydown', function (e) {
    var k = e.key;
    if (k === 'ArrowRight' || k === 'PageDown' || k === ' ' || k === 'Enter') { e.preventDefault(); next(); }
    else if (k === 'ArrowLeft' || k === 'PageUp' || k === 'Backspace') { e.preventDefault(); prev(); }
    else if (k === 'Home') { go(0); }
    else if (k === 'End') { go(slides.length - 1); s = maxStep(slides[i]); render(); }
    else if (k === 'n' || k === 'N') { notes.classList.toggle('on'); }
    else if (k === 'f' || k === 'F') {
      if (document.fullscreenElement) { document.exitFullscreen(); }
      else if (document.documentElement.requestFullscreen) { document.documentElement.requestFullscreen(); }
    }
  });

  fit();
  var h = parseInt((location.hash || '').replace('#', ''), 10);
  go(isNaN(h) ? 0 : h - 1);
  window.deck = { go: go, count: slides.length, next: next, prev: prev };
})();
