# -*- coding: utf-8 -*-
"""Cover page, authentication, role dashboards, patient screens, administration."""
from ui import head, kpi, card, card_flush, table, person, pill, field, txt, sel, area

PAGES = {}

# =========================================================================
# 0. index.html — prototype cover / screen map  (not part of the MVC app)
# =========================================================================
SITEMAP = [
    ("AccountController", "/Views/Account/", [
        ("Login", "account-login.html", "Sign in, role selection, forgot password"),
        ("AccessDenied", "error-access-denied.html", "Shown when a role lacks permission"),
    ]),
    ("DashboardController", "/Views/Dashboard/", [
        ("Admin", "dashboard-admin.html", "Practice KPIs, revenue, chair utilisation, alerts"),
        ("Dentist", "dashboard-dentist.html", "My day: chair list, next patient, pending notes"),
        ("Reception", "dashboard-reception.html", "Arrivals queue, check-in, payments due today"),
    ]),
    ("PatientsController", "/Views/Patients/", [
        ("Index", "patients-index.html", "Searchable, filterable patient register"),
        ("Create", "patients-create.html", "Registration wizard — demographics, medical, insurance, consent"),
        ("Details", "patients-details.html", "Full record: timeline, appointments, chart, invoices, files"),
    ]),
    ("AppointmentsController", "/Views/Appointments/", [
        ("Calendar", "appointments-calendar.html", "Week grid by chair/dentist, drag-to-book slots"),
        ("Index", "appointments-index.html", "List view with status filters and bulk actions"),
        ("Create", "appointments-create.html", "Booking form — patient, procedure, dentist, slot"),
        ("Reschedule", "appointments-reschedule.html", "Move / cancel with reason and notification"),
        ("WaitingList", "appointments-waitlist.html", "Standby patients to slot into cancellations"),
    ]),
    ("TreatmentsController", "/Views/Treatments/", [
        ("Chart", "treatments-chart.html", "Interactive odontogram + per-tooth history"),
        ("Plan", "treatments-plan.html", "Phased treatment plan with estimate and consent"),
        ("Procedures", "treatments-procedures.html", "Procedure / fee catalogue (ADA-style codes)"),
        ("Prescriptions", "treatments-prescriptions.html", "Prescription pad and history"),
    ]),
    ("BillingController", "/Views/Billing/", [
        ("Invoices", "billing-invoices.html", "Invoice register with ageing and status"),
        ("InvoiceDetails", "billing-invoice-details.html", "Printable invoice with line items and payments"),
        ("CreateInvoice", "billing-invoice-create.html", "Build an invoice from completed procedures"),
        ("Payments", "billing-payments.html", "Payment ledger, take payment, refunds"),
        ("Claims", "billing-claims.html", "Insurance claim tracking and resubmission"),
    ]),
    ("ReportsController", "/Views/Reports/", [
        ("Index", "reports-index.html", "Revenue, production, no-shows, recall performance"),
    ]),
    ("AdminController", "/Views/Admin/", [
        ("Users", "admin-users.html", "Staff accounts, roles and permissions matrix"),
        ("Clinic", "admin-clinic.html", "Locations, chairs/operatories, working hours"),
        ("Settings", "admin-settings.html", "Branding, reminders, taxes, numbering, integrations"),
    ]),
]


def _sitemap_html():
    out = ['<div class="sitemap">']
    for ctrl, path, actions in SITEMAP:
        out.append('<div class="ctrl">%s <code>%s</code></div><ul>' % (ctrl, path))
        for name, file, desc in actions:
            out.append('<li><a href="%s"><i class="bi bi-arrow-right-short"></i>%s</a> '
                       '<span class="text-muted">— %s</span></li>' % (file, name, desc))
        out.append('</ul>')
    out.append('</div>')
    return "\n".join(out)


_roles_cards = """
<div class="row g-3">
  <div class="col-md-4">
    <a href="#" data-set-role="Admin" data-go="home" class="card-x h-100 d-block p-4 text-decoration-none">
      <div class="ic ic-teal mb-3" style="width:46px;height:46px;border-radius:14px;display:grid;place-items:center"><i class="bi bi-shield-lock" style="font-size:20px"></i></div>
      <div class="fw-semibold text-dark">Enter as Admin</div>
      <div class="text-muted small mt-1">Everything: clinic KPIs, users &amp; roles, fees, reports, settings.</div>
    </a>
  </div>
  <div class="col-md-4">
    <a href="#" data-set-role="Dentist" data-go="home" class="card-x h-100 d-block p-4 text-decoration-none">
      <div class="ic ic-purple mb-3" style="width:46px;height:46px;border-radius:14px;display:grid;place-items:center"><i class="bi bi-person-vcard" style="font-size:20px"></i></div>
      <div class="fw-semibold text-dark">Enter as Dentist</div>
      <div class="text-muted small mt-1">Clinical only: my day, charting, treatment plans, prescriptions.</div>
    </a>
  </div>
  <div class="col-md-4">
    <a href="#" data-set-role="Receptionist" data-go="home" class="card-x h-100 d-block p-4 text-decoration-none">
      <div class="ic ic-blue mb-3" style="width:46px;height:46px;border-radius:14px;display:grid;place-items:center"><i class="bi bi-headset" style="font-size:20px"></i></div>
      <div class="fw-semibold text-dark">Enter as Receptionist</div>
      <div class="text-muted small mt-1">Front desk: arrivals, booking, waiting list, payments.</div>
    </a>
  </div>
</div>"""

PAGES["index.html"] = {
    "title": "Screen map",
    "bare": True,
    "body": """
<div style="background:linear-gradient(150deg,#0d1b2a 0%,#0b4f4a 60%,#0e8f84 100%);color:#fff;padding:46px 0 54px">
  <div class="container" style="max-width:1080px">
    <div class="d-flex align-items-center gap-3 mb-4">
      <span class="logo" style="width:44px;height:44px;border-radius:13px;background:rgba(255,255,255,.15);display:grid;place-items:center;font-size:21px"><i class="bi bi-hexagon-fill"></i></span>
      <div>
        <div style="font-size:20px;font-weight:700;letter-spacing:-.02em">DentaSuite</div>
        <div style="font-size:12px;opacity:.75;letter-spacing:.08em;text-transform:uppercase">ASP.NET MVC interface prototype</div>
      </div>
    </div>
    <h1 style="color:#fff;font-size:34px;max-width:760px;line-height:1.2">Every screen your clinic runs on — menus, hierarchy and styling, ready to approve.</h1>
    <p style="max-width:700px;opacity:.85;font-size:15px;margin-top:14px">
      This is the interface layer only: Razor views, layout, navigation and controllers with stubbed actions.
      No data access, no domain logic — your models and services drop straight in.
      Click through as any of the three roles and see how the navigation and screens change.
    </p>
    <div class="d-flex gap-2 flex-wrap mt-4">
      <a href="account-login.html" class="btn btn-light fw-semibold"><i class="bi bi-box-arrow-in-right me-1"></i>Start at the sign-in screen</a>
      <a href="#map" class="btn btn-outline-light"><i class="bi bi-diagram-2 me-1"></i>See the page hierarchy</a>
    </div>
  </div>
</div>

<div class="container py-5" style="max-width:1080px">
  <h2 class="mb-1">Pick a role</h2>
  <p class="text-muted mb-4">The role you choose is remembered as you navigate — the sidebar, dashboard and in-page controls all adapt.</p>
  """ + _roles_cards + """

  <div class="row g-3 mt-4">
    <div class="col-md-4">""" + card("", """<div class="d-flex gap-3"><i class="bi bi-columns-gap text-secondary" style="font-size:20px"></i>
      <div><div class="fw-semibold">Clean separation</div><div class="text-muted small">Views hold markup only. Every value is a placeholder where a view-model property will go — no queries, no services, nothing to unpick.</div></div></div>""") + """</div>
    <div class="col-md-4">""" + card("", """<div class="d-flex gap-3"><i class="bi bi-palette text-secondary" style="font-size:20px"></i>
      <div><div class="fw-semibold">Skinnable</div><div class="text-muted small">Bootstrap 5 plus one stylesheet built entirely on CSS variables — change six values in <code>:root</code> and the whole suite re-skins.</div></div></div>""") + """</div>
    <div class="col-md-4">""" + card("", """<div class="d-flex gap-3"><i class="bi bi-phone text-secondary" style="font-size:20px"></i>
      <div><div class="fw-semibold">Responsive</div><div class="text-muted small">Tested at 360, 768, 1024 and 1440 px. Sidebar collapses to an off-canvas drawer, tables scroll, forms stack.</div></div></div>""") + """</div>
  </div>

  <hr class="my-5">

  <h2 id="map" class="mb-1">Page hierarchy</h2>
  <p class="text-muted mb-4">Controller → action → view. Every link below is a working screen in this prototype.</p>
  """ + card("", _sitemap_html()) + """

  <p class="text-muted small mt-4 mb-0">Prototype only — all names, figures and clinical data on these screens are fictional sample content.</p>
</div>
"""}

