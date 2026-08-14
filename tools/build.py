#!/usr/bin/env python3
"""
Static generator for the DentaSuite clickable prototype.

Each output .html file mirrors one Razor view of the ASP.NET MVC project, e.g.
    patients-index.html   ->  /Views/Patients/Index.cshtml
The shared shell below is the equivalent of /Views/Shared/_Layout.cshtml.
"""
import os, re, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "prototype")
sys.path.insert(0, HERE)

BS_CSS = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
BS_JS = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
BI_CSS = "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css"
FONT = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"

# --------------------------------------------------------------------------
# Navigation tree  (group, [ (label, file, icon, roles, badge) ])
# --------------------------------------------------------------------------
NAV = [
    ("Overview", [
        ("Dashboard",        "dashboard-admin.html",       "bi-grid-1x2",        "Admin", ""),
        ("My Day",           "dashboard-dentist.html",     "bi-sun",             "Dentist", ""),
        ("Front Desk",       "dashboard-reception.html",   "bi-door-open",       "Receptionist", ""),
    ]),
    ("Patients", [
        ("All Patients",     "patients-index.html",        "bi-people",          "Admin,Dentist,Receptionist", ""),
        ("Register Patient", "patients-create.html",       "bi-person-plus",     "Admin,Receptionist", ""),
        ("Patient Record",   "patients-details.html",      "bi-folder2-open",    "Admin,Dentist,Receptionist", ""),
    ]),
    ("Appointments", [
        ("Calendar",         "appointments-calendar.html", "bi-calendar3",       "Admin,Dentist,Receptionist", ""),
        ("Appointment List", "appointments-index.html",    "bi-list-check",      "Admin,Dentist,Receptionist", ""),
        ("Book Appointment", "appointments-create.html",   "bi-calendar-plus",   "Admin,Receptionist", ""),
        ("Reschedule",       "appointments-reschedule.html","bi-arrow-left-right","Admin,Dentist,Receptionist", ""),
        ("Waiting List",     "appointments-waitlist.html", "bi-hourglass-split", "Admin,Receptionist", "6"),
    ]),
    ("Clinical", [
        ("Dental Chart",     "treatments-chart.html",      "bi-diagram-3",       "Admin,Dentist", ""),
        ("Treatment Plan",   "treatments-plan.html",       "bi-clipboard2-pulse","Admin,Dentist", ""),
        ("Procedure Catalogue","treatments-procedures.html","bi-journal-medical","Admin,Dentist", ""),
        ("Prescriptions",    "treatments-prescriptions.html","bi-capsule",       "Admin,Dentist", ""),
    ]),
    ("Billing", [
        ("Invoices",         "billing-invoices.html",      "bi-receipt",         "Admin,Receptionist", ""),
        ("New Invoice",      "billing-invoice-create.html","bi-file-earmark-plus","Admin,Receptionist", ""),
        ("Payments",         "billing-payments.html",      "bi-credit-card",     "Admin,Receptionist", ""),
        ("Insurance Claims", "billing-claims.html",        "bi-shield-check",    "Admin,Receptionist", "3"),
    ]),
    ("Insights", [
        ("Reports",          "reports-index.html",         "bi-bar-chart-line",  "Admin", ""),
    ]),
    ("Administration", [
        ("Users & Roles",    "admin-users.html",           "bi-person-badge",    "Admin", ""),
        ("Clinic & Chairs",  "admin-clinic.html",          "bi-hospital",        "Admin", ""),
        ("Settings",         "admin-settings.html",        "bi-gear",            "Admin", ""),
    ]),
]


