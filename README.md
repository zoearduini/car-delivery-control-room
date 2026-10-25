# Bahn Sentinel: Car Delivery Operations Control Room

An enterprise-grade, single-screen operations control room application engineered for human dispatchers managing long-haul finished vehicle logistics corridors across Europe (Germany, Denmark, Sweden, Finland).

Built for the **Bahn Hackathon** (24–25 October 2026), addressing the operational challenge of high-density finished vehicle transport triage and human-in-the-loop dispatch.

---

## 1. Executive Summary & Core Philosophy

Bahn coordinates over 25,000 used car transits annually across European borders utilizing freelance driver networks. In finished vehicle logistics, road transit conditions, ferry capacities, driver rest regulations, and dealership handovers evolve continuously.

### The 40% Control Room Criterion: High Signal, Low Noise
Traditional logistics dashboards overwhelm operators with raw data tables or bulky Kanban columns. **Bahn Sentinel** adheres to a strict operational philosophy:
* **Quiet vs. Actionable Triage:** Most vehicles are moving on schedule without issue. The system separates quiet orders from the operator's active focus, surfacing only the exceptions that require human judgment.
* **Sentinel Background Audit ("What Was Checked"):** *"For every hidden order, say what was checked. An order nobody checked is not fine."* For all quiet orders (`needs_human: false`), the Order Dossier displays an automated Sentinel verification card verifying GPS corridor tolerance, e-CMR digital consignment note compliance, receiving dealership release clearance, and maritime ferry allocations.
* **Human-in-the-Loop Domain Law:** Autonomous agents **never** contact a paying dealership or client directly. The agent performs 100% of the investigative legwork first, then presents the dispatcher with structured, ready-to-decide recovery options with a **10-second countdown confirmation window** (complete with instant **Modify** and **Undo** capabilities).

---

## 2. Key Capabilities & Benchmark Scenario Coverage

### 1. Grounded Financials & Real Dataset Ledgers
* **Driver Fees:** Directly queried from active assignment records (`work_assignments.jsonl`) and marketplace offers (`market_offers.jsonl`), replacing synthetic formulas with true contracted fees.
* **Trip Expenses & DKK Currency Conversion:** Real travel and fuel expenses from `expenses.jsonl`, automatically normalizing Danish Krone (DKK) to Euro (EUR) with explicit breakdown displays (e.g. `42.21 EUR (315.00 DKK)`).
* **Operating Margin:** Calculates realistic operating margins (26%–33%) reflecting real-world finished vehicle logistics overheads.
* **Marketplace Gig Broadcasts:** For unassigned vehicles, surfaces live marketplace demand signals (fee, published timestamp, and freelance driver view counts).

### 2. Full Benchmark Scenario Resolution
* **Road Breakdown (`CD-420322` / Bentley Continental GT):** Engine temperature alert triggered on A7 motorway near Allertal West. Halted safely at rest stop. Triage cards provide towing authorization, roadside repair dispatch, and dealership schedule notification drafts.
* **Baltic Sea Ferry Capacity Exceeded (`CD-420299` / BMW M4):** Finnlines Travemünde → Helsinki evening departure fully booked. System maps intermediate port transition pins and stages rebooking decisions for the next available sailing (+€220).
* **Transfer Yard Relay Driver Cancellation (`CD-420702` / Mercedes-Benz C-Class):** Multi-leg transit where Leg 1 completed to Kassel Logistics Hub, but Leg 2 onward driver cancelled. Grounded with an intermediate transfer yard map stop, staging marketplace bounty publication (€220) and safe compound overnight storage vouchers.
* **Missing Signed Handover Proof (`CD-420164`):** Customer accounting desk inquiry resolved by linking inspection photos while enforcing document verification protocols.

### 3. European Corridors & Multi-Modal Routing
* **Actual Highway Paths:** Uses real European road geometries connecting origin and destination coordinates across Germany, Denmark, Sweden, and Finland.
* **Multi-Modal Maritime Crossings:** Visualizes Baltic Sea ferry legs (Travemünde ↔ Helsinki Vuosaari) with distinct maritime route styling and terminal check-in waypoints.
* **Interactive Leaflet Cockpit:** Auto-fits route bounds with custom high-contrast pins for pickup, current position, intermediate yards/ports, and final delivery.

### 4. Multi-Channel Unified Communications Hub
* Tabbed operational feed categorizing communications into **Driver Mobile App**, **Dealership Email**, **Site & Station Desk**, and **Internal Dispatch**.
* Channels maintain full thread integrity: customer-facing queries and operator replies remain threaded together, while private internal dispatch directives remain isolated.
* **All Channels** view provides a unified chronological transcript of all counterparty interactions.

---

## 3. Project Structure

This directory is completely self-contained and ready to run from an empty branch:

