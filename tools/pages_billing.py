# -*- coding: utf-8 -*-
"""Invoicing, payments and insurance-claim screens."""
from ui import head, kpi, card, card_flush, table, person, pill, field, txt, sel, area

PAGES = {}

# =========================================================================
# billing-invoices.html
# =========================================================================
_inv_rows = []
for num, ini, name, pid, date, due, total, paid, bal, status, tone in [
    ("INV-2481", "RJ", "Rania Jabari", "PT-10233", "29 Jul 2026", "28 Aug 2026", "$890.00", "$470.00", "$420.00", "Part paid", "amber"),
    ("INV-2480", "AC", "Aisha Chowdhury", "PT-10455", "10 Aug 2026", "09 Sep 2026", "$490.00", "$0.00", "$490.00", "Sent", "blue"),
    ("INV-2479", "SN", "Sara Nowak", "PT-10188", "09 Aug 2026", "08 Sep 2026", "$120.00", "$0.00", "$120.00", "Sent", "blue"),
    ("INV-2478", "MK", "Marcus Kelly", "PT-10428", "12 Aug 2026", "11 Sep 2026", "$310.00", "$310.00", "$0.00", "Paid", "green"),
    ("INV-2477", "EW", "Elena Whitfield", "PT-10391", "12 Aug 2026", "11 Sep 2026", "$65.00", "$0.00", "$65.00", "Due today", "amber"),
    ("INV-2451", "PL", "Peter Lindqvist", "PT-10099", "02 Jul 2026", "01 Aug 2026", "$740.00", "$0.00", "$740.00", "Overdue 30 d", "red"),
    ("INV-2448", "HN", "Hugo Nakamura", "PT-10310", "28 Jun 2026", "28 Jul 2026", "$220.00", "$220.00", "$0.00", "Paid", "green"),
    ("INV-2440", "GM", "Grace Mbeki", "PT-10061", "21 Jun 2026", "21 Jul 2026", "$185.00", "$0.00", "$185.00", "Overdue 24 d", "red"),
    ("INV-2432", "TA", "Tobias Ackerman", "PT-10502", "18 Jun 2026", "18 Jul 2026", "$1,240.00", "$1,240.00", "$0.00", "Paid", "green"),
    ("INV-2428", "DS", "Daniel Sorenson", "PT-10477", "15 Jun 2026", "15 Jul 2026", "$0.00", "$0.00", "$0.00", "Draft", "gray"),
]:
    _inv_rows.append(
        '<tr><td><input class="form-check-input" type="checkbox"></td>'
        '<td class="fw-semibold"><a class="text-decoration-none" href="billing-invoice-details.html">%s</a></td>'
        '<td>%s</td><td>%s<div class="t-sub">due %s</div></td>'
        '<td class="text-end">%s</td><td class="text-end text-muted">%s</td>'
        '<td class="text-end fw-semibold">%s</td><td>%s</td>'
        '<td class="text-end"><div class="dropdown"><button class="btn btn-ghost btn-sm" data-bs-toggle="dropdown"><i class="bi bi-three-dots"></i></button>'
        '<ul class="dropdown-menu dropdown-menu-end">'
        '<li><a class="dropdown-item" href="billing-invoice-details.html"><i class="bi bi-eye me-2"></i>View invoice</a></li>'
        '<li><a class="dropdown-item" href="billing-payments.html"><i class="bi bi-credit-card me-2"></i>Take payment</a></li>'
        '<li><a class="dropdown-item" href="#"><i class="bi bi-send me-2"></i>Send to patient</a></li>'
        '<li><a class="dropdown-item" href="billing-claims.html"><i class="bi bi-shield-check me-2"></i>Submit claim</a></li>'
        '<li><hr class="dropdown-divider"></li>'
        '<li><a class="dropdown-item text-danger" href="#" data-roles="Admin"><i class="bi bi-x-circle me-2"></i>Void invoice</a></li>'
        '</ul></div></td></tr>'
        % (num, person(ini, name, pid), date, due, total, paid, bal, pill(status, tone)))

