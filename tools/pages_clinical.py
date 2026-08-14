# -*- coding: utf-8 -*-
"""Appointment scheduling screens and clinical (charting / planning) screens."""
from ui import head, kpi, card, card_flush, table, person, pill, field, txt, sel, area

PAGES = {}

# =========================================================================
# Weekly calendar grid
# =========================================================================
DAYS = [("Mon", "11"), ("Tue", "12"), ("Wed", "13"), ("Thu", "14"), ("Fri", "15"), ("Sat", "16")]
TIMES = ["08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
         "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30"]

# (time, day index) -> (rowspan, css tone, title, meta)
BOOKINGS = {
    ("08:00", 0): (2, "teal", "E. Whitfield", "Scale &amp; polish · Hyg 1"),
    ("09:00", 0): (2, "blue", "P. Lindqvist", "Denture fit · Chair 3"),
    ("10:30", 0): (3, "purple", "A. Chowdhury", "Crown prep #16 · Chair 1"),
    ("14:00", 0): (2, "teal", "G. Mbeki", "Check-up · Chair 2"),

    ("08:30", 1): (2, "blue", "S. Nowak", "Implant review · Chair 1"),
    ("10:00", 1): (4, "purple", "R. Jabari", "Root canal S1 · Chair 2"),
    ("13:00", 1): (2, "teal", "H. Nakamura", "Check-up · Chair 3"),
    ("15:00", 1): (2, "amber", "Staff meeting", "All chairs blocked"),

    ("09:00", 2): (2, "teal", "M. Kelly", "Filling #27 · Chair 2"),
    ("11:00", 2): (2, "blue", "T. Ackerman", "Crown fit · Chair 1"),
    ("14:30", 2): (3, "purple", "New patient", "Implant consult · Chair 1"),

    ("09:30", 3): (1, "teal", "M. Kelly", "Filling #26 · Chair 2"),
    ("10:00", 3): (1, "teal", "E. Whitfield", "Scale &amp; polish · Hyg 1"),
    ("10:45", 3): (0, "", "", ""),   # sentinel, ignored
    ("11:00", 3): (2, "purple", "H. Nakamura", "Extraction #48 · Chair 2"),
    ("12:00", 3): (2, "blue", "D. Sorenson", "Implant consult · Chair 1"),
    ("14:00", 3): (2, "amber", "A. Chowdhury", "Crown prep — unconfirmed"),
    ("15:00", 3): (2, "teal", "P. Lindqvist", "Denture adj. · Chair 3"),

    ("08:30", 4): (2, "blue", "G. Mbeki", "Hygiene · Hyg 1"),
    ("11:00", 4): (3, "purple", "R. Jabari", "Root canal S2 · Chair 2"),
    ("13:30", 4): (2, "red", "CANCELLED", "Slot free — offer to waiting list"),

    ("09:00", 5): (2, "teal", "Emergency slot", "Held open"),
    ("11:00", 5): (2, "blue", "S. Nowak", "Review · Chair 1"),
}


def _calendar():
    consumed = set()
    rows = []
    for ti, t in enumerate(TIMES):
        cells = ['<td class="timecol">%s</td>' % (t if t.endswith(":00") else "")]
        for di in range(len(DAYS)):
            if (t, di) in consumed:
                continue
            b = BOOKINGS.get((t, di))
            if b and b[0] > 0:
                span, tone, title, meta = b
                for k in range(1, span):
                    if ti + k < len(TIMES):
                        consumed.add((TIMES[ti + k], di))
                cells.append(
                    '<td rowspan="%d"><a class="appt appt-%s d-block text-decoration-none" href="appointments-reschedule.html">'
                    '<strong>%s</strong><span>%s</span></a></td>' % (span, tone, title, meta))
            else:
                cells.append('<td class="free"><a href="appointments-create.html" class="d-block h-100" '
                             'style="min-height:44px" title="Book %s"></a></td>' % t)
        rows.append("<tr>%s</tr>" % "".join(cells))

    ths = "".join('<th%s>%s<small>Aug %s</small></th>' % (' class="today"' if d[0] == "Thu" else "", d[0], d[1])
                  for d in DAYS)
    return """<div class="cal-wrap"><table class="cal">
  <thead><tr><th style="width:74px"></th>%s</tr></thead>
  <tbody>%s</tbody>
</table></div>""" % (ths, "".join(rows))


PAGES["appointments-calendar.html"] = {
    "title": "Calendar",
    "razor": "Views/Appointments/Calendar.cshtml",
    "body": head([("Home", "dashboard-admin.html"), ("Appointments", "appointments-index.html"), ("Calendar", "")],
                 "Appointment calendar",
                 "Week of 11–16 August 2026 · click an empty slot to book",
                 '<div class="btn-group"><button class="btn btn-soft btn-sm">Day</button>'
                 '<button class="btn btn-soft btn-sm active">Week</button>'
                 '<button class="btn btn-soft btn-sm">Month</button></div>'
                 '<a class="btn btn-soft" href="appointments-waitlist.html" data-roles="Admin,Receptionist">'
                 '<i class="bi bi-hourglass-split me-1"></i>Waiting list <span class="badge text-bg-light">6</span></a>'
                 '<a class="btn btn-brand" href="appointments-create.html" data-roles="Admin,Receptionist">'
                 '<i class="bi bi-calendar-plus me-1"></i>Book</a>') + """
<div class="row g-3 mb-3">
  <div class="col-12">
    """ + card("", """
      <div class="d-flex flex-wrap gap-2 align-items-end">
        <div class="btn-group me-2">
          <button class="btn btn-soft btn-sm"><i class="bi bi-chevron-left"></i></button>
          <button class="btn btn-soft btn-sm">Today</button>
          <button class="btn btn-soft btn-sm"><i class="bi bi-chevron-right"></i></button>
        </div>
        <div style="min-width:170px"><label class="form-label">Dentist</label>""" +
               sel(["All dentists", "Dr. Amara Okafor", "Dr. Luca Bianchi", "Dr. Sofia Reyes", "M. Adeyemi, RDH"]) + """</div>
        <div style="min-width:150px"><label class="form-label">Chair</label>""" +
               sel(["All chairs", "Chair 1", "Chair 2", "Chair 3", "Hygiene 1"]) + """</div>
        <div style="min-width:150px"><label class="form-label">Status</label>""" +
               sel(["All", "Confirmed", "Unconfirmed", "Cancelled"]) + """</div>
        <div class="ms-auto d-flex gap-3 small text-muted align-items-center flex-wrap">
          <span><i class="bi bi-square-fill" style="color:var(--brand-500)"></i> Confirmed</span>
          <span><i class="bi bi-square-fill" style="color:#3b82f6"></i> Scheduled</span>
          <span><i class="bi bi-square-fill" style="color:#8b5cf6"></i> Long procedure</span>
          <span><i class="bi bi-square-fill" style="color:#f59e0b"></i> Unconfirmed</span>
          <span><i class="bi bi-square-fill" style="color:#ef4444"></i> Cancelled</span>
        </div>
      </div>
    """) + """
  </div>
</div>
""" + card_flush("", _calendar()) + """
"""}

