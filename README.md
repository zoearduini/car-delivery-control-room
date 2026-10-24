# Car Delivery Control Room — Final Submission

An enterprise-grade, single-screen operations control room application designed for human dispatchers managing long-haul finished vehicle logistics across European transport corridors (Germany, Denmark, Sweden, Finland).

Built for the **Prompt Operations Hackathon** (24–25 October 2026), responding to the challenge set by **Bahn**.

---

## 1. Overview & Operational Philosophy

Bahn moves over 25,000 used cars annually across European borders with freelance drivers. In long-haul finished vehicle logistics, road transit conditions, ferry capacities, and dealership handovers change every hour.

The legacy approach to vehicle logistics was built around sprawling 7-lane Kanban boards where human dispatchers had to continuously inspect dozens of quiet, moving cars to spot occasional anomalies. 

### Core Design Tenet: "Agents do the legwork, people decide"
- **High-Signal Fleet Triage (The 40% Control Room Criterion):**
  - **77+ orders are proceeding quietly on schedule.** Rather than cluttering the operator's mental buffer, they remain in the quiet queue.
  - **Only the orders requiring human intervention are surfaced**, categorized cleanly into actionable groups:
    - `🚨 Road Breakdown` (e.g. `CD-420322` Bentley engine warning stop on the A7)
    - `⚓ Baltic Ferry Disruptions` (e.g. `CD-420299` Finnlines Travemünde sailing capacity exhaustion)
    - `📄 Documentation & Gate Release Holds` (missing commercial seller release notes, unsigned CMRs)
    - `⏱️ Schedule & Relay Delays` (e.g. `CD-420702` Kassel Logistics Hub multi-leg driver cancellation)
    - `🔍 Cosmetic Damage Claims` (post-delivery buyer condition dispute claims)
- **The Domain Law (Strict Human-in-the-Loop):**
  Under no circumstances is an autonomous agent permitted to send unreviewed external messages to paying clients or dealerships. The system automates 100% of the evidence gathering, checks telemetry, and simulates driver inquiries, but brings the operator a **concrete decision proposal with a 10-second countdown safety window and interactive modification capabilities**.
- **Evidence Provenance & Verification:**
  Every statement, sensor ping, and handover document is strictly attributed by source (`DRIVER`, `CUSTOMER`, `OPERATOR`, `SYSTEM`) and timestamp, paired 1-to-1 with actual physical evidence files (official consignment CMR PDFs, condition inspection photos, expense receipts).

---

## 2. Project Architecture & Zero-Dependency Execution

The solution is completely self-contained with **zero external database dependencies** (no SQLite, Postgres, Redis, Prisma, or Docker required). It runs immediately on standard Python 3.10+ and serves a responsive single-page application (SPA).

```text
submission_final/
├── .env.example                     # Optional OpenRouter API key template
├── .gitignore                       # Clean Git exclusion rules
├── requirements.txt                 # Lightweight dependencies (fastapi, uvicorn, pydantic)
├── run.py                           # Single-command launcher
├── README.md                        # Master documentation and AI process report
├── Saved log/                       # Audit export directory (.gitkeep)
├── control_room_app/
│   ├── __init__.py                  # Package descriptor
│   ├── backend.py                   # FastAPI REST backend & autonomous agent harness
│   └── static/
│       ├── index.html               # Single-page control room UI (Tailwind CSS, Alpine.js, Leaflet)
│       ├── bahn-logo.png            # Official Bahn corporate logo
│       ├── car-images/              # 24 vehicle preview renders (WebP)
│       └── car-logos/               # 16 automotive manufacturer brand badges (SVG)
├── dataset/
│   └── data/                        # 40+ operational dataset collections (.jsonl)
└── attachments/
    ├── manifest.json                # Attachment lookup index (58 records)
    ├── documents/                   # 30 official consignment notes (CMR) & release orders (PDF)
    ├── photos/                      # 16 proof-of-delivery & vehicle condition photos (JPG)
    └── receipts/                    # 12 driver expense & travel receipts (PDF)
```

---

## 3. Setup & Execution (Fresh Clone)

### Prerequisites
- Python 3.10, 3.11, 3.12, or 3.13
- Any modern web browser (Chrome, Edge, Firefox, Safari)

### Quickstart
```bash
# 1. Clone repository and navigate to root
cd submission_final

# 2. (Optional) Create and activate a clean virtual environment
python -m venv .venv

# On Linux / macOS:
source .venv/bin/activate
# On Windows PowerShell:
.venv\Scripts\Activate.ps1

# 3. Install lightweight dependencies
pip install -r requirements.txt

# 4. Launch the Control Room
python run.py
```