PAGES["billing-invoices.html"] = {
    "title": "Invoices",
    "razor": "Views/Billing/Invoices.cshtml",
    "body": head([("Home", "dashboard-admin.html"), ("Billing", ""), ("Invoices", "")],
                 "Invoices",
                 "94 open · $36,240 outstanding · 11 overdue",
                 '<button class="btn btn-soft"><i class="bi bi-send me-1"></i>Send statements</button>'
                 '<a class="btn btn-brand" href="billing-invoice-create.html"><i class="bi bi-file-earmark-plus me-1"></i>New invoice</a>') + """
<div class="row g-3 mb-3">""" + (
        kpi("bi-cash-stack", "teal", "$36,240", "Total outstanding") +
        kpi("bi-hourglass", "amber", "$14,760", "Over 30 days") +
        kpi("bi-check2-circle", "green", "$171,930", "Collected this month") +
        kpi("bi-percent", "blue", "92.2%", "Collection rate")) + """
</div>

""" + card("", """
<div class="row g-2 align-items-end">
  <div class="col-lg-3 col-md-6"><label class="form-label">Search</label>
    <div class="input-group"><span class="input-group-text bg-white border-end-0"><i class="bi bi-search text-muted"></i></span>
    <input class="form-control border-start-0" placeholder="Invoice number or patient"></div></div>
  <div class="col-lg-2 col-md-3 col-6"><label class="form-label">Status</label>""" +
           sel(["All statuses", "Draft", "Sent", "Part paid", "Paid", "Overdue", "Void"]) + """</div>
  <div class="col-lg-2 col-md-3 col-6"><label class="form-label">Ageing</label>""" +
           sel(["Any", "Current", "31–60 days", "61–90 days", "90+ days"]) + """</div>
  <div class="col-lg-2 col-md-3 col-6"><label class="form-label">From</label>""" + txt("", "2026-06-01", "date") + """</div>
  <div class="col-lg-2 col-md-3 col-6"><label class="form-label">To</label>""" + txt("", "2026-08-14", "date") + """</div>
  <div class="col-lg-1 col-12"><button class="btn btn-brand w-100">Apply</button></div>
</div>
""") + """

<div class="mt-3">
""" + card_flush("", table(
        [('<input class="form-check-input" type="checkbox">', ' style="width:34px"'),
         "Invoice", "Patient", "Issued", ("Total", ' class="text-end"'), ("Paid", ' class="text-end"'),
         ("Balance", ' class="text-end"'), "Status", ("", ' class="text-end"')],
        ["".join(_inv_rows)]),
        actions='<div class="d-flex gap-2 flex-wrap"><button class="btn btn-soft btn-sm"><i class="bi bi-envelope me-1"></i>Chase selected</button>'
                '<button class="btn btn-soft btn-sm"><i class="bi bi-download me-1"></i>Export</button></div>',
        foot="""<div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
  <span class="text-muted small">Showing 1–10 of 94</span>
  <nav><ul class="pagination pagination-sm mb-0">
    <li class="page-item disabled"><span class="page-link">Previous</span></li>
    <li class="page-item active"><span class="page-link">1</span></li>
    <li class="page-item"><a class="page-link" href="#">2</a></li>
    <li class="page-item"><a class="page-link" href="#">Next</a></li>
  </ul></nav></div>""") + """
</div>
"""}

# =========================================================================
# billing-invoice-details.html
# =========================================================================
_line = lambda code, desc, tooth, qty, fee, disc, total: (
    '<tr><td class="t-main">%s</td><td>%s<div class="t-sub">Tooth %s</div></td>'
    '<td class="text-center">%s</td><td class="text-end">%s</td><td class="text-end text-muted">%s</td>'
    '<td class="text-end fw-semibold">%s</td></tr>' % (code, desc, tooth, qty, fee, disc, total))

