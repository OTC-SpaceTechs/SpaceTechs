# Space Techs Website — Build Guide

A phased, check-as-you-go plan for building out the Django project. Each phase builds on the last — don't skip ahead to `projects` before `core`/`membership` auth is solid, since almost everything else depends on the User model.

---

## Phase 0 — Foundation (you're here ✅ / 🔲)

- [x] Create Django project
- [x] Start `core` app
- [x] Install & configure Django REST Framework (`pip install djangorestframework`, add to `INSTALLED_APPS`)
- [x] Decide on database now (SQLite is fine for dev, but if you'll want full-text search later, set up **Postgres** early — switching later is a pain) — went with Postgres (local via Homebrew, `spacetechs` db)
- [x] Set up `.env` handling (`django-environ` or `python-decouple`) for `SECRET_KEY`, DB creds, etc. — using `django-environ`
- [x] Initialize git repo + `.gitignore` if not already done

**Why first:** everything downstream (auth, permissions, API) assumes these choices are locked in.

---

## Phase 1 — `core`: Custom User Model

⚠️ **Do this before your first migration.** Swapping to a custom User model after you've already migrated is painful.

- [x] In `core/models.py`, create `class User(AbstractUser): pass` (add fields later as needed)
- [x] Set `AUTH_USER_MODEL = "core.User"` in `settings.py`
- [x] Run `makemigrations` / `migrate` — confirm it works before building anything else
- [x] Register `User` in `admin.py` so you can manage accounts from the Django admin immediately
- [x] Set up Django Groups for officer roles (Chair, Vice-Chair, Secretary, Treasurer, Directors of Projects, Director of Research, Director of Outreach, SEDS Rep, Member-at-Large)
  - Use **Groups**, not a hardcoded `role` field — your constitution explicitly allows officer positions to be added/removed over time
- [x] Decide now: will regular members log in at all, or is auth just for officers? (Affects Phase 2 scope)
*Officers only*

---

## Phase 2 — `membership` app

- [x] `Member` model — likely a `OneToOneField` to `User`, plus:
  - `join_date`, `active_status`, `major` (optional), `bio` (optional)
- [x] `OfficerHistory` model — tracks who held what role and when:
  - `member` (FK), `role` (FK to Group or choice field), `start_date`, `end_date` (nullable)
  - This is what makes leadership transitions traceable later — directly supports the constitution's continuity language
- [x] Django admin registration for both
- [x] Basic member list view (even just admin-only at first)

**Stop and test:** create a couple of fake members/officers in the admin panel and confirm relationships work before moving on.

---

## Phase 3 — `events` app

- [x] `Event` model:
  - `title`, `date`, `event_type` (meeting / social / launch / fundraiser / workshop), `description`, `location` (optional)
- [x] Load in your Fall Semester Plans as seed data (management command or admin entry) — good way to test the model with real data
- [x] Public list/detail views (no auth needed — this is your public calendar)
- [x] DRF serializer + viewset for `Event` (your first real API endpoint — good warm-up before tackling `projects`)

**Why now:** simplest app, no complex relationships, good place to practice the model → admin → view → API pattern you'll repeat everywhere else.

---

## Phase 4 — `projects` app (the big one)

Build this in sub-steps — don't try to do it all in one migration.

- [ ] **4a.** `Project` model: `name`, `description`, `status` (active/archived), `start_date`
- [ ] **4b.** `Document` model: FK to `Project`, `title`, `file` (FileField) or `content` (TextField), `doc_type` (design / research / procedure / results)
- [ ] **4c.** `ComponentInventory` model: FK to `Project`, `name`, `quantity`, `cost`, `supplier`, `notes`
- [ ] **4d.** `LessonLearned` model — this is your weather-balloon-notes structure, formalized:
  - FK to `Project`, `question`, `answer`, `category` (e.g. "sealing," "payload," "FAA/comms"), optional `image` field
  - This turns scattered PDFs/notes into something searchable
- [ ] Admin registration for all four, with inlines (e.g. show `LessonLearned` entries inline on the `Project` admin page)
- [ ] DRF serializers/viewsets once models are stable
- [ ] Decide: public read access to project docs, or member-only? (Probably member-only for raw docs, public for a project showcase page)

---

## Phase 5 — `inventory` app *(optional — fold into `projects` if you want to stay lean)*

- [ ] `Equipment` model: `name`, `condition`, `custodian` (FK to Member, nullable), `checked_out_to_project` (FK, nullable), `acquisition_date`
- [ ] Only build this as a separate app if equipment gets shared across multiple projects — otherwise `ComponentInventory` from Phase 4 covers it

---

## Phase 6 — `finance` app *(officer-only)*

- [ ] `PurchaseRequest` model: `requested_by` (FK), `amount`, `purpose`, `status` (pending/approved/denied), `project` (FK, optional), `approved_by` (FK, nullable)
- [ ] Restrict all views to Treasurer/Chair/Vice-Chair groups from Phase 1
- [ ] This can stay admin-only (no custom frontend needed) for a long time — low priority to build custom views here

---

## Phase 7 — `outreach` app

- [ ] `Speaker` / `Event` tie-in (could reuse `events` with a `guest_speaker` field instead of a new model — evaluate before building)
- [ ] `Opportunity` model: `name`, `type` (conference/grant/sponsorship/scholarship), `deadline`, `status`, `notes`
- [ ] Lowest priority — build only once core/membership/projects/events are solid

---

## Phase 8 — Permissions & Public/Private Split

- [ ] Map out URL structure now that models exist:
  - `/` — public site (events, project showcase, about)
  - `/portal/` or `/members/` — auth-required (full project docs, inventory, finance)
- [ ] Use DRF permission classes (`IsAuthenticated`, custom `IsOfficer`) rather than checking groups manually in every view
- [ ] Test as a "regular member" account AND an "officer" account to confirm the split actually works

---

## Phase 9 — Polish

- [ ] Full-text search on `LessonLearned` / `Document` (Postgres `SearchVector` if you set up Postgres in Phase 0)
- [ ] Seed data / fixtures for demo purposes
- [ ] API docs (drf-spectacular or similar) if others will consume the API
- [ ] Deployment prep (env vars, static files, `ALLOWED_HOSTS`, etc.)

---

## Quick Reference: Build Order

```
core (User model)
   ↓
membership (Member, OfficerHistory)
   ↓
events (simplest — practice the pattern)
   ↓
projects (the core value of the site)
   ↓
inventory / finance / outreach (lower priority, build as needed)
   ↓
permissions & public/private split
   ↓
polish (search, docs, deploy)
```

**Rule of thumb:** if a model needs a FK to `User` or `Member`, it can't be built before Phase 1–2 are done. Everything else is fairly independent — build in whatever order matches what the club needs soonest.