# =========================================================================
# 1. account-login.html
# =========================================================================
PAGES["account-login.html"] = {
    "title": "Sign in",
    "bare": True,
    "body": """
<div class="auth">
  <div class="auth-art">
    <div class="d-flex align-items-center gap-3">
      <span style="width:42px;height:42px;border-radius:13px;background:rgba(255,255,255,.16);display:grid;place-items:center;font-size:20px"><i class="bi bi-hexagon-fill"></i></span>
      <div style="font-size:19px;font-weight:700">DentaSuite</div>
    </div>
    <div style="position:relative;z-index:2">
      <h2 style="color:#fff;font-size:30px;line-height:1.25;max-width:440px">One place for patients, chairs, charts and cash-flow.</h2>
      <p style="opacity:.8;max-width:420px;margin-top:14px">Registration, scheduling, clinical charting, invoicing and payments — with each role seeing exactly what it needs and nothing more.</p>
      <div class="d-flex gap-4 mt-4" style="opacity:.9">
        <div><div style="font-size:22px;font-weight:700">3</div><div style="font-size:12px;opacity:.75">roles</div></div>
        <div><div style="font-size:22px;font-weight:700">8</div><div style="font-size:12px;opacity:.75">controllers</div></div>
        <div><div style="font-size:22px;font-weight:700">25</div><div style="font-size:12px;opacity:.75">views</div></div>
      </div>
    </div>
    <div style="font-size:12px;opacity:.6;position:relative;z-index:2">Interface prototype · Views/Account/Login.cshtml</div>
  </div>

  <div class="auth-form">
    <div class="inner">
      <h1 class="mb-1" style="font-size:24px">Sign in</h1>
      <p class="text-muted mb-4" style="font-size:13.5px">Welcome back. Use your clinic account to continue.</p>

      <div class="mb-3">
        <label class="form-label">Email or staff ID</label>
        <input class="form-control" placeholder="you@clinic.com" value="a.okafor@brightsmile.clinic">
      </div>
      <div class="mb-3">
        <label class="form-label">Password</label>
        <div class="input-group">
          <input class="form-control" type="password" value="password">
          <button class="btn btn-soft" type="button"><i class="bi bi-eye"></i></button>
        </div>
      </div>

      <div class="section-title mt-4">Sign in as (prototype)</div>
      <div class="d-grid gap-2 mb-3">
        <a href="#" data-set-role="Admin" data-go="home" class="role-card">
          <span class="avatar">AO</span>
          <span class="lh-sm"><span class="d-block fw-semibold" style="font-size:13.5px">Dr. Amara Okafor</span>
          <span class="d-block text-muted" style="font-size:12px">Practice Administrator</span></span>
          <i class="bi bi-arrow-right ms-auto text-muted"></i>
        </a>
        <a href="#" data-set-role="Dentist" data-go="home" class="role-card">
          <span class="avatar">LB</span>
          <span class="lh-sm"><span class="d-block fw-semibold" style="font-size:13.5px">Dr. Luca Bianchi</span>
          <span class="d-block text-muted" style="font-size:12px">Dentist — Chair 2</span></span>
          <i class="bi bi-arrow-right ms-auto text-muted"></i>
        </a>
        <a href="#" data-set-role="Receptionist" data-go="home" class="role-card">
          <span class="avatar">PN</span>
          <span class="lh-sm"><span class="d-block fw-semibold" style="font-size:13.5px">Priya Nair</span>
          <span class="d-block text-muted" style="font-size:12px">Front Desk</span></span>
          <i class="bi bi-arrow-right ms-auto text-muted"></i>
        </a>
      </div>

      <div class="d-flex justify-content-between align-items-center mb-3">
        <div class="form-check">
          <input class="form-check-input" type="checkbox" id="rm" checked>
          <label class="form-check-label small" for="rm">Keep me signed in</label>
        </div>
        <a href="#" class="small text-muted">Forgot password?</a>
      </div>

      <p class="text-center text-muted small mb-0">
        Prototype — <a href="index.html">back to the screen map</a>
      </p>
    </div>
  </div>
</div>
"""}

# =========================================================================
# 2. dashboard-admin.html
# =========================================================================
_admin_kpis = (
    kpi("bi-calendar-check", "teal", "48", "Appointments today", "▲ 6 vs last Thursday") +
    kpi("bi-currency-dollar", "green", "$9,420", "Production today", "▲ 12% vs target") +
    kpi("bi-person-plus", "blue", "7", "New patients this week", "▲ 2") +
    kpi("bi-exclamation-triangle", "amber", "$14,760", "Outstanding &gt; 30 days", "▼ $1,200", "text-danger")
)

_chair_rows = "".join(
    '<tr><td><span class="t-main">%s</span><div class="t-sub">%s</div></td>'
    '<td style="min-width:180px"><div class="stat-bar"><span style="width:%s"></span></div></td>'
    '<td class="text-end fw-semibold">%s</td></tr>' % r
    for r in [
        ("Chair 1", "Dr. Amara Okafor", "88%", "88%"),
        ("Chair 2", "Dr. Luca Bianchi", "74%", "74%"),
        ("Chair 3", "Dr. Sofia Reyes", "61%", "61%"),
        ("Hygiene 1", "M. Adeyemi, RDH", "93%", "93%"),
    ])

_revenue_bars = "".join('<div class="b%s" style="height:%s"></div>' % (m, h) for m, h in
                        [("", "46%"), ("", "62%"), ("", "55%"), ("", "78%"), ("", "70%"),
                         ("", "88%"), (" mut", "34%")])

PAGES["dashboard-admin.html"] = {
    "title": "Dashboard",
    "razor": "Views/Dashboard/Admin.cshtml",
    "body": head([("Home", "dashboard-admin.html"), ("Dashboard", "")],
                 "Practice dashboard",
                 "Thursday, 14 August 2026 · Bright Smile Dental — Riverside",
                 '<a class="btn btn-soft" href="reports-index.html"><i class="bi bi-bar-chart-line me-1"></i>Reports</a>'
                 '<a class="btn btn-brand" href="appointments-create.html"><i class="bi bi-calendar-plus me-1"></i>Book appointment</a>') + """
<div class="row g-3 mb-3">""" + _admin_kpis + """</div>

<div class="row g-3">
  <div class="col-xl-8">
    """ + card("Production — last 7 days", """
      <div class="d-flex align-items-end justify-content-between mb-3">
        <div><div style="font-size:26px;font-weight:700;letter-spacing:-.03em">$52,180</div>
        <div class="text-muted small">Collected this week · <span class="text-success fw-semibold">▲ 9.4%</span> vs previous</div></div>
        <div class="d-none d-sm-flex gap-3 small text-muted">
          <span><i class="bi bi-square-fill" style="color:var(--brand-500)"></i> Produced</span>
          <span><i class="bi bi-square-fill" style="color:#c3cedb"></i> Today (partial)</span>
        </div>
      </div>
      <div class="mini-bars">""" + _revenue_bars + """</div>
      <div class="bars-x"><span>Fri</span><span>Sat</span><span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Today</span></div>
    """, actions='<select class="form-select form-select-sm" style="width:auto"><option>Last 7 days</option><option>This month</option><option>This quarter</option></select>') + """
  </div>
  <div class="col-xl-4">
    """ + card_flush("Chair utilisation", table(
        ["Chair", "Utilisation", ("", ' class="text-end"')], [_chair_rows]),
        sub="Booked vs available hours, today") + """
  </div>
</div>

<div class="row g-3 mt-0">
  <div class="col-xl-7">
    """ + card_flush("Next appointments", table(
        ["Time", "Patient", "Procedure", "Dentist", "Status", ""],
        ["".join([
            '<tr><td class="fw-semibold">09:30</td><td>' + person("MK", "Marcus Kelly", "PT-10428") +
            '</td><td>Composite filling <span class="t-sub d-block">#26 occlusal</span></td><td>Dr. Bianchi</td><td>' +
            pill("Checked in", "green") + '</td><td class="text-end"><a class="btn btn-soft btn-sm" href="patients-details.html">Open</a></td></tr>',
            '<tr><td class="fw-semibold">10:00</td><td>' + person("EW", "Elena Whitfield", "PT-10391") +
            '</td><td>Scale &amp; polish</td><td>M. Adeyemi</td><td>' + pill("Confirmed", "blue") +
            '</td><td class="text-end"><a class="btn btn-soft btn-sm" href="patients-details.html">Open</a></td></tr>',
            '<tr><td class="fw-semibold">10:45</td><td>' + person("TA", "Tobias Ackerman", "PT-10502") +
            '</td><td>Crown fit <span class="t-sub d-block">#36 zirconia</span></td><td>Dr. Okafor</td><td>' +
            pill("Confirmed", "blue") + '</td><td class="text-end"><a class="btn btn-soft btn-sm" href="patients-details.html">Open</a></td></tr>',
            '<tr><td class="fw-semibold">11:30</td><td>' + person("RJ", "Rania Jabari", "PT-10233") +
            '</td><td>Root canal — session 2</td><td>Dr. Bianchi</td><td>' + pill("Unconfirmed", "amber") +
            '</td><td class="text-end"><a class="btn btn-soft btn-sm" href="appointments-reschedule.html">Chase</a></td></tr>',
            '<tr><td class="fw-semibold">12:15</td><td>' + person("DS", "Daniel Sorenson", "PT-10477") +
            '</td><td>Consultation — implant</td><td>Dr. Okafor</td><td>' + pill("New patient", "purple") +
            '</td><td class="text-end"><a class="btn btn-soft btn-sm" href="patients-details.html">Open</a></td></tr>',
        ])]),
        actions='<a class="btn btn-ghost btn-sm" href="appointments-calendar.html">Open calendar <i class="bi bi-arrow-right"></i></a>') + """
  </div>

  <div class="col-xl-5">
    """ + card("Needs attention", """
      <div class="d-grid gap-2">
        <a href="billing-claims.html" class="d-flex align-items-center gap-3 p-2 rounded" style="border:1px solid var(--line)">
          <span class="ic ic-red" style="width:36px;height:36px;border-radius:11px;display:grid;place-items:center"><i class="bi bi-shield-exclamation"></i></span>
          <span class="lh-sm"><span class="d-block fw-semibold text-dark" style="font-size:13.5px">3 insurance claims rejected</span>
          <span class="d-block text-muted" style="font-size:12px">Oldest 9 days · $2,140 at risk</span></span>
          <i class="bi bi-chevron-right ms-auto text-muted"></i>
        </a>
        <a href="appointments-waitlist.html" class="d-flex align-items-center gap-3 p-2 rounded" style="border:1px solid var(--line)">
          <span class="ic ic-amber" style="width:36px;height:36px;border-radius:11px;display:grid;place-items:center"><i class="bi bi-hourglass-split"></i></span>
          <span class="lh-sm"><span class="d-block fw-semibold text-dark" style="font-size:13.5px">6 patients waiting for a slot</span>
          <span class="d-block text-muted" style="font-size:12px">2 flagged urgent</span></span>
          <i class="bi bi-chevron-right ms-auto text-muted"></i>
        </a>
        <a href="billing-invoices.html" class="d-flex align-items-center gap-3 p-2 rounded" style="border:1px solid var(--line)">
          <span class="ic ic-blue" style="width:36px;height:36px;border-radius:11px;display:grid;place-items:center"><i class="bi bi-receipt"></i></span>
          <span class="lh-sm"><span class="d-block fw-semibold text-dark" style="font-size:13.5px">11 invoices overdue</span>
          <span class="d-block text-muted" style="font-size:12px">$14,760 outstanding beyond 30 days</span></span>
          <i class="bi bi-chevron-right ms-auto text-muted"></i>
        </a>
        <a href="patients-index.html" class="d-flex align-items-center gap-3 p-2 rounded" style="border:1px solid var(--line)">
          <span class="ic ic-teal" style="width:36px;height:36px;border-radius:11px;display:grid;place-items:center"><i class="bi bi-arrow-repeat"></i></span>
          <span class="lh-sm"><span class="d-block fw-semibold text-dark" style="font-size:13.5px">34 recalls due this month</span>
          <span class="d-block text-muted" style="font-size:12px">18 not yet contacted</span></span>
          <i class="bi bi-chevron-right ms-auto text-muted"></i>
        </a>
      </div>
    """) + """
    <div class="mt-3">
    """ + card("Recent activity", """
      <div class="tl">
        <div class="tl-item"><span class="dot"></span><div class="tl-t">Invoice INV-2478 paid — $310</div><div class="tl-m">Priya Nair · 12 minutes ago</div></div>
        <div class="tl-item"><span class="dot"></span><div class="tl-t">Treatment plan approved — R. Jabari</div><div class="tl-m">Dr. Luca Bianchi · 40 minutes ago</div></div>
        <div class="tl-item"><span class="dot"></span><div class="tl-t">New patient registered — D. Sorenson</div><div class="tl-m">Priya Nair · 1 hour ago</div></div>
        <div class="tl-item"><span class="dot"></span><div class="tl-t">Appointment cancelled — 15:00 Chair 3</div><div class="tl-m">Patient request · 2 hours ago</div></div>
      </div>
    """) + """
    </div>
  </div>
</div>
"""}