PAGES["billing-invoice-details.html"] = {
    "title": "Invoice INV-2481",
    "razor": "Views/Billing/InvoiceDetails.cshtml",
    "body": head([("Home", "dashboard-admin.html"), ("Billing", "billing-invoices.html"), ("INV-2481", "")],
                 "Invoice INV-2481",
                 "Rania Jabari · PT-10233 · issued 29 July 2026 · due 28 August 2026",
                 '<button class="btn btn-soft"><i class="bi bi-printer me-1"></i>Print</button>'
                 '<button class="btn btn-soft"><i class="bi bi-send me-1"></i>Email to patient</button>'
                 '<a class="btn btn-brand" href="billing-payments.html"><i class="bi bi-credit-card me-1"></i>Take payment</a>') + """
<div class="row g-3">
  <div class="col-xl-8">
    """ + card_flush("", """
      <div class="card-x-body">
        <div class="d-flex justify-content-between flex-wrap gap-3">
          <div>
            <div class="d-flex align-items-center gap-2 mb-2">
              <span class="avatar"><i class="bi bi-hexagon-fill"></i></span>
              <div><div class="fw-bold">Bright Smile Dental</div>
              <div class="text-muted small">Riverside practice</div></div>
            </div>
            <div class="text-muted small">1180 Riverside Drive<br>San Francisco, CA 94107<br>+1 415 555 0110</div>
          </div>
          <div class="text-end">
            <div class="fw-bold" style="font-size:19px">INVOICE</div>
            <div class="text-muted small">INV-2481</div>
            <div class="mt-2">""" + pill("Part paid", "amber") + """</div>
          </div>
        </div>
        <hr>
        <div class="row">
          <div class="col-md-6">
            <div class="section-title">Bill to</div>
            <div class="fw-semibold">Rania Jabari</div>
            <div class="text-muted small">PT-10233<br>88 Marina Boulevard, Apt 12<br>San Francisco, CA 94123<br>+1 415 302 5566</div>
          </div>
          <div class="col-md-6">
            <div class="section-title">Details</div>
            <dl class="dl-x row">
              <div class="col-6"><dt>Issued</dt><dd>29 Jul 2026</dd></div>
              <div class="col-6"><dt>Due</dt><dd>28 Aug 2026</dd></div>
              <div class="col-6"><dt>Treating dentist</dt><dd>Dr. Luca Bianchi</dd></div>
              <div class="col-6"><dt>Insurer</dt><dd>Delta Dental · #DD-4471902</dd></div>
            </dl>
          </div>
        </div>
      </div>
      """ + table(["Code", "Description", ("Qty", ' class="text-center"'), ("Unit fee", ' class="text-end"'),
                   ("Discount", ' class="text-end"'), ("Amount", ' class="text-end"')],
                  ["".join([
                      _line("D3330", "Endodontic therapy — molar (session 1)", "36", "1", "$890.00", "—", "$890.00"),
                      _line("D0220", "Periapical radiograph — first film", "36", "2", "$45.00", "− $45.00", "$45.00"),
                      _line("D9110", "Palliative treatment of dental pain", "—", "1", "$95.00", "− $95.00", "$0.00"),
                  ])]) + """
      <div class="card-x-body pt-0">
        <div class="d-flex justify-content-end">
          <table style="font-size:13.5px;min-width:280px">
            <tr><td class="pe-4 text-muted">Subtotal</td><td class="text-end">$1,030.00</td></tr>
            <tr><td class="pe-4 text-muted">Discount</td><td class="text-end">− $140.00</td></tr>
            <tr><td class="pe-4 text-muted">Insurance estimate</td><td class="text-end text-success">− $0.00 <span class="text-muted" style="font-size:11px">(claim pending)</span></td></tr>
            <tr><td class="pe-4 text-muted">Tax</td><td class="text-end">$0.00</td></tr>
            <tr style="border-top:1px solid var(--line)"><td class="pe-4 pt-2 fw-semibold">Total</td><td class="text-end pt-2 fw-semibold">$890.00</td></tr>
            <tr><td class="pe-4 text-muted">Paid</td><td class="text-end">− $470.00</td></tr>
            <tr><td class="pe-4 fw-bold" style="font-size:15px">Balance due</td><td class="text-end fw-bold" style="font-size:15px">$420.00</td></tr>
          </table>
        </div>
        <div class="section-title mt-3">Notes</div>
        <p class="text-muted small mb-0">Session 2 booked for 14 August. Palliative fee waived as goodwill after the emergency visit.
        Payment plan agreed: $420 due on completion.</p>
      </div>
    """) + """
  </div>

  <div class="col-xl-4">
    """ + card("Payments", """
      <div class="tl">
        <div class="tl-item"><span class="dot"></span><div class="tl-t">$470.00 — card (terminal)</div>
          <div class="tl-m">29 Jul 2026 · Priya Nair · ref TX-99412</div></div>
        <div class="tl-item"><span class="dot" style="border-color:#cbd5e1"></span><div class="tl-t">$420.00 — expected</div>
          <div class="tl-m">Due on completion of session 2</div></div>
      </div>
      <a class="btn btn-brand w-100 mt-2" href="billing-payments.html"><i class="bi bi-credit-card me-1"></i>Record a payment</a>
      <button class="btn btn-soft w-100 mt-2" data-roles="Admin"><i class="bi bi-arrow-counterclockwise me-1"></i>Issue refund</button>
    """) + """
    <div class="mt-3">""" + card("Insurance claim", """
      <div class="d-flex justify-content-between align-items-center mb-2">
        <span class="text-muted small">Claim CLM-8841</span>""" + pill("Submitted", "blue") + """
      </div>
      <dl class="dl-x">
        <dt>Insurer</dt><dd>Delta Dental</dd>
        <dt>Submitted</dt><dd>30 Jul 2026 · electronic</dd>
        <dt>Estimated benefit</dt><dd>$623.00</dd>
        <dt>Response due</dt><dd>within 14 working days</dd>
      </dl>
      <a class="btn btn-soft btn-sm w-100" href="billing-claims.html">Open claim</a>
    """) + """</div>
    <div class="mt-3">""" + card("Activity", """
      <div class="tl">
        <div class="tl-item"><span class="dot"></span><div class="tl-t">Reminder emailed</div><div class="tl-m">12 Aug 2026 · opened</div></div>
        <div class="tl-item"><span class="dot"></span><div class="tl-t">Claim submitted</div><div class="tl-m">30 Jul 2026 · Priya Nair</div></div>
        <div class="tl-item"><span class="dot"></span><div class="tl-t">Invoice issued</div><div class="tl-m">29 Jul 2026 · Priya Nair</div></div>
      </div>
    """) + """</div>
  </div>
</div>
"""}

