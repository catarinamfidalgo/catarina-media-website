/**
 * Contact form receiver for catarina.media.
 *
 * This runs in Catarina's own Google account, not on anyone else's service.
 * It receives the form, sends the message to her Gmail, and replies to the
 * page so the form can tell the visitor whether it actually arrived. Nothing
 * is stored anywhere, and no account beyond her own is involved.
 *
 * Why this exists: the site is static and a static page cannot send mail. The
 * form used to hand the message to the visitor's own mail app with mailto:.
 * On a phone that mostly works. On a desktop with no mail app configured, and
 * most people read mail in a browser tab, the click did nothing at all and the
 * enquiry was lost with nothing to say it had happened.
 *
 * The destination address lives here, in a private script, rather than in the
 * public page. It is never read from the request, so this cannot be used to
 * send mail to anybody else.
 *
 * ── SETUP ────────────────────────────────────────────────────────────────
 *  1. Go to script.google.com and choose New project.
 *  2. Delete whatever is in the editor and paste this whole file in.
 *  3. Put the address to receive at in TO, below.
 *  4. Click Deploy ▸ New deployment.
 *       Type            Web app
 *       Execute as      Me
 *       Who has access  Anyone            ← required; the form is public
 *  5. Authorise it when asked. It is your own script, so Google shows the
 *     "unverified app" warning: Advanced ▸ Go to (project name).
 *  6. Copy the Web app URL it gives you and send it to Claude, or paste it
 *     into data-endpoint on the form in assets/source.html yourself.
 *
 *  To change anything later, edit here then Deploy ▸ Manage deployments ▸
 *  edit ▸ Version: New version. The URL stays the same.
 */

// ── The only line you need to edit ───────────────────────────────────────
var TO = "PUT_YOUR_ADDRESS_HERE@example.com";

// Subject line prefix, so these are easy to filter in Gmail.
var TAG = "[catarina.media]";

// Refuse more than this many in an hour, so a bot cannot flood the inbox.
var MAX_PER_HOUR = 12;


function doPost(e) {
  try {
    var p = (e && e.parameter) || {};

    // Honeypot. Invisible to people, filled in by bots.
    if (p._gotcha) return reply(true, "ok");

    // Anything submitted within two seconds of the page loading is a script.
    var elapsed = Number(p.elapsed || 0);
    if (elapsed > 0 && elapsed < 2000) return reply(true, "ok");

    if (!underRateLimit()) return reply(false, "rate limited");

    var name = clean(p.name, 120);
    var from = clean(p.email, 160);
    var msg  = clean(p.message, 8000);

    if (!name || !from || !msg) return reply(false, "missing fields");
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(from)) return reply(false, "bad email");

    var company = clean(p.company, 160);
    var type    = clean(p.type, 120);

    var subject = TAG + " " + (type ? type + " — " : "") + (name || "enquiry");

    var body =
      "Name:     " + name + "\n" +
      "Email:    " + from + "\n" +
      "Company:  " + (company || "—") + "\n" +
      "Type:     " + (type || "—") + "\n" +
      "Language: " + (clean(p.lang, 12) || "—") + "\n" +
      "Page:     " + (clean(p.page, 300) || "—") + "\n" +
      "\n" + msg + "\n";

    MailApp.sendEmail({
      to: TO,
      subject: subject,
      body: body,
      name: "catarina.media",
      // Reply goes straight back to the enquirer rather than to this script.
      replyTo: from
    });

    return reply(true, "sent");
  } catch (err) {
    return reply(false, String(err));
  }
}


// A GET is someone opening the URL in a browser. Say nothing useful.
function doGet() {
  return reply(true, "ok");
}


function clean(v, max) {
  if (v === undefined || v === null) return "";
  return String(v).replace(/\s+$/, "").replace(/^\s+/, "").slice(0, max);
}


function underRateLimit() {
  var props = PropertiesService.getScriptProperties();
  var now = Date.now();
  var hits = [];
  try {
    hits = JSON.parse(props.getProperty("hits") || "[]");
  } catch (err) {
    hits = [];
  }
  hits = hits.filter(function (t) { return now - t < 3600 * 1000; });
  if (hits.length >= MAX_PER_HOUR) return false;
  hits.push(now);
  props.setProperty("hits", JSON.stringify(hits));
  return true;
}


function reply(ok, detail) {
  return ContentService
    .createTextOutput(JSON.stringify({ ok: ok, detail: detail }))
    .setMimeType(ContentService.MimeType.JSON);
}