# =========================================================================
# 3. dashboard-dentist.html
# =========================================================================
PAGES["dashboard-dentist.html"] = {
    "title": "My day",
    "razor": "Views/Dashboard/Dentist.cshtml",
    "body": head([("Home", "dashboard-dentist.html"), ("My day", "")],
                 "My day",
                 "Thursday, 14 August 2026 · Chair 2 · 8 patients booked",
                 '<a class="btn btn-soft" href="treatments-plan.html"><i class="bi bi-clipboard2-pulse me-1"></i>Treatment plans</a>'
                 '<a class="btn btn-brand" href="treatments-chart.html"><i class="bi bi-diagram-3 me-1"></i>Open chart</a>') + """
<div class="row g-3 mb-3">""" + (
        kpi("bi-people", "teal", "8", "Patients today") +
        kpi("bi-clock-history", "blue", "5h 40m", "Chair time booked") +
        kpi("bi-pencil-square", "amber", "3", "Clinical notes unsigned") +
        kpi("bi-clipboard-check", "green", "2", "Plans awaiting consent")) + """
</div>

<div class="row g-3">
  <div class="col-xl-5">
    """ + card("Now in the chair", """
      <div class="d-flex gap-3 align-items-start">
        <span class="avatar lg">MK</span>
        <div class="flex-grow-1">
          <div class="d-flex align-items-center gap-2 flex-wrap">
            <h3 style="font-size:17px;margin:0">Marcus Kelly</h3>""" + pill("In chair", "green") + """
          </div>
          <div class="text-muted small">PT-10428 · 34 y · Male · Last visit 12 Feb 2026</div>
          <div class="mt-2 d-flex gap-2 flex-wrap">
            <span class="pill pill-red"><i class="bi bi-exclamation-triangle-fill"></i>Penicillin allergy</span>
            <span class="pill pill-amber"><i class="bi bi-heart-pulse-fill"></i>Hypertension</span>
          </div>
        </div>
      </div>
      <hr>
      <dl class="dl-x row">
        <div class="col-6"><dt>Booked procedure</dt><dd>Composite filling — #26 occlusal</dd></div>
        <div class="col-6"><dt>Slot</dt><dd>09:30 – 10:00 · Chair 2</dd></div>
        <div class="col-6"><dt>Anaesthetic</dt><dd>Articaine 4% 1:100k</dd></div>
        <div class="col-6"><dt>Plan phase</dt><dd>Phase 1 of 3</dd></div>
      </dl>
      <div class="d-flex gap-2 flex-wrap">
        <a class="btn btn-brand btn-sm" href="treatments-chart.html"><i class="bi bi-diagram-3 me-1"></i>Chart</a>
        <a class="btn btn-soft btn-sm" href="treatments-plan.html"><i class="bi bi-clipboard2-pulse me-1"></i>Plan</a>
        <a class="btn btn-soft btn-sm" href="treatments-prescriptions.html"><i class="bi bi-capsule me-1"></i>Prescribe</a>
        <a class="btn btn-soft btn-sm" href="patients-details.html"><i class="bi bi-folder2-open me-1"></i>Record</a>
      </div>
    """, sub="09:30 · started 6 minutes ago") + """
  </div>

  <div class="col-xl-7">
    """ + card_flush("My schedule", table(
        ["Time", "Patient", "Procedure", "Status", ""],
        ["".join([
            '<tr><td class="fw-semibold">09:30</td><td>' + person("MK", "Marcus Kelly", "PT-10428") +
            '</td><td>Composite filling #26</td><td>' + pill("In chair", "green") +
            '</td><td class="text-end"><a class="btn btn-soft btn-sm" href="treatments-chart.html">Chart</a></td></tr>',
            '<tr><td class="fw-semibold">10:15</td><td>' + person("RJ", "Rania Jabari", "PT-10233") +
            '</td><td>Root canal — session 2</td><td>' + pill("Confirmed", "blue") +
            '</td><td class="text-end"><a class="btn btn-soft btn-sm" href="treatments-chart.html">Chart</a></td></tr>',
            '<tr><td class="fw-semibold">11:00</td><td>' + person("HN", "Hugo Nakamura", "PT-10310") +
            '</td><td>Extraction #48</td><td>' + pill("Confirmed", "blue") +
            '</td><td class="text-end"><a class="btn btn-soft btn-sm" href="treatments-chart.html">Chart</a></td></tr>',
            '<tr><td class="fw-semibold">11:45</td><td class="text-muted" colspan="4"><em>Break — 30 min</em></td></tr>',
            '<tr><td class="fw-semibold">12:15</td><td>' + person("SN", "Sara Nowak", "PT-10188") +
            '</td><td>Review — implant site</td><td>' + pill("Confirmed", "blue") +
            '</td><td class="text-end"><a class="btn btn-soft btn-sm" href="treatments-chart.html">Chart</a></td></tr>',
            '<tr><td class="fw-semibold">14:00</td><td>' + person("AC", "Aisha Chowdhury", "PT-10455") +
            '</td><td>Crown prep #16</td><td>' + pill("Unconfirmed", "amber") +
            '</td><td class="text-end"><a class="btn btn-soft btn-sm" href="treatments-chart.html">Chart</a></td></tr>',
            '<tr><td class="fw-semibold">15:00</td><td>' + person("PL", "Peter Lindqvist", "PT-10099") +
            '</td><td>Denture adjustment</td><td>' + pill("Confirmed", "blue") +
            '</td><td class="text-end"><a class="btn btn-soft btn-sm" href="treatments-chart.html">Chart</a></td></tr>',
        ])]),
        actions='<a class="btn btn-ghost btn-sm" href="appointments-calendar.html">Week view <i class="bi bi-arrow-right"></i></a>') + """
  </div>
</div>

<div class="row g-3 mt-0">
  <div class="col-xl-7">
    """ + card_flush("Clinical notes awaiting signature", table(
        ["Patient", "Visit", "Procedure", ""],
        ["".join([
            '<tr><td>' + person("EW", "Elena Whitfield", "PT-10391") + '</td><td>12 Aug 2026</td>'
            '<td>Scale &amp; polish</td><td class="text-end"><a class="btn btn-soft btn-sm" href="treatments-chart.html">Review &amp; sign</a></td></tr>',
            '<tr><td>' + person("TA", "Tobias Ackerman", "PT-10502") + '</td><td>11 Aug 2026</td>'
            '<td>Crown prep #36</td><td class="text-end"><a class="btn btn-soft btn-sm" href="treatments-chart.html">Review &amp; sign</a></td></tr>',
            '<tr><td>' + person("HN", "Hugo Nakamura", "PT-10310") + '</td><td>08 Aug 2026</td>'
            '<td>Emergency exam</td><td class="text-end"><a class="btn btn-soft btn-sm" href="treatments-chart.html">Review &amp; sign</a></td></tr>',
        ])])) + """
  </div>
  <div class="col-xl-5">
    """ + card("Quick actions", """
      <div class="row g-2">
        <div class="col-6"><a href="treatments-prescriptions.html" class="btn btn-soft w-100 py-3"><i class="bi bi-capsule d-block mb-1" style="font-size:19px"></i>New prescription</a></div>
        <div class="col-6"><a href="treatments-plan.html" class="btn btn-soft w-100 py-3"><i class="bi bi-clipboard2-plus d-block mb-1" style="font-size:19px"></i>New plan</a></div>
        <div class="col-6"><a href="appointments-create.html" class="btn btn-soft w-100 py-3"><i class="bi bi-calendar-plus d-block mb-1" style="font-size:19px"></i>Book follow-up</a></div>
        <div class="col-6"><a href="patients-index.html" class="btn btn-soft w-100 py-3"><i class="bi bi-search d-block mb-1" style="font-size:19px"></i>Find patient</a></div>
      </div>
      <div class="alert alert-light border mt-3 mb-0 small">
        <i class="bi bi-info-circle me-1 text-secondary"></i>
        Billing, staff administration and practice reports are hidden for the Dentist role — switch role from the avatar menu to compare.
      </div>
    """) + """
  </div>
</div>
"""}