# =========================================================================
# billing-invoice-create.html
# =========================================================================
PAGES["billing-invoice-create.html"] = {
    "title": "New invoice",
    "razor": "Views/Billing/CreateInvoice.cshtml",
    "body": head([("Home", "dashboard-admin.html"), ("Billing", "billing-invoices.html"), ("New invoice", "")],
                 "New invoice",
                 "Pull completed procedures straight from the treatment record, or add lines manually",
                 '<a class="btn btn-soft" href="billing-invoices.html">Cancel</a>'
                 '<button class="btn btn-soft">Save as draft</button>'
                 '<button class="btn btn-brand"><i class="bi bi-check2 me-1"></i>Issue invoice</button>') + """
<div class="row g-3">
  <div class="col-xl-8">
    """ + card("Invoice header", """
      <div class="row">
        <div class="col-md-6 mb-3">
          <label class="form-label req">Patient</label>
          <div class="input-group">
            <span class="input-group-text bg-white border-end-0"><i class="bi bi-search text-muted"></i></span>
            <input class="form-control border-start-0" value="Kelly, Marcus — PT-10428">
          </div>
        </div>
        """ + field("Invoice number", txt("", "INV-2482"), "col-md-3", hint="Auto-numbered") + """
        """ + field("Issue date", txt("", "2026-08-14", "date"), "col-md-3") + """
        """ + field("Treating dentist", sel(["Dr. Luca Bianchi", "Dr. Amara Okafor", "Dr. Sofia Reyes"]), "col-md-4") + """
        """ + field("Payment terms", sel(["Due on receipt", "Net 14", "Net 30"]), "col-md-4") + """
        """ + field("Insurer", sel(["Delta Dental", "Cigna", "MetLife", "Self-pay"]), "col-md-4") + """
      </div>
    """) + """

    <div class="mt-3">""" + card_flush("Line items",
        table(["Code", "Description", ("Qty", ' class="text-center"'), ("Unit fee", ' class="text-end"'),
               ("Discount", ' class="text-end"'), ("Amount", ' class="text-end"'), ("", ' class="text-end"')],
              ["".join([
                  '<tr><td class="t-main">D2392</td><td>Composite restoration, two surfaces<div class="t-sub">Tooth 26 · completed today</div></td>'
                  '<td class="text-center">1</td><td class="text-end">$240.00</td><td class="text-end">—</td>'
                  '<td class="text-end fw-semibold">$240.00</td>'
                  '<td class="text-end"><button class="btn btn-ghost btn-sm"><i class="bi bi-x-lg"></i></button></td></tr>',
                  '<tr><td class="t-main">D0220</td><td>Periapical radiograph<div class="t-sub">Tooth 26</div></td>'
                  '<td class="text-center">1</td><td class="text-end">$45.00</td><td class="text-end">—</td>'
                  '<td class="text-end fw-semibold">$45.00</td>'
                  '<td class="text-end"><button class="btn btn-ghost btn-sm"><i class="bi bi-x-lg"></i></button></td></tr>',
                  '<tr><td colspan="7" class="p-3">'
                  '<div class="row g-2 align-items-end">'
                  '<div class="col-md-3"><label class="form-label">Procedure</label>'
                  '<select class="form-select form-select-sm"><option>Search the catalogue…</option>'
                  '<option>D1110 — Prophylaxis, adult</option><option>D2740 — Crown</option></select></div>'
                  '<div class="col-md-2"><label class="form-label">Tooth</label><input class="form-control form-control-sm" placeholder="#"></div>'
                  '<div class="col-md-2"><label class="form-label">Qty</label><input class="form-control form-control-sm" value="1"></div>'
                  '<div class="col-md-2"><label class="form-label">Fee</label><input class="form-control form-control-sm" placeholder="0.00"></div>'
                  '<div class="col-md-2"><label class="form-label">Discount</label><input class="form-control form-control-sm" placeholder="0.00"></div>'
                  '<div class="col-md-1"><button class="btn btn-soft btn-sm w-100"><i class="bi bi-plus-lg"></i></button></div>'
                  '</div></td></tr>',
              ])]),
        actions='<button class="btn btn-soft btn-sm"><i class="bi bi-clipboard2-pulse me-1"></i>Import from treatment plan</button>',
        foot="""<div class="d-flex justify-content-end">
          <table style="font-size:13.5px;min-width:280px">
            <tr><td class="pe-4 text-muted">Subtotal</td><td class="text-end">$285.00</td></tr>
            <tr><td class="pe-4 text-muted">Insurance estimate (70%)</td><td class="text-end text-success">− $199.50</td></tr>
            <tr><td class="pe-4 text-muted">Tax (0%)</td><td class="text-end">$0.00</td></tr>
            <tr style="border-top:1px solid var(--line)"><td class="pe-4 pt-2 fw-bold" style="font-size:15px">Patient pays</td>
            <td class="text-end pt-2 fw-bold" style="font-size:15px">$85.50</td></tr>
          </table></div>""") + """</div>
  </div>

  <div class="col-xl-4">
    """ + card("Take payment now", """
      <p class="text-muted small">Optional — record a payment as the invoice is issued.</p>
      <div class="row">
        """ + field("Amount", txt("", "$85.50"), "col-12") + """
        """ + field("Method", sel(["Card — terminal", "Cash", "Bank transfer", "Payment plan", "None"]), "col-12") + """
      </div>
      <div class="form-check"><input class="form-check-input" type="checkbox" checked id="pr"><label class="form-check-label small" for="pr">Print receipt</label></div>
      <div class="form-check mb-3"><input class="form-check-input" type="checkbox" checked id="pe"><label class="form-check-label small" for="pe">Email invoice to patient</label></div>
      <button class="btn btn-brand w-100"><i class="bi bi-check2 me-1"></i>Issue &amp; take payment</button>
    """) + """
    <div class="mt-3">""" + card("Insurance", """
      <dl class="dl-x">
        <dt>Policy</dt><dd>Delta Dental · #DD-2210847</dd>
        <dt>Annual maximum</dt><dd>$1,500.00</dd>
        <dt>Used this year</dt><dd>$680.00</dd>
        <dt>Remaining</dt><dd class="text-success">$820.00</dd>
      </dl>
      <div class="stat-bar mb-2"><span style="width:45%"></span></div>
      <div class="form-check"><input class="form-check-input" type="checkbox" checked id="cl"><label class="form-check-label small" for="cl">Submit claim automatically when issued</label></div>
    """) + """</div>
  </div>
</div>
"""}

