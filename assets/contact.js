/* Contact form handler.

   Submitting composes a message in the visitor's own email app, with every
   field already filled in. Nothing is posted to a server, so no third party
   ever holds the message — the same approach nfc.cool uses for its "Email
   us" button.

   The destination address is NOT written here in readable form. This file is
   public at /assets/contact.js, and an address in plain text is harvested by
   spam scrapers within days. It is base64-encoded in the form's data-eml
   attribute and decoded at the moment of sending. That is obfuscation, not
   encryption: it defeats the scrapers that simply scan for an @, which is
   what they overwhelmingly are, not a person who looks deliberately.

   Trade-off to know about: if the visitor's machine has no mail app set up,
   the browser hands them an empty "add an account" dialog and the enquiry is
   lost, with nothing to tell us it happened.
*/
(function () {
  "use strict";

  var form = document.getElementById("contact-form");
  if (!form) return;

  var status = document.getElementById("form-status");

  function val(id) {
    var el = document.getElementById(id);
    return el ? el.value.trim() : "";
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    if (typeof form.reportValidity === "function" && !form.reportValidity()) return;

    // Honeypot: invisible to people, irresistible to bots.
    var trap = form.querySelector("input[name=_gotcha]");
    if (trap && trap.value) return;

    var encoded = form.getAttribute("data-eml");
    if (!encoded || !window.atob) return;

    var name = val("name"), type = val("video-type");

    var body =
      "Name: " + name + "\n" +
      "Email: " + val("email") + "\n" +
      "Company: " + (val("company") || "—") + "\n" +
      "Type of video: " + (type || "—") + "\n\n" +
      val("message") + "\n";

    var href = window.atob(encoded) +
      "?subject=" + encodeURIComponent(
        type ? (type + " — " + (name || "enquiry")) : ("Enquiry" + (name ? " — " + name : ""))) +
      "&body=" + encodeURIComponent(body);

    window.location.href = href;

    if (status) {
      status.textContent =
        "Opening your email app — your message is ready to send.";
    }
  });
})();
