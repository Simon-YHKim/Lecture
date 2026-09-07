/* 자습 교재 런타임 — 외부 의존 0. 저장 실패해도 본문은 그대로 읽힌다. */
(function () {
  'use strict';
  // 한 차시가 여러 쪽으로 나뉘어도 메모와 진도는 차시 하나로 합친다
  var SCOPE = document.body.getAttribute('data-progress-key')
    || (location.pathname.split('/').pop() || 'index');
  var KEY = 'acad-selfstudy/' + SCOPE;
  var mem = {};                       // localStorage 가 막히면 여기로 떨어진다
  var store = {
    get: function (k, d) {
      try { var v = localStorage.getItem(KEY + '/' + k); if (v !== null) return JSON.parse(v); }
      catch (e) { }
      return Object.prototype.hasOwnProperty.call(mem, k) ? mem[k] : d;
    },
    set: function (k, v) {
      mem[k] = v;
      try { localStorage.setItem(KEY + '/' + k, JSON.stringify(v)); return true; }
      catch (e) { return false; }
    },
    // 인덱스가 각 차시의 진도를 읽을 때 쓴다
    getFor: function (file, k, d) {
      try { var v = localStorage.getItem('acad-selfstudy/' + file + '/' + k); if (v !== null) return JSON.parse(v); }
      catch (e) { }
      return d;
    }
  };
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ── 언어 ─────────────────────────────── */
  var root = document.documentElement;
  function setLang(l) {
    document.body.setAttribute('data-lang', l);
    root.setAttribute('lang', l);
    $$('[data-lang-btn]').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-lang-btn') === l));
    });
    try { localStorage.setItem('acad-selfstudy/lang', JSON.stringify(l)); } catch (e) { mem.lang = l; }
  }
  var savedLang = 'ko';
  try { var sl = localStorage.getItem('acad-selfstudy/lang'); if (sl) savedLang = JSON.parse(sl); } catch (e) { }
  setLang(savedLang === 'en' ? 'en' : 'ko');
  $$('[data-lang-btn]').forEach(function (b) {
    b.addEventListener('click', function () { setLang(b.getAttribute('data-lang-btn')); });
  });

  /* ── 테마 ─────────────────────────────── */
  function setTheme(t) {
    if (t === 'auto') root.removeAttribute('data-theme'); else root.setAttribute('data-theme', t);
    try { localStorage.setItem('acad-selfstudy/theme', JSON.stringify(t)); } catch (e) { mem.theme = t; }
    var b = $('#theme-btn');
    var w = { auto: ['자동', 'Auto'], dark: ['어둡게', 'Dark'], light: ['밝게', 'Light'] }[t];
    if (b) b.innerHTML = '<span class="k">' + w[0] + '</span><span class="e">' + w[1] + '</span>';
  }
  var th = 'auto';
  try { var st = localStorage.getItem('acad-selfstudy/theme'); if (st) th = JSON.parse(st); } catch (e) { }
  setTheme(th);
  var tb = $('#theme-btn');
  if (tb) tb.addEventListener('click', function () {
    var cur = root.getAttribute('data-theme') || 'auto';
    setTheme(cur === 'auto' ? 'light' : cur === 'light' ? 'dark' : 'auto');
  });

  /* ── 탭 ───────────────────────────────── */
  var tabs = $$('nav.tabs button[role="tab"]');
  function selectTab(id, push) {
    tabs.forEach(function (t) {
      var on = t.getAttribute('aria-controls') === id;
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
    });
    $$('[role="tabpanel"]').forEach(function (p) { p.hidden = p.id !== id; });
    store.set('tab', id);
    if (push && history.replaceState) history.replaceState(null, '', '#' + id);
    window.scrollTo({ top: 0, behavior: 'auto' });
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { selectTab(t.getAttribute('aria-controls'), true); });
    t.addEventListener('keydown', function (e) {
      var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (!d) return;
      e.preventDefault();
      var n = tabs[(i + d + tabs.length) % tabs.length];
      n.focus(); selectTab(n.getAttribute('aria-controls'), true);
    });
  });
  if (tabs.length) {
    var want = (location.hash || '').slice(1) || store.get('tab', '') || tabs[0].getAttribute('aria-controls');
    if (!document.getElementById(want)) want = tabs[0].getAttribute('aria-controls');
    selectTab(want, false);
  }

  /* ── 진도 ─────────────────────────────── */
  var boxes = $$('input[type="checkbox"][data-step]');
  var TOTAL = parseInt(document.body.getAttribute('data-step-total') || '0', 10) || boxes.length;
  var mine = boxes.map(function (b) { return b.getAttribute('data-step'); });
  var doneSet = store.get('done', []);
  if (!Array.isArray(doneSet)) doneSet = [];
  function paint() {
    boxes.forEach(function (b) {
      var li = b.closest('li');
      if (li) li.classList.toggle('done', b.checked);
    });
    // 이 쪽이 가진 단계만 갈아끼우고, 다른 쪽에서 체크한 것은 그대로 둔다
    var keep = doneSet.filter(function (id) { return mine.indexOf(id) < 0; });
    var here = boxes.filter(function (b) { return b.checked; })
      .map(function (b) { return b.getAttribute('data-step'); });
    doneSet = keep.concat(here);
    store.set('done', doneSet);
    store.set('total', TOTAL);
    var pct = TOTAL ? Math.round(100 * doneSet.length / TOTAL) : 0;
    var f = $('#prog-fill'); if (f) f.style.width = pct + '%';
    var l = $('#prog-txt');
    if (l) l.textContent = doneSet.length + ' / ' + TOTAL + ' (' + pct + '%)';
  }
  boxes.forEach(function (b) {
    if (doneSet.indexOf(b.getAttribute('data-step')) >= 0) b.checked = true;
    b.addEventListener('change', paint);
  });
  if (boxes.length) paint();
  var rst = $('#reset-prog');
  if (rst) rst.addEventListener('click', function () {
    boxes.forEach(function (b) { b.checked = false; });
    doneSet = [];
    paint();
  });

  /* ── 인덱스 진도 표시 ─────────────────── */
  $$('[data-prog-of]').forEach(function (el) {
    var file = el.getAttribute('data-prog-of');
    var d = store.getFor(file, 'done', []);
    var t = store.getFor(file, 'total', 0);
    if (!t || !Array.isArray(d)) { el.textContent = el.getAttribute('data-empty') || ''; return; }
    el.textContent = Math.round(100 * d.length / t) + '%';
  });

  /* ── 메모 ─────────────────────────────── */
  var panel = $('#memo'); if (!panel) return;
  var list = $('#memo-list'), out = $('#memo-out'), pick = $('#pick');
  var notes = store.get('notes', []);
  if (!Array.isArray(notes)) notes = [];
  var pending = null;

  function label(el) {
    var a = el && el.closest ? el.closest('[data-memo]') : null;
    return a ? a.getAttribute('data-memo') : '';
  }
  function render() {
    list.innerHTML = '';
    if (!notes.length) {
      var p = document.createElement('p');
      p.className = 'memo-empty';
      p.textContent = document.body.getAttribute('data-lang') === 'en'
        ? 'Select any text in the page, then press the Note button that appears.'
        : '본문에서 글을 드래그해 선택하면 [메모] 버튼이 뜨고, 그 자리가 인용으로 고정됩니다.';
      list.appendChild(p);
      return;
    }
    notes.forEach(function (n, i) {
      var d = document.createElement('div'); d.className = 'memo-item';
      var loc = document.createElement('div'); loc.className = 'loc'; loc.textContent = n.loc || '';
      var q = document.createElement('blockquote'); q.textContent = n.quote;
      var ta = document.createElement('textarea');
      ta.value = n.text || '';
      ta.setAttribute('aria-label', (n.loc || '') + ' 메모');
      ta.addEventListener('input', function () { notes[i].text = ta.value; store.set('notes', notes); });
      var rm = document.createElement('button'); rm.className = 'rm'; rm.type = 'button';
      rm.innerHTML = '<span class="k">✕ 삭제</span><span class="e">✕ Delete</span>';
      rm.addEventListener('click', function () { notes.splice(i, 1); store.set('notes', notes); render(); });
      d.appendChild(loc); d.appendChild(q); d.appendChild(ta); d.appendChild(rm);
      list.appendChild(d);
    });
  }
  render();

  function open(v) {
    panel.setAttribute('data-open', v ? '1' : '0');
    var b = $('#memo-btn'); if (b) b.setAttribute('aria-pressed', String(!!v));
    panel.setAttribute('aria-hidden', String(!v));
  }
  var mb = $('#memo-btn'); if (mb) mb.addEventListener('click', function () { open(panel.getAttribute('data-open') !== '1'); });
  var mc = $('#memo-close'); if (mc) mc.addEventListener('click', function () { open(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { open(false); pick.style.display = 'none'; } });

  document.addEventListener('mouseup', function (e) {
    if (panel.contains(e.target) || e.target === pick) return;
    setTimeout(function () {
      var s = window.getSelection();
      var txt = s ? String(s).trim() : '';
      if (!txt || txt.length < 2) { pick.style.display = 'none'; return; }
      var node = s.anchorNode;
      var host = node && node.nodeType === 3 ? node.parentElement : node;
      if (!host || !host.closest || !host.closest('main')) { pick.style.display = 'none'; return; }
      pending = { quote: txt.length > 220 ? txt.slice(0, 220) + '…' : txt, loc: label(host), el: host.closest('[data-memo]') };
      var r = s.getRangeAt(0).getBoundingClientRect();
      pick.style.display = 'block';
      pick.style.left = Math.max(8, r.left + window.scrollX) + 'px';
      pick.style.top = (r.bottom + window.scrollY + 6) + 'px';
    }, 0);
  });
  pick.addEventListener('click', function () {
    if (!pending) return;
    notes.push({ quote: pending.quote, loc: pending.loc, text: '' });
    if (pending.el) pending.el.classList.add('memo-anchor');
    store.set('notes', notes);
    render(); open(true); pick.style.display = 'none';
    window.getSelection().removeAllRanges();
  });

  function compose() {
    var en = document.body.getAttribute('data-lang') === 'en';
    var head = (document.title || '') + '\n';
    var lines = notes.map(function (n, i) {
      return (i + 1) + ') [' + (n.loc || '-') + ']\n   “' + n.quote + '”\n   → ' + (n.text || (en ? '(no note)' : '(메모 없음)'));
    });
    var tail = en
      ? '\nIf any of the above conflict with each other, name the conflict first, propose a priority order, and only then proceed.'
      : '\n위 항목 중 서로 상충하는 것이 있으면 먼저 짚고 우선순위를 제시한 뒤 진행할 것.';
    return head + lines.join('\n') + '\n' + tail;
  }
  var cp = $('#memo-copy');
  if (cp) cp.addEventListener('click', function () {
    var text = compose();
    out.value = text;
    var base = cp.innerHTML;
    var done = function (ok) {
      cp.innerHTML = ok
        ? '<span class="k">✓ 복사됐습니다</span><span class="e">✓ Copied</span>'
        : '<span class="k">↓ 아래 창에서 직접 복사하세요</span><span class="e">↓ Copy from the box below</span>';
      setTimeout(function () { cp.innerHTML = base; }, 2600);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () { done(true); }, function () { legacy(); });
    } else legacy();
    function legacy() {
      out.hidden = false; out.select();
      var ok = false;
      try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
      done(ok);
    }
  });
  var sh = $('#memo-show');
  if (sh) sh.addEventListener('click', function () { out.hidden = !out.hidden; if (!out.hidden) out.value = compose(); });
})();