# =========================================================================
# billing-payments.html
# =========================================================================
_pay_rows = []
for ref, when, ini, name, pid, inv, method, amount, status, tone in [
    ("TX-99518", "Today 09:12", "MK", "Marcus Kelly", "PT-10428", "INV-2478", "Card — terminal", "$310.00", "Settled", "green"),
    ("TX-99511", "Today 08:40", "TA", "Tobias Ackerman", "PT-10502", "INV-2432", "Bank transfer", "$1,240.00", "Settled", "green"),
    ("TX-99504", "13 Aug 17:20", "EW", "Elena Whitfield", "PT-10391", "INV-2477", "Cash", "$65.00", "Settled", "green"),
    ("TX-99498", "13 Aug 11:05", "SN", "Sara Nowak", "PT-10188", "INV-2479", "Card — online", "$120.00", "Pending", "amber"),
    ("TX-99412", "29 Jul 14:33", "RJ", "Rania Jabari", "PT-10233", "INV-2481", "Card — terminal", "$470.00", "Settled", "green"),
    ("TX-99388", "24 Jul 10:02", "GM", "Grace Mbeki", "PT-10061", "INV-2440", "Card — terminal", "− $85.00", "Refunded", "red"),
]:
    _pay_rows.append(
        '<tr><td class="fw-semibold">%s<div class="t-sub">%s</div></td><td>%s</td>'
        '<td><a class="text-decoration-none" href="billing-invoice-details.html">%s</a></td>'
        '<td>%s</td><td class="text-end fw-semibold">%s</td><td>%s</td>'
        '<td class="text-end"><button class="btn btn-soft btn-sm"><i class="bi bi-printer"></i></button></td></tr>'
        % (ref, when, person(ini, name, pid), inv, method, amount, pill(status, tone)))