# =========================================================================
# appointments-index.html
# =========================================================================
_ap_rows = []
for date, time, ini, name, pid, proc, dentist, chair, status, tone in [
    ("14 Aug", "09:30", "MK", "Marcus Kelly", "PT-10428", "Composite filling #26", "Dr. Bianchi", "Chair 2", "In chair", "green"),
    ("14 Aug", "10:00", "EW", "Elena Whitfield", "PT-10391", "Scale &amp; polish", "M. Adeyemi", "Hygiene 1", "Checked in", "green"),
    ("14 Aug", "10:45", "TA", "Tobias Ackerman", "PT-10502", "Crown fit #36", "Dr. Okafor", "Chair 1", "Confirmed", "blue"),
    ("14 Aug", "11:00", "HN", "Hugo Nakamura", "PT-10310", "Extraction #48", "Dr. Bianchi", "Chair 2", "Confirmed", "blue"),
    ("14 Aug", "11:30", "RJ", "Rania Jabari", "PT-10233", "Root canal — session 2", "Dr. Bianchi", "Chair 2", "Unconfirmed", "amber"),
    ("14 Aug", "12:15", "DS", "Daniel Sorenson", "PT-10477", "Implant consultation", "Dr. Okafor", "Chair 1", "New patient", "purple"),
    ("15 Aug", "08:30", "AC", "Aisha Chowdhury", "PT-10455", "Crown prep #16", "Dr. Okafor", "Chair 1", "Unconfirmed", "amber"),
    ("15 Aug", "09:15", "PL", "Peter Lindqvist", "PT-10099", "Denture fit", "Dr. Reyes", "Chair 3", "Confirmed", "blue"),
    ("15 Aug", "11:00", "SN", "Sara Nowak", "PT-10188", "Implant review", "Dr. Okafor", "Chair 1", "Confirmed", "blue"),
    ("13 Aug", "16:00", "GM", "Grace Mbeki", "PT-10061", "Check-up", "Dr. Reyes", "Chair 3", "No-show", "red"),
]:
    _ap_rows.append(
        '<tr><td><input class="form-check-input" type="checkbox"></td>'
        '<td class="fw-semibold">%s<div class="t-sub">%s</div></td>'
        '<td><a class="text-decoration-none" href="patients-details.html">%s</a></td>'
        '<td>%s</td><td>%s<div class="t-sub">%s</div></td><td>%s</td>'
        '<td class="text-end"><div class="dropdown"><button class="btn btn-ghost btn-sm" data-bs-toggle="dropdown"><i class="bi bi-three-dots"></i></button>'
        '<ul class="dropdown-menu dropdown-menu-end">'
        '<li><a class="dropdown-item" href="patients-details.html"><i class="bi bi-folder2-open me-2"></i>Patient record</a></li>'
        '<li><a class="dropdown-item" href="appointments-reschedule.html"><i class="bi bi-arrow-left-right me-2"></i>Reschedule</a></li>'
        '<li><a class="dropdown-item" href="treatments-chart.html" data-roles="Admin,Dentist"><i class="bi bi-diagram-3 me-2"></i>Open chart</a></li>'
        '<li><a class="dropdown-item" href="billing-invoice-create.html" data-roles="Admin,Receptionist"><i class="bi bi-receipt me-2"></i>Invoice</a></li>'
        '<li><hr class="dropdown-divider"></li>'
        '<li><a class="dropdown-item text-danger" href="appointments-reschedule.html"><i class="bi bi-x-circle me-2"></i>Cancel</a></li>'
        '</ul></div></td></tr>'
        % (time, date, person(ini, name, pid), proc, dentist, chair, pill(status, tone)))

PAGES["appointments-index.html"] = {
    "title": "Appointments",
    "razor": "Views/Appointments/Index.cshtml",
    "body": head([("Home", "dashboard-admin.html"), ("Appointments", "")],
                 "Appointments",
                 "48 today · 9 unconfirmed · 1 no-show yesterday",
                 '<a class="btn btn-soft" href="appointments-calendar.html"><i class="bi bi-calendar3 me-1"></i>Calendar view</a>'
                 '<a class="btn btn-brand" href="appointments-create.html" data-roles="Admin,Receptionist"><i class="bi bi-calendar-plus me-1"></i>Book</a>') + """
""" + card("", """
<div class="row g-2 align-items-end">
  <div class="col-lg-3 col-md-6"><label class="form-label">Search</label>
    <div class="input-group"><span class="input-group-text bg-white border-end-0"><i class="bi bi-search text-muted"></i></span>
    <input class="form-control border-start-0" placeholder="Patient name or ID"></div></div>
  <div class="col-lg-2 col-md-3 col-6"><label class="form-label">From</label>""" + txt("", "2026-08-13", "date") + """</div>
  <div class="col-lg-2 col-md-3 col-6"><label class="form-label">To</label>""" + txt("", "2026-08-15", "date") + """</div>
  <div class="col-lg-2 col-md-4 col-6"><label class="form-label">Status</label>""" +
           sel(["All statuses", "Scheduled", "Confirmed", "Checked in", "Completed", "Cancelled", "No-show"]) + """</div>
  <div class="col-lg-2 col-md-4 col-6"><label class="form-label">Dentist</label>""" +
           sel(["All dentists", "Dr. Amara Okafor", "Dr. Luca Bianchi", "Dr. Sofia Reyes", "M. Adeyemi, RDH"]) + """</div>
  <div class="col-lg-1 col-md-4 col-12"><button class="btn btn-brand w-100">Apply</button></div>
</div>
""") + """
<div class="mt-3">
""" + card_flush("", table(
        [('<input class="form-check-input" type="checkbox">', ' style="width:34px"'),
         "When", "Patient", "Procedure", "Dentist / chair", "Status", ("", ' class="text-end"')],
        ["".join(_ap_rows)]),
        actions='<div class="d-flex gap-2"><button class="btn btn-soft btn-sm"><i class="bi bi-send me-1"></i>Send reminders</button>'
                '<button class="btn btn-soft btn-sm"><i class="bi bi-printer me-1"></i>Print day sheet</button></div>',
        foot="""<div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
  <span class="text-muted small">Showing 1–10 of 132</span>
  <nav><ul class="pagination pagination-sm mb-0">
    <li class="page-item disabled"><span class="page-link">Previous</span></li>
    <li class="page-item active"><span class="page-link">1</span></li>
    <li class="page-item"><a class="page-link" href="#">2</a></li>
    <li class="page-item"><a class="page-link" href="#">Next</a></li>
  </ul></nav></div>""") + """
</div>
"""}