def nav_html(active_file):
    out = []
    for group, items in NAV:
        roles = sorted({r for it in items for r in it[3].split(",")})
        out.append('<div class="nav-group" data-roles="%s">' % ",".join(roles))
        out.append('<div class="nav-group-title">%s</div>' % group)
        for label, file, icon, item_roles, badge in items:
            cls = "nav-link-x active" if file == active_file else "nav-link-x"
            b = '<span class="badge rounded-pill text-bg-light">%s</span>' % badge if badge else ""
            out.append('<a class="%s" href="%s" data-roles="%s"><i class="bi %s"></i><span>%s</span>%s</a>'
                       % (cls, file, item_roles, icon, label, b))
        out.append('</div>')
    return "\n".join(out)


SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{title} · DentaSuite</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{font}" rel="stylesheet">
<link href="{bs}" rel="stylesheet">
<link href="{bi}" rel="stylesheet">
<link href="assets/css/site.css" rel="stylesheet">
</head>
<body>
<div class="proto-ribbon no-print">
  <i class="bi bi-eye"></i>
  <span>Interface prototype — <strong>{razor}</strong></span>
  <span class="d-none d-md-inline">·</span>
  <a href="index.html" class="d-none d-md-inline">screen map</a>
</div>

<div class="backdrop-x"></div>
<div class="app">

  <!-- ============ _Layout.cshtml : sidebar navigation ============ -->
  <aside class="sidebar">
    <a class="brand" href="dashboard-admin.html" data-role-home>
      <span class="logo"><i class="bi bi-hexagon-fill"></i></span>
      <span>DentaSuite<small>Clinic Suite</small></span>
    </a>
    {nav}
    <div class="sidebar-foot">
      <a href="index.html"><i class="bi bi-diagram-2 me-1"></i>Screen map</a>
      <a href="account-login.html"><i class="bi bi-box-arrow-right me-1"></i>Sign out</a>
      <div class="mt-2 opacity-75">v0.9 · prototype</div>
    </div>
  </aside>

  <div class="main">
    <!-- ============ _Layout.cshtml : top bar ============ -->
    <header class="topbar no-print">
      <button class="icon-btn d-lg-none" data-toggle-nav aria-label="Menu"><i class="bi bi-list"></i></button>
      <div class="searchbox d-none d-sm-block">
        <i class="bi bi-search"></i>
        <input type="search" placeholder="Search patients, invoices, appointments…" aria-label="Search">
      </div>
      <div class="ms-auto d-flex align-items-center gap-2">
        <a class="icon-btn d-none d-md-grid" href="appointments-create.html" title="Book appointment"><i class="bi bi-calendar-plus"></i></a>
        <button class="icon-btn" title="Notifications" data-bs-toggle="dropdown" data-bs-auto-close="outside">
          <i class="bi bi-bell"></i><span class="dot"></span>
        </button>
        <ul class="dropdown-menu dropdown-menu-end" style="width:290px">
          <li class="px-2 py-1 small text-muted fw-semibold">Notifications</li>
          <li><a class="dropdown-item" href="appointments-waitlist.html"><i class="bi bi-hourglass-split text-warning me-2"></i>6 patients on the waiting list</a></li>
          <li><a class="dropdown-item" href="billing-claims.html"><i class="bi bi-shield-exclamation text-danger me-2"></i>3 insurance claims rejected</a></li>
          <li><a class="dropdown-item" href="billing-invoices.html"><i class="bi bi-receipt text-primary me-2"></i>INV-2451 is 30 days overdue</a></li>
        </ul>

        <div class="dropdown">
          <button class="userchip" data-bs-toggle="dropdown">
            <span class="avatar" data-role-initials>AO</span>
            <span class="text-start d-none d-sm-block lh-sm">
              <span class="d-block fw-semibold" style="font-size:13px" data-role-name>Dr. Amara Okafor</span>
              <span class="d-block text-muted" style="font-size:11.5px" data-role-title>Practice Administrator</span>
            </span>
            <i class="bi bi-chevron-down text-muted ms-1" style="font-size:11px"></i>
          </button>
          <ul class="dropdown-menu dropdown-menu-end" style="width:250px">
            <li class="px-2 pt-1 pb-2 small text-muted">
              Prototype: switch role to see how the menus and screens change.
            </li>
            <li><a class="dropdown-item" href="#" data-set-role="Admin" data-go="home"><i class="bi bi-shield-lock me-2 text-secondary"></i>Admin</a></li>
            <li><a class="dropdown-item" href="#" data-set-role="Dentist" data-go="home"><i class="bi bi-person-vcard me-2 text-secondary"></i>Dentist</a></li>
            <li><a class="dropdown-item" href="#" data-set-role="Receptionist" data-go="home"><i class="bi bi-headset me-2 text-secondary"></i>Receptionist</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="admin-settings.html"><i class="bi bi-gear me-2 text-secondary"></i>Settings</a></li>
            <li><a class="dropdown-item" href="account-login.html"><i class="bi bi-box-arrow-right me-2 text-secondary"></i>Sign out</a></li>
          </ul>
        </div>
      </div>
    </header>

    <!-- ============ @RenderBody() ============ -->
    <main class="page">
{body}
    </main>
  </div>