### Accessing the Application
Open your browser and navigate to:
```
http://127.0.0.1:8000
```

*(Optional OpenRouter API Key)*: The application works 100% offline with comprehensive built-in dispatch heuristics. If you wish to connect live frontier LLMs (GPT-4o, Claude 3.5 Sonnet, Llama 3.1 70B) for the AI Copilot, copy `.env.example` to `.env` and supply your `OPENROUTER_API_KEY`.

---

## 4. Benchmark Scenario Showcase

The control room incorporates specific handling for key challenge benchmark orders:

1. **`CD-420322` / `ord-00322` (Bentley Continental GT — Motorway Safety Stop):**
   - *Scenario:* Red engine warning lamp triggered on the A7 motorway; vehicle halted safely at Allertal West rest area.
   - *Agent Legwork:* Pings driver mobile app to confirm driver safety off the highway; checks warranty and roadside assistance limits.
   - *Operator Action:* One-click decision to dispatch roadside recovery service (€250.00) or flatbed towing (€420.00) with a 10-second confirmation window.
2. **`CD-420299` / `ord-00299` (BMW M4 Competition — Baltic Sea Ferry Disruption):**
   - *Scenario:* Transit congestion outside Hamburg causes driver to miss the scheduled 14:00 Finnlines sailing from Travemünde to Helsinki; the 22:00 departure is sold out.
   - *Agent Legwork:* Audits available quotes from `travel_options.jsonl`; identifies next verified vehicle deck space departing at 12:00 UTC (€387.00); validates driver mandatory rest hour compliance.
   - *Operator Action:* Staged rebooking authorization and draft arrival delay notice.
3. **`CD-420702` / `ord-00702` (Toyota Corolla — Kassel Relay Transfer Yard Crisis):**
   - *Scenario:* Multi-segment relay through a staffed transfer hub. Leg 1 (Origin → Kassel Logistics Hub) completed safely by Driver 1 (`drv-00563`). Vehicle parked in compound staging. Driver 2 booking (`drv-00564`) was CANCELLED due to a missed release slot.
   - *Agent Legwork:* Identifies vehicle staged at Kassel yard slot B-14; queries available freelance driver capacity in Hesse.
   - *Operator Action:* Targeted relay decisions: *"Publish Urgent Marketplace Bounty for Kassel → Destination Leg (€220.00)"* and *"Contact Kassel Yard Desk to Confirm Overnight Storage Voucher"*.
4. **`CD-420360` / `ord-00360` (Marketplace Offer Grounding):**
   - *Scenario:* Unassigned order pulled from real dataset records with a published market fee of €2,125.00 (`fee_cents: 212500`).
   - *Driver App Broadcast:* Real-time demand signal inspection (`market_offer_demand_signals.jsonl`) showing published fee, driver views, and quick actions to boost fees.
5. **Quiet Orders ("What Was Checked" Audit):**
   - *Scenario:* Orders with `needs_human: false` (e.g. `CD-420004`).
   - *Verification Panel:* Prominent green audit card rendering the Bahn Sentinel background checklist (active GPS corridor tolerance, e-CMR digital consignment compliance, site gate clearance, and maritime deck confirmation).

---

## 5. AI Engineering & Collaboration Process (30% Evaluation Criteria)

In accordance with the hackathon judging rubric, this section documents how our team leveraged AI coding agents (Claude Code, Antigravity, and OpenAI Codex) during development, detailing prompts, validations, hallucinations, and architectural decisions.

### 5.1 Coding Agents Used & Functional Roles
- **Claude Code & Antigravity (Architecture & REST API Modeling):**
  Used to synthesize the 40+ synthetic operational JSONL collections into unified relational schemas and design the state machines for order triage, multi-channel communications, and audit trails.
- **OpenAI Codex (Mathematical Geometries & FX Normalization):**
  Used to generate road waypoint corridor calculations via OSRM, Baltic Sea ferry waypoint transitions, and multi-currency exchange rate conversions (converting Danish Kroner DKK to EUR with standard 0.134 parity).

### 5.2 What We Prompted For
1. **Zero-Database In-Memory Streaming:** Prompted agents to load and index 40+ raw JSONL files directly on startup into memory structures, completely avoiding external SQL or Docker dependencies to ensure instant evaluation on any judge's laptop.
2. **Strict Human-in-the-Loop Safeguards:** Engineered system prompts that strictly prevent autonomous agents from sending unapproved outbound communications to clients or dealerships.
3. **High-Signal UI Density:** Prompted for an executive obsidian/zinc dispatch control room that eliminates cognitive clutter, replacing 7-lane Kanban boards with exception-based triage.