PAGES["billing-payments.html"] = {
    "title": "Payments",
    "razor": "Views/Billing/Payments.cshtml",
    "body": head([("Home", "dashboard-admin.html"), ("Billing", "billing-invoices.html"), ("Payments", "")],
                 "Payments",
                 "Today: $1,735.00 collected across 6 transactions",
                 '<button class="btn btn-soft"><i class="bi bi-cash-coin me-1"></i>Cash-up / end of day</button>'
                 '<button class="btn btn-brand" data-bs-toggle="modal" data-bs-target="#payModal"><i class="bi bi-plus-lg me-1"></i>Take payment</button>') + """
<div class="row g-3 mb-3">""" + (
        kpi("bi-credit-card-2-front", "teal", "$1,240", "Card") +
        kpi("bi-cash", "green", "$65", "Cash") +
        kpi("bi-bank", "blue", "$430", "Bank transfer") +
        kpi("bi-arrow-counterclockwise", "red", "$85", "Refunds")) + """
</div>

""" + card_flush("Payment ledger", table(
        ["Reference", "Patient", "Invoice", "Method", ("Amount", ' class="text-end"'), "Status", ("", ' class="text-end"')],
        ["".join(_pay_rows)]),
        actions='<div class="d-flex gap-2 flex-wrap">'
                '<div style="min-width:150px">' + sel(["Today", "Yesterday", "This week", "This month"]) + '</div>'
                '<div style="min-width:150px">' + sel(["All methods", "Card", "Cash", "Bank transfer", "Insurance"]) + '</div>'
                '</div>') + """

<!-- Take payment — Views/Billing/_TakePaymentModal.cshtml -->
<div class="modal fade" id="payModal" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered modal-lg">
    <div class="modal-content">
      <div class="modal-header border-0 pb-0"><h5 class="modal-title">Take a payment</h5>
        <button class="btn-close" data-bs-dismiss="modal"></button></div>
      <div class="modal-body">
        <div class="row">
          <div class="col-md-6 mb-3">
            <label class="form-label req">Patient</label>
            <div class="input-group"><span class="input-group-text bg-white border-end-0"><i class="bi bi-search text-muted"></i></span>
            <input class="form-control border-start-0" value="Jabari, Rania — PT-10233"></div>
          </div>
          """ + field("Invoice", sel(["INV-2481 — balance $420.00", "INV-2455 — balance $0.00", "Payment on account"]), "col-md-6") + """
          """ + field("Amount", txt("", "$420.00"), "col-md-4", req=True) + """
          """ + field("Method", sel(["Card — terminal", "Card — keyed", "Cash", "Bank transfer", "Cheque", "Insurance"]), "col-md-4") + """
          """ + field("Date received", txt("", "2026-08-14", "date"), "col-md-4") + """
          """ + field("Reference / note", txt("Terminal reference, cheque number…"), "col-12") + """
        </div>
        <div class="d-flex gap-4 flex-wrap">
          <div class="form-check"><input class="form-check-input" type="checkbox" checked id="m1"><label class="form-check-label small" for="m1">Print receipt</label></div>
          <div class="form-check"><input class="form-check-input" type="checkbox" checked id="m2"><label class="form-check-label small" for="m2">Email receipt</label></div>
          <div class="form-check"><input class="form-check-input" type="checkbox" id="m3"><label class="form-check-label small" for="m3">Mark invoice as settled in full</label></div>
        </div>
      </div>
      <div class="modal-footer border-0">
        <button class="btn btn-soft" data-bs-dismiss="modal">Cancel</button>
        <button class="btn btn-brand"><i class="bi bi-check2 me-1"></i>Record payment</button>
      </div>
    </div>
  </div>
</div>
"""}

