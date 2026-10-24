# Car Delivery Control Room — Baseline Solution

An enterprise-grade, single-screen operations control room application designed for human dispatchers managing long-haul finished vehicle logistics across Europe.

---

## 1. Overview

The **Car Delivery Control Room** empowers control room operators to monitor, triage, and intervene in live vehicle delivery transport operations across European corridors (Germany, Denmark, Sweden, Finland).

### Key Baseline Capabilities
- **Fleet-Wide Live Triage & Filtering**: Real-time table monitoring of active vehicle transports with multi-dimensional filtering by operational condition (`🚨 Road Breakdown`, `⏱️ Driver Delay Risk`, `🎨 Cosmetic Damage`, `🟢 Normal Operation`, `🟣 Handled / Pending Confirmation`) and sorting options.
- **Corridor & Multi-Modal Routing**: Interactive Leaflet maps rendering actual European highway paths via live OSRM integration and Baltic Sea maritime ferry legs (Travemünde ↔ Helsinki port transitions) with aligned milestone pins.
- **Milestone & Telematics Tracking**: Milestone execution timeline synchronizing route checkpoints, geofence entries/exits, and rest area stops with exact color-coded map pins.
- **Multi-Channel Conversation History**: Categorized tabbed communications hub separating messages across distinct channels (`Driver Mobile App`, `Dealership Email`, `Site & Station Desk`, `Internal Dispatch`).
- **Autonomous Agent Activity Monitoring**: Inspection of AI and automated system actions with distinct visual badges (`COMPLETED`, `PROPOSED`, `FAILED`) and human-in-the-loop approval/rejection workflows.
- **Handover Proofs & Attachments**: Verification of digital handover inspection protocols and physical high-resolution delivery/pickup photos with interactive zoom previews.
- **Financial Clearance & Settlement**: Complete invoice and expense ledger featuring 1-to-1 PDF receipt inspection, automatic foreign exchange conversion (DKK → EUR), metric highlights (Gross Revenue, Driver Payouts, Trip Expenses, Net Margin), and chronological order sorting.
- **Audit Logging & State Persistence**: Comprehensive audit trail capturing dispatcher decisions and inbox actions with full Export, Import, and Clear capabilities.

---

## 2. Project Structure

This directory represents the complete, self-contained root for the `control-room-app` branch:

```text
.
├── .env.example                     # Environment template (OpenRouter API key)
├── .gitignore                       # Standard Python / IDE exclusions
├── requirements.txt                 # Exact Python dependencies
├── run.py                           # One-click startup script
├── README.md                        # Documentation and setup instructions
├── Saved log/                       # Export directory for operator audit logs
│   └── .gitkeep
├── app/ (or control_room_app/)
│   ├── __init__.py                  # Package descriptor
│   ├── backend.py                   # FastAPI REST backend and routing logic
│   └── static/
│       ├── index.html               # Single-page control room UI (Tailwind CSS, Alpine.js, Leaflet)
│       ├── bahn-logo.png            # Official Bahn corporate logo
│       ├── car-images/              # 24 vehicle preview images (WebP)
│       └── car-logos/               # 16 automotive manufacturer brand badges (SVG)
├── dataset/
│   └── data/                        # 36 essential .jsonl operational dataset collections
│       ├── addresses.jsonl
│       ├── agent_proposals.jsonl
│       ├── alerts.jsonl
│       ├── assignment_steps.jsonl
│       ├── conversations.jsonl
│       ├── custody_asset_events.jsonl
│       ├── custody_assets.jsonl
│       ├── customers.jsonl
│       ├── documents.jsonl
│       ├── drivers.jsonl
│       ├── endpoint_claims.jsonl
│       ├── expenses.jsonl
│       ├── ferry_terminal_events.jsonl
│       ├── ferry_terminals.jsonl
│       ├── incidents.jsonl
│       ├── messages.jsonl
│       ├── operational_events.jsonl
│       ├── order_endpoint_details.jsonl
│       ├── order_items.jsonl
│       ├── order_notes.jsonl
│       ├── orders.jsonl
│       ├── proofs.jsonl
│       ├── sites.jsonl
│       ├── support_inbox_messages.jsonl
│       ├── support_inbox_threads.jsonl
│       ├── terminal_road_estimates.jsonl
│       ├── time_windows.jsonl
│       ├── tracking_observations.jsonl
│       ├── transport_plans.jsonl
│       ├── transport_points.jsonl
│       ├── transport_segments.jsonl
│       ├── travel_options.jsonl
│       ├── travel_reservations.jsonl
│       ├── vehicles.jsonl
│       ├── work_assignments.jsonl
│       └── work_items.jsonl
└── attachments/
    ├── manifest.json                # Attachment lookup index (58 records)
    ├── documents/                   # 30 official consignment notes (CMR) & release orders (PDF)
    ├── photos/                      # 16 proof-of-delivery & vehicle condition photos (JPG)
    └── receipts/                    # 12 driver expense & travel receipts (PDF)
```

---

## 3. Setup & Execution

