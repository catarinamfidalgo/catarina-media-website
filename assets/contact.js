/* Contact form handler.

   Submissions POST to a form backend, which forwards them to the inbox.
   The destination address is held by the backend and is deliberately NOT in
   this file: everything here is public at /assets/contact.js, so any address
   written here would be harvested by spam scrapers. The endpoint ID below
   reveals nothing on its own.

   TO ACTIVATE:
   1. Sign up free at https://formspree.io and create a form.
   2. Point it at the destination inbox there, in their dashboard.
   3. Copy the endpoint it gives you (https://formspree.io/f/xxxxxxxx)
      and replace YOUR_FORM_ID below. That is the only edit needed.
*/
(function () {
  "use strict";

  var FORM_ENDPOINT = "https://formspree.io/f/YOUR_FORM_ID";

  var form = document.getElementById("contact-form");
  if (!form) return;

  var status = document.getElementById("form-status");
  var configured = FORM_ENDPOINT.indexOf("YOUR_FORM_ID") === -1;

  function say(msg) {
    if (status) status.textContent = msg;
  }

  function val(id) {
    var el = document.getElementById(id);
    return el ? el.value.trim() : "";
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    if (typeof form.reportValidity === "function" && !form.reportValidity()) return;

    // Honeypot: a real person never sees this field, so anything in it is a bot.
    var trap = form.querySelector("input[name=_gotcha]");
    if (trap && trap.value) return;

    if (!configured || !window.fetch) {
      say("The form isn't connected yet. Please try again shortly.");
      return;
    }

    var btn = form.querySelector("button[type=submit]");
    say("Sending…");
    if (btn) btn.disabled = true;

    fetch(FORM_ENDPOINT, {
      method: "POST",
      headers: { "Accept": "application/json", "Content-Type": "application/json" },
      body: JSON.stringify({
        name: val("name"),
        email: val("email"),
        company: val("company"),
        video_type: val("video-type"),
        message: val("message"),
        _subject: "Website inquiry — " + (val("name") || "New message")
      })
    })
      .then(function (res) {
        if (!res.ok) throw new Error(res.status);
        form.reset();
        say("Thank you — your message has been sent. I'll get back to you personally.");
      })
      .catch(function () {
        say("Sorry, that didn't send. Please check your connection and try again.");
      })
      .finally(function () {
        if (btn) btn.disabled = false;
      });
  });
})();
