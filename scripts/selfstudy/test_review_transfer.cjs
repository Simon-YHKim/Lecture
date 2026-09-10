const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const test = require('node:test');
const assert = require('node:assert/strict');

const asset = name => fs.readFileSync(path.join(__dirname, 'assets', name), 'utf8');
const memo = asset('deck_memo.html');
const nav = asset('deck_nav.html');
function section(text, start, end) {
  const a = text.indexOf(start), b = text.indexOf(end, a);
  assert.ok(a >= 0 && b > a);
  return text.slice(a, b);
}
function validator() {
  const context = vm.createContext({sceneIds: ['scene-a', 'scene-b'], reviewId: 'edition-1'});
  vm.runInContext(section(memo, '  function validateBackup(', "  document.getElementById('mmbackup')"), context);
  return context.validateBackup;
}
function fixture() {
  return {format: 'autocad-review', version: 1, reviewId: 'edition-1', notes: [
    {scope: 'slide', where: '1차시', quote: '원문', note: '<b>의견</b>', slide: 99, sceneId: 'scene-a'},
    {scope: 'all', where: '공통', quote: '', note: '전체 의견', sceneId: null}
  ], scripts: {'scene-b': ''}};
}

test('both production scripts parse without a browser', () => {
  for (const text of [memo, nav]) {
    for (const m of text.matchAll(/<script>([\s\S]*?)<\/script>/g)) new vm.Script(m[1]);
  }
});
test('restore resolves scene IDs and preserves literal text and intentional empty scripts', () => {
  const next = validator()(fixture());
  assert.equal(next.notes[0].slide, 0);
  assert.equal(next.notes[1].slide, null);
  assert.equal(next.notes[0].note, '<b>의견</b>');
  assert.equal(next.scripts['scene-b'], '');
});
test('reject another edition, format and invalid scene identifiers', () => {
  for (const change of [d => d.reviewId = 'other', d => d.version = 2,
    d => d.notes[0].sceneId = 'missing', d => d.scripts.unknown = 'text',
    d => d.scripts = JSON.parse('{"__proto__":"invalid"}')]) {
    const data = fixture(); change(data);
    assert.throws(() => validator()(data));
  }
});
test('reject malformed or excessive text without changing the input', () => {
  for (const change of [d => d.notes = {}, d => d.notes[0].note = {},
    d => d.notes[0].quote = 'x'.repeat(401), d => d.scripts = [],
    d => d.notes[0].scope = 'unknown']) {
    const data = fixture(); change(data); const before = JSON.stringify(data);
    assert.throws(() => validator()(data));
    assert.equal(JSON.stringify(data), before);
  }
});
test('unsaved script capture follows its scene ID even after the current slide changes', () => {
  let saved = 0;
  const context = vm.createContext({
    slides: [{sceneId: 'old', notes: '원문'}, {sceneId: 'next', notes: '다음'}], i: 1,
    noteText: {dataset: {scene: 'old'}, textContent: '수정한 대본', getAttribute: () => 'true'},
    edits: {}, saveEdits: () => saved++
  });
  vm.runInContext(section(nav, '  function captureEdit(', "  noteText.addEventListener('input'"), context);
  context.captureEdit();
  assert.equal(context.edits.old, '수정한 대본');
  assert.equal(context.edits.next, undefined);
  context.noteText.textContent = '';
  context.captureEdit();
  assert.equal(context.edits.old, '');
  context.noteText.textContent = '원문';
  context.captureEdit();
  assert.equal(Object.hasOwn(context.edits, 'old'), false);
  assert.equal(saved, 3);
});
test('backup round-trip includes common notes, slide notes and script edits', () => {
  const original = fixture();
  const context = vm.createContext({
    reviewId: 'edition-1', sceneIds: ['scene-a', 'scene-b'],
    items: original.notes.map((n, i) => ({...n, slide: i === 0 ? 0 : null})),
    window: {__deckScript: {list: () => [{sceneId: 'scene-b', now: ''}]}}
  });
  vm.runInContext(section(memo, '  function backup()', '  // Validate the entire file'), context);
  const restored = validator()(JSON.parse(JSON.stringify(context.backup())));
  assert.equal(restored.notes.length, 2);
  assert.equal(restored.scripts['scene-b'], '');
});

test('backup does not relabel an old note when slide order changes', () => {
  const context = vm.createContext({reviewId: 'edition-1', sceneIds: ['new', 'old'],
    items: [{scope: 'slide', sceneId: 'old', slide: 0, where: '', quote: '', note: ''}],
    window: {__deckScript: {list: () => []}}});
  vm.runInContext(section(memo, '  function backup()', '  // Validate the entire file'), context);
  assert.equal(context.backup().notes[0].sceneId, 'old');
});
test('an oversized note remains intact and does not create an unusable backup', () => {
  const data = fixture(); data.notes[0].note = 'x'.repeat(100001);
  let callback, downloads = 0, message = '';
  const context = vm.createContext({
    document: {getElementById: () => ({addEventListener: (_event, fn) => callback = fn})},
    backup: () => data, validateBackup: validator(), Blob,
    download: () => downloads++, say: text => message = text
  });
  vm.runInContext(section(memo, "  document.getElementById('mmbackup')", '  var fileInput ='), context);
  callback();
  assert.equal(downloads, 0);
  assert.equal(data.notes[0].note.length, 100001);
  assert.match(message, /기록은 유지/);
});
