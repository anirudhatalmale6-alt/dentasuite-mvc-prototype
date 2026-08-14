#!/usr/bin/env python3
"""Screenshot every prototype page at desktop + a couple at mobile width."""
import http.server, socketserver, threading, os, sys, functools, socket

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prototype")
SHOTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")
os.makedirs(SHOTS, exist_ok=True)

# bind port 0 so we never collide with another user's server on this box
sock = socket.socket()
sock.bind(("127.0.0.1", 0))
PORT = sock.getsockname()[1]
sock.close()

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
BASE = "http://127.0.0.1:%d/" % PORT
print("serving", ROOT, "on", BASE)

DESKTOP = [
    ("index.html", "Admin", "00-screen-map"),
    ("account-login.html", "Admin", "01-login"),
    ("dashboard-admin.html", "Admin", "02-dashboard-admin"),
    ("dashboard-dentist.html", "Dentist", "03-dashboard-dentist"),
    ("dashboard-reception.html", "Receptionist", "04-front-desk"),
    ("patients-index.html", "Admin", "05-patients"),
    ("patients-create.html", "Receptionist", "06-register-patient"),
    ("patients-details.html", "Admin", "07-patient-record"),
    ("appointments-calendar.html", "Receptionist", "08-calendar"),
    ("appointments-index.html", "Admin", "09-appointment-list"),
    ("appointments-create.html", "Receptionist", "10-book-appointment"),
    ("appointments-reschedule.html", "Receptionist", "11-reschedule"),
    ("appointments-waitlist.html", "Receptionist", "12-waiting-list"),
    ("treatments-chart.html", "Dentist", "13-dental-chart"),
    ("treatments-plan.html", "Dentist", "14-treatment-plan"),
    ("treatments-procedures.html", "Admin", "15-procedure-catalogue"),
    ("treatments-prescriptions.html", "Dentist", "16-prescriptions"),
    ("billing-invoices.html", "Admin", "17-invoices"),
    ("billing-invoice-details.html", "Receptionist", "18-invoice"),
    ("billing-invoice-create.html", "Receptionist", "19-new-invoice"),
    ("billing-payments.html", "Receptionist", "20-payments"),
    ("billing-claims.html", "Admin", "21-insurance-claims"),
    ("reports-index.html", "Admin", "22-reports"),
    ("admin-users.html", "Admin", "23-users-roles"),
    ("admin-clinic.html", "Admin", "24-clinic-chairs"),
    ("admin-settings.html", "Admin", "25-settings"),
    ("error-access-denied.html", "Dentist", "26-access-denied"),
]

MOBILE = [
    ("dashboard-reception.html", "Receptionist", "m1-front-desk"),
    ("patients-index.html", "Admin", "m2-patients"),
    ("treatments-chart.html", "Dentist", "m3-dental-chart"),
    ("billing-invoice-details.html", "Receptionist", "m4-invoice"),
]

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()

    ctx = b.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    pg = ctx.new_page()
    for f, role, name in DESKTOP:
        pg.goto(BASE + f + "?role=" + role, wait_until="networkidle")
        pg.wait_for_timeout(450)
        pg.screenshot(path=os.path.join(SHOTS, name + ".png"))
        print("  ", name)
    ctx.close()

    ctx = b.new_context(viewport={"width": 390, "height": 760}, device_scale_factor=2,
                        is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    for f, role, name in MOBILE:
        pg.goto(BASE + f + "?role=" + role, wait_until="networkidle")
        pg.wait_for_timeout(450)
        pg.screenshot(path=os.path.join(SHOTS, name + ".png"))
        print("  ", name)
    ctx.close()
    b.close()

httpd.shutdown()
print("done ->", SHOTS)
