/**
 * Member Billing Tracker: Apps Script.
 * All the checks are formulas in the sheet. This script only adds a menu and emails the
 * Fix List to the front desk each morning.
 *
 * Setup: in the Google Sheet, open Extensions > Apps Script, paste this file, save,
 * reload the sheet, then use the "Front desk" menu.
 */

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Front desk')
    .addItem("Email me today's fix list", 'emailFixList')
    .addItem('Send the fix list every morning', 'turnOnDailyEmail')
    .addToUi();
}

/** Reads the Fix List tab and returns one object per problem. */
function readFixList(sheet) {
  const values = sheet.getRange(5, 1, sheet.getLastRow() - 4, 7).getValues();
  return values
    .filter(r => r[2] !== '')
    .map(r => ({ action: r[0], name: r[1], memberId: r[2], phone: r[3], why: r[4], amount: r[5], ref: r[6] }));
}

/** Builds the plain email text. Kept separate so it can be tested outside Google. */
function buildFixListEmail(items, dateText) {
  if (items.length === 0) {
    return { subject: 'Fix list for ' + dateText + ': nothing to fix', body: 'Nothing on the fix list today.' };
  }
  const lines = items.map((it, i) =>
    (i + 1) + '. ' + it.action + ': ' + it.name + ' (' + it.memberId + ', ' + it.phone + '). ' + it.why + '. $' + it.amount + ' [' + it.ref + ']');
  return {
    subject: 'Fix list for ' + dateText + ': ' + items.length + (items.length === 1 ? ' thing' : ' things') + ' to fix',
    body: 'Good morning! Here is today\'s fix list.\n\n' + lines.join('\n') +
      '\n\nLook members up by ID, never by name. Two members can have the same name.'
  };
}

function emailFixList() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const items = readFixList(ss.getSheetByName('Fix List'));
  const dateText = Utilities.formatDate(new Date(), ss.getSpreadsheetTimeZone(), 'MMM d, yyyy');
  const msg = buildFixListEmail(items, dateText);
  MailApp.sendEmail(Session.getActiveUser().getEmail(), msg.subject, msg.body);
}

/** Creates one daily trigger at about 8am, replacing any earlier one. */
function turnOnDailyEmail() {
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === 'emailFixList')
    .forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('emailFixList').timeBased().everyDays(1).atHour(8).create();
  SpreadsheetApp.getUi().alert('Done. The fix list will be emailed to you every morning around 8am.');
}

if (typeof module !== 'undefined') module.exports = { readFixList, buildFixListEmail, emailFixList, turnOnDailyEmail };
