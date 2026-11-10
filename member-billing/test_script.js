// Tests Code.gs outside Google with simple stand-ins for SpreadsheetApp, MailApp and ScriptApp.
// Reads the fix list rows from a spreadsheet engine's results (exported as JSON by the caller).
const assert = require('assert');
const fs = require('fs');
const rows = JSON.parse(fs.readFileSync(process.argv[2], 'utf8')); // Fix List rows from row 5 down
let sent = [], triggers = [], alerts = [];
global.SpreadsheetApp = {
  getActiveSpreadsheet: () => ({
    getSheetByName: () => ({ getLastRow: () => rows.length + 4, getRange: () => ({ getValues: () => rows }) }),
    getSpreadsheetTimeZone: () => 'America/Los_Angeles'
  }),
  getUi: () => ({ alert: m => alerts.push(m) })
};
global.Utilities = { formatDate: () => 'Oct 31, 2026' };
global.Session = { getActiveUser: () => ({ getEmail: () => 'frontdesk@example.com' }) };
global.MailApp = { sendEmail: (to, subject, body) => sent.push({ to, subject, body }) };
const mk = name => ({ getHandlerFunction: () => name });
global.ScriptApp = {
  getProjectTriggers: () => triggers,
  deleteTrigger: t => { triggers = triggers.filter(x => x !== t); },
  newTrigger: name => ({ timeBased: () => ({ everyDays: d => ({ atHour: h => ({ create: () => triggers.push(Object.assign(mk(name), { d, h })) }) }) }) })
};
const S = require('./Code.gs.js');
let n = 0; const ok = (c, m) => { assert(c, m); n++; console.log('PASS ' + m); };

S.emailFixList();
const filled = rows.filter(r => r[1] !== '').length;
ok(sent.length === 1, 'sends exactly one email');
ok(sent[0].subject === `Fix list for Oct 31, 2026: ${filled} things to fix`, 'subject has the count: ' + sent[0].subject);
ok(sent[0].body.split('\n').filter(l => /^\d+\. /.test(l)).length === filled, 'one line per problem');
ok(sent[0].body.includes('Chris Morgan (M-1031'), 'same-name member is listed with their ID');
ok(!/Chris Morgan \(M-1012/.test(sent[0].body), 'the other Chris Morgan (M-1012) is not on the list');
ok(S.buildFixListEmail([], 'Nov 1, 2026').subject.endsWith('nothing to fix'), 'empty list gets a clear subject');
triggers = [mk('emailFixList'), mk('somethingElse')];
S.turnOnDailyEmail(); S.turnOnDailyEmail();
ok(triggers.filter(t => t.getHandlerFunction() === 'emailFixList').length === 1, 'turning it on twice leaves one daily trigger');
ok(triggers.some(t => t.getHandlerFunction() === 'somethingElse'), 'other triggers are left alone');
ok(triggers.find(t => t.getHandlerFunction() === 'emailFixList').h === 8, 'trigger runs at 8am');
console.log(`\n${n} script checks passed\n--- sample email ---\n${sent[0].subject}\n${sent[0].body}`);