# =========================================================================
# appointments-create.html
# =========================================================================
_slot = lambda t, state: (
    '<button class="btn btn-sm %s w-100 mb-2" %s>%s</button>'
    % ("btn-brand" if state == "sel" else ("btn-soft" if state == "free" else "btn-soft"),
       'disabled style="opacity:.45"' if state == "busy" else "", t))

PAGES["appointments-create.html"] = {
    "title": "Book appointment",
    "razor": "Views/Appointments/Create.cshtml",
    "body": head([("Home", "dashboard-admin.html"), ("Appointments", "appointments-index.html"), ("Book", "")],
                 "Book an appointment",
                 "Pick the patient and procedure — the slot finder filters chairs by dentist and duration",
                 '<a class="btn btn-soft" href="appointments-calendar.html">Cancel</a>'
                 '<button class="btn btn-brand"><i class="bi bi-check2 me-1"></i>Confirm booking</button>') + """
<div class="row g-3">
  <div class="col-xl-7">
    """ + card("Appointment details", """
      <div class="section-title">Patient</div>
      <div class="row">
        <div class="col-md-8 mb-3">
          <label class="form-label req">Patient</label>
          <div class="input-group">
            <span class="input-group-text bg-white border-end-0"><i class="bi bi-search text-muted"></i></span>
            <input class="form-control border-start-0" value="Kelly, Marcus — PT-10428">
            <button class="btn btn-soft">Clear</button>
          </div>
          <div class="form-text">Type a name, ID or phone number. <a href="patients-create.html">Register a new patient</a> if they're not on file.</div>
        </div>
        """ + field("Appointment type", sel(["Treatment", "Check-up", "Hygiene", "Emergency", "Consultation"]), "col-md-4") + """
      </div>
      <div class="alert alert-light border d-flex gap-2 align-items-center py-2 px-3">
        <span class="avatar sm">MK</span>
        <div class="small"><strong>Marcus Kelly</strong> · PT-10428 · 34 y
          <span class="pill pill-red ms-1"><i class="bi bi-exclamation-triangle-fill"></i>Penicillin allergy</span>
          <span class="pill pill-purple ms-1"><i class="bi bi-emoji-frown-fill"></i>Anxiety — allow extra time</span>
        </div>
      </div>

      <div class="section-title">Procedure</div>
      <div class="row">
        """ + field("Procedure", sel(["D2392 — Composite, two surfaces", "D1110 — Prophylaxis, adult",
                                      "D2740 — Crown, porcelain/ceramic", "D3310 — Endodontic therapy, anterior",
                                      "D7140 — Extraction, erupted tooth"]), "col-md-6", req=True) + """
        """ + field("Tooth / quadrant", txt("", "#27"), "col-md-3", hint='<a href="treatments-chart.html">Pick on chart</a>') + """
        """ + field("Duration", sel(["30 min", "45 min", "60 min", "90 min", "120 min"], "45 min"), "col-md-3") + """
        """ + field("Dentist", sel(["Dr. Luca Bianchi", "Dr. Amara Okafor", "Dr. Sofia Reyes", "M. Adeyemi, RDH"]), "col-md-6", req=True) + """
        """ + field("Chair", sel(["Auto — first available", "Chair 1", "Chair 2", "Chair 3", "Hygiene 1"]), "col-md-6") + """
        """ + field("Notes for the clinician", area("e.g. patient prefers topical anaesthetic first", 2), "col-12") + """
      </div>

      <div class="section-title">Reminders</div>
      <div class="d-flex gap-4 flex-wrap">
        <div class="form-check"><input class="form-check-input" type="checkbox" checked id="r1"><label class="form-check-label small" for="r1">SMS 48 h before</label></div>
        <div class="form-check"><input class="form-check-input" type="checkbox" checked id="r2"><label class="form-check-label small" for="r2">SMS 2 h before</label></div>
        <div class="form-check"><input class="form-check-input" type="checkbox" id="r3"><label class="form-check-label small" for="r3">Email confirmation now</label></div>
        <div class="form-check"><input class="form-check-input" type="checkbox" id="r4"><label class="form-check-label small" for="r4">Add to waiting list for an earlier slot</label></div>
      </div>
    """) + """
  </div>

  <div class="col-xl-5">
    """ + card("Find a slot", """
      <div class="row g-2 mb-3">
        <div class="col-7"><label class="form-label">Date</label>""" + txt("", "2026-08-28", "date") + """</div>
        <div class="col-5"><label class="form-label">Part of day</label>""" + sel(["Any", "Morning", "Afternoon"]) + """</div>
      </div>
      <div class="d-flex justify-content-between align-items-center mb-2">
        <span class="small fw-semibold">Friday 28 August · Dr. Bianchi</span>
        <span class="small text-muted">45 min slots</span>
      </div>
      <div class="row g-2">
        <div class="col-4">""" + _slot("08:00", "free") + """</div>
        <div class="col-4">""" + _slot("08:45", "busy") + """</div>
        <div class="col-4">""" + _slot("09:30", "busy") + """</div>
        <div class="col-4">""" + _slot("10:15", "free") + """</div>
        <div class="col-4">""" + _slot("11:00", "free") + """</div>
        <div class="col-4">""" + _slot("11:45", "busy") + """</div>
        <div class="col-4">""" + _slot("13:00", "free") + """</div>
        <div class="col-4">""" + _slot("13:45", "free") + """</div>
        <div class="col-4">""" + _slot("14:00", "sel") + """</div>
        <div class="col-4">""" + _slot("15:15", "free") + """</div>
        <div class="col-4">""" + _slot("16:00", "busy") + """</div>
        <div class="col-4">""" + _slot("16:45", "free") + """</div>
      </div>
    """, sub="Greyed slots are already taken") + """

    <div class="mt-3">""" + card("Summary", """
      <dl class="dl-x">
        <dt>Patient</dt><dd>Marcus Kelly · PT-10428</dd>
        <dt>Procedure</dt><dd>D2392 — Composite, two surfaces · #27</dd>
        <dt>With</dt><dd>Dr. Luca Bianchi · Chair 2</dd>
        <dt>When</dt><dd>Friday 28 August 2026, 14:00 – 14:45</dd>
        <dt>Estimated fee</dt><dd data-roles="Admin,Receptionist">$240.00 · insurance covers $168.00</dd>
      </dl>
      <button class="btn btn-brand w-100"><i class="bi bi-check2 me-1"></i>Confirm booking</button>
      <button class="btn btn-soft w-100 mt-2">Save &amp; book another</button>
    """) + """</div>
  </div>
</div>
"""}