# =========================================================================
# 4. dashboard-reception.html
# =========================================================================
PAGES["dashboard-reception.html"] = {
    "title": "Front desk",
    "razor": "Views/Dashboard/Reception.cshtml",
    "body": head([("Home", "dashboard-reception.html"), ("Front desk", "")],
                 "Front desk",
                 "Thursday, 14 August 2026 · 48 appointments · 3 chairs running",
                 '<a class="btn btn-soft" href="patients-create.html"><i class="bi bi-person-plus me-1"></i>Register patient</a>'
                 '<a class="btn btn-brand" href="appointments-create.html"><i class="bi bi-calendar-plus me-1"></i>Book appointment</a>') + """
<div class="row g-3 mb-3">""" + (
        kpi("bi-person-check", "green", "12", "Arrived / checked in") +
        kpi("bi-hourglass-split", "amber", "3", "Waiting &gt; 10 min") +
        kpi("bi-telephone", "blue", "9", "Unconfirmed tomorrow") +
        kpi("bi-cash-coin", "teal", "$1,860", "To collect today")) + """
</div>

<div class="row g-3">
  <div class="col-xl-8">
    """ + card_flush("Arrivals", table(
        ["Time", "Patient", "Dentist / chair", "Status", "Balance", ""],
        ["".join([
            '<tr><td class="fw-semibold">09:30</td><td>' + person("MK", "Marcus Kelly", "PT-10428") +
            '</td><td>Dr. Bianchi · Chair 2</td><td>' + pill("In chair", "green") +
            '</td><td>$0.00</td><td class="text-end"><a class="btn btn-soft btn-sm" href="billing-invoice-create.html">Invoice</a></td></tr>',
            '<tr><td class="fw-semibold">09:45</td><td>' + person("EW", "Elena Whitfield", "PT-10391") +
            '</td><td>M. Adeyemi · Hygiene 1</td><td>' + pill("Waiting 14 min", "amber") +
            '</td><td>$65.00</td><td class="text-end"><a class="btn btn-soft btn-sm" href="billing-payments.html">Take payment</a></td></tr>',
            '<tr><td class="fw-semibold">10:00</td><td>' + person("TA", "Tobias Ackerman", "PT-10502") +
            '</td><td>Dr. Okafor · Chair 1</td><td>' + pill("Arrived", "blue") +
            '</td><td>$0.00</td><td class="text-end"><a class="btn btn-brand btn-sm" href="#">Check in</a></td></tr>',
            '<tr><td class="fw-semibold">10:30</td><td>' + person("RJ", "Rania Jabari", "PT-10233") +
            '</td><td>Dr. Bianchi · Chair 2</td><td>' + pill("Not arrived", "gray") +
            '</td><td>$420.00</td><td class="text-end"><a class="btn btn-soft btn-sm" href="appointments-reschedule.html">Call</a></td></tr>',
            '<tr><td class="fw-semibold">10:45</td><td>' + person("DS", "Daniel Sorenson", "PT-10477") +
            '</td><td>Dr. Okafor · Chair 1</td><td>' + pill("New — forms pending", "purple") +
            '</td><td>$0.00</td><td class="text-end"><a class="btn btn-soft btn-sm" href="patients-create.html">Finish registration</a></td></tr>',
            '<tr><td class="fw-semibold">11:15</td><td>' + person("HN", "Hugo Nakamura", "PT-10310") +
            '</td><td>Dr. Bianchi · Chair 2</td><td>' + pill("Not arrived", "gray") +
            '</td><td>$0.00</td><td class="text-end"><a class="btn btn-soft btn-sm" href="appointments-reschedule.html">Reschedule</a></td></tr>',
        ])]),
        actions='<div class="btn-group btn-group-sm"><button class="btn btn-soft active">Today</button>'
                '<button class="btn btn-soft">Tomorrow</button></div>'
                '<a class="btn btn-ghost btn-sm" href="appointments-index.html">All appointments</a>') + """
  </div>

  <div class="col-xl-4">
    """ + card("Confirmation queue", """
      <p class="text-muted small">Tomorrow, 15 August — 9 appointments still unconfirmed.</p>
      <div class="d-grid gap-2">
        <div class="d-flex align-items-center gap-2 p-2 rounded" style="border:1px solid var(--line)">""" +
                 person("AC", "Aisha Chowdhury", "08:30 · Crown prep") + """
          <div class="ms-auto d-flex gap-1">
            <button class="icon-btn" style="width:32px;height:32px" title="Call"><i class="bi bi-telephone"></i></button>
            <button class="icon-btn" style="width:32px;height:32px" title="SMS"><i class="bi bi-chat-dots"></i></button>
          </div>
        </div>
        <div class="d-flex align-items-center gap-2 p-2 rounded" style="border:1px solid var(--line)">""" +
                 person("PL", "Peter Lindqvist", "09:15 · Denture fit") + """
          <div class="ms-auto d-flex gap-1">
            <button class="icon-btn" style="width:32px;height:32px" title="Call"><i class="bi bi-telephone"></i></button>
            <button class="icon-btn" style="width:32px;height:32px" title="SMS"><i class="bi bi-chat-dots"></i></button>
          </div>
        </div>
        <div class="d-flex align-items-center gap-2 p-2 rounded" style="border:1px solid var(--line)">""" +
                 person("SN", "Sara Nowak", "11:00 · Review") + """
          <div class="ms-auto d-flex gap-1">
            <button class="icon-btn" style="width:32px;height:32px" title="Call"><i class="bi bi-telephone"></i></button>
            <button class="icon-btn" style="width:32px;height:32px" title="SMS"><i class="bi bi-chat-dots"></i></button>
          </div>
        </div>
      </div>
      <button class="btn btn-soft btn-sm w-100 mt-3"><i class="bi bi-send me-1"></i>Send all SMS reminders</button>
    """) + """
    <div class="mt-3">""" + card("Waiting list", """
      <p class="text-muted small mb-2">Patients who will take an earlier slot if one frees up.</p>
      <div class="d-flex justify-content-between align-items-center">
        <div><div class="fw-semibold">6 patients</div><div class="text-muted small">2 urgent · longest wait 11 days</div></div>
        <a class="btn btn-soft btn-sm" href="appointments-waitlist.html">Open</a>
      </div>
    """) + """</div>
  </div>
</div>
"""}

# =========================================================================
# 5. patients-index.html
# =========================================================================
_pt_rows = []
for pid, ini, name, age, phone, last, nxt, bal, status, tone in [
    ("PT-10428", "MK", "Marcus Kelly", "34 y · Male", "+1 415 220 8841", "12 Feb 2026", "Today 09:30", "$0.00", "Active", "green"),
    ("PT-10391", "EW", "Elena Whitfield", "51 y · Female", "+1 415 887 2210", "06 Mar 2026", "Today 09:45", "$65.00", "Active", "green"),
    ("PT-10502", "TA", "Tobias Ackerman", "29 y · Male", "+1 415 664 1197", "31 Jul 2026", "Today 10:45", "$0.00", "Active", "green"),
    ("PT-10233", "RJ", "Rania Jabari", "42 y · Female", "+1 415 302 5566", "29 Jul 2026", "Today 11:30", "$420.00", "Overdue", "red"),
    ("PT-10477", "DS", "Daniel Sorenson", "38 y · Male", "+1 415 118 9043", "—", "Today 12:15", "$0.00", "New", "purple"),
    ("PT-10310", "HN", "Hugo Nakamura", "63 y · Male", "+1 415 445 7781", "02 Aug 2026", "Today 11:00", "$0.00", "Active", "green"),
    ("PT-10188", "SN", "Sara Nowak", "27 y · Female", "+1 415 990 3312", "18 Jun 2026", "22 Aug 2026", "$120.00", "Active", "green"),
    ("PT-10455", "AC", "Aisha Chowdhury", "45 y · Female", "+1 415 771 6620", "10 Aug 2026", "15 Aug 2026", "$0.00", "Active", "green"),
    ("PT-10099", "PL", "Peter Lindqvist", "71 y · Male", "+1 415 233 4409", "09 Aug 2026", "—", "$0.00", "Inactive", "gray"),
    ("PT-10061", "GM", "Grace Mbeki", "19 y · Female", "+1 415 556 8890", "21 May 2026", "—", "$0.00", "Recall due", "amber"),
]:
    _pt_rows.append(
        '<tr>'
        '<td><input class="form-check-input" type="checkbox"></td>'
        '<td><a href="patients-details.html" class="text-decoration-none">' + person(ini, name, pid) + '</a></td>'
        '<td class="t-sub">' + age + '</td>'
        '<td class="t-sub">' + phone + '</td>'
        '<td>' + last + '</td>'
        '<td>' + nxt + '</td>'
        '<td class="fw-semibold">' + bal + '</td>'
        '<td>' + pill(status, tone) + '</td>'
        '<td class="text-end">'
        '<div class="dropdown"><button class="btn btn-ghost btn-sm" data-bs-toggle="dropdown"><i class="bi bi-three-dots"></i></button>'
        '<ul class="dropdown-menu dropdown-menu-end">'
        '<li><a class="dropdown-item" href="patients-details.html"><i class="bi bi-folder2-open me-2"></i>Open record</a></li>'
        '<li><a class="dropdown-item" href="appointments-create.html"><i class="bi bi-calendar-plus me-2"></i>Book appointment</a></li>'
        '<li><a class="dropdown-item" href="treatments-chart.html" data-roles="Admin,Dentist"><i class="bi bi-diagram-3 me-2"></i>Dental chart</a></li>'
        '<li><a class="dropdown-item" href="billing-invoice-create.html" data-roles="Admin,Receptionist"><i class="bi bi-receipt me-2"></i>New invoice</a></li>'
        '<li><hr class="dropdown-divider"></li>'
        '<li><a class="dropdown-item text-danger" href="#" data-roles="Admin"><i class="bi bi-archive me-2"></i>Archive patient</a></li>'
        '</ul></div></td></tr>')

PAGES["patients-index.html"] = {
    "title": "Patients",
    "razor": "Views/Patients/Index.cshtml",
    "body": head([("Home", "dashboard-admin.html"), ("Patients", "")],
                 "Patients",
                 "2,418 registered · 1,904 active",
                 '<button class="btn btn-soft" data-roles="Admin"><i class="bi bi-upload me-1"></i>Export</button>'
                 '<a class="btn btn-brand" href="patients-create.html" data-roles="Admin,Receptionist"><i class="bi bi-person-plus me-1"></i>Register patient</a>') + """
""" + card("", """
<div class="row g-2 align-items-end">
  <div class="col-lg-4 col-md-6">
    <label class="form-label">Search</label>
    <div class="input-group">
      <span class="input-group-text bg-white border-end-0"><i class="bi bi-search text-muted"></i></span>
      <input class="form-control border-start-0" placeholder="Name, patient ID, phone or email">
    </div>
  </div>
  <div class="col-lg-2 col-md-3 col-6">
    <label class="form-label">Status</label>
    """ + sel(["All statuses", "Active", "New", "Recall due", "Overdue", "Inactive"]) + """
  </div>
  <div class="col-lg-2 col-md-3 col-6">
    <label class="form-label">Primary dentist</label>
    """ + sel(["All dentists", "Dr. Amara Okafor", "Dr. Luca Bianchi", "Dr. Sofia Reyes"]) + """
  </div>
  <div class="col-lg-2 col-md-3 col-6">
    <label class="form-label">Last visit</label>
    """ + sel(["Any time", "Last 30 days", "Last 6 months", "Over 12 months ago"]) + """
  </div>
  <div class="col-lg-2 col-md-3 col-6 d-flex gap-2">
    <button class="btn btn-brand flex-grow-1">Apply</button>
    <button class="btn btn-soft"><i class="bi bi-x-lg"></i></button>
  </div>
</div>
""") + """

<div class="mt-3">
""" + card_flush("", table(
        [('<input class="form-check-input" type="checkbox">', ' style="width:34px"'),
         "Patient", "Age / sex", "Phone", "Last visit", "Next appointment", "Balance", "Status",
         ("", ' class="text-end"')],
        ["".join(_pt_rows)]),
        foot="""<div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
  <span class="text-muted small">Showing 1–10 of 2,418</span>
  <nav><ul class="pagination pagination-sm mb-0">
    <li class="page-item disabled"><span class="page-link">Previous</span></li>
    <li class="page-item active"><span class="page-link">1</span></li>
    <li class="page-item"><a class="page-link" href="#">2</a></li>
    <li class="page-item"><a class="page-link" href="#">3</a></li>
    <li class="page-item"><a class="page-link" href="#">Next</a></li>
  </ul></nav>
</div>""") + """
</div>
"""}

