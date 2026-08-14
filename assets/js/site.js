/* ===================================================================
   DentaSuite prototype behaviour
   - Role switching (Admin / Dentist / Receptionist)
   - Mobile sidebar
   - Odontogram interaction
   In the real MVC app the role logic is server-side
   (@if (User.IsInRole("Admin")) / [Authorize(Roles = "...")]).
   Here it is client-side purely so the prototype can be demoed.
   =================================================================== */
(function () {
  "use strict";

  var ROLES = {
    Admin:        { name: "Dr. Amara Okafor",  title: "Practice Administrator", initials: "AO", home: "dashboard-admin.html" },
    Dentist:      { name: "Dr. Luca Bianchi",  title: "Dentist — Chair 2",      initials: "LB", home: "dashboard-dentist.html" },
    Receptionist: { name: "Priya Nair",        title: "Front Desk",             initials: "PN", home: "dashboard-reception.html" }
  };
  var KEY = "dentasuite.role";

  function currentRole() {
    var r = null;
    try { r = localStorage.getItem(KEY); } catch (e) { /* private mode */ }
    var q = new URLSearchParams(location.search).get("role");
    if (q && ROLES[q]) { r = q; setRole(q, true); }
    return ROLES[r] ? r : "Admin";
  }

  function setRole(role, quiet) {
    if (!ROLES[role]) return;
    try { localStorage.setItem(KEY, role); } catch (e) {}
    if (!quiet) applyRole(role);
  }

  function applyRole(role) {
    var meta = ROLES[role];

    // Show / hide anything tagged with data-roles="Admin,Dentist"
    document.querySelectorAll("[data-roles]").forEach(function (el) {
      var allowed = el.getAttribute("data-roles").split(",").map(function (s) { return s.trim(); });
      var ok = allowed.indexOf(role) > -1;
      if (el.classList.contains("role-only")) {
        el.classList.toggle("show", ok);
      } else {
        el.style.display = ok ? "" : "none";
      }
    });

    document.querySelectorAll("[data-role-name]").forEach(function (el) { el.textContent = meta.name; });
    document.querySelectorAll("[data-role-title]").forEach(function (el) { el.textContent = meta.title; });
    document.querySelectorAll("[data-role-initials]").forEach(function (el) { el.textContent = meta.initials; });
    document.querySelectorAll("[data-role-label]").forEach(function (el) { el.textContent = role; });
    document.querySelectorAll("[data-role-home]").forEach(function (el) { el.setAttribute("href", meta.home); });
    document.querySelectorAll("[data-role-check]").forEach(function (el) {
      el.classList.toggle("d-none", el.getAttribute("data-role-check") !== role);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var role = currentRole();
    applyRole(role);

    document.querySelectorAll("[data-set-role]").forEach(function (el) {
      el.addEventListener("click", function (ev) {
        ev.preventDefault();
        var r = el.getAttribute("data-set-role");
        setRole(r);
        var target = el.getAttribute("data-go");
        if (target === "home") { location.href = ROLES[r].home; }
        else if (target) { location.href = target; }
      });
    });

    // ---- mobile sidebar ----
    var sb = document.querySelector(".sidebar");
    var bd = document.querySelector(".backdrop-x");
    function closeNav() { if (sb) sb.classList.remove("open"); if (bd) bd.classList.remove("show"); }
    document.querySelectorAll("[data-toggle-nav]").forEach(function (b) {
      b.addEventListener("click", function () {
        if (!sb) return;
        sb.classList.toggle("open");
        if (bd) bd.classList.toggle("show", sb.classList.contains("open"));
      });
    });
    if (bd) bd.addEventListener("click", closeNav);
    window.addEventListener("resize", function () { if (window.innerWidth > 991) closeNav(); });

    // ---- odontogram ----
    var states = ["healthy", "caries", "filled", "crown", "rct", "implant", "extract", "missing"];
    var labels = {
      healthy: "Sound", caries: "Caries", filled: "Restoration", crown: "Crown / onlay",
      rct: "Root canal", implant: "Implant", extract: "Planned extraction", missing: "Missing"
    };
    var brush = null;

    document.querySelectorAll(".legend .lg[data-state]").forEach(function (lg) {
      lg.addEventListener("click", function () {
        var s = lg.getAttribute("data-state");
        brush = (brush === s) ? null : s;
        document.querySelectorAll(".legend .lg").forEach(function (x) {
          x.style.borderColor = ""; x.style.background = "#fff";
        });
        if (brush) { lg.style.borderColor = "var(--brand-500)"; lg.style.background = "var(--brand-50)"; }
        var hint = document.getElementById("brushHint");
        if (hint) hint.textContent = brush ? ("Brush: " + labels[brush] + " — click a tooth to apply") : "Pick a condition, then click a tooth.";
      });
    });

    document.querySelectorAll(".tooth").forEach(function (t) {
      t.addEventListener("click", function () {
        if (brush) {
          t.setAttribute("data-state", brush);
        } else {
          var cur = t.getAttribute("data-state") || "healthy";
          t.setAttribute("data-state", states[(states.indexOf(cur) + 1) % states.length]);
        }
        document.querySelectorAll(".tooth.sel").forEach(function (x) { x.classList.remove("sel"); });
        t.classList.add("sel");
        var num = t.getAttribute("data-tooth");
        var st = t.getAttribute("data-state") || "healthy";
        var d1 = document.getElementById("selTooth");
        var d2 = document.getElementById("selState");
        if (d1) d1.textContent = "Tooth " + num;
        if (d2) d2.textContent = labels[st];
        var panel = document.getElementById("toothPanel");
        if (panel) panel.classList.remove("d-none");
      });
    });

    // Prototype-only: keep unfinished demo controls from looking broken.
    document.querySelectorAll('a[href="#"]:not([data-bs-toggle])').forEach(function (a) {
      a.addEventListener("click", function (e) { e.preventDefault(); });
    });
  });
})();