# =========================================================================
# billing-claims.html
# =========================================================================
_claim_rows = []
for cid, ini, name, pid, insurer, submitted, amount, benefit, status, tone in [
    ("CLM-8841", "RJ", "Rania Jabari", "PT-10233", "Delta Dental", "30 Jul 2026", "$890.00", "$623.00", "Submitted", "blue"),
    ("CLM-8839", "AC", "Aisha Chowdhury", "PT-10455", "Cigna", "28 Jul 2026", "$490.00", "$245.00", "Rejected", "red"),
    ("CLM-8836", "PL", "Peter Lindqvist", "PT-10099", "MetLife", "22 Jul 2026", "$740.00", "$370.00", "Rejected", "red"),
    ("CLM-8830", "HN", "Hugo Nakamura", "PT-10310", "Delta Dental", "18 Jul 2026", "$220.00", "$154.00", "Paid", "green"),
    ("CLM-8828", "GM", "Grace Mbeki", "PT-10061", "Cigna", "15 Jul 2026", "$185.00", "$92.50", "Rejected", "red"),
    ("CLM-8821", "TA", "Tobias Ackerman", "PT-10502", "MetLife", "12 Jul 2026", "$1,240.00", "$620.00", "Paid", "green"),
]:
    _claim_rows.append(
        '<tr><td class="fw-semibold">%s</td><td>%s</td><td>%s</td><td>%s</td>'
        '<td class="text-end">%s</td><td class="text-end text-success">%s</td><td>%s</td>'
        '<td class="text-end"><a class="btn btn-soft btn-sm" href="billing-invoice-details.html">Open</a></td></tr>'
        % (cid, person(ini, name, pid), insurer, submitted, amount, benefit, pill(status, tone)))