# =========================================================================
# 6. patients-create.html
# =========================================================================
PAGES["patients-create.html"] = {
    "title": "Register patient",
    "razor": "Views/Patients/Create.cshtml",
    "body": head([("Home", "dashboard-admin.html"), ("Patients", "patients-index.html"), ("Register", "")],
                 "Register a new patient",
                 "Step 1 of 4 — personal details",
                 '<a class="btn btn-soft" href="patients-index.html">Cancel</a>'
                 '<button class="btn btn-brand">Save &amp; continue <i class="bi bi-arrow-right ms-1"></i></button>') + """
<div class="steps mb-3">
  <span class="step active"><span class="n">1</span>Personal</span>
  <span class="step"><span class="n">2</span>Medical history</span>
  <span class="step"><span class="n">3</span>Insurance</span>
  <span class="step"><span class="n">4</span>Consent &amp; documents</span>
</div>

<div class="row g-3">
  <div class="col-xl-8">
    """ + card("Personal details", """
      <div class="section-title">Identity</div>
      <div class="row">
        """ + field("Title", sel(["Mr", "Mrs", "Ms", "Dr", "Mx"]), "col-md-2") + """
        """ + field("First name", txt("e.g. Daniel"), "col-md-5", req=True) + """
        """ + field("Last name", txt("e.g. Sorenson"), "col-md-5", req=True) + """
        """ + field("Date of birth", txt("", "", "date"), "col-md-4", req=True) + """
        """ + field("Sex", sel(["Select…", "Female", "Male", "Other", "Prefer not to say"]), "col-md-4") + """
        """ + field("Patient ID", txt("Auto-generated", "PT-10503"), "col-md-4",
                    hint="Generated by the server; shown read-only in the real app.") + """
      </div>

      <div class="section-title">Contact</div>
      <div class="row">
        """ + field("Mobile", txt("+1 415 000 0000"), "col-md-4", req=True) + """
        """ + field("Alternate phone", txt("Optional"), "col-md-4") + """
        """ + field("Email", txt("name@example.com", "", "email"), "col-md-4") + """
        """ + field("Address line 1", txt("Street and number"), "col-md-8") + """
        """ + field("Postcode", txt(""), "col-md-4") + """
        """ + field("City", txt(""), "col-md-4") + """
        """ + field("State / region", txt(""), "col-md-4") + """
        """ + field("Country", sel(["United States", "United Kingdom", "Canada", "Australia", "Other"]), "col-md-4") + """
        """ + field("Preferred contact", sel(["SMS", "Email", "Phone call", "WhatsApp"]), "col-md-4",
                    hint="Used for appointment reminders.") + """
      </div>

      <div class="section-title">Clinic</div>
      <div class="row">
        """ + field("Primary dentist", sel(["Unassigned", "Dr. Amara Okafor", "Dr. Luca Bianchi", "Dr. Sofia Reyes"]), "col-md-4") + """
        """ + field("Referral source", sel(["Walk-in", "Google", "Existing patient", "Insurer directory", "Other clinic"]), "col-md-4") + """
        """ + field("Recall interval", sel(["6 months", "3 months", "12 months", "None"]), "col-md-4") + """
        """ + field("Internal note", area("Anything the team should know before the first visit…", 3), "col-12") + """
      </div>
    """, foot="""<div class="d-flex justify-content-between flex-wrap gap-2">
      <button class="btn btn-soft" disabled><i class="bi bi-arrow-left me-1"></i>Back</button>
      <div class="d-flex gap-2">
        <button class="btn btn-soft">Save as draft</button>
        <button class="btn btn-brand">Save &amp; continue<i class="bi bi-arrow-right ms-1"></i></button>
      </div>
    </div>""") + """
  </div>

  <div class="col-xl-4">
    """ + card("Emergency contact", """
      <div class="row">
        """ + field("Full name", txt(""), "col-12") + """
        """ + field("Relationship", sel(["Spouse", "Parent", "Child", "Sibling", "Friend", "Other"]), "col-12") + """
        """ + field("Phone", txt("+1 415 000 0000"), "col-12") + """
      </div>
    """) + """
    <div class="mt-3">""" + card("Photo &amp; documents", """
      <div class="text-center p-4 rounded" style="border:1.5px dashed var(--line);background:#fbfdfe">
        <i class="bi bi-cloud-arrow-up text-muted" style="font-size:26px"></i>
        <div class="fw-semibold mt-2" style="font-size:13.5px">Drop files here</div>
        <div class="text-muted small">ID, referral letter, radiographs · PDF, JPG, PNG</div>
        <button class="btn btn-soft btn-sm mt-2">Browse files</button>
      </div>
    """) + """</div>
    <div class="mt-3">""" + card("Validation", """
      <p class="text-muted small mb-2">The view is wired for server-side validation — every field carries a validation slot ready for your model annotations.</p>
      <div class="alert alert-danger py-2 px-3 mb-2 small"><i class="bi bi-exclamation-circle me-1"></i>Last name is required.</div>
      <div class="alert alert-warning py-2 px-3 mb-0 small"><i class="bi bi-people me-1"></i>A patient with this mobile number already exists — <a href="patients-details.html">Sorenson, D.</a></div>
    """) + """</div>
  </div>
</div>
"""}