### Prerequisites
- Python 3.10+ (tested on Python 3.10, 3.11, 3.12, 3.13)
- Modern web browser (Chrome, Edge, Firefox, Safari)

### Step 1: Install Dependencies
Create a virtual environment (recommended) and install the lightweight requirements:

```bash
# Optional: create and activate virtual environment
python -m venv .venv

# On Linux / macOS:
source .venv/bin/activate
# On Windows PowerShell:
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Environment Configuration (Optional)
The control room functions 100% locally with rule-based heuristics out of the box. If you wish to enable the AI Dispatch Assistant via OpenRouter, configure `.env`:

```bash
cp .env.example .env
# Edit .env and supply your OPENROUTER_API_KEY
```

### Step 3: Run the Application
Launch the server using either the convenient startup runner or standard uvicorn:

**Option A (Recommended Runner):**
```bash
python run.py
```

**Option B (Direct Uvicorn CLI):**
```bash
uvicorn control_room_app.backend:app --host 127.0.0.1 --port 8000 --reload
```

### Step 4: Open the Control Room
Open your browser and navigate to:
```
http://127.0.0.1:8000
```

---

## 4. Data & Assets Used

The solution includes only the assets and data files directly required by the baseline runtime logic, omitting all unneeded challenge artifacts (such as unused template starters, legacy mockups, presentation slides, or testing scripts).

### A. Operational Datasets (`dataset/data/`)
The backend loads 36 `.jsonl` collections to reconstruct the delivery environment:
1. `orders.jsonl`, `order_items.jsonl`: Commercial vehicle delivery orders, status, reference IDs, and contractual milestones.
2. `vehicles.jsonl`: Vehicle specifications (make, model, VIN, registration, condition notes).
3. `drivers.jsonl`: Driver rosters, operational status, phone, email, and certifications.
4. `customers.jsonl`: Dealership and buyer accounts with contact details.
5. `addresses.jsonl`, `sites.jsonl`: Physical hubs, delivery compounds, and geographical coordinates.
6. `time_windows.jsonl`: Pickup and delivery SLA windows.
7. `tracking_observations.jsonl`: Real-time GPS pings, speed, heading, and battery/fuel levels.
8. `alerts.jsonl`, `incidents.jsonl`: Operational alarms (telemetry flatlines, route deviations, break-in/breakdown reports).
9. `transport_plans.jsonl`, `transport_points.jsonl`, `transport_segments.jsonl`: Pre-planned routing segments and waypoints.
10. `ferry_terminals.jsonl`, `ferry_terminal_events.jsonl`, `terminal_road_estimates.jsonl`: Ro-Ro ferry schedules, congestion buffers, and boarding windows.
11. `travel_options.jsonl`, `travel_reservations.jsonl`: Driver train/ferry tickets and return travel bookings.
12. `messages.jsonl`, `conversations.jsonl`, `support_inbox_threads.jsonl`, `support_inbox_messages.jsonl`: Multi-channel communication threads.
13. `agent_proposals.jsonl`: Autonomous recommendation actions and operational proposals.
14. `documents.jsonl`, `proofs.jsonl`: Delivery confirmation records, CMR forms, and damage reports.
15. `expenses.jsonl`: Driver expense logs, toll receipts, fuel purchases, and charging costs.
16. `custody_assets.jsonl`, `custody_asset_events.jsonl`: Key tags, charge cards, and vehicle asset custody transitions.
17. `work_items.jsonl`, `work_assignments.jsonl`, `assignment_steps.jsonl`, `endpoint_claims.jsonl`, `operational_events.jsonl`, `order_endpoint_details.jsonl`, `order_notes.jsonl`: Operational execution flow and state machine events.

*(Excluded 12 unused challenge files: `agents.jsonl`, `custody_reports.jsonl`, `internal_notifications.jsonl`, `manifest.json`, `market_offers.jsonl`, `market_offer_demand_signals.jsonl`, `market_offer_demand_windows.jsonl`, `market_offer_exposures.jsonl`, `market_offer_reach_checks.jsonl`, `operators.jsonl`, `site_visits.jsonl`, `travel_confirmations.jsonl`)*.

### B. Attachments & Physical Proofs (`attachments/`)
- `manifest.json`: Index mapping attachment UUIDs to orders, proof records, and document types.
- `photos/` (16 JPGs): Actual physical evidence images (delivery handovers, scratch/dent inspections, key handovers).
- `documents/` (30 PDFs): Official CMR consignment notes and release authorizations.
- `receipts/` (12 PDFs): Itemized driver expenses (fuel, highway tolls, parking vouchers, and charging bills).

### C. Static UI Assets (`control_room_app/static/`)
- `index.html`: Responsive single-page application built with Tailwind CSS, Alpine.js, and Leaflet.
- `bahn-logo.png`: Branding header asset.
- `car-images/` (24 WebP files): High-fidelity vehicle renders mapped dynamically by vehicle make and model.
- `car-logos/` (16 SVG files): Automotive manufacturer logos for fast visual identification in the fleet overview table.
