# DentaSuite — dental clinic management, interface prototype

Live prototype: **https://anirudhatalmale6-alt.github.io/dentasuite-mvc-prototype/**

This is the **visual prototype step** for the ASP.NET MVC (C#) interface layer — 27 clickable
screens covering patient registration, scheduling and rescheduling, clinical charting, invoicing
and payments, adapting to three roles (Admin, Dentist, Receptionist).

It is deliberately static HTML so it can be reviewed in a browser with nothing to install.
Every screen here maps 1:1 to a Razor view in the MVC project that follows once the flow is approved.

---

## How to review it

1. Open the link above — you land on the **screen map** (full controller → action → view hierarchy).
2. Pick a role, or start at the sign-in screen.
3. Switch roles at any time from the avatar menu, top right. The sidebar, the dashboard and the
   in-page buttons all change — that's the role adaptation, not a mock-up of it.
4. Things that genuinely work: role switching, the odontogram (click teeth / pick a condition brush),
   tabs, modals, dropdowns, the responsive collapse. Everything else is intentionally inert —
   this layer has no data access and no domain logic.

---

## Screen → Razor view map

| Prototype file | MVC view | Controller action |
|---|---|---|
| `account-login.html` | `Views/Account/Login.cshtml` | `AccountController.Login()` |
| `error-access-denied.html` | `Views/Account/AccessDenied.cshtml` | `AccountController.AccessDenied()` |
| `dashboard-admin.html` | `Views/Dashboard/Admin.cshtml` | `DashboardController.Admin()` |
| `dashboard-dentist.html` | `Views/Dashboard/Dentist.cshtml` | `DashboardController.Dentist()` |
| `dashboard-reception.html` | `Views/Dashboard/Reception.cshtml` | `DashboardController.Reception()` |
| `patients-index.html` | `Views/Patients/Index.cshtml` | `PatientsController.Index()` |
| `patients-create.html` | `Views/Patients/Create.cshtml` | `PatientsController.Create()` |
| `patients-details.html` | `Views/Patients/Details.cshtml` | `PatientsController.Details(id)` |
| `appointments-calendar.html` | `Views/Appointments/Calendar.cshtml` | `AppointmentsController.Calendar()` |
| `appointments-index.html` | `Views/Appointments/Index.cshtml` | `AppointmentsController.Index()` |
| `appointments-create.html` | `Views/Appointments/Create.cshtml` | `AppointmentsController.Create()` |
| `appointments-reschedule.html` | `Views/Appointments/Reschedule.cshtml` | `AppointmentsController.Reschedule(id)` |
| `appointments-waitlist.html` | `Views/Appointments/WaitingList.cshtml` | `AppointmentsController.WaitingList()` |
| `treatments-chart.html` | `Views/Treatments/Chart.cshtml` | `TreatmentsController.Chart(patientId)` |
| `treatments-plan.html` | `Views/Treatments/Plan.cshtml` | `TreatmentsController.Plan(id)` |
| `treatments-procedures.html` | `Views/Treatments/Procedures.cshtml` | `TreatmentsController.Procedures()` |
| `treatments-prescriptions.html` | `Views/Treatments/Prescriptions.cshtml` | `TreatmentsController.Prescriptions(patientId)` |
| `billing-invoices.html` | `Views/Billing/Invoices.cshtml` | `BillingController.Invoices()` |
| `billing-invoice-details.html` | `Views/Billing/InvoiceDetails.cshtml` | `BillingController.InvoiceDetails(id)` |
| `billing-invoice-create.html` | `Views/Billing/CreateInvoice.cshtml` | `BillingController.CreateInvoice()` |
| `billing-payments.html` | `Views/Billing/Payments.cshtml` | `BillingController.Payments()` |
| `billing-claims.html` | `Views/Billing/Claims.cshtml` | `BillingController.Claims()` |
| `reports-index.html` | `Views/Reports/Index.cshtml` | `ReportsController.Index()` |
| `admin-users.html` | `Views/Admin/Users.cshtml` | `AdminController.Users()` |
| `admin-clinic.html` | `Views/Admin/Clinic.cshtml` | `AdminController.Clinic()` |
| `admin-settings.html` | `Views/Admin/Settings.cshtml` | `AdminController.Settings()` |

`index.html` is the prototype cover / screen map only — it is not part of the MVC app.

The shared shell (sidebar, top bar, notifications, user menu) becomes
`Views/Shared/_Layout.cshtml`; the page header, person cell, status pill, KPI tile and the two
modals become partials under `Views/Shared/`.

---

## Role model

| Capability | Admin | Dentist | Receptionist |
|---|:--:|:--:|:--:|
| View patient register | ● | ● | ● |
| Register / edit patients | ● | | ● |
| Archive patients | ● | | |
| Book & reschedule | ● | ● | ● |
| Dental charting | ● | ● | |
| Sign clinical notes | | ● | |
| Prescribe | | ● | |
| Create invoices | ● | | ● |
| Record payments / refunds | ● | | ● |
| Edit fee schedule | ● | | |
| Practice reports | ● | | |
| Manage users & settings | ● | | |

In the prototype this is driven by a `data-roles="Admin,Receptionist"` attribute plus a few lines of
JavaScript, purely so the demo can switch roles in the browser. In the MVC project the same matrix
becomes `[Authorize(Roles = "…")]` on the controller action **and** `@if (User.IsInRole("…"))` in the
view, so a hidden control can't be reached by typing the URL either.

---

## Styling

* Bootstrap 5.3 (CDN) — grid, utilities, dropdowns, tabs, modals, pagination.
* Bootstrap Icons 1.11.
* Inter (Google Fonts).
* One project stylesheet, `assets/css/site.css`, built entirely on CSS custom properties.

Re-skinning is a `:root` edit — brand ramp, sidebar colour, page background, border colour, corner
radius and shadows are all variables. No colour is hard-coded in the markup except the status tints,
which are themselves variables.

Responsive: verified at 360, 390, 768, 1024 and 1440 px. Sidebar collapses to an off-canvas drawer
below 992 px, wide tables scroll inside their own container, and the page body never scrolls
horizontally. Light palette is pinned so mobile auto-dark-mode doesn't repaint the clinical screens.

---

## What's next (on approval)

The full ASP.NET MVC project folder: `Controllers/` with stubbed actions returning `View()`,
`Views/` with the Razor equivalents of every screen above, `Views/Shared/_Layout.cshtml`,
view-model placeholders, `wwwroot/` assets, and a README covering the view/controller structure
and third-party libraries. No data access, no domain logic — your models and services drop in
without touching the UI.

---

## Repo layout

```
/                     the prototype itself (GitHub Pages root)
  index.html          screen map / cover
  *.html              27 screens
  assets/css/site.css theme
  assets/js/site.js   role switching, odontogram, mobile nav
/tools                the small Python generator used to build the static pages
/screenshots          desktop + mobile captures of every screen
```

All patient names, figures and clinical data are fictional sample content.