# =========================================================================
# 7. patients-details.html
# =========================================================================
PAGES["patients-details.html"] = {
    "title": "Patient record",
    "razor": "Views/Patients/Details.cshtml",
    "body": head([("Home", "dashboard-admin.html"), ("Patients", "patients-index.html"), ("Marcus Kelly", "")],
                 "Marcus Kelly",
                 "PT-10428 · 34 y · Male · Registered 04 Jan 2021",
                 '<a class="btn btn-soft" href="appointments-create.html"><i class="bi bi-calendar-plus me-1"></i>Book</a>'
                 '<a class="btn btn-soft" href="billing-invoice-create.html" data-roles="Admin,Receptionist"><i class="bi bi-receipt me-1"></i>New invoice</a>'
                 '<a class="btn btn-brand" href="treatments-chart.html" data-roles="Admin,Dentist"><i class="bi bi-diagram-3 me-1"></i>Open chart</a>') + """
<div class="row g-3">
  <div class="col-xl-4">
    """ + card("", """
      <div class="d-flex gap-3">
        <span class="avatar lg">MK</span>
        <div>
          <h3 style="font-size:17px;margin:0 0 2px">Marcus Kelly</h3>
          <div class="text-muted small">PT-10428 · 34 y · Male</div>
          <div class="d-flex gap-1 mt-2 flex-wrap">""" + pill("Active", "green") + pill("Insured", "blue") + """</div>
        </div>
      </div>
      <hr>
      <div class="d-flex gap-2 flex-wrap mb-3">
        <span class="pill pill-red"><i class="bi bi-exclamation-triangle-fill"></i>Penicillin allergy</span>
        <span class="pill pill-amber"><i class="bi bi-heart-pulse-fill"></i>Hypertension</span>
        <span class="pill pill-purple"><i class="bi bi-emoji-frown-fill"></i>Dental anxiety</span>
      </div>
      <dl class="dl-x">
        <dt>Mobile</dt><dd>+1 415 220 8841</dd>
        <dt>Email</dt><dd>m.kelly@example.com</dd>
        <dt>Address</dt><dd>221 Riverside Drive, Apt 4B<br>San Francisco, CA 94107</dd>
        <dt>Primary dentist</dt><dd>Dr. Luca Bianchi</dd>
        <dt>Recall</dt><dd>Every 6 months — next due 12 Aug 2026</dd>
        <dt>Emergency contact</dt><dd>Nora Kelly (spouse) · +1 415 220 8842</dd>
      </dl>
      <div class="d-flex gap-2">
        <button class="btn btn-soft btn-sm flex-grow-1"><i class="bi bi-pencil me-1"></i>Edit</button>
        <button class="btn btn-soft btn-sm" data-roles="Admin"><i class="bi bi-archive"></i></button>
      </div>
    """) + """
    <div class="mt-3">""" + card("Account", """
      <div class="d-flex justify-content-between mb-2"><span class="text-muted">Lifetime treatment value</span><span class="fw-semibold">$6,940</span></div>
      <div class="d-flex justify-content-between mb-2"><span class="text-muted">Outstanding balance</span><span class="fw-semibold text-success">$0.00</span></div>
      <div class="d-flex justify-content-between mb-3"><span class="text-muted">Insurance remaining</span><span class="fw-semibold">$820 of $1,500</span></div>
      <div class="stat-bar mb-1"><span style="width:45%"></span></div>
      <div class="text-muted" style="font-size:11.5px">Benefit year resets 01 Jan 2027</div>
    """) + """</div>
  </div>

  <div class="col-xl-8">
    <ul class="nav nav-tabs mb-3">
      <li class="nav-item"><a class="nav-link active" href="#tl" data-bs-toggle="tab">Timeline</a></li>
      <li class="nav-item"><a class="nav-link" href="#ap" data-bs-toggle="tab">Appointments</a></li>
      <li class="nav-item"><a class="nav-link" href="#md" data-bs-toggle="tab">Medical</a></li>
      <li class="nav-item" data-roles="Admin,Receptionist"><a class="nav-link" href="#iv" data-bs-toggle="tab">Invoices</a></li>
      <li class="nav-item"><a class="nav-link" href="#fl" data-bs-toggle="tab">Files</a></li>
    </ul>

    <div class="tab-content">
      <div class="tab-pane fade show active" id="tl">
        """ + card("Clinical &amp; account history", """
          <div class="tl">
            <div class="tl-item"><span class="dot"></span><div class="tl-t">Composite filling — #26 occlusal</div>
              <div class="tl-m">Today 09:30 · Dr. Luca Bianchi · in progress</div></div>
            <div class="tl-item"><span class="dot"></span><div class="tl-t">Treatment plan approved — 3 phases, $1,240</div>
              <div class="tl-m">12 Aug 2026 · Dr. Luca Bianchi · consent signed</div></div>
            <div class="tl-item"><span class="dot"></span><div class="tl-t">Payment received — $310 (card)</div>
              <div class="tl-m">12 Feb 2026 · Priya Nair · INV-2201</div></div>
            <div class="tl-item"><span class="dot"></span><div class="tl-t">Scale &amp; polish + bitewing radiographs</div>
              <div class="tl-m">12 Feb 2026 · M. Adeyemi, RDH</div></div>
            <div class="tl-item"><span class="dot"></span><div class="tl-t">Extraction — #38 (impacted)</div>
              <div class="tl-m">03 Sep 2025 · Dr. Amara Okafor</div></div>
            <div class="tl-item"><span class="dot"></span><div class="tl-t">Patient registered</div>
              <div class="tl-m">04 Jan 2021 · reception</div></div>
          </div>
        """) + """
      </div>

      <div class="tab-pane fade" id="ap">
        """ + card_flush("Appointments", table(
            ["Date", "Time", "Procedure", "Dentist", "Status", ""],
            ["".join([
                '<tr><td>14 Aug 2026</td><td>09:30</td><td>Composite filling #26</td><td>Dr. Bianchi</td><td>' +
                pill("In chair", "green") + '</td><td class="text-end"><a class="btn btn-soft btn-sm" href="appointments-reschedule.html">Manage</a></td></tr>',
                '<tr><td>28 Aug 2026</td><td>14:00</td><td>Composite filling #27</td><td>Dr. Bianchi</td><td>' +
                pill("Scheduled", "blue") + '</td><td class="text-end"><a class="btn btn-soft btn-sm" href="appointments-reschedule.html">Manage</a></td></tr>',
                '<tr><td>12 Feb 2026</td><td>11:15</td><td>Scale &amp; polish</td><td>M. Adeyemi</td><td>' +
                pill("Completed", "gray") + '</td><td class="text-end"><a class="btn btn-soft btn-sm" href="#">View</a></td></tr>',
                '<tr><td>19 Nov 2025</td><td>16:00</td><td>Check-up</td><td>Dr. Bianchi</td><td>' +
                pill("No-show", "red") + '</td><td class="text-end"><a class="btn btn-soft btn-sm" href="#">View</a></td></tr>',
            ])]), actions='<a class="btn btn-brand btn-sm" href="appointments-create.html"><i class="bi bi-calendar-plus me-1"></i>Book</a>') + """
      </div>

      <div class="tab-pane fade" id="md">
        """ + card("Medical history", """
          <div class="alert alert-danger py-2 px-3 small"><i class="bi bi-exclamation-triangle-fill me-1"></i>
            <strong>Allergies:</strong> Penicillin (rash, 2016), latex (mild).</div>
          <div class="row">
            <div class="col-md-6"><dl class="dl-x">
              <dt>Conditions</dt><dd>Hypertension — controlled</dd>
              <dt>Current medication</dt><dd>Amlodipine 5 mg daily</dd>
              <dt>Smoking</dt><dd>Ex-smoker, quit 2019</dd>
            </dl></div>
            <div class="col-md-6"><dl class="dl-x">
              <dt>Pregnancy</dt><dd>N/A</dd>
              <dt>Anticoagulants</dt><dd>None</dd>
              <dt>Last reviewed</dt><dd>12 Aug 2026 by Dr. Bianchi</dd>
            </dl></div>
          </div>
          <div class="section-title">Notes</div>
          <p class="text-muted small mb-0">Marked dental anxiety — prefers morning appointments and a longer chair slot. Responds well to topical anaesthetic before injection.</p>
        """, actions='<button class="btn btn-soft btn-sm" data-roles="Admin,Dentist"><i class="bi bi-pencil me-1"></i>Update history</button>') + """
      </div>

      <div class="tab-pane fade" id="iv">
        """ + card_flush("Invoices", table(
            ["Invoice", "Date", "Amount", "Paid", "Balance", "Status", ""],
            ["".join([
                '<tr><td class="fw-semibold"><a href="billing-invoice-details.html">INV-2478</a></td><td>12 Aug 2026</td>'
                '<td>$310.00</td><td>$310.00</td><td>$0.00</td><td>' + pill("Paid", "green") +
                '</td><td class="text-end"><a class="btn btn-soft btn-sm" href="billing-invoice-details.html">View</a></td></tr>',
                '<tr><td class="fw-semibold"><a href="billing-invoice-details.html">INV-2201</a></td><td>12 Feb 2026</td>'
                '<td>$185.00</td><td>$185.00</td><td>$0.00</td><td>' + pill("Paid", "green") +
                '</td><td class="text-end"><a class="btn btn-soft btn-sm" href="billing-invoice-details.html">View</a></td></tr>',
                '<tr><td class="fw-semibold"><a href="billing-invoice-details.html">INV-1988</a></td><td>03 Sep 2025</td>'
                '<td>$640.00</td><td>$640.00</td><td>$0.00</td><td>' + pill("Paid", "green") +
                '</td><td class="text-end"><a class="btn btn-soft btn-sm" href="billing-invoice-details.html">View</a></td></tr>',
            ])]), actions='<a class="btn btn-brand btn-sm" href="billing-invoice-create.html">New invoice</a>') + """
      </div>

      <div class="tab-pane fade" id="fl">
        """ + card("Files &amp; radiographs", """
          <div class="row g-3">
            <div class="col-6 col-md-3"><div class="p-3 rounded text-center" style="border:1px solid var(--line)">
              <i class="bi bi-file-earmark-image text-secondary" style="font-size:26px"></i>
              <div class="small fw-semibold mt-2">Bitewing L</div><div class="text-muted" style="font-size:11px">12 Feb 2026</div></div></div>
            <div class="col-6 col-md-3"><div class="p-3 rounded text-center" style="border:1px solid var(--line)">
              <i class="bi bi-file-earmark-image text-secondary" style="font-size:26px"></i>
              <div class="small fw-semibold mt-2">Bitewing R</div><div class="text-muted" style="font-size:11px">12 Feb 2026</div></div></div>
            <div class="col-6 col-md-3"><div class="p-3 rounded text-center" style="border:1px solid var(--line)">
              <i class="bi bi-file-earmark-pdf text-secondary" style="font-size:26px"></i>
              <div class="small fw-semibold mt-2">Consent form</div><div class="text-muted" style="font-size:11px">12 Aug 2026</div></div></div>
            <div class="col-6 col-md-3"><div class="p-3 rounded text-center" style="border:1.5px dashed var(--line);background:#fbfdfe">
              <i class="bi bi-plus-lg text-muted" style="font-size:26px"></i>
              <div class="small fw-semibold mt-2">Upload</div><div class="text-muted" style="font-size:11px">PDF, JPG, DICOM</div></div></div>
          </div>
        """) + """
      </div>
    </div>
  </div>
</div>
"""}

# =========================================================================
# 8. reports-index.html
# =========================================================================
PAGES["reports-index.html"] = {
    "title": "Reports",
    "razor": "Views/Reports/Index.cshtml",
    "body": head([("Home", "dashboard-admin.html"), ("Reports", "")],
                 "Reports",
                 "August 2026 · Bright Smile Dental — Riverside",
                 '<select class="form-select" style="width:auto"><option>This month</option><option>Last month</option><option>This quarter</option><option>Year to date</option></select>'
                 '<button class="btn btn-soft"><i class="bi bi-printer me-1"></i>Print</button>'
                 '<button class="btn btn-brand"><i class="bi bi-download me-1"></i>Export CSV</button>') + """
<div class="row g-3 mb-3">""" + (
        kpi("bi-graph-up-arrow", "green", "$186,400", "Production MTD", "▲ 8.1% vs July") +
        kpi("bi-cash-stack", "teal", "$171,930", "Collections MTD", "92.2% collection rate") +
        kpi("bi-person-x", "amber", "4.6%", "No-show rate", "▼ 0.8 pts", "text-success") +
        kpi("bi-arrow-repeat", "blue", "68%", "Recall conversion", "▲ 3 pts")) + """
</div>

<div class="row g-3">
  <div class="col-xl-8">
    """ + card("Production by dentist", """
      <div class="mini-bars" style="height:150px">
        <div class="b" style="height:92%"></div><div class="b" style="height:78%"></div>
        <div class="b" style="height:64%"></div><div class="b mut" style="height:41%"></div>
        <div class="b mut" style="height:29%"></div>
      </div>
      <div class="bars-x"><span>Okafor</span><span>Bianchi</span><span>Reyes</span><span>Adeyemi</span><span>Locum</span></div>
    """) + """
  </div>
  <div class="col-xl-4">
    """ + card("Revenue mix", """
      <div class="mb-3"><div class="d-flex justify-content-between small mb-1"><span>Restorative</span><span class="fw-semibold">38%</span></div><div class="stat-bar"><span style="width:38%"></span></div></div>
      <div class="mb-3"><div class="d-flex justify-content-between small mb-1"><span>Preventive / hygiene</span><span class="fw-semibold">24%</span></div><div class="stat-bar"><span style="width:24%"></span></div></div>
      <div class="mb-3"><div class="d-flex justify-content-between small mb-1"><span>Endodontics</span><span class="fw-semibold">16%</span></div><div class="stat-bar"><span style="width:16%"></span></div></div>
      <div class="mb-3"><div class="d-flex justify-content-between small mb-1"><span>Prosthetics</span><span class="fw-semibold">14%</span></div><div class="stat-bar"><span style="width:14%"></span></div></div>
      <div><div class="d-flex justify-content-between small mb-1"><span>Surgical</span><span class="fw-semibold">8%</span></div><div class="stat-bar"><span style="width:8%"></span></div></div>
    """) + """
  </div>
</div>

<div class="row g-3 mt-0">
  <div class="col-xl-6">
    """ + card_flush("Aged debtors", table(
        ["Bracket", "Invoices", "Amount", "Share"],
        ["".join([
            '<tr><td>Current</td><td>64</td><td class="fw-semibold">$21,480</td><td style="min-width:120px"><div class="stat-bar"><span style="width:59%"></span></div></td></tr>',
            '<tr><td>31–60 days</td><td>18</td><td class="fw-semibold">$8,920</td><td><div class="stat-bar"><span style="width:24%"></span></div></td></tr>',
            '<tr><td>61–90 days</td><td>7</td><td class="fw-semibold">$3,640</td><td><div class="stat-bar"><span style="width:10%"></span></div></td></tr>',
            '<tr><td>90+ days</td><td>5</td><td class="fw-semibold text-danger">$2,200</td><td><div class="stat-bar"><span style="width:7%"></span></div></td></tr>',
        ])]), actions='<a class="btn btn-ghost btn-sm" href="billing-invoices.html">Open invoices</a>') + """
  </div>
  <div class="col-xl-6">
    """ + card_flush("Report library", table(
        ["Report", "Description", ""],
        ["".join([
            '<tr><td class="t-main">Daily sheet</td><td class="t-sub">Production, collections and appointments for one day</td><td class="text-end"><button class="btn btn-soft btn-sm">Run</button></td></tr>',
            '<tr><td class="t-main">Outstanding balances</td><td class="t-sub">Ageing by patient with last contact date</td><td class="text-end"><button class="btn btn-soft btn-sm">Run</button></td></tr>',
            '<tr><td class="t-main">Recall performance</td><td class="t-sub">Due, contacted, booked and attended</td><td class="text-end"><button class="btn btn-soft btn-sm">Run</button></td></tr>',
            '<tr><td class="t-main">Chair utilisation</td><td class="t-sub">Booked vs available hours by chair and dentist</td><td class="text-end"><button class="btn btn-soft btn-sm">Run</button></td></tr>',
            '<tr><td class="t-main">Insurance claims</td><td class="t-sub">Submitted, paid, rejected and pending by insurer</td><td class="text-end"><button class="btn btn-soft btn-sm">Run</button></td></tr>',
        ])])) + """
  </div>
</div>
"""}