# =========================================================================
# appointments-reschedule.html
# =========================================================================
PAGES["appointments-reschedule.html"] = {
    "title": "Reschedule",
    "razor": "Views/Appointments/Reschedule.cshtml",
    "body": head([("Home", "dashboard-admin.html"), ("Appointments", "appointments-index.html"), ("Reschedule", "")],
                 "Reschedule or cancel",
                 "Appointment APT-88421 · Rania Jabari · 14 Aug 2026, 11:30",
                 '<a class="btn btn-soft" href="appointments-index.html">Back</a>'
                 '<button class="btn btn-brand"><i class="bi bi-arrow-left-right me-1"></i>Move appointment</button>') + """
<div class="row g-3">
  <div class="col-xl-5">
    """ + card("Current appointment", """
      <div class="d-flex gap-3 mb-3">
        <span class="avatar lg">RJ</span>
        <div>
          <h3 style="font-size:16px;margin:0">Rania Jabari</h3>
          <div class="text-muted small">PT-10233 · 42 y · +1 415 302 5566</div>
          <div class="mt-2">""" + pill("Unconfirmed", "amber") + """</div>
        </div>
      </div>
      <dl class="dl-x">
        <dt>Procedure</dt><dd>D3330 — Root canal therapy, molar (session 2 of 2)</dd>
        <dt>Dentist / chair</dt><dd>Dr. Luca Bianchi · Chair 2</dd>
        <dt>When</dt><dd>Thursday 14 August 2026, 11:30 – 12:30</dd>
        <dt>Booked</dt><dd>29 July 2026 by Priya Nair</dd>
        <dt>Reminders sent</dt><dd>SMS 12 Aug · SMS 14 Aug 09:30 — no reply</dd>
      </dl>
      <div class="alert alert-warning py-2 px-3 small mb-0">
        <i class="bi bi-exclamation-triangle me-1"></i>Outstanding balance $420.00 — front desk should collect before the next visit.
      </div>
    """) + """
  </div>

  <div class="col-xl-7">
    """ + card("Move to a new slot", """
      <div class="row g-2 mb-3">
        <div class="col-md-4"><label class="form-label">New date</label>""" + txt("", "2026-08-18", "date") + """</div>
        <div class="col-md-4"><label class="form-label">Dentist</label>""" + sel(["Dr. Luca Bianchi", "Dr. Amara Okafor", "Dr. Sofia Reyes"]) + """</div>
        <div class="col-md-4"><label class="form-label">Duration</label>""" + sel(["60 min", "45 min", "90 min"]) + """</div>
      </div>
      <div class="row g-2">
        <div class="col-3">""" + _slot("09:00", "free") + """</div>
        <div class="col-3">""" + _slot("10:00", "busy") + """</div>
        <div class="col-3">""" + _slot("11:00", "sel") + """</div>
        <div class="col-3">""" + _slot("13:00", "free") + """</div>
        <div class="col-3">""" + _slot("14:00", "free") + """</div>
        <div class="col-3">""" + _slot("15:00", "busy") + """</div>
        <div class="col-3">""" + _slot("16:00", "free") + """</div>
        <div class="col-3">""" + _slot("16:45", "free") + """</div>
      </div>
      <div class="row mt-2">
        """ + field("Reason for the change", sel(["Patient request", "Clinician unavailable", "Clinical reason",
                                                  "Emergency slot needed", "Practice closure", "Other"]), "col-md-6") + """
        """ + field("Note (internal)", txt("Optional"), "col-md-6") + """
      </div>
      <div class="d-flex gap-4 flex-wrap mb-3">
        <div class="form-check"><input class="form-check-input" type="checkbox" checked id="n1"><label class="form-check-label small" for="n1">Notify patient by SMS</label></div>
        <div class="form-check"><input class="form-check-input" type="checkbox" id="n2"><label class="form-check-label small" for="n2">Notify by email</label></div>
        <div class="form-check"><input class="form-check-input" type="checkbox" checked id="n3"><label class="form-check-label small" for="n3">Offer the freed slot to the waiting list</label></div>
      </div>
      <div class="d-flex gap-2 flex-wrap">
        <button class="btn btn-brand"><i class="bi bi-arrow-left-right me-1"></i>Move to Mon 18 Aug, 11:00</button>
        <button class="btn btn-soft" data-bs-toggle="modal" data-bs-target="#cancelModal"><i class="bi bi-x-circle me-1"></i>Cancel appointment</button>
        <button class="btn btn-soft" data-roles="Admin,Receptionist"><i class="bi bi-person-x me-1"></i>Mark as no-show</button>
      </div>
    """) + """
  </div>
</div>

<!-- Cancel confirmation — Views/Appointments/_CancelModal.cshtml -->
<div class="modal fade" id="cancelModal" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header border-0 pb-0"><h5 class="modal-title">Cancel this appointment?</h5>
        <button class="btn-close" data-bs-dismiss="modal"></button></div>
      <div class="modal-body">
        <p class="text-muted small">Rania Jabari · 14 Aug 2026, 11:30 · Root canal session 2.</p>
        <label class="form-label">Cancellation reason</label>
        """ + sel(["Patient request", "Patient unwell", "Clinician unavailable", "Late cancellation (&lt;24 h)", "Other"]) + """
        <div class="form-check mt-3"><input class="form-check-input" type="checkbox" checked id="c1"><label class="form-check-label small" for="c1">Send cancellation SMS</label></div>
        <div class="form-check"><input class="form-check-input" type="checkbox" checked id="c2"><label class="form-check-label small" for="c2">Release the slot to the waiting list</label></div>
        <div class="form-check" data-roles="Admin,Receptionist"><input class="form-check-input" type="checkbox" id="c3"><label class="form-check-label small" for="c3">Apply late-cancellation fee ($40)</label></div>
      </div>
      <div class="modal-footer border-0">
        <button class="btn btn-soft" data-bs-dismiss="modal">Keep appointment</button>
        <button class="btn btn-danger">Cancel appointment</button>
      </div>
    </div>
  </div>
</div>
"""}

