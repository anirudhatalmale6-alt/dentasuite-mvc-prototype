"""Small HTML helpers shared by the page modules (mirrors the partial views
   that would live in /Views/Shared/ in the real MVC project)."""


def head(crumbs, heading, sub, actions=""):
    """_PageHeader.cshtml — breadcrumb + title + action buttons."""
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


def kpi(icon, tone, value, label, delta="", delta_tone="text-success", roles=None):
    r = ' data-roles="%s"' % roles if roles else ""
    d = '<div class="delta %s">%s</div>' % (delta_tone, delta) if delta else ""
    return """<div class="col-6 col-xl-3"%s>
  <div class="card-x h-100"><div class="kpi">
    <div class="ic ic-%s"><i class="bi %s"></i></div>
    <div><div class="val">%s</div><div class="lbl">%s</div>%s</div>
  </div></div>
</div>""" % (r, tone, icon, value, label, d)


def card(title, body, sub="", actions="", foot="", cls=""):
    h = ""
    if title:
        h = """<div class="card-x-head">
    <div><h2>%s</h2>%s</div>
    <div class="d-flex gap-2 align-items-center">%s</div>
  </div>""" % (title, ('<p class="sub">%s</p>' % sub) if sub else "", actions)
    f = '<div class="card-x-foot">%s</div>' % foot if foot else ""
    return '<div class="card-x %s">%s<div class="card-x-body">%s</div>%s</div>' % (cls, h, body, f)


def card_flush(title, body, sub="", actions="", foot="", cls=""):
    """Card whose body has no padding — for full-bleed tables."""
    h = ""
    if title:
        h = """<div class="card-x-head">
    <div><h2>%s</h2>%s</div>
    <div class="d-flex gap-2 align-items-center flex-wrap">%s</div>
  </div>""" % (title, ('<p class="sub">%s</p>' % sub) if sub else "", actions)
    f = '<div class="card-x-foot">%s</div>' % foot if foot else ""
    return '<div class="card-x %s">%s%s%s</div>' % (cls, h, body, f)


def table(headers, rows, cls=""):
    th = "".join("<th%s>%s</th>" % (h[1] if isinstance(h, tuple) else "", h[0] if isinstance(h, tuple) else h)
                 for h in headers)
    return """<div class="table-responsive">
  <table class="table table-x %s">
    <thead><tr>%s</tr></thead>
    <tbody>%s</tbody>
  </table>
</div>""" % (cls, th, "".join(rows))


def person(initials, name, sub, gray=False):
    return """<div class="d-flex align-items-center gap-2">
  <span class="avatar sm%s">%s</span>
  <span><span class="d-block t-main">%s</span><span class="d-block t-sub">%s</span></span>
</div>""" % (" gray" if gray else "", initials, name, sub)


def pill(text, tone, dot=True):
    d = '<i class="bi bi-circle-fill"></i>' if dot else ""
    return '<span class="pill pill-%s">%s%s</span>' % (tone, d, text)


def field(label, control, col="col-md-6", hint="", req=False):
    h = '<div class="form-text">%s</div>' % hint if hint else ""
    return '<div class="%s mb-3"><label class="form-label%s">%s</label>%s%s</div>' % (
        col, " req" if req else "", label, control, h)


def txt(placeholder="", value="", ph_type="text"):
    v = ' value="%s"' % value if value else ""
    return '<input type="%s" class="form-control" placeholder="%s"%s>' % (ph_type, placeholder, v)


def sel(options, selected=None):
    o = "".join('<option%s>%s</option>' % (" selected" if x == selected else "", x) for x in options)
    return '<select class="form-select">%s</select>' % o


def area(placeholder="", rows=3, value=""):
    return '<textarea class="form-control" rows="%d" placeholder="%s">%s</textarea>' % (rows, placeholder, value)