# =========================================================================
# 9. admin-users.html
# =========================================================================
_perm_row = lambda label, a, d, r: (
    '<tr><td class="t-main">%s</td>'
    '<td class="text-center">%s</td><td class="text-center">%s</td><td class="text-center">%s</td></tr>'
    % (label,
       '<i class="bi bi-check-circle-fill text-success"></i>' if a else '<i class="bi bi-dash text-muted"></i>',
       '<i class="bi bi-check-circle-fill text-success"></i>' if d else '<i class="bi bi-dash text-muted"></i>',
       '<i class="bi bi-check-circle-fill text-success"></i>' if r else '<i class="bi bi-dash text-muted"></i>'))

PAGES["admin-users.html"] = {
    "title": "Users & roles",
    "razor": "Views/Admin/Users.cshtml",
    "body": head([("Home", "dashboard-admin.html"), ("Administration", ""), ("Users &amp; roles", "")],
                 "Users &amp; roles",
                 "12 staff accounts · 3 roles",
                 '<button class="btn btn-soft"><i class="bi bi-shield-lock me-1"></i>Role editor</button>'
                 '<button class="btn btn-brand"><i class="bi bi-person-plus me-1"></i>Add user</button>') + """
<div class="row g-3">
  <div class="col-xl-7">
    """ + card_flush("Staff accounts", table(
        ["User", "Role", "Chair / room", "Last sign-in", "Status", ""],
        ["".join([
            '<tr><td>' + person("AO", "Dr. Amara Okafor", "a.okafor@brightsmile.clinic") + '</td><td>' +
            pill("Admin", "teal", False) + '</td><td>Chair 1</td><td class="t-sub">Today 07:42</td><td>' +
            pill("Active", "green") + '</td><td class="text-end"><button class="btn btn-ghost btn-sm"><i class="bi bi-three-dots"></i></button></td></tr>',
            '<tr><td>' + person("LB", "Dr. Luca Bianchi", "l.bianchi@brightsmile.clinic") + '</td><td>' +
            pill("Dentist", "purple", False) + '</td><td>Chair 2</td><td class="t-sub">Today 08:05</td><td>' +
            pill("Active", "green") + '</td><td class="text-end"><button class="btn btn-ghost btn-sm"><i class="bi bi-three-dots"></i></button></td></tr>',
            '<tr><td>' + person("SR", "Dr. Sofia Reyes", "s.reyes@brightsmile.clinic") + '</td><td>' +
            pill("Dentist", "purple", False) + '</td><td>Chair 3</td><td class="t-sub">Yesterday 18:20</td><td>' +
            pill("Active", "green") + '</td><td class="text-end"><button class="btn btn-ghost btn-sm"><i class="bi bi-three-dots"></i></button></td></tr>',
            '<tr><td>' + person("MA", "M. Adeyemi, RDH", "m.adeyemi@brightsmile.clinic") + '</td><td>' +
            pill("Dentist", "purple", False) + '</td><td>Hygiene 1</td><td class="t-sub">Today 08:31</td><td>' +
            pill("Active", "green") + '</td><td class="text-end"><button class="btn btn-ghost btn-sm"><i class="bi bi-three-dots"></i></button></td></tr>',
            '<tr><td>' + person("PN", "Priya Nair", "p.nair@brightsmile.clinic") + '</td><td>' +
            pill("Receptionist", "blue", False) + '</td><td>Front desk</td><td class="t-sub">Today 07:55</td><td>' +
            pill("Active", "green") + '</td><td class="text-end"><button class="btn btn-ghost btn-sm"><i class="bi bi-three-dots"></i></button></td></tr>',
            '<tr><td>' + person("JT", "Jonas Tveit", "j.tveit@brightsmile.clinic", True) + '</td><td>' +
            pill("Receptionist", "blue", False) + '</td><td>Front desk</td><td class="t-sub">02 Aug 2026</td><td>' +
            pill("Suspended", "gray") + '</td><td class="text-end"><button class="btn btn-ghost btn-sm"><i class="bi bi-three-dots"></i></button></td></tr>',
        ])])) + """
  </div>
  <div class="col-xl-5">
    """ + card_flush("Permission matrix", table(
        ["Capability", ("Admin", ' class="text-center"'), ("Dentist", ' class="text-center"'), ("Recept.", ' class="text-center"')],
        ["".join([
            _perm_row("View patient register", 1, 1, 1),
            _perm_row("Register / edit patients", 1, 0, 1),
            _perm_row("Archive patients", 1, 0, 0),
            _perm_row("Book &amp; reschedule", 1, 1, 1),
            _perm_row("Dental charting", 1, 1, 0),
            _perm_row("Sign clinical notes", 0, 1, 0),
            _perm_row("Prescribe", 0, 1, 0),
            _perm_row("Create invoices", 1, 0, 1),
            _perm_row("Record payments / refunds", 1, 0, 1),
            _perm_row("Edit fee schedule", 1, 0, 0),
            _perm_row("Practice reports", 1, 0, 0),
            _perm_row("Manage users &amp; settings", 1, 0, 0),
        ])]), sub="Drives the sidebar, the action buttons and the [Authorize] attributes",
        actions='<button class="btn btn-soft btn-sm">Edit roles</button>') + """
    <div class="mt-3">""" + card("", """
      <div class="d-flex gap-3">
        <i class="bi bi-lock text-secondary" style="font-size:19px"></i>
        <div class="small text-muted">
          In the MVC project each capability maps to an <code>[Authorize(Roles = "…")]</code> attribute on the
          controller action, and to a <code>data-roles</code>-style <code>@if (User.IsInRole(…))</code> block in the view,
          so a hidden button can never be reached by URL either.
          <a href="error-access-denied.html">See the access-denied screen</a>.
        </div>
      </div>
    """) + """</div>
  </div>
</div>
"""}

# =========================================================================
# 10. admin-clinic.html
# =========================================================================
PAGES["admin-clinic.html"] = {
    "title": "Clinic & chairs",
    "razor": "Views/Admin/Clinic.cshtml",
    "body": head([("Home", "dashboard-admin.html"), ("Administration", ""), ("Clinic &amp; chairs", "")],
                 "Clinic &amp; chairs",
                 "Locations, operatories and opening hours",
                 '<button class="btn btn-brand"><i class="bi bi-plus-lg me-1"></i>Add chair</button>') + """
<div class="row g-3">
  <div class="col-xl-7">
    """ + card_flush("Chairs / operatories", table(
        ["Chair", "Location", "Assigned to", "Equipment", "Status", ""],
        ["".join([
            '<tr><td class="t-main">Chair 1</td><td>Riverside</td><td>Dr. Amara Okafor</td>'
            '<td class="t-sub">Intraoral camera, apex locator</td><td>' + pill("In use", "green") +
            '</td><td class="text-end"><button class="btn btn-ghost btn-sm"><i class="bi bi-pencil"></i></button></td></tr>',
            '<tr><td class="t-main">Chair 2</td><td>Riverside</td><td>Dr. Luca Bianchi</td>'
            '<td class="t-sub">Intraoral camera, microscope</td><td>' + pill("In use", "green") +
            '</td><td class="text-end"><button class="btn btn-ghost btn-sm"><i class="bi bi-pencil"></i></button></td></tr>',
            '<tr><td class="t-main">Chair 3</td><td>Riverside</td><td>Dr. Sofia Reyes</td>'
            '<td class="t-sub">Standard</td><td>' + pill("Free", "blue") +
            '</td><td class="text-end"><button class="btn btn-ghost btn-sm"><i class="bi bi-pencil"></i></button></td></tr>',
            '<tr><td class="t-main">Hygiene 1</td><td>Riverside</td><td>M. Adeyemi, RDH</td>'
            '<td class="t-sub">Ultrasonic scaler</td><td>' + pill("In use", "green") +
            '</td><td class="text-end"><button class="btn btn-ghost btn-sm"><i class="bi bi-pencil"></i></button></td></tr>',
            '<tr><td class="t-main">Chair 4</td><td>Riverside</td><td class="text-muted">Unassigned</td>'
            '<td class="t-sub">Standard</td><td>' + pill("Maintenance", "amber") +
            '</td><td class="text-end"><button class="btn btn-ghost btn-sm"><i class="bi bi-pencil"></i></button></td></tr>',
        ])])) + """
  </div>
  <div class="col-xl-5">
    """ + card("Opening hours", """
      <div class="d-flex justify-content-between align-items-center py-2" style="border-bottom:1px solid var(--line)"><span class="fw-semibold small">Monday</span><span class="text-muted small">08:00 – 18:00</span></div>
      <div class="d-flex justify-content-between align-items-center py-2" style="border-bottom:1px solid var(--line)"><span class="fw-semibold small">Tuesday</span><span class="text-muted small">08:00 – 18:00</span></div>
      <div class="d-flex justify-content-between align-items-center py-2" style="border-bottom:1px solid var(--line)"><span class="fw-semibold small">Wednesday</span><span class="text-muted small">08:00 – 20:00</span></div>
      <div class="d-flex justify-content-between align-items-center py-2" style="border-bottom:1px solid var(--line)"><span class="fw-semibold small">Thursday</span><span class="text-muted small">08:00 – 18:00</span></div>
      <div class="d-flex justify-content-between align-items-center py-2" style="border-bottom:1px solid var(--line)"><span class="fw-semibold small">Friday</span><span class="text-muted small">08:00 – 16:00</span></div>
      <div class="d-flex justify-content-between align-items-center py-2" style="border-bottom:1px solid var(--line)"><span class="fw-semibold small">Saturday</span><span class="text-muted small">09:00 – 13:00</span></div>
      <div class="d-flex justify-content-between align-items-center py-2"><span class="fw-semibold small">Sunday</span><span class="text-muted small">Closed</span></div>
      <button class="btn btn-soft btn-sm w-100 mt-3"><i class="bi bi-pencil me-1"></i>Edit hours</button>
    """) + """
    <div class="mt-3">""" + card("Closures &amp; holidays", """
      <div class="d-flex gap-2 align-items-center mb-2"><span class="pill pill-amber"><i class="bi bi-calendar-x"></i>02 Sep 2026</span><span class="small text-muted">Staff training — closed all day</span></div>
      <div class="d-flex gap-2 align-items-center mb-2"><span class="pill pill-amber"><i class="bi bi-calendar-x"></i>24–26 Dec 2026</span><span class="small text-muted">Holiday closure</span></div>
      <button class="btn btn-soft btn-sm w-100 mt-2"><i class="bi bi-plus-lg me-1"></i>Add closure</button>
    """) + """</div>
  </div>
</div>
"""}