# =========================================================================
# appointments-waitlist.html
# =========================================================================
_wl_rows = []
for ini, name, pid, want, pref, waited, urg, tone in [
    ("AC", "Aisha Chowdhury", "PT-10455", "Crown prep #16 · 60 min", "Any weekday morning", "11 days", "Urgent", "red"),
    ("HN", "Hugo Nakamura", "PT-10310", "Extraction #48 · 45 min", "Mon / Wed only", "8 days", "Urgent", "red"),
    ("GM", "Grace Mbeki", "PT-10061", "Check-up · 30 min", "After 16:00", "6 days", "Routine", "gray"),
    ("SN", "Sara Nowak", "PT-10188", "Implant review · 30 min", "Any", "4 days", "Routine", "gray"),
    ("PL", "Peter Lindqvist", "PT-10099", "Denture adjustment · 30 min", "Tue / Thu", "3 days", "Routine", "gray"),
    ("EW", "Elena Whitfield", "PT-10391", "Hygiene · 45 min", "Saturday preferred", "1 day", "Routine", "gray"),
]:
    _wl_rows.append(
        '<tr><td>%s</td><td>%s</td><td class="t-sub">%s</td><td>%s</td><td>%s</td>'
        '<td class="text-end"><a class="btn btn-brand btn-sm" href="appointments-create.html">Offer slot</a> '
        '<button class="btn btn-ghost btn-sm"><i class="bi bi-x-lg"></i></button></td></tr>'
        % (person(ini, name, pid), want, pref, waited, pill(urg, tone)))

PAGES["appointments-waitlist.html"] = {
    "title": "Waiting list",
    "razor": "Views/Appointments/WaitingList.cshtml",
    "body": head([("Home", "dashboard-admin.html"), ("Appointments", "appointments-index.html"), ("Waiting list", "")],
                 "Waiting list",
                 "6 patients want an earlier slot · 1 slot freed today",
                 '<a class="btn btn-soft" href="appointments-calendar.html"><i class="bi bi-calendar3 me-1"></i>Calendar</a>'
                 '<button class="btn btn-brand"><i class="bi bi-broadcast me-1"></i>Broadcast free slot</button>') + """
<div class="row g-3 mb-3">
  <div class="col-12">
    <div class="card-x" style="border-color:var(--brand-100);background:var(--brand-50)">
      <div class="card-x-body d-flex flex-wrap gap-3 align-items-center">
        <span class="ic ic-teal" style="width:42px;height:42px;border-radius:13px;display:grid;place-items:center"><i class="bi bi-calendar2-check"></i></span>
        <div class="flex-grow-1">
          <div class="fw-semibold">A slot has just freed up — Friday 15 Aug, 13:30 · Chair 2 · 60 min</div>
          <div class="text-muted small">2 waiting patients match the duration and their stated preferences.</div>
        </div>
        <button class="btn btn-brand"><i class="bi bi-send me-1"></i>Offer to matching patients</button>
      </div>
    </div>
  </div>
</div>
""" + card_flush("", table(
        ["Patient", "Wants", "Availability", "Waiting", "Priority", ("", ' class="text-end"')],
        ["".join(_wl_rows)]),
        actions='<div style="min-width:180px">' + sel(["All priorities", "Urgent only", "Routine only"]) + "</div>") + """
"""}

# =========================================================================
# treatments-chart.html  (odontogram)
# =========================================================================
TOOTH_SVG = ('<svg viewBox="0 0 24 28" aria-hidden="true"><path d="M12 2c4.2 0 8 2.1 8 7 0 4-1.6 6.1-2.1 10.1'
             'C17.4 22.6 16.8 26 15.3 26S13.4 22 12 22s-1.9 4-3.4 4-2-3.4-2.5-6.9C5.6 15.1 4 13 4 9c0-4.9 3.8-7 8-7z" '
             'fill="currentColor" fill-opacity=".14" stroke="currentColor" stroke-opacity=".5" stroke-width="1.3"/></svg>')

PRESET = {"16": "crown", "26": "caries", "27": "caries", "36": "rct", "38": "missing",
          "46": "filled", "47": "filled", "48": "extract", "11": "filled", "21": "filled",
          "34": "implant"}


def _quad(nums, lower=False):
    out = []
    for n in nums:
        st = PRESET.get(n, "healthy")
        out.append('<button class="tooth%s" data-tooth="%s" data-state="%s" type="button">'
                   '<span class="crown">%s</span><span class="num">%s</span></button>'
                   % (" lower" if lower else "", n, st, TOOTH_SVG, n))
    return '<div class="quad">%s</div>' % "".join(out)


UR = [str(n) for n in range(18, 10, -1)]     # 18..11
UL = [str(n) for n in range(21, 29)]         # 21..28
LR = [str(n) for n in range(48, 40, -1)]     # 48..41
LL = [str(n) for n in range(31, 39)]         # 31..38

_odontogram = """
<div class="chart-wrap">
  <div class="arch">
    <div class="arch-label">Upper — maxillary</div>
    <div class="arch-row">%s%s</div>
    <div class="arch-label">Lower — mandibular</div>
    <div class="arch-row">%s%s</div>
  </div>
</div>
""" % (_quad(UR), _quad(UL), _quad(LR, True), _quad(LL, True))

_legend = """
<div class="legend">
  <span class="lg" data-state="healthy"><span class="sw"></span>Sound</span>
  <span class="lg" data-state="caries"><span class="sw" style="background:#fdecec;border-color:#ef4444"></span>Caries</span>
  <span class="lg" data-state="filled"><span class="sw" style="background:#e8f0fe;border-color:#3b82f6"></span>Restoration</span>
  <span class="lg" data-state="crown"><span class="sw" style="background:#fef4e2;border-color:#f59e0b"></span>Crown / onlay</span>
  <span class="lg" data-state="rct"><span class="sw" style="background:#f1ecfe;border-color:#8b5cf6"></span>Root canal</span>
  <span class="lg" data-state="implant"><span class="sw" style="background:#e7f8f1;border-color:#10b981"></span>Implant</span>
  <span class="lg" data-state="extract"><span class="sw" style="background:#fdecec;border-color:#b91c1c;border-style:dashed"></span>Planned extraction</span>
  <span class="lg" data-state="missing"><span class="sw" style="background:#e2e8f0;border-style:dashed"></span>Missing</span>
</div>
<div class="text-muted small mt-2" id="brushHint">Pick a condition, then click a tooth. Clicking without a brush cycles through states.</div>
"""