PAGES["billing-claims.html"] = {
    "title": "Insurance claims",
    "razor": "Views/Billing/Claims.cshtml",
    "body": head([("Home", "dashboard-admin.html"), ("Billing", "billing-invoices.html"), ("Insurance claims", "")],
                 "Insurance claims",
                 "18 open claims · 3 rejected and awaiting resubmission",
                 '<button class="btn btn-soft"><i class="bi bi-arrow-repeat me-1"></i>Sync statuses</button>'
                 '<button class="btn btn-brand"><i class="bi bi-plus-lg me-1"></i>New claim</button>') + """
<div class="row g-3 mb-3">""" + (
        kpi("bi-send", "blue", "18", "Submitted / open") +
        kpi("bi-check2-circle", "green", "$8,410", "Paid this month") +
        kpi("bi-x-octagon", "red", "3", "Rejected", "$2,140 at risk", "text-danger") +
        kpi("bi-clock", "amber", "9 days", "Average settlement")) + """
</div>

<div class="row g-3">
  <div class="col-xl-8">
    """ + card_flush("Claims", table(
        ["Claim", "Patient", "Insurer", "Submitted", ("Claimed", ' class="text-end"'),
         ("Benefit", ' class="text-end"'), "Status", ("", ' class="text-end"')],
        ["".join(_claim_rows)]),
        actions='<div style="min-width:170px">' + sel(["All statuses", "Draft", "Submitted", "Paid", "Rejected"]) + '</div>') + """
  </div>
  <div class="col-xl-4">
    """ + card("Rejections to action", """
      <div class="d-grid gap-2">
        <div class="p-3 rounded" style="border:1px solid var(--line)">
          <div class="d-flex justify-content-between align-items-start">
            <div class="fw-semibold" style="font-size:13.5px">CLM-8839 · Cigna</div>""" + pill("9 days", "red") + """
          </div>
          <div class="text-muted small mt-1">Reason: procedure code D2740 requires a pre-authorisation reference.</div>
          <button class="btn btn-soft btn-sm mt-2 w-100">Fix &amp; resubmit</button>
        </div>
        <div class="p-3 rounded" style="border:1px solid var(--line)">
          <div class="d-flex justify-content-between align-items-start">
            <div class="fw-semibold" style="font-size:13.5px">CLM-8836 · MetLife</div>""" + pill("6 days", "amber") + """
          </div>
          <div class="text-muted small mt-1">Reason: patient policy number does not match insurer records.</div>
          <button class="btn btn-soft btn-sm mt-2 w-100">Fix &amp; resubmit</button>
        </div>
        <div class="p-3 rounded" style="border:1px solid var(--line)">
          <div class="d-flex justify-content-between align-items-start">
            <div class="fw-semibold" style="font-size:13.5px">CLM-8828 · Cigna</div>""" + pill("4 days", "amber") + """
          </div>
          <div class="text-muted small mt-1">Reason: annual maximum already reached for the benefit year.</div>
          <button class="btn btn-soft btn-sm mt-2 w-100">Bill the patient instead</button>
        </div>
      </div>
    """) + """
  </div>
</div>
"""}
