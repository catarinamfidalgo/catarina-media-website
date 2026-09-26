/* Contact form handler.

   The form posts to a Google Apps Script that Catarina owns, running in her
   own account, which mails the message to her and answers back so this page
   can say whether it actually arrived. See assets/contact-endpoint.gs for the
   script and how to deploy it.

   Why not mailto: alone, which is what this used to do. Handing the message
   to the visitor's own mail app means the send happens somewhere we cannot
   see. On a phone that is usually fine. On a desktop with no mail app set up,
   and most people read mail in a browser tab, clicking Send opened an empty
   "add an account" dialog, or did nothing at all, and the enquiry was gone
   with nothing to record that anyone had tried. Tolerable for a page people
   reach by searching her name. Not tolerable for traffic she pays for.

   mailto: is still here as the fallback for when the request fails, so a
   visitor is never left with no way to reach her. The address is base64 in
   the form's data-eml attribute, decoded only at that moment: obfuscation
   against scrapers that scan for an @, which is what they overwhelmingly
   are. The endpoint itself needs no address in the page at all.
*/
(function () {
  "use strict";

  var form = document.getElementById("contact-form");
  if (!form) return;

  var status = document.getElementById("form-status");
  var button = form.querySelector("button[type=submit], input[type=submit]");
  var buttonText = button ? button.textContent : "";
  var loadedAt = Date.now();
  var sending = false;

  function val(id) {
    var el = document.getElementById(id);
    return el ? el.value.trim() : "";
  }

  function say(msg, kind) {
    if (!status) return;
    status.textContent = msg;
    status.setAttribute("data-state", kind || "");
  }

  function busy(on) {
    sending = on;
    if (!button) return;
    button.disabled = on;
    button.textContent = on ? (button.getAttribute("data-sending") || "Sending…")
                            : buttonText;
  }

  function lead(type) {
    // Recorded only once the endpoint has confirmed the mail was sent, so
    // this counts enquiries rather than button presses. The old version
    // fired on click, before the mail app had even opened, which meant a
    // campaign that produced nothing could still report conversions.
    if (typeof window.gtag === "function") {
      window.gtag("event", "generate_lead", {
        form_name: "contact",
        video_type: type || "unspecified"
      });
    }
  }

  function mailtoHref(name, type) {
    var encoded = form.getAttribute("data-eml");
    if (!encoded || !window.atob) return "";
    var body =
      "Name: " + name + "\n" +
      "Email: " + val("email") + "\n" +
      "Company: " + (val("company") || "—") + "\n" +
      "Type of video: " + (type || "—") + "\n\n" +
      val("message") + "\n";
    return window.atob(encoded) +
      "?subject=" + encodeURIComponent(
        type ? (type + " — " + (name || "enquiry")) : ("Enquiry" + (name ? " — " + name : ""))) +
      "&body=" + encodeURIComponent(body);
  }

  function fallback(name, type, why) {
    var href = mailtoHref(name, type);
    if (!href) {
      say("Something went wrong sending that. Please try again in a moment.", "error");
      return;
    }
    say("Opening your email app instead — your message is ready to send.", "warn");
    window.location.href = href;
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (sending) return;

    if (typeof form.reportValidity === "function" && !form.reportValidity()) return;

    // Honeypot: invisible to people, irresistible to bots.
    var trap = form.querySelector("input[name=_gotcha]");
    if (trap && trap.value) return;

    var name = val("name"), type = val("video-type");
    var endpoint = form.getAttribute("data-endpoint");

    // Not deployed yet: behave exactly as before rather than breaking.
    if (!endpoint) {
      lead(type);
      fallback(name, type, "no endpoint configured");
      return;
    }

    var data = new URLSearchParams();
    data.set("name", name);
    data.set("email", val("email"));
    data.set("company", val("company"));
    data.set("type", type);
    data.set("message", val("message"));
    data.set("lang", document.documentElement.lang || "");
    data.set("page", location.pathname);
    data.set("elapsed", String(Date.now() - loadedAt));
    if (trap) data.set("_gotcha", trap.value);

    busy(true);
    say("Sending…", "busy");

    // Form-encoded with no custom headers, so the browser treats it as a
    // simple request and does not preflight. Apps Script cannot answer a
    // preflight, and a CORS failure here would look identical to the server
    // being down.
    fetch(endpoint, { method: "POST", body: data })
      .then(function (res) {
        return res.text().then(function (text) {
          var ok = res.ok;
          try { ok = ok && JSON.parse(text).ok !== false; } catch (err) { /* not JSON */ }
          return ok;
        });
      })
      .then(function (ok) {
        busy(false);
        if (!ok) { fallback(name, type, "endpoint refused"); return; }
        lead(type);
        form.reset();
        say("Thank you, your message has been sent. Catarina will reply to you directly.", "ok");
      })
      .catch(function (err) {
        busy(false);
        fallback(name, type, err);
      });
  });
})();