### 5.3 What Coding Agents Got Wrong (Errors & Hallucinations Caught)
1. **Database & Infrastructure Over-Engineering:**
   * *AI Error:* Early agent prompts repeatedly attempted to introduce PostgreSQL, Prisma ORM, and Redis cache containers, asserting that 40 tables required an external relational database.
   * *Human Correction:* We rejected this architecture. In a hackathon setting, external DB dependencies create Docker failures, port collisions, and migration headaches. We forced the agents to implement pure Python in-memory indexing, cutting startup time to under 0.2 seconds.
2. **Autonomous Action Hallucinations (Domain Law Violation):**
   * *AI Error:* One agent suggested an autonomous recovery feature where the system would automatically email receiving dealerships and auto-book replacement ferries.
   * *Human Correction:* In finished vehicle logistics, sending an unreviewed email to a dealer principal regarding a delayed Bentley or Porsche damages commercial relationships. We rejected full autonomy and instituted the **10-second reversible human confirmation staging modal with editable notes**.
3. **Currency Inconsistencies:**
   * *AI Error:* Initial financial aggregators mixed DKK expenses (Danish bridge tolls and Copenhagen fuel receipts) with EUR values without foreign exchange conversion, inflating expense margins.
   * *Human Correction:* We added an FX normalization layer converting all DKK currency values by the official factor (`0.134`).

### 5.4 What Was Thrown Away
- **Discarded the Starter 7-Lane Kanban Board:** The starter kit provided a traditional status-lane board (Intake, Ready, On Market, Booked, Moving, Delivered, Cancelled). We threw this away entirely. A dispatcher with 100 cars cannot scan 7 columns; they need to know which 22 cars require intervention right now.
- **Discarded Generic Developer UI Libraries:** Threw away off-the-shelf component libraries that look like developer tools. We built a custom obsidian dispatch palette (`#0D0F12`), custom Leaflet telemetry pins, real automotive brand SVG logos, and actual vehicle preview renders.
- **Discarded Instant Auto-Execute Triggers:** Any action triggered by an operator or agent proposal previously executed immediately. We threw this away and replaced it with a staged modal with a live countdown and an interactive "Modify" interface, creating a true enterprise dispatch workflow.

### 5.5 Two-Tier Agent Architecture
Our solution implements a deliberate two-tier design:
1. **Tier 1 — The Sentinel Inspector (Deterministic Background Engine):**
   Runs continuously across telemetry beacons, CMR consignment validations, and ferry cutoffs without burning expensive tokens or suffering from stochastic hallucinations during critical dispatch windows.
2. **Tier 2 — The Conversational Dispatch Copilot (LLM-Powered Reasoning):**
   A dual-scope language model assistant (Fleet Scope vs. Car Scope) that helps operators analyze complex multi-factor incidents, inspect driver rest hours, and draft communications under human supervision.

---

## 6. Audit Logging & State Persistence

Every decision executed by an operator—whether dismissing a false alarm, approving roadside assistance, rebooking maritime passage, or postponing an unlinked support ticket—is immutably recorded in the **Global Operations Audit Log**.
- **10-Second Undo Window:** Operators can cancel staged actions during the countdown before events are committed.
- **Export to Disk:** One-click export writes formatted `.json` logs directly into `Saved log/` on the server filesystem.
- **Import & Replay:** Operators can upload historical audit logs to inspect past shift decisions.
- **Simulation Reset:** The top bar includes a `"Reset Simulation"` button, allowing evaluators to return all 100 orders to their original snapshot state for repeatable demonstrations.

---

## 7. Submission Checklist & Compliance

- [x] **Runs from a fresh clone** (`pip install -r requirements.txt` followed by `python run.py`).
- [x] **Zero external database dependencies** (pure Python in-memory store).
- [x] **40% Control Room:** High-signal triage (77 Quiet / 23 Actionable), quiet order verification panel, multi-channel provenance.
- [x] **30% Taste:** Non-engineer dispatch UI, calm typography, vehicle preview imagery, interactive European route maps.
- [x] **30% AI Engineering:** Comprehensive documentation of coding agent prompts, hallucinations caught, and rejected architectures.
- [x] **Strict Human-in-the-Loop:** 10-second confirmation window, zero unapproved customer communications.