# =========================================================================
# 11. admin-settings.html
# =========================================================================
PAGES["admin-settings.html"] = {
    "title": "Settings",
    "razor": "Views/Admin/Settings.cshtml",
    "body": head([("Home", "dashboard-admin.html"), ("Administration", ""), ("Settings", "")],
                 "Settings",
                 "Branding, reminders, billing rules and integrations",
                 '<button class="btn btn-soft">Discard</button><button class="btn btn-brand">Save changes</button>') + """
<div class="row g-3">
  <div class="col-lg-3">
    <div class="card-x p-2">
      <a class="nav-link-x active" href="#brand" data-bs-toggle="tab" style="color:var(--ink);background:var(--brand-50);box-shadow:none"><i class="bi bi-palette"></i>Branding</a>
      <a class="nav-link-x" href="#remind" data-bs-toggle="tab" style="color:var(--ink-2)"><i class="bi bi-bell"></i>Reminders</a>
      <a class="nav-link-x" href="#bill" data-bs-toggle="tab" style="color:var(--ink-2)"><i class="bi bi-receipt"></i>Billing</a>
      <a class="nav-link-x" href="#integr" data-bs-toggle="tab" style="color:var(--ink-2)"><i class="bi bi-plug"></i>Integrations</a>
    </div>
  </div>
  <div class="col-lg-9">
    <div class="tab-content">
      <div class="tab-pane fade show active" id="brand">
        """ + card("Branding", """
          <div class="row">
            """ + field("Clinic name", txt("", "Bright Smile Dental"), "col-md-6") + """
            """ + field("Trading location", txt("", "Riverside"), "col-md-6") + """
          </div>
          <div class="section-title">Theme</div>
          <p class="text-muted small">The whole interface is driven by six CSS variables — change these and every screen re-skins.</p>
          <div class="row g-3">
            <div class="col-6 col-md-3"><label class="form-label">Primary</label><input type="color" class="form-control form-control-color w-100" value="#0e8f84"></div>
            <div class="col-6 col-md-3"><label class="form-label">Sidebar</label><input type="color" class="form-control form-control-color w-100" value="#0d1b2a"></div>
            <div class="col-6 col-md-3"><label class="form-label">Page background</label><input type="color" class="form-control form-control-color w-100" value="#f4f7fa"></div>
            <div class="col-6 col-md-3"><label class="form-label">Corner radius</label>""" + sel(["Rounded (14px)", "Soft (8px)", "Square (4px)"]) + """</div>
          </div>
          <div class="section-title">Logo</div>
          <div class="d-flex align-items-center gap-3">
            <span class="logo" style="width:52px;height:52px;border-radius:15px;background:linear-gradient(135deg,var(--brand-500),var(--brand-700));display:grid;place-items:center;color:#fff;font-size:23px"><i class="bi bi-hexagon-fill"></i></span>
            <button class="btn btn-soft btn-sm">Upload logo</button>
            <span class="text-muted small">SVG or PNG, min 128×128</span>
          </div>
        """) + """
      </div>

      <div class="tab-pane fade" id="remind">
        """ + card("Appointment reminders", """
          <div class="row">
            """ + field("First reminder", sel(["48 hours before", "72 hours before", "24 hours before"]), "col-md-6") + """
            """ + field("Second reminder", sel(["2 hours before", "Morning of", "None"]), "col-md-6") + """
            """ + field("Channel", sel(["SMS then email", "SMS only", "Email only", "WhatsApp"]), "col-md-6") + """
            """ + field("Reply handling", sel(["Allow 'C' to confirm", "No replies", "Route to front desk"]), "col-md-6") + """
            """ + field("SMS template", area("", 3, "Hi {PatientFirstName}, this is a reminder of your appointment at Bright Smile Dental on {AppointmentDate} at {AppointmentTime}. Reply C to confirm."), "col-12",
                        hint="Merge fields are resolved server-side.") + """
          </div>
          <div class="form-check form-switch"><input class="form-check-input" type="checkbox" checked id="s1"><label class="form-check-label small" for="s1">Send recall reminders when a patient becomes due</label></div>
          <div class="form-check form-switch"><input class="form-check-input" type="checkbox" checked id="s2"><label class="form-check-label small" for="s2">Notify front desk of unconfirmed appointments each morning</label></div>
        """) + """
      </div>

      <div class="tab-pane fade" id="bill">
        """ + card("Billing rules", """
          <div class="row">
            """ + field("Currency", sel(["USD ($)", "EUR (€)", "GBP (£)", "AUD ($)"]), "col-md-4") + """
            """ + field("Tax rate", txt("", "0.00 %"), "col-md-4") + """
            """ + field("Payment terms", sel(["Due on receipt", "Net 14", "Net 30"]), "col-md-4") + """
            """ + field("Invoice number format", txt("", "INV-####"), "col-md-4") + """
            """ + field("Next invoice number", txt("", "2479"), "col-md-4") + """
            """ + field("Late fee after", sel(["30 days", "45 days", "60 days", "Never"]), "col-md-4") + """
          </div>
          <div class="form-check form-switch"><input class="form-check-input" type="checkbox" checked id="b1"><label class="form-check-label small" for="b1">Allow part payments and payment plans</label></div>
          <div class="form-check form-switch"><input class="form-check-input" type="checkbox" id="b2"><label class="form-check-label small" for="b2">Require a deposit for appointments over $500</label></div>
        """) + """
      </div>

      <div class="tab-pane fade" id="integr">
        """ + card_flush("Integrations", table(
            ["Service", "Purpose", "Status", ""],
            ["".join([
                '<tr><td class="t-main">SMS gateway</td><td class="t-sub">Appointment reminders and confirmations</td><td>' +
                pill("Connected", "green") + '</td><td class="text-end"><button class="btn btn-soft btn-sm">Configure</button></td></tr>',
                '<tr><td class="t-main">Card terminal</td><td class="t-sub">In-clinic card payments</td><td>' +
                pill("Connected", "green") + '</td><td class="text-end"><button class="btn btn-soft btn-sm">Configure</button></td></tr>',
                '<tr><td class="t-main">Insurance clearing house</td><td class="t-sub">Electronic claim submission</td><td>' +
                pill("Not connected", "gray") + '</td><td class="text-end"><button class="btn btn-soft btn-sm">Connect</button></td></tr>',
                '<tr><td class="t-main">Imaging bridge</td><td class="t-sub">Radiograph capture into the patient file</td><td>' +
                pill("Not connected", "gray") + '</td><td class="text-end"><button class="btn btn-soft btn-sm">Connect</button></td></tr>',
                '<tr><td class="t-main">Accounting export</td><td class="t-sub">Nightly journal export</td><td>' +
                pill("Error", "red") + '</td><td class="text-end"><button class="btn btn-soft btn-sm">Fix</button></td></tr>',
            ])]), sub="Each row is a stub — the view only renders whatever your service layer reports") + """
      </div>
    </div>
  </div>
</div>
"""}

# =========================================================================
# 12. error-access-denied.html
# =========================================================================
PAGES["error-access-denied.html"] = {
    "title": "Access denied",
    "razor": "Views/Account/AccessDenied.cshtml",
    "body": """
<div class="d-flex align-items-center justify-content-center" style="min-height:60vh">
  <div class="text-center" style="max-width:460px">
    <div class="ic ic-amber mx-auto mb-3" style="width:64px;height:64px;border-radius:20px;display:grid;place-items:center;font-size:28px"><i class="bi bi-shield-lock"></i></div>
    <h1 style="font-size:22px">You don't have access to this screen</h1>
    <p class="text-muted">Your role — <strong data-role-label>Admin</strong> — isn't permitted to open this page.
    If you think that's wrong, ask a practice administrator to review your permissions.</p>
    <div class="d-flex gap-2 justify-content-center flex-wrap mt-3">
      <a class="btn btn-brand" href="dashboard-admin.html" data-role-home><i class="bi bi-house me-1"></i>Back to my dashboard</a>
      <a class="btn btn-soft" href="index.html">Screen map</a>
    </div>
  </div>
</div>
"""}