```text
submission_final/
├── .env.example                     # Environment template (optional OpenRouter API key)
├── .gitignore                       # Standard Python / OS exclusions
├── requirements.txt                 # Exact lightweight Python dependencies
├── run.py                           # One-click startup script
├── README.md                        # Documentation and architecture guide
├── Saved log/                       # Export directory for operator audit logs
│   └── .gitkeep
├── control_room_app/
│   ├── __init__.py                  # Package descriptor
│   ├── backend.py                   # FastAPI REST backend and dispatch logic
│   └── static/
│       ├── index.html               # Single-page control room UI (Tailwind CSS, Leaflet)
│       ├── bahn-logo.png            # Official Bahn corporate logo
│       ├── car-images/              # 24 vehicle preview renders (WebP)
│       └── car-logos/               # 16 automotive manufacturer brand badges (SVG)
├── dataset/
│   └── data/                        # 36 JSONL operational dataset collections
│       ├── orders.jsonl
│       ├── vehicles.jsonl
│       ├── tracking_observations.jsonl
│       ├── work_assignments.jsonl
│       ├── market_offers.jsonl
│       ├── expenses.jsonl
│       ├── messages.jsonl
│       ├── proofs.jsonl
│       └── ... (36 collections total)
└── attachments/                     # 58 physical proof files & attachments
    ├── manifest.json
    ├── documents/                   # CMR consignment notes and vehicle release forms
    ├── photos/                      # Vehicle inspection and damage documentation
    └── receipts/                    # Fuel and toll vouchers
```

---

## 4. Setup & Quickstart

### Prerequisites
* Python 3.10, 3.11, 3.12, or 3.13
* Any modern web browser (Chrome, Edge, Firefox, Safari)

### Single-Command Execution
```bash
# 1. Clone repository and navigate to submission directory
git clone <repo_url>
cd submission_final

# 2. (Optional) Create and activate a virtual environment
python -m venv .venv

# On Windows PowerShell:
.venv\Scripts\Activate.ps1
# On Linux / macOS:
source .venv/bin/activate

# 3. Install dependencies (< 10 seconds, zero binary extensions)
pip install -r requirements.txt

# 4. Launch the Bahn Control Room
python run.py
```

### Accessing the Control Room
Open your browser and navigate to:
```text
http://127.0.0.1:8000
```

> **Zero External Databases:** The entire system runs purely in-memory from the 36 raw JSONL files and local assets. No Docker, PostgreSQL, Redis, or cloud provisioning required.

---

## 5. AI Engineering & Collaboration Process (Hackathon Slide 11)

### 1. Which Coding Agents Were Used and for What
* **Anthropic Claude Code & Antigravity (Google DeepMind):** Used for end-to-end architectural modeling, FastAPI endpoint design, responsive single-page dispatch cockpit layout, and strict human-in-the-loop state machine enforcement.
* **OpenAI Codex:** Utilized for rapid mathematical prototyping of European geographical corridor bounds, DKK/EUR currency exchange matrices, and OSRM coordinate interpolations.
* **OpenRouter / GPT-4o-mini (Integrated Copilot):** Embedded directly into the control room backend (`/api/agent/chat`) to serve as an on-demand dispatcher copilot with instant local heuristic fallback.

### 2. What Prompts Were Given
* **Grounding in Raw Data:** *"Model all dispatch and commercial entities strictly from the 36 raw JSONL collections. Do not synthesize mock values when active assignments, market offers, or expenses exist in the dataset."*
* **Domain Policy Enforcement:** *"Autonomous agents are strictly forbidden from contacting paying dealerships or receiving clients directly. All agent actions must be presented as decision proposals with explicit 10-second staging windows for operator review and modification."*
* **High Signal / Low Noise UI:** *"Design an obsidian dark dispatch cockpit that hides quiet nominal vehicles while providing explicit 'What Was Checked' Sentinel audit checklists for verified safe orders."*

### 3. What Worked Well
* **In-Memory Graph Traversal:** Loading all 36 JSONL files into Python dictionaries at startup resulted in sub-millisecond response times across all 100 orders without requiring complex SQL or ORM layers.
* **Declarative Single-Page Architecture:** Consolidating the entire dispatcher interface into a modular, responsive HTML5/Tailwind/Leaflet single-page application eliminated build-step fragility (no Webpack, npm, or node_modules required).
* **Two-Tier Agent Structure:** Dividing background investigative legwork from the operator decision interface gave the AI assistant high operational utility while keeping humans firmly in command.

### 4. What Failed & What Required Human Steering
* **Naïve Channel Splitting:** Initial filtering routed messages strictly by author role, which accidentally split customer questions and operator replies across two tabs. Human architectural review corrected this to preserve full conversational thread context.
* **Currency Normalization:** Early expense aggregates failed on Danish Krone (DKK) receipts because raw amounts were summed directly with Euro figures. We guided the model to implement deterministic ISO currency lookup with live conversion rates.
* **Kassel Intermediate Yard Disconnect:** Standard routing algorithms assumed simple point-to-point journeys. Human operational domain knowledge was required to teach the model how to stage intermediate transfer yards when a relay driver assignment cancels midway.

---

## 6. Verification & Quality Assurance

The codebase has undergone a 100% automated verification pass:
* **All 100 Orders Verified:** Complete European coordinate validity (lat 48°–65° N, lng 9°–25° E), multi-point road geometry polylines, and milestone waypoints.
* **Zero Runtime Polling:** No real-time timeline scrubbers, speed multipliers, or background ticking loops. Clean, deterministic state transitions.
* **Repeatable Demo State:** The **Reset Baseline** button instantly clears all session decisions and returns the entire fleet to its initial state for repeatable jury presentations.