PAGES["treatments-chart.html"] = {
    "title": "Dental chart",
    "razor": "Views/Treatments/Chart.cshtml",
    "body": head([("Home", "dashboard-dentist.html"), ("Patients", "patients-index.html"),
                  ("Marcus Kelly", "patients-details.html"), ("Chart", "")],
                 "Dental chart — Marcus Kelly",
                 "PT-10428 · FDI notation · charted 14 Aug 2026 by Dr. Luca Bianchi",
                 '<button class="btn btn-soft"><i class="bi bi-clock-history me-1"></i>Chart history</button>'
                 '<a class="btn btn-soft" href="treatments-plan.html"><i class="bi bi-clipboard2-pulse me-1"></i>Treatment plan</a>'
                 '<button class="btn btn-brand"><i class="bi bi-pen me-1"></i>Sign &amp; save</button>') + """
<div class="row g-3">
  <div class="col-xl-8">
    """ + card("Odontogram", _odontogram + '<hr class="my-3">' + _legend,
               sub="Interactive — this is the real behaviour, not a picture",
               actions='<div class="btn-group btn-group-sm"><button class="btn btn-soft active">Adult</button>'
                       '<button class="btn btn-soft">Primary</button></div>') + """

    <div class="mt-3" id="toothPanel">
      """ + card('<span id="selTooth">Tooth 26</span>', """
        <div class="d-flex gap-2 flex-wrap mb-3">
          <span class="pill pill-teal">Current state: <strong id="selState">Caries</strong></span>
          <span class="pill pill-gray">Surfaces: MO</span>
        </div>
        <div class="row">
          """ + field("Finding", sel(["Caries", "Sound", "Existing restoration", "Fractured", "Sensitive", "Mobility"]), "col-md-4") + """
          """ + field("Surfaces", sel(["MO", "O", "MOD", "DO", "B", "L"]), "col-md-4") + """
          """ + field("Planned procedure", sel(["D2392 — Composite, two surfaces", "D2740 — Crown", "D3330 — Root canal", "None"]), "col-md-4") + """
          """ + field("Clinical note", area("Findings, materials, anaesthetic, patient response…", 3,
                                            "MO caries, moderate depth, no pulpal involvement. Articaine 4% infiltration. Composite A2, incremental cure, occlusion checked."), "col-12") + """
        </div>
        <div class="d-flex gap-2 flex-wrap">
          <button class="btn btn-brand btn-sm"><i class="bi bi-check2 me-1"></i>Save finding</button>
          <button class="btn btn-soft btn-sm"><i class="bi bi-plus-lg me-1"></i>Add to treatment plan</button>
          <button class="btn btn-soft btn-sm"><i class="bi bi-image me-1"></i>Attach radiograph</button>
        </div>
      """, sub="Click any tooth above to load its record") + """
    </div>
  </div>

  <div class="col-xl-4">
    """ + card("Patient", """
      <div class="d-flex gap-3">
        <span class="avatar lg">MK</span>
        <div><h3 style="font-size:16px;margin:0">Marcus Kelly</h3>
        <div class="text-muted small">PT-10428 · 34 y · Male</div></div>
      </div>
      <div class="d-flex gap-2 flex-wrap mt-3">
        <span class="pill pill-red"><i class="bi bi-exclamation-triangle-fill"></i>Penicillin allergy</span>
        <span class="pill pill-amber"><i class="bi bi-heart-pulse-fill"></i>Hypertension</span>
      </div>
      <hr>
      <a class="btn btn-soft btn-sm w-100" href="patients-details.html"><i class="bi bi-folder2-open me-1"></i>Full record</a>
    """) + """

    <div class="mt-3">""" + card_flush("Charted findings", table(
        ["Tooth", "Finding", "Status"],
        ["".join([
            '<tr><td class="t-main">26</td><td>Caries MO</td><td>' + pill("Treating today", "amber") + '</td></tr>',
            '<tr><td class="t-main">27</td><td>Caries O</td><td>' + pill("Planned", "blue") + '</td></tr>',
            '<tr><td class="t-main">16</td><td>Crown, ceramic</td><td>' + pill("Existing", "gray") + '</td></tr>',
            '<tr><td class="t-main">36</td><td>Root canal + crown</td><td>' + pill("Existing", "gray") + '</td></tr>',
            '<tr><td class="t-main">38</td><td>Missing (extracted 2025)</td><td>' + pill("Historic", "gray") + '</td></tr>',
            '<tr><td class="t-main">48</td><td>Impacted</td><td>' + pill("Extraction planned", "red") + '</td></tr>',
            '<tr><td class="t-main">34</td><td>Implant + crown</td><td>' + pill("Existing", "gray") + '</td></tr>',
        ])])) + """</div>

    <div class="mt-3">""" + card("Periodontal summary", """
      <div class="d-flex justify-content-between small mb-1"><span>BPE sextant scores</span><span class="text-muted">12 Feb 2026</span></div>
      <div class="d-flex gap-1 mb-3">
        <span class="pill pill-green">1</span><span class="pill pill-green">1</span><span class="pill pill-amber">2</span>
        <span class="pill pill-green">1</span><span class="pill pill-amber">2</span><span class="pill pill-green">1</span>
      </div>
      <div class="d-flex justify-content-between small mb-1"><span>Plaque score</span><span class="fw-semibold">18%</span></div>
      <div class="stat-bar mb-2"><span style="width:18%"></span></div>
      <div class="d-flex justify-content-between small mb-1"><span>Bleeding on probing</span><span class="fw-semibold">11%</span></div>
      <div class="stat-bar"><span style="width:11%"></span></div>
    """) + """</div>
  </div>
</div>
"""}

# =========================================================================
# treatments-plan.html
# =========================================================================
_plan_row = lambda ph, code, desc, tooth, fee, ins, st, tone: (
    '<tr><td>%s</td><td class="t-main">%s</td><td>%s<div class="t-sub">Tooth %s</div></td>'
    '<td class="text-end">%s</td><td class="text-end text-muted">%s</td><td>%s</td>'
    '<td class="text-end"><button class="btn btn-ghost btn-sm"><i class="bi bi-three-dots"></i></button></td></tr>'
    % (ph, code, desc, tooth, fee, ins, pill(st, tone)))