</div>

<script src="{bsjs}"></script>
<script src="assets/js/site.js"></script>
</body>
</html>
"""

BARE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{title} · DentaSuite</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{font}" rel="stylesheet">
<link href="{bs}" rel="stylesheet">
<link href="{bi}" rel="stylesheet">
<link href="assets/css/site.css" rel="stylesheet">
</head>
<body>
{body}
<script src="{bsjs}"></script>
<script src="assets/js/site.js"></script>
</body>
</html>
"""


def page_header(crumbs, heading, sub, actions=""):
    """Breadcrumb + H1 + action buttons — used at the top of every content view."""
    cr = ""
    if crumbs:
        parts = []
        for i, (label, href) in enumerate(crumbs):
            last = i == len(crumbs) - 1
            if last or not href:
                parts.append('<li class="breadcrumb-item active" aria-current="page">%s</li>' % label)
            else:
                parts.append('<li class="breadcrumb-item"><a href="%s">%s</a></li>' % (href, label))
        cr = '<ol class="breadcrumb">%s</ol>' % "".join(parts)
    return """<div class="page-head">
  <div>
    %s
    <h1>%s</h1>
    <p class="sub">%s</p>
  </div>
  <div class="d-flex gap-2 flex-wrap no-print">%s</div>
</div>""" % (cr, heading, sub, actions)


def build():
    import pages_core, pages_clinical, pages_billing
    pages = {}
    pages.update(pages_core.PAGES)
    pages.update(pages_clinical.PAGES)
    pages.update(pages_billing.PAGES)

    os.makedirs(OUT, exist_ok=True)
    for fname, p in pages.items():
        tpl = BARE if p.get("bare") else SHELL
        subs = {"{title}": p["title"], "{font}": FONT, "{bs}": BS_CSS, "{bi}": BI_CSS,
                "{bsjs}": BS_JS, "{nav}": nav_html(fname), "{razor}": p.get("razor", ""),
                "{body}": p["body"]}
        html_out = tpl
        for k, v in subs.items():          # plain replace: page bodies may contain { }
            html_out = html_out.replace(k, v)
        with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
            f.write(html_out)
    print("built %d pages -> %s" % (len(pages), OUT))

    # ---- link check: every internal href must resolve to a generated file ----
    bad = []
    for fname in os.listdir(OUT):
        if not fname.endswith(".html"):
            continue
        src = open(os.path.join(OUT, fname), encoding="utf-8").read()
        for href in re.findall(r'href="([^"]+)"', src):
            if href.startswith(("http", "#", "mailto:", "tel:")):
                continue
            target = href.split("?")[0].split("#")[0]
            if not target:
                continue
            if not os.path.exists(os.path.join(OUT, target)):
                bad.append((fname, href))
    if bad:
        print("BROKEN LINKS:")
        for f, h in bad:
            print("  %s -> %s" % (f, h))
        sys.exit(1)
    print("link check: OK (no dead internal links)")


if __name__ == "__main__":
    build()
