# Release Template — `/bq-release template` (alpha.24)

Turn a finished project into a reusable starter/template/product. Shape: **argument under `/bq-release`** (launch-kit family, approved alpha.22). Skills: release-gate + security-reviewer + database-architect (tenancy).

## Outputs — `.bequite/templates/`

TEMPLATE_BRIEF · TEMPLATE_SCOPE · CUSTOMIZATION_GUIDE · DEMO_DATA_PLAN · SECURITY_AND_SECRET_SCAN · TENANCY_AND_DATA_ISOLATION · INSTALL_GUIDE · LICENSING_NOTES · SUPPORT_NOTES · RELEASE_CHECKLIST.

## Use cases

One system built once, reused/sold many times: ecommerce theme · pharmacy/restaurant/clinic management template · course-platform template · dashboard/SaaS starter · agency boilerplate · Gumroad digital product.

## Best practices + risks (mandatory)

Remove secrets (scan) · env examples only · **seed/demo data only — never real client data** · avoid hardcoded branding · update path · licensing · support boundaries · customization guide (what the buyer can/can't safely change) · screenshots/demo.

## System-design risk (the headline)

**Multi-tenant data isolation is a first-class requirement** (SYSTEM_DESIGN_REASONING_STANDARD): two pharmacies on the same system must NOT access each other's data; restaurant A's data must not leak to restaurant B; the multi-tenant-vs-single-tenant decision must be **explicit** in TENANCY_AND_DATA_ISOLATION, with the isolation mechanism named and tested. Demo data must contain zero real client data. **Built alpha.24 — NOT live-tested.**