PAGES["treatments-plan.html"] = {
    "title": "Treatment plan",
    "razor": "Views/Treatments/Plan.cshtml",
    "body": head([("Home", "dashboard-dentist.html"), ("Patients", "patients-index.html"),
                  ("Marcus Kelly", "patients-details.html"), ("Treatment plan", "")],
                 "Treatment plan — Marcus Kelly",
                 "PLAN-3312 · created 12 Aug 2026 by Dr. Luca Bianchi · consent signed",
                 '<button class="btn btn-soft"><i class="bi bi-printer me-1"></i>Print estimate</button>'
                 '<button class="btn btn-soft" data-roles="Admin,Receptionist"><i class="bi bi-receipt me-1"></i>Convert to invoice</button>'
                 '<button class="btn btn-brand"><i class="bi bi-plus-lg me-1"></i>Add procedure</button>') + """
<div class="row g-3 mb-3">""" + (
        kpi("bi-list-ol", "teal", "3", "Phases") +
        kpi("bi-cash", "green", "$1,240", "Plan total") +
        kpi("bi-shield-check", "blue", "$820", "Insurance estimate") +
        kpi("bi-percent", "amber", "35%", "Completed")) + """
</div>

<div class="row g-3">
  <div class="col-xl-8">
    """ + card_flush("Planned procedures", table(
        ["Phase", "Code", "Procedure", ("Fee", ' class="text-end"'), ("Insurance", ' class="text-end"'), "Status", ""],
        ["".join([
            _plan_row("1", "D2392", "Composite restoration, two surfaces", "26", "$240.00", "$168.00", "In progress", "amber"),
            _plan_row("1", "D2391", "Composite restoration, one surface", "27", "$180.00", "$126.00", "Scheduled", "blue"),
            _plan_row("2", "D7140", "Extraction, erupted tooth", "48", "$220.00", "$154.00", "Planned", "gray"),
            _plan_row("2", "D1110", "Prophylaxis, adult", "—", "$110.00", "$110.00", "Planned", "gray"),
            _plan_row("3", "D2740", "Crown, porcelain / ceramic", "16", "$490.00", "$262.00", "Planned", "gray"),
        ])]),
        foot="""<div class="d-flex justify-content-end">
          <table style="font-size:13.5px">
            <tr><td class="pe-4 text-muted">Subtotal</td><td class="text-end fw-semibold">$1,240.00</td></tr>
            <tr><td class="pe-4 text-muted">Estimated insurance</td><td class="text-end fw-semibold text-success">− $820.00</td></tr>
            <tr><td class="pe-4 text-muted">Patient portion</td><td class="text-end fw-bold" style="font-size:15px">$420.00</td></tr>
          </table></div>""") + """

    <div class="mt-3">""" + card("Consent &amp; communication", """
      <div class="row g-3">
        <div class="col-md-6">
          <div class="d-flex gap-3 p-3 rounded" style="border:1px solid var(--line)">
            <i class="bi bi-file-earmark-check text-success" style="font-size:22px"></i>
            <div><div class="fw-semibold" style="font-size:13.5px">Treatment consent</div>
            <div class="text-muted small">Signed 12 Aug 2026 · digital signature on file</div>
            <a href="#" class="small">View document</a></div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="d-flex gap-3 p-3 rounded" style="border:1px solid var(--line)">
            <i class="bi bi-envelope-paper text-secondary" style="font-size:22px"></i>
            <div><div class="fw-semibold" style="font-size:13.5px">Estimate sent to patient</div>
            <div class="text-muted small">12 Aug 2026 · email · opened</div>
            <a href="#" class="small">Resend</a></div>
          </div>
        </div>
      </div>
    """) + """</div>
  </div>

  <div class="col-xl-4">
    """ + card("Phasing", """
      <div class="tl">
        <div class="tl-item"><span class="dot"></span>
          <div class="tl-t">Phase 1 — Stabilise <span class="pill pill-amber ms-1">In progress</span></div>
          <div class="tl-m">Restore #26 and #27 · 2 visits · $420</div></div>
        <div class="tl-item"><span class="dot" style="border-color:#cbd5e1"></span>
          <div class="tl-t">Phase 2 — Surgical &amp; hygiene</div>
          <div class="tl-m">Extract #48, full prophylaxis · 2 visits · $330</div></div>
        <div class="tl-item"><span class="dot" style="border-color:#cbd5e1"></span>
          <div class="tl-t">Phase 3 — Restore</div>
          <div class="tl-m">Crown #16 · 2 visits · $490</div></div>
      </div>
      <button class="btn btn-soft btn-sm w-100 mt-3"><i class="bi bi-calendar-plus me-1"></i>Book the next phase</button>
    """) + """
    <div class="mt-3">""" + card("Alternatives discussed", """
      <div class="d-flex justify-content-between align-items-start mb-2">
        <div><div class="fw-semibold" style="font-size:13.5px">#16 — Crown vs large composite</div>
        <div class="text-muted small">Composite $260 · shorter lifespan discussed</div></div>
        <span class="pill pill-gray">Declined</span>
      </div>
      <div class="d-flex justify-content-between align-items-start">
        <div><div class="fw-semibold" style="font-size:13.5px">#48 — Extraction vs monitor</div>
        <div class="text-muted small">Recurrent pericoronitis; extraction advised</div></div>
        <span class="pill pill-green">Accepted</span>
      </div>
    """) + """</div>
  </div>
</div>
"""}

# =========================================================================
# treatments-procedures.html
# =========================================================================
_proc_rows = []
for code, name, cat, dur, fee, ins in [
    ("D0120", "Periodic oral evaluation", "Diagnostic", "15 min", "$65.00", "100%"),
    ("D0274", "Bitewing radiographs — four films", "Diagnostic", "10 min", "$85.00", "100%"),
    ("D1110", "Prophylaxis — adult", "Preventive", "45 min", "$110.00", "100%"),
    ("D1206", "Topical fluoride varnish", "Preventive", "10 min", "$45.00", "80%"),
    ("D2391", "Composite restoration — one surface", "Restorative", "30 min", "$180.00", "70%"),
    ("D2392", "Composite restoration — two surfaces", "Restorative", "45 min", "$240.00", "70%"),
    ("D2740", "Crown — porcelain / ceramic", "Prosthetic", "90 min", "$490.00", "50%"),
    ("D3310", "Endodontic therapy — anterior", "Endodontic", "75 min", "$620.00", "70%"),
    ("D3330", "Endodontic therapy — molar", "Endodontic", "120 min", "$890.00", "70%"),
    ("D4341", "Periodontal scaling — per quadrant", "Periodontal", "45 min", "$195.00", "80%"),
    ("D6010", "Surgical implant placement", "Surgical", "120 min", "$1,850.00", "50%"),
    ("D7140", "Extraction — erupted tooth", "Surgical", "45 min", "$220.00", "70%"),
]:
    _proc_rows.append(
        '<tr><td class="t-main">%s</td><td>%s</td><td>%s</td><td>%s</td>'
        '<td class="text-end fw-semibold">%s</td><td class="text-end">%s</td>'
        '<td class="text-end"><button class="btn btn-ghost btn-sm" data-roles="Admin"><i class="bi bi-pencil"></i></button>'
        '<a class="btn btn-ghost btn-sm" href="appointments-create.html"><i class="bi bi-calendar-plus"></i></a></td></tr>'
        % (code, name, '<span class="pill pill-gray">%s</span>' % cat, dur, fee, ins))

PAGES["treatments-procedures.html"] = {
    "title": "Procedure catalogue",
    "razor": "Views/Treatments/Procedures.cshtml",
    "body": head([("Home", "dashboard-admin.html"), ("Clinical", ""), ("Procedure catalogue", "")],
                 "Procedure &amp; fee catalogue",
                 "128 procedures · fee schedule 2026 · effective 01 Jan 2026",
                 '<button class="btn btn-soft" data-roles="Admin"><i class="bi bi-upload me-1"></i>Import fee schedule</button>'
                 '<button class="btn btn-brand" data-roles="Admin"><i class="bi bi-plus-lg me-1"></i>Add procedure</button>') + """
""" + card("", """
<div class="row g-2 align-items-end">
  <div class="col-lg-4 col-md-6"><label class="form-label">Search</label>
    <div class="input-group"><span class="input-group-text bg-white border-end-0"><i class="bi bi-search text-muted"></i></span>
    <input class="form-control border-start-0" placeholder="Code or description"></div></div>
  <div class="col-lg-3 col-md-6"><label class="form-label">Category</label>""" +
           sel(["All categories", "Diagnostic", "Preventive", "Restorative", "Endodontic",
                "Periodontal", "Prosthetic", "Surgical", "Orthodontic"]) + """</div>
  <div class="col-lg-3 col-md-6"><label class="form-label">Fee schedule</label>""" +
           sel(["Standard 2026", "Insurance — Delta", "Insurance — Cigna", "Concession"]) + """</div>
  <div class="col-lg-2 col-md-6"><button class="btn btn-brand w-100">Apply</button></div>
</div>
""") + """
<div class="mt-3">
""" + card_flush("", table(
        ["Code", "Procedure", "Category", "Chair time", ("Fee", ' class="text-end"'),
         ("Typical cover", ' class="text-end"'), ("", ' class="text-end"')],
        ["".join(_proc_rows)]),
        foot='<span class="text-muted small">Showing 12 of 128 · fees shown are practice defaults and can be overridden per invoice line.</span>') + """
</div>
"""}

# =========================================================================
# treatments-prescriptions.html
# =========================================================================
PAGES["treatments-prescriptions.html"] = {
    "title": "Prescriptions",
    "razor": "Views/Treatments/Prescriptions.cshtml",
    "body": head([("Home", "dashboard-dentist.html"), ("Clinical", ""), ("Prescriptions", "")],
                 "Prescriptions",
                 "Marcus Kelly · PT-10428 · allergy: penicillin",
                 '<a class="btn btn-soft" href="patients-details.html">Patient record</a>'
                 '<button class="btn btn-brand"><i class="bi bi-printer me-1"></i>Print &amp; sign</button>') + """
<div class="row g-3">
  <div class="col-xl-6">
    """ + card("New prescription", """
      <div class="alert alert-danger py-2 px-3 small"><i class="bi bi-exclamation-triangle-fill me-1"></i>
        <strong>Allergy alert:</strong> penicillin — amoxicillin and derivatives are blocked for this patient.</div>
      <div class="row">
        """ + field("Medication", sel(["Metronidazole 400 mg", "Clindamycin 150 mg", "Ibuprofen 400 mg",
                                       "Paracetamol 500 mg", "Chlorhexidine 0.2% mouthwash"]), "col-md-6", req=True) + """
        """ + field("Form", sel(["Tablet", "Capsule", "Suspension", "Mouthwash", "Gel"]), "col-md-6") + """
        """ + field("Dose", txt("", "400 mg"), "col-md-4", req=True) + """
        """ + field("Frequency", sel(["Three times daily", "Twice daily", "Four times daily", "As required"]), "col-md-4") + """
        """ + field("Duration", sel(["5 days", "3 days", "7 days", "10 days"]), "col-md-4") + """
        """ + field("Quantity", txt("", "15 tablets"), "col-md-4") + """
        """ + field("Repeats", sel(["0", "1", "2"]), "col-md-4") + """
        """ + field("Route", sel(["Oral", "Topical"]), "col-md-4") + """
        """ + field("Directions to patient", area("", 2, "Take one tablet three times a day with food. Complete the full course. Avoid alcohol."), "col-12") + """
      </div>
      <div class="d-flex gap-2">
        <button class="btn btn-brand"><i class="bi bi-pen me-1"></i>Sign &amp; issue</button>
        <button class="btn btn-soft">Save draft</button>
      </div>
    """) + """
  </div>

  <div class="col-xl-6">
    """ + card_flush("Prescription history", table(
        ["Date", "Medication", "Prescriber", "Status"],
        ["".join([
            '<tr><td>12 Aug 2026</td><td class="t-main">Ibuprofen 400 mg<div class="t-sub">TDS, 5 days</div></td>'
            '<td>Dr. Bianchi</td><td>' + pill("Issued", "green") + '</td></tr>',
            '<tr><td>03 Sep 2025</td><td class="t-main">Metronidazole 400 mg<div class="t-sub">TDS, 5 days</div></td>'
            '<td>Dr. Okafor</td><td>' + pill("Completed", "gray") + '</td></tr>',
            '<tr><td>03 Sep 2025</td><td class="t-main">Chlorhexidine 0.2%<div class="t-sub">Rinse BD, 7 days</div></td>'
            '<td>Dr. Okafor</td><td>' + pill("Completed", "gray") + '</td></tr>',
        ])])) + """
    <div class="mt-3">""" + card("Printed prescription preview", """
      <div class="p-3 rounded" style="border:1px solid var(--line);background:#fff">
        <div class="d-flex justify-content-between align-items-start mb-3">
          <div><div class="fw-bold">Bright Smile Dental — Riverside</div>
          <div class="text-muted small">1180 Riverside Drive, San Francisco, CA 94107</div></div>
          <span class="avatar">Rx</span>
        </div>
        <hr>
        <div class="small"><strong>Patient:</strong> Marcus Kelly · DOB 18 Mar 1992</div>
        <div class="small mb-3"><strong>Allergies:</strong> Penicillin, latex</div>
        <div class="p-2 rounded mb-3" style="background:#f8fafc">
          <div class="fw-semibold">Metronidazole 400 mg tablets</div>
          <div class="small text-muted">One tablet three times daily with food for 5 days. 15 tablets. No repeats.</div>
        </div>
        <div class="d-flex justify-content-between align-items-end">
          <div class="small text-muted">Issued 14 Aug 2026</div>
          <div class="text-end"><div style="border-top:1px solid var(--line);width:150px"></div>
          <div class="small text-muted">Dr. Luca Bianchi · GDC 284119</div></div>
        </div>
      </div>
    """) + """</div>
  </div>
</div>
"""}
