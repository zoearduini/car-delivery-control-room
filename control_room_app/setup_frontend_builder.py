import os

output_path = "control_room_app/static/index.html"

with open("control_room_app/build_clean_frontend.py", "w", encoding="utf-8") as f:
    f.write('''# Clean Frontend Generator for Car Delivery Control Room
import os

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bahn Operations Control Room | Europe Fleet Dispatch</title>
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  
  <!-- Leaflet Maps CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&display=swap');
    
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: #F8F9FA;
      color: #1A1D20;
    }
    
    code, pre, .font-mono {
      font-family: 'JetBrains Mono', monospace;
    }

    /* Custom subtle scrollbars */
    .custom-scrollbar::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
      background: #F1F3F5;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
      background: #CED4DA;
      border-radius: 3px;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb:hover {
      background: #ADB5BD;
    }

    /* Pulse animation for active incidents */
    @keyframes subtle-pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.85; transform: scale(1.02); }
    }
    .pulse-urgent {
      animation: subtle-pulse 2s infinite ease-in-out;
    }

    /* Leaflet hover tooltip styling */
    .leaflet-tooltip.custom-hover-tip {
      background: #121417;
      color: #ffffff;
      border: 1px solid #374151;
      border-radius: 6px;
      font-size: 12px;
      padding: 6px 10px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }
    .leaflet-tooltip-left:before, .leaflet-tooltip-right:before, .leaflet-tooltip-top:before, .leaflet-tooltip-bottom:before {
      border: none !important;
    }
  </style>
</head>
<body class="h-screen flex flex-col overflow-hidden relative">

  <!-- TOAST CONTAINER -->
  <div id="toast-container" class="fixed top-5 right-5 z-[9999] flex flex-col space-y-2 pointer-events-none"></div>

  <!-- INLINE ACTION CONFIRMATION & 5S UNDO BANNER (No alert/popup windows!) -->
  <div id="action-undo-bar" class="hidden fixed bottom-6 left-1/2 -translate-x-1/2 z-50 bg-[#121417] text-white px-5 py-3.5 rounded-xl shadow-2xl border border-gray-700 flex items-center space-x-4 max-w-xl w-full">
    <div class="w-8 h-8 rounded-full bg-amber-400 text-black flex items-center justify-center shrink-0 font-bold">
      <i data-lucide="clock" class="w-4 h-4"></i>
    </div>
    <div class="flex-1 min-w-0">
      <div class="flex items-center space-x-2">
        <span class="text-[10px] uppercase font-bold text-amber-400 tracking-wider">Action Scheduled</span>
        <span class="text-[10px] text-gray-400">Auto-executing in <strong id="undo-countdown-sec" class="text-white font-mono">5s</strong></span>
      </div>
      <p id="undo-action-title" class="text-xs font-bold text-gray-100 truncate mt-0.5">Rebooking Travemünde Ferry Crossing</p>
      <div class="w-full bg-gray-800 rounded-full h-1 mt-1.5 overflow-hidden">
        <div id="undo-progress-bar" class="bg-amber-400 h-1 rounded-full transition-all duration-1000 ease-linear" style="width: 100%;"></div>
      </div>
    </div>
    <div class="flex items-center space-x-2 shrink-0">
      <button onclick="cancelPendingAction()" class="px-3 py-1.5 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-xs font-bold transition flex items-center space-x-1 shadow-sm">
        <i data-lucide="x" class="w-3.5 h-3.5"></i>
        <span>Undo</span>
      </button>
      <button onclick="executePendingActionNow()" class="px-3 py-1.5 bg-amber-400 hover:bg-amber-500 text-black rounded-lg text-xs font-bold transition flex items-center space-x-1 shadow-sm">
        <i data-lucide="check" class="w-3.5 h-3.5"></i>
        <span>Execute Now</span>
      </button>
    </div>
  </div>

  <!-- TOP APP HEADER BAR -->
  <header class="h-16 bg-[#121417] text-white flex items-center justify-between px-8 border-b border-gray-800 shrink-0 select-none">
    <!-- Left: Logo & Global Navigation -->
    <div class="flex items-center space-x-6">
      <div class="flex items-center space-x-3 cursor-pointer" onclick="goToFleetView()">
        <img src="/static/bahn-logo.png" alt="Bahn Logo" class="w-8 h-8 rounded object-contain bg-white p-0.5 shadow-sm">
        <div>
          <span class="font-extrabold text-sm tracking-wider uppercase text-amber-400">BAHN OPERATIONS</span>
          <span class="text-xs text-gray-300 font-semibold ml-1.5">Control Room</span>
        </div>
      </div>

      <!-- Navigation Tabs -->
      <nav class="flex items-center space-x-1 bg-gray-900 p-1 rounded-lg border border-gray-800 text-xs">
        <button id="nav-btn-fleet" onclick="goToFleetView()" class="px-3 py-1.5 rounded-md font-semibold bg-amber-500 text-black flex items-center space-x-1.5 transition">
          <i data-lucide="car" class="w-3.5 h-3.5"></i>
          <span id="nav-fleet-label">Fleet Overview</span>
        </button>
        <button id="nav-btn-inbox" onclick="switchGlobalView('inbox')" class="px-3 py-1.5 rounded-md font-medium text-gray-300 hover:text-white flex items-center space-x-1.5 transition">
          <i data-lucide="inbox" class="w-3.5 h-3.5"></i>
          <span>Support Inbox</span>
          <span id="nav-inbox-badge" class="bg-amber-500 text-black px-1.5 py-0.2 rounded-full text-[10px] font-bold">4</span>
        </button>
        <button id="nav-btn-history" onclick="switchGlobalView('history')" class="px-3 py-1.5 rounded-md font-medium text-gray-300 hover:text-white flex items-center space-x-1.5 transition">
          <i data-lucide="history" class="w-3.5 h-3.5"></i>
          <span>Operations Audit Log</span>
        </button>
        <button id="nav-btn-finance" onclick="switchGlobalView('finance')" class="px-3 py-1.5 rounded-md font-medium text-gray-300 hover:text-white flex items-center space-x-1.5 transition">
          <i data-lucide="coins" class="w-3.5 h-3.5"></i>
          <span>Financials & Earnings</span>
        </button>
      </nav>
    </div>

    <!-- Right: Operator ID & AI Trigger -->
    <div class="flex items-center space-x-3 text-xs">
      <!-- Operator ID Pill -->
      <div class="bg-gray-800/90 hover:bg-gray-800 border border-gray-700 px-3 py-1.5 rounded-lg flex items-center space-x-2 text-gray-300 font-mono transition">
        <i data-lucide="shield" class="w-3.5 h-3.5 text-amber-400"></i>
        <span>Operator: <strong id="operator-display" class="text-white">OP-042</strong></span>
        <button onclick="promptOperatorId()" class="text-gray-400 hover:text-white ml-1">
          <i data-lucide="edit-2" class="w-3 h-3"></i>
        </button>
      </div>

      <!-- AI Assistant Button in Top Bar -->
      <button onclick="toggleAiSidebar()" class="px-3.5 py-1.5 rounded-lg bg-purple-600 hover:bg-purple-700 text-white font-bold flex items-center space-x-1.5 shadow-sm transition">
        <i data-lucide="bot" class="w-3.5 h-3.5"></i>
        <span>AI Assistant</span>
      </button>
    </div>
  </header>

  <!-- ================= VIEW 1: FLEET OVERVIEW (HOME) ================= -->
  <div id="view-home" class="flex-1 flex flex-col overflow-hidden bg-white">

    <!-- SUB-HEADER: STATUS FILTER & CONTROLS (Fixed height and padding so layout never shifts) -->
    <div class="h-14 bg-white border-b border-gray-200 px-8 flex items-center justify-between shrink-0 select-none">

      <!-- Left Filters: Status & Problems -->
      <div class="flex items-center space-x-3 text-xs">
        <!-- Status Filter Tabs (Starts with All Cars by default per user request) -->
        <div class="flex bg-gray-100 p-1 rounded-lg border border-gray-200 font-semibold">
          <button id="btn-status-all" onclick="setStatusFilter('all')" class="px-3.5 py-1.5 rounded-md bg-white text-black font-bold shadow-xs transition">
            All Cars (<span id="count-all">100</span>)
          </button>
          <button id="btn-status-ok" onclick="setStatusFilter('ok')" class="px-3.5 py-1.5 rounded-md text-emerald-800 hover:bg-white transition flex items-center space-x-1">
            <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
            <span>OK / On Track (<span id="count-ok">78</span>)</span>
          </button>
          <button id="btn-status-not-ok" onclick="setStatusFilter('not_ok')" class="px-3.5 py-1.5 rounded-md text-rose-700 hover:bg-white transition flex items-center space-x-1.5">
            <i data-lucide="alert-triangle" class="w-3.5 h-3.5"></i>
            <span>Needs Attention (<span id="count-not-ok">22</span>)</span>
          </button>
        </div>

        <!-- Problem Dropdown Filter -->
        <div id="problem-filter-box" class="flex items-center space-x-2">
          <span class="text-gray-400 text-[11px] font-bold uppercase">Issue Category:</span>
          <select id="problem-select" onchange="onProblemSelectChange()" class="border border-gray-300 rounded-lg px-2.5 py-1.5 bg-gray-50 text-gray-800 text-xs font-semibold focus:outline-none focus:border-amber-500">
            <option value="all">All Issues (22)</option>
            <option value="breakdown">Road Breakdowns & Warnings (1)</option>
            <option value="ferry">Ferry Capacity & Disruption (2)</option>
            <option value="documents">Missing Documents & Gate Release (11)</option>
            <option value="schedule">Schedule & Relay Delays (5)</option>
            <option value="claims">Post-Delivery Damage Claims (3)</option>
          </select>
        </div>
      </div>

      <!-- Right Controls: Sorting & Search -->
      <div class="flex items-center space-x-3 text-xs">
        <div class="flex items-center space-x-1.5">
          <span class="text-gray-400 text-[11px] font-bold uppercase">Sort:</span>
          <select id="sort-select" onchange="onSortChange()" class="border border-gray-300 rounded-lg px-2.5 py-1.5 bg-gray-50 text-gray-800 text-xs font-semibold focus:outline-none focus:border-amber-500">
            <option value="newest" selected>Newest Orders</option>
            <option value="critical">Critical Attention First</option>
            <option value="oldest">Oldest Orders</option>
            <option value="alphabetical">Vehicle Make & Model</option>
            <option value="status">Transit Status</option>
          </select>
        </div>

        <div class="relative w-64">
          <i data-lucide="search" class="w-3.5 h-3.5 absolute left-3 top-2.5 text-gray-400"></i>
          <input type="text" id="fleet-search" oninput="onSearchInput()" placeholder="Filter VIN, plate, customer..." class="w-full pl-8 pr-3 py-1.5 bg-gray-50 border border-gray-300 rounded-lg text-xs text-gray-900 focus:outline-none focus:border-amber-500 focus:bg-white transition">
        </div>
      </div>
    </div>

    <!-- MAIN FLEET TABLE (table-fixed and permanent scrollbar gutter so spaces never shift!) -->
    <div class="flex-1 overflow-y-scroll custom-scrollbar px-8 py-4" style="scrollbar-gutter: stable;">
      <div class="border border-gray-200 rounded-xl overflow-hidden shadow-xs bg-white min-h-[540px]">
        <table class="w-full text-left border-collapse text-xs table-fixed">
          <thead class="bg-gray-50/90 border-b border-gray-200 text-gray-500 font-bold uppercase tracking-wider text-[11px] sticky top-0 z-10">
            <tr>
              <th class="w-28 p-3.5 pl-5">Order Ref</th>
              <th class="w-64 p-3.5">Vehicle</th>
              <th class="w-48 p-3.5">Corridor Route</th>
              <th class="w-40 p-3.5">Current Position</th>
              <th class="w-44 p-3.5">Assigned Driver</th>
              <th class="w-56 p-3.5">Operational Condition</th>
              <th class="w-24 p-3.5 pr-5 text-right">Action</th>
            </tr>
          </thead>
          <tbody id="fleet-table-tbody" class="divide-y divide-gray-100">
            <!-- Dynamically populated rows -->
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- ================= VIEW 2: CAR DETAIL DOSSIER ================= -->
  <div id="view-car-detail" class="hidden flex-1 flex flex-col overflow-hidden bg-[#F8F9FA]">
    
    <!-- TOP BREADCRUMB / BACK BAR -->
    <div class="h-12 bg-white border-b border-gray-200 px-8 flex items-center justify-between shrink-0 select-none">
      <div class="flex items-center space-x-3">
        <button onclick="goBackToFleetTable()" class="flex items-center space-x-1.5 text-xs font-bold text-gray-700 hover:text-black transition">
          <i data-lucide="arrow-left" class="w-4 h-4"></i>
          <span>All Cars</span>
        </button>
        <span class="text-gray-300">/</span>
        <span class="text-gray-500 font-mono text-[11px]" id="detail-nav-id">ORD-00322</span>
        <span class="text-gray-300">-</span>
        <span class="font-bold text-gray-900" id="detail-nav-car">2022 Bentley Continental GT</span>
      </div>

      <div class="flex items-center space-x-2 text-xs">
        <button onclick="openAiSidebarForCar()" class="px-3 py-1.5 rounded-lg bg-purple-50 text-purple-700 font-bold hover:bg-purple-100 transition flex items-center space-x-1.5 border border-purple-200">
          <i data-lucide="sparkles" class="w-3.5 h-3.5 text-purple-600"></i>
          <span>Ask AI About This Car</span>
        </button>
      </div>
    </div>

    <!-- MAIN DOSSIER SCROLLABLE CONTENT (Ordered sequentially per user request!) -->
    <div class="flex-1 overflow-y-auto custom-scrollbar p-8 max-w-6xl w-full mx-auto space-y-8">

      <!-- VEHICLE DELIVERY PIPELINE STEPPER -->
      <div class="bg-white rounded-xl border border-gray-200 p-4 shadow-xs">
        <div class="flex items-center justify-between text-xs font-bold text-gray-500 mb-2.5">
          <span class="uppercase tracking-wider text-[11px] text-gray-400">Transport Chain Lifecycle</span>
          <span id="pipeline-current-status" class="font-mono text-gray-800 bg-gray-100 px-2 py-0.5 rounded text-[11px]">IN_TRANSIT</span>
        </div>
        <div id="pipeline-stepper" class="grid grid-cols-5 gap-2 text-xs">
          <!-- Dynamically populated 5 steps -->
        </div>
      </div>

      <!-- SITUATION / ACTIVE ISSUE BANNER (Full description shown in details!) -->
      <div id="detail-alert-box" class="hidden p-4 rounded-xl bg-rose-50 border border-rose-300 text-rose-950 space-y-1 shadow-xs">
        <div class="flex items-center space-x-2 font-bold text-sm text-rose-800">
          <i data-lucide="alert-octagon" class="w-4 h-4 text-rose-600"></i>
          <span id="detail-alert-title">Operational Situation: Action Required</span>
        </div>
        <p id="detail-alert-desc" class="text-xs text-rose-900 leading-relaxed font-medium">
          Detailed issue explanation loading...
        </p>
      </div>

      <!-- QUICK NAVIGATION ANCHOR PILLS -->
      <div class="sticky top-0 z-20 bg-[#F8F9FA]/90 backdrop-blur-sm py-2 flex items-center space-x-2 text-xs font-bold border-b border-gray-200 select-none">
        <a href="#car-section-deal" class="px-3 py-1.5 rounded-lg bg-white border border-gray-200 text-gray-800 hover:bg-gray-100 transition shadow-xs flex items-center space-x-1">
          <i data-lucide="file-badge" class="w-3.5 h-3.5 text-amber-500"></i>
          <span>1. Deal Details</span>
        </a>
        <a href="#car-section-route" class="px-3 py-1.5 rounded-lg bg-white border border-gray-200 text-gray-800 hover:bg-gray-100 transition shadow-xs flex items-center space-x-1">
          <i data-lucide="map" class="w-3.5 h-3.5 text-blue-500"></i>
          <span>2. Route & Tracking</span>
        </a>
        <a href="#car-section-docs" class="px-3 py-1.5 rounded-lg bg-white border border-gray-200 text-gray-800 hover:bg-gray-100 transition shadow-xs flex items-center space-x-1">
          <i data-lucide="file-check" class="w-3.5 h-3.5 text-emerald-500"></i>
          <span>3. Documents & Proofs</span>
        </a>
        <a id="anchor-pill-ferry" href="#car-section-ferry" class="hidden px-3 py-1.5 rounded-lg bg-white border border-gray-200 text-gray-800 hover:bg-gray-100 transition shadow-xs flex items-center space-x-1">
          <i data-lucide="ship" class="w-3.5 h-3.5 text-indigo-500"></i>
          <span>4. Ferry & Sea</span>
        </a>
        <a href="#car-section-chat" class="px-3 py-1.5 rounded-lg bg-white border border-gray-200 text-gray-800 hover:bg-gray-100 transition shadow-xs flex items-center space-x-1">
          <i data-lucide="message-circle" class="w-3.5 h-3.5 text-purple-500"></i>
          <span>5. Communications</span>
        </a>
        <a href="#car-section-actions" class="px-3 py-1.5 rounded-lg bg-amber-50 border border-amber-300 text-amber-900 hover:bg-amber-100 transition shadow-xs flex items-center space-x-1 ml-auto">
          <i data-lucide="sliders" class="w-3.5 h-3.5 text-amber-600"></i>
          <span>Operator Actions</span>
        </a>
      </div>

      <!-- ================= 1. FIRST: DETAILS OF THE DEAL ================= -->
      <section id="car-section-deal" class="space-y-4 pt-2">
        <div class="flex items-center space-x-2">
          <span class="w-6 h-6 rounded-full bg-amber-500 text-black flex items-center justify-center font-bold text-xs">1</span>
          <h2 class="text-base font-black text-gray-900">Commercial Deal & Vehicle Specifications</h2>
        </div>

        <div class="grid grid-cols-3 gap-5">
          <!-- Commercial Deal Terms Card -->
          <div class="bg-white rounded-xl border border-gray-200 p-5 shadow-xs space-y-3">
            <div class="flex items-center justify-between border-b border-gray-100 pb-2">
              <span class="text-[11px] font-bold uppercase text-gray-400">Deal Contract Terms</span>
              <span id="deal-billing-ref" class="font-mono text-[10px] text-gray-600 font-bold bg-gray-100 px-2 py-0.5 rounded">INV-CD-00000</span>
            </div>
            <div class="space-y-2 text-xs">
              <div class="flex justify-between"><span class="text-gray-500">Customer Dealership:</span> <strong id="deal-cust-name" class="text-gray-900">Dealer Name</strong></div>
              <div class="flex justify-between"><span class="text-gray-500">Contact Email:</span> <span id="deal-cust-email" class="font-mono text-gray-700">dealer@auto.de</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Contact Phone:</span> <span id="deal-cust-phone" class="font-mono text-gray-700">+49 89 0000</span></div>
              <div class="flex justify-between pt-1 border-t border-gray-100"><span class="text-gray-500">Contract Value:</span> <strong id="deal-contract-val" class="text-emerald-700 font-mono font-bold">896.78 EUR</strong></div>
              <div class="flex justify-between"><span class="text-gray-500">Driver Fee Payout:</span> <span id="deal-driver-fee" class="font-mono text-gray-800">645.68 EUR</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Gross Margin:</span> <span id="deal-margin" class="font-mono text-gray-700">251.10 EUR</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Payment Terms:</span> <span id="deal-terms" class="text-gray-600">Net 14 Days</span></div>
            </div>
          </div>

          <!-- Vehicle Technical Card -->
          <div class="bg-white rounded-xl border border-gray-200 p-5 shadow-xs space-y-3">
            <div class="flex items-center justify-between border-b border-gray-100 pb-2">
              <span class="text-[11px] font-bold uppercase text-gray-400">Vehicle Dossier</span>
              <span id="deal-veh-plate" class="font-mono text-xs font-bold bg-gray-900 text-white px-2 py-0.5 rounded">DEMO-PLATE</span>
            </div>
            <div class="flex items-center space-x-4">
              <div class="w-24 h-16 rounded-lg bg-gray-100 border border-gray-200 overflow-hidden flex items-center justify-center shrink-0">
                <img id="deal-veh-img" src="" alt="Vehicle" class="w-full h-full object-cover">
              </div>
              <div class="min-w-0">
                <h3 id="deal-veh-title" class="font-black text-sm text-gray-900 truncate">Make Model</h3>
                <span id="deal-veh-year" class="text-xs text-gray-500 block">2022 Petrol Edition</span>
              </div>
            </div>
            <div class="space-y-1.5 text-xs pt-1">
              <div class="flex justify-between"><span class="text-gray-500">VIN:</span> <span id="deal-veh-vin" class="font-mono text-gray-900 text-[11px]">WBA33AY0000000000</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Powertrain:</span> <span id="deal-veh-fuel" class="text-gray-700">Internal Combustion</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Transport Mode:</span> <span id="deal-transport-mode" class="text-gray-800 font-semibold">Direct Road</span></div>
            </div>
          </div>

          <!-- Assigned Driver & Milestone Windows -->
          <div class="bg-white rounded-xl border border-gray-200 p-5 shadow-xs space-y-3">
            <div class="flex items-center justify-between border-b border-gray-100 pb-2">
              <span class="text-[11px] font-bold uppercase text-gray-400">Driver & Schedule SLA</span>
              <span class="px-2 py-0.5 rounded font-bold text-[10px] bg-emerald-100 text-emerald-800">SLA Active</span>
            </div>
            <div class="space-y-2 text-xs">
              <div class="flex justify-between"><span class="text-gray-500">Assigned Driver:</span> <strong id="deal-driver-name" class="text-gray-900">Kasper Kovelund</strong></div>
              <div class="flex justify-between"><span class="text-gray-500">Driver Phone:</span> <span id="deal-driver-phone" class="font-mono text-gray-700">+49 170 00000</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Duty Status:</span> <span class="text-emerald-700 font-semibold">Dispatch Confirmed</span></div>
              <div class="flex justify-between pt-1 border-t border-gray-100"><span class="text-gray-500">Pickup Window:</span> <span id="deal-pickup-window" class="font-mono text-gray-700 text-[11px]">2026-10-19 08:00</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Promised Delivery:</span> <strong id="deal-delivery-deadline" class="font-mono text-amber-800 text-[11px]">2026-10-21 18:00</strong></div>
            </div>
          </div>
        </div>
      </section>

      <!-- ================= 2. SECOND: ROUTE & LIVE TRACKING ================= -->
      <section id="car-section-route" class="space-y-4 pt-4 border-t border-gray-200">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <span class="w-6 h-6 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-xs">2</span>
            <h2 class="text-base font-black text-gray-900">Highway Route Corridor & Live Positioning</h2>
          </div>
          <!-- Legend pill -->
          <div class="flex items-center space-x-3 text-[11px] font-bold text-gray-600 bg-white px-3 py-1.5 rounded-lg border border-gray-200 shadow-xs">
            <span class="flex items-center space-x-1"><span class="w-2.5 h-2.5 rounded-full bg-blue-600"></span><span>Start</span></span>
            <span class="flex items-center space-x-1"><span class="w-4 h-1 bg-blue-600 rounded"></span><span>Route Done</span></span>
            <span class="flex items-center space-x-1"><span class="w-2.5 h-2.5 rounded-full bg-rose-600 pulse-urgent"></span><span>Car Here Now</span></span>
            <span class="flex items-center space-x-1"><span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span><span>Intermediate Stops</span></span>
            <span class="flex items-center space-x-1"><span class="w-4 h-1 border-t-2 border-dashed border-amber-500"></span><span>Remaining Route</span></span>
            <span class="flex items-center space-x-1"><span class="w-2.5 h-2.5 rounded-full bg-emerald-600"></span><span>Destination</span></span>
          </div>
        </div>

        <div class="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-xs flex flex-col">
          <!-- Interactive Leaflet Map Container -->
          <div id="leaflet-map-container" class="w-full h-96 relative z-10 bg-gray-100"></div>

          <!-- Corridor Milestones Bar under Map -->
          <div class="p-4 bg-gray-50 border-t border-gray-200 flex items-center justify-between text-xs">
            <div id="route-checkpoints-strip" class="flex items-center space-x-4 overflow-x-auto custom-scrollbar flex-1 mr-4">
              <!-- Populated dynamically -->
            </div>
            <button onclick="recenterMap()" class="px-3 py-1.5 bg-white hover:bg-gray-100 text-gray-700 border border-gray-300 rounded-md font-bold text-xs flex items-center space-x-1.5 shrink-0 transition">
              <i data-lucide="crosshair" class="w-3.5 h-3.5"></i>
              <span>Recenter</span>
            </button>
          </div>
        </div>
      </section>

      <!-- ================= 3. THIRD: DOCUMENTS AND PROOFS ================= -->
      <section id="car-section-docs" class="space-y-4 pt-4 border-t border-gray-200">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <span class="w-6 h-6 rounded-full bg-emerald-600 text-white flex items-center justify-center font-bold text-xs">3</span>
            <h2 class="text-base font-black text-gray-900">Legal Documents, Inspection Proofs & Receipts</h2>
          </div>
          <span class="text-xs text-gray-500 font-semibold">Includes real PDFs, photos, and digital sign-off records</span>
        </div>

        <div class="space-y-4">
          <!-- 3A. Legal Documents (CMR, Release forms) -->
          <div class="bg-white rounded-xl border border-gray-200 p-5 shadow-xs space-y-3">
            <div class="flex items-center justify-between border-b border-gray-100 pb-2">
              <h3 class="text-xs font-bold uppercase text-gray-700 flex items-center space-x-1.5">
                <i data-lucide="file-text" class="w-3.5 h-3.5 text-blue-600"></i>
                <span>Signed Legal Transport Documents (CMR & Gate Releases)</span>
              </h3>
              <span id="docs-count-badge" class="text-[10px] bg-blue-50 text-blue-800 font-bold px-2 py-0.5 rounded">0 Documents</span>
            </div>
            <div id="docs-verification-grid" class="grid grid-cols-3 gap-3">
              <!-- Populated with View PDF buttons -->
            </div>
          </div>

          <!-- 3B. Handover Proofs & Photo Gallery -->
          <div class="bg-white rounded-xl border border-gray-200 p-5 shadow-xs space-y-3">
            <div class="flex items-center justify-between border-b border-gray-100 pb-2">
              <h3 class="text-xs font-bold uppercase text-gray-700 flex items-center space-x-1.5">
                <i data-lucide="camera" class="w-3.5 h-3.5 text-emerald-600"></i>
                <span>Physical Inspection Photos & Handover Verification</span>
              </h3>
              <span id="gallery-total-badge" class="text-[10px] bg-emerald-50 text-emerald-800 font-bold px-2 py-0.5 rounded">Photos on File</span>
            </div>
            <div id="gallery-grid-container" class="grid grid-cols-4 gap-4">
              <!-- Photo thumbnails with zoom modal -->
            </div>
          </div>

          <!-- 3C. Trip Expenses & Receipts -->
          <div class="bg-white rounded-xl border border-gray-200 p-5 shadow-xs space-y-3">
            <div class="flex items-center justify-between border-b border-gray-100 pb-2">
              <h3 class="text-xs font-bold uppercase text-gray-700 flex items-center space-x-1.5">
                <i data-lucide="receipt" class="w-3.5 h-3.5 text-amber-600"></i>
                <span>Trip Expenses & Fuel/Toll Receipts</span>
              </h3>
              <span id="expenses-count-badge" class="text-[10px] bg-amber-50 text-amber-800 font-bold px-2 py-0.5 rounded">Receipts on File</span>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs border-collapse">
                <thead class="bg-gray-50 text-gray-500 font-bold uppercase text-[10px] border-b border-gray-200">
                  <tr>
                    <th class="p-2.5">Category</th>
                    <th class="p-2.5">Vendor / Payee</th>
                    <th class="p-2.5">Amount</th>
                    <th class="p-2.5">Status</th>
                    <th class="p-2.5 text-right">Proof File</th>
                  </tr>
                </thead>
                <tbody id="dossier-expenses-list" class="divide-y divide-gray-100">
                  <!-- Populated with View Receipt PDF buttons -->
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      <!-- ================= 4. FOURTH: FERRY & MARITIME (CONDITIONAL) ================= -->
      <section id="car-section-ferry" class="hidden space-y-4 pt-4 border-t border-gray-200">
        <div class="flex items-center space-x-2">
          <span class="w-6 h-6 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold text-xs">4</span>
          <h2 class="text-base font-black text-gray-900">Maritime Passage & Ferry Booking (Baltic Sea Corridor)</h2>
        </div>

        <div class="bg-white rounded-xl border border-gray-200 p-6 shadow-xs space-y-5">
          <div class="flex items-center justify-between border-b border-gray-100 pb-3">
            <div>
              <h3 class="text-sm font-bold text-gray-900 flex items-center space-x-2">
                <i data-lucide="anchor" class="w-4 h-4 text-indigo-600"></i>
                <span>Finnlines Baltic RoRo Service: Travemünde to Helsinki Vuosaari</span>
              </h3>
              <p class="text-xs text-gray-500 mt-0.5">Commercial vehicle freight sailing with reserved deck placement</p>
            </div>
            <span class="px-2.5 py-1 rounded bg-indigo-50 text-indigo-800 border border-indigo-200 font-mono text-xs font-bold">29h Baltic Sea Crossing</span>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <h4 class="text-xs font-bold uppercase text-gray-400 mb-2">Confirmed Reservations</h4>
              <div id="travel-booked-list" class="space-y-2"></div>
            </div>
            <div>
              <h4 class="text-xs font-bold uppercase text-gray-400 mb-2">Available Maritime Quotes / Next Departures</h4>
              <div id="travel-options-list" class="space-y-2"></div>
            </div>
          </div>
        </div>
      </section>

      <!-- ================= 5. FIFTH: CHAT & COMMUNICATIONS ================= -->
      <section id="car-section-chat" class="space-y-4 pt-4 border-t border-gray-200">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <span class="w-6 h-6 rounded-full bg-purple-600 text-white flex items-center justify-center font-bold text-xs">5</span>
            <h2 class="text-base font-black text-gray-900">Operational Communication Log</h2>
          </div>
          <span class="text-xs text-gray-500">Live dataset feed from <code class="font-mono">messages.jsonl</code> & driver app</span>
        </div>

        <div class="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-xs flex flex-col h-[420px]">
          <!-- Chat header with counterparty info -->
          <div class="h-11 bg-gray-50 border-b border-gray-200 px-4 flex items-center justify-between shrink-0">
            <div class="flex items-center space-x-2">
              <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
              <strong id="chat-counterparty-name" class="text-xs text-gray-900 font-bold">Driver & Dealer Channel</strong>
            </div>
            <span class="text-[11px] text-gray-400">Strict Human Sign-off Policy</span>
          </div>

          <!-- Chat messages feed -->
          <div id="wa-messages-container" class="flex-1 p-4 overflow-y-auto custom-scrollbar space-y-3 bg-[#FAFBFD]">
            <!-- Dynamically populated bubbles -->
          </div>

          <!-- Operator response box -->
          <div class="p-3 bg-white border-t border-gray-200 flex items-center space-x-2 shrink-0">
            <input type="text" id="wa-input" placeholder="Type verified dispatch instruction to driver or dealer..." class="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-xs text-gray-900 focus:outline-none focus:border-purple-500">
            <button onclick="handleSendDriverMessage()" class="px-4 py-2 bg-gray-900 hover:bg-black text-white font-bold text-xs rounded-lg flex items-center space-x-1.5 transition shadow-xs">
              <i data-lucide="send" class="w-3.5 h-3.5"></i>
              <span>Send Directive</span>
            </button>
          </div>
        </div>
      </section>

      <!-- ================= 6. ADDITIONAL ON-DEMAND: OPERATOR ACTION PANEL ================= -->
      <section id="car-section-actions" class="pt-4 border-t border-gray-200 pb-12">
        <div class="bg-amber-50/90 rounded-xl border-2 border-amber-400 p-5 shadow-xs space-y-3">
          <!-- Collapsible Header Toggle -->
          <div class="flex items-center justify-between cursor-pointer" onclick="toggleActionsAccordion()">
            <div class="flex items-center space-x-2">
              <i data-lucide="sliders" class="w-4 h-4 text-amber-700"></i>
              <h3 class="text-sm font-bold text-amber-950">Operator Action Decisions (<span id="actions-available-count">0</span> Available)</h3>
              <span class="text-[11px] text-amber-800 font-medium">Click to expand / collapse</span>
            </div>
            <div class="flex items-center space-x-3">
              <span class="text-xs text-amber-900 font-mono">Signed as: <strong id="decision-operator-label">OP-042</strong></span>
              <i id="actions-accordion-chevron" data-lucide="chevron-down" class="w-4 h-4 text-amber-800 transition-transform duration-200"></i>
            </div>
          </div>

          <!-- Collapsible Actions Content -->
          <div id="actions-accordion-content" class="pt-2 border-t border-amber-200/80 space-y-3">
            <div id="dynamic-decision-container" class="grid grid-cols-2 gap-3">
              <!-- Populated dynamically with Confirm Action buttons triggering 5s undo -->
            </div>
          </div>
        </div>
      </section>

    </div>
  </div>

  <!-- ================= VIEW 3: SUPPORT INBOX ================= -->
  <div id="view-inbox" class="hidden flex-1 flex flex-col overflow-hidden bg-white">
    <!-- Header -->
    <div class="h-16 bg-white border-b border-gray-200 px-8 flex items-center justify-between shrink-0 shadow-xs select-none">
      <div>
        <h2 class="text-lg font-black text-gray-900 flex items-center space-x-2">
          <i data-lucide="inbox" class="w-5 h-5 text-amber-500"></i>
          <span>Support Communications Inbox</span>
        </h2>
        <p class="text-xs text-gray-500 mt-0.5">Driver queries, expense payout questions, and dealer document requests</p>
      </div>
      <div class="flex items-center space-x-2 text-xs">
        <span class="px-3 py-1 rounded-full bg-amber-100 text-amber-900 font-bold">5 Active Inquiries</span>
        <span class="px-3 py-1 rounded-full bg-rose-100 text-rose-800 font-bold">4 Open Unresolved</span>
      </div>
    </div>

    <!-- Scrollable Content with Helpdesk Guide -->
    <div class="flex-1 overflow-y-auto custom-scrollbar p-8">
      <div class="max-w-4xl mx-auto space-y-4">
        
        <!-- Helpful Explanatory Banner per user question! -->
        <div class="bg-blue-50/90 border border-blue-200 rounded-xl p-4 flex items-start space-x-3 text-xs text-blue-950 shadow-xs mb-4">
          <div class="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center shrink-0 mt-0.5">
            <i data-lucide="help-circle" class="w-4 h-4"></i>
          </div>
          <div class="space-y-1">
            <strong class="font-bold text-sm text-blue-900 block">Why do we have a Support Inbox & What is it for?</strong>
            <p class="text-blue-800 leading-relaxed">
              In freight operations, freelance drivers and dealerships send questions via the driver app or direct email.
              For example, driver Tobias messages asking whether to start his duty at 10:00, or a dealership asks for a signed CMR waybill.
              When an inquiry doesn't belong to a single closed vehicle, it arrives in this Support Inbox so the dispatch operator can triage it, link it to the correct car, and confirm directives safely.
            </p>
          </div>
        </div>

        <!-- Thread List -->
        <div id="support-inbox-threads-list" class="space-y-4">
          <!-- Populated dynamically with rich helpdesk cards -->
        </div>
      </div>
    </div>
  </div>

  <!-- ================= VIEW 4: OPERATIONS AUDIT LOG ================= -->
  <div id="view-history" class="hidden flex-1 flex flex-col overflow-hidden bg-white">
    <div class="h-16 bg-white border-b border-gray-200 px-8 flex items-center justify-between shrink-0 shadow-xs select-none">
      <div>
        <h2 class="text-lg font-black text-gray-900 flex items-center space-x-2">
          <i data-lucide="history" class="w-5 h-5 text-amber-500"></i>
          <span>Global Operations Audit Log</span>
        </h2>
        <p class="text-xs text-gray-500 mt-0.5">Immutable record of every operator action, autonomous proposal, and verified milestone</p>
      </div>
      <div class="flex items-center space-x-2 text-xs">
        <button onclick="exportAuditLog()" class="px-3 py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-800 rounded-lg font-bold flex items-center space-x-1 transition">
          <i data-lucide="download" class="w-3.5 h-3.5"></i>
          <span>Export JSON</span>
        </button>
      </div>
    </div>

    <div class="flex-1 overflow-y-auto custom-scrollbar p-8">
      <div class="max-w-5xl mx-auto border border-gray-200 rounded-xl overflow-hidden bg-white shadow-xs">
        <table class="w-full text-left text-xs border-collapse">
          <thead class="bg-gray-50 text-gray-500 font-bold uppercase text-[11px] border-b border-gray-200">
            <tr>
              <th class="p-3.5 pl-4">Timestamp</th>
              <th class="p-3.5">Order Ref</th>
              <th class="p-3.5">Car</th>
              <th class="p-3.5">Operator</th>
              <th class="p-3.5">Action Executed</th>
              <th class="p-3.5 pr-4">Operational Notes</th>
            </tr>
          </thead>
          <tbody id="global-history-tbody" class="divide-y divide-gray-100"></tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- ================= VIEW 5: FINANCIALS & EARNINGS ================= -->
  <div id="view-finance" class="hidden flex-1 flex flex-col overflow-hidden bg-[#F8F9FA]">
    <div class="h-16 bg-white border-b border-gray-200 px-8 flex items-center justify-between shrink-0 shadow-xs select-none">
      <div>
        <h2 class="text-lg font-black text-gray-900 flex items-center space-x-2">
          <i data-lucide="coins" class="w-5 h-5 text-amber-500"></i>
          <span>Fleet Financials & Trip Expenses</span>
        </h2>
        <p class="text-xs text-gray-500 mt-0.5">Itemized fuel, highway tolls, driver per diems, and gross margins</p>
      </div>
      <span class="px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 font-bold text-xs">Reconciliation Active</span>
    </div>

    <div class="flex-1 overflow-y-auto custom-scrollbar p-8">
      <div class="max-w-6xl mx-auto space-y-6">
        <!-- Top Metrics Grid -->
        <div class="grid grid-cols-4 gap-4">
          <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-xs">
            <span class="text-gray-400 text-xs font-bold uppercase">Total Fleet Revenue</span>
            <div id="fin-total-revenue" class="text-2xl font-black text-gray-900 mt-1 font-mono">EUR 84,320</div>
            <span class="text-[11px] text-emerald-600 font-semibold mt-1 block">100 B2B Deliveries</span>
          </div>
          <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-xs">
            <span class="text-gray-400 text-xs font-bold uppercase">Driver Payouts</span>
            <div id="fin-driver-payouts" class="text-2xl font-black text-gray-900 mt-1 font-mono">EUR 61,450</div>
            <span class="text-[11px] text-gray-500 mt-1 block">Freelance Driver Fees</span>
          </div>
          <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-xs">
            <span class="text-gray-400 text-xs font-bold uppercase">Approved Expenses</span>
            <div id="fin-approved-expenses" class="text-2xl font-black text-amber-600 mt-1 font-mono">EUR 7,842</div>
            <span class="text-[11px] text-gray-500 mt-1 block">Fuel, Tolls & Lodging</span>
          </div>
          <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-xs">
            <span class="text-gray-400 text-xs font-bold uppercase">Net Gross Margin</span>
            <div id="fin-net-margin" class="text-2xl font-black text-emerald-700 mt-1 font-mono">EUR 15,028</div>
            <span class="text-[11px] text-emerald-700 font-semibold mt-1 block">17.8% Operating Margin</span>
          </div>
        </div>

        <!-- Expenses List Table -->
        <div class="bg-white rounded-xl border border-gray-200 shadow-xs overflow-hidden">
          <div class="p-4 border-b border-gray-200 font-bold text-xs uppercase text-gray-700">
            Itemized Expense Receipts & Digital Claims
          </div>
          <table class="w-full text-left text-xs border-collapse">
            <thead class="bg-gray-50 text-gray-500 font-bold uppercase text-[10px] border-b border-gray-200">
              <tr>
                <th class="p-3.5 pl-4">Category</th>
                <th class="p-3.5">Vendor</th>
                <th class="p-3.5">Order</th>
                <th class="p-3.5">Amount</th>
                <th class="p-3.5">Status</th>
                <th class="p-3.5 pr-4 text-right">Proof File</th>
              </tr>
            </thead>
            <tbody id="financials-expenses-tbody" class="divide-y divide-gray-100"></tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <!-- ================= SLIDE-OVER AI ASSISTANT SIDEBAR ================= -->
  <div id="ai-sidebar-backdrop" onclick="closeAiSidebar()" class="hidden fixed inset-0 bg-black/40 backdrop-blur-xs z-40 transition-opacity"></div>
  
  <aside id="ai-sidebar" class="fixed top-0 right-0 h-full w-[440px] bg-white shadow-2xl border-l border-gray-200 z-50 flex flex-col transform translate-x-full transition-transform duration-300 ease-in-out">
    <!-- Header with Info Button inside per user request! -->
    <div class="p-4 bg-[#121417] text-white flex items-center justify-between border-b border-gray-800 shrink-0">
      <div class="flex items-center space-x-2.5">
        <div class="w-8 h-8 rounded-lg bg-purple-600 flex items-center justify-center text-white">
          <i data-lucide="bot" class="w-4 h-4"></i>
        </div>
        <div>
          <h3 class="text-sm font-bold text-white leading-tight">AI Operations Assistant</h3>
          <span class="text-[10px] text-purple-300 font-medium">Multi-Model Logistics Intelligence</span>
        </div>
      </div>
      <div class="flex items-center space-x-2">
        <!-- Info & Credit Button (Inside AI Assistant per user request) -->
        <button onclick="toggleInfoModal()" title="System Information & Credits" class="px-2.5 py-1 rounded-md bg-gray-800/90 hover:bg-gray-700 text-amber-400 border border-gray-700 flex items-center space-x-1 text-[11px] font-bold transition">
          <i data-lucide="info" class="w-3.5 h-3.5"></i>
          <span>$20.00 Credits</span>
        </button>
        <button onclick="toggleAiSidebar()" class="text-gray-400 hover:text-white p-1 rounded-lg transition">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>
    </div>

    <!-- AI Controls & Model Selector -->
    <div class="p-3 bg-gray-50 border-b border-gray-200 space-y-2.5 shrink-0 text-xs">
      <!-- AI Model Dropdown (OpenRouter Multi-Model) -->
      <div class="flex items-center justify-between">
        <label class="text-[11px] font-bold text-gray-500 uppercase">AI Model:</label>
        <select id="ai-model-select" class="bg-white border border-gray-300 rounded-md px-2 py-1 text-xs font-semibold text-gray-800 focus:outline-none focus:border-purple-500">
          <option value="openai/gpt-4o-mini" selected>OpenAI GPT-4o Mini</option>
          <option value="google/gemini-2.5-flash">Google Gemini 2.5 Flash</option>
          <option value="deepseek/deepseek-chat">DeepSeek V3</option>
          <option value="anthropic/claude-3.5-sonnet">Anthropic Claude Sonnet</option>
        </select>
      </div>

      <!-- Scope Switcher: Fleet Overview vs Single Car -->
      <div class="flex bg-gray-200/80 p-0.5 rounded-lg text-xs font-bold">
        <button id="ai-scope-fleet" onclick="setAiScope('fleet')" class="flex-1 py-1 rounded-md bg-white text-gray-900 shadow-xs transition">
          Fleet Overview (100 Cars)
        </button>
        <button id="ai-scope-car" onclick="setAiScope('car')" class="flex-1 py-1 rounded-md text-gray-600 hover:text-black transition">
          Car Focus (<span id="ai-active-car-pill">Select Car</span>)
        </button>
      </div>
    </div>

    <!-- Active Car Context Card (When in car scope) -->
    <div id="ai-car-context-box" class="hidden px-4 py-2.5 bg-purple-50 border-b border-purple-100 flex items-center justify-between text-xs text-purple-950">
      <div class="flex items-center space-x-2">
        <i data-lucide="car" class="w-3.5 h-3.5 text-purple-600"></i>
        <span>Focus Car: <strong id="ai-context-car-name">BMW 3 Series</strong></span>
      </div>
      <span id="ai-context-car-plate" class="font-mono text-[10px] bg-white px-2 py-0.5 rounded border border-purple-200 font-bold">DEMO-PLATE</span>
    </div>

    <!-- Messages Chat Feed -->
    <div id="ai-chat-messages" class="flex-1 p-4 overflow-y-auto custom-scrollbar space-y-3 bg-[#FAFBFD] text-xs">
      <div class="p-3 bg-purple-100/60 rounded-xl text-purple-950 space-y-1">
        <strong class="font-bold flex items-center space-x-1.5">
          <i data-lucide="sparkles" class="w-3.5 h-3.5 text-purple-600"></i>
          <span>Welcome Operator OP-042</span>
        </strong>
        <p class="leading-relaxed text-[11px]">
          I can analyze fleet delays, suggest optimal driver assignments, audit CMR paperwork, and verify roadside assistance plans.
          Ask me any operational question or run the autonomous resolution dispatcher below.
        </p>
      </div>
    </div>

    <!-- Autonomous Dispatcher Action Trigger -->
    <div class="p-3 bg-amber-50/80 border-t border-amber-200 flex items-center justify-between text-xs">
      <div>
        <strong class="text-amber-950 block text-[11px]">Autonomous Resolution Agent</strong>
        <span class="text-[10px] text-amber-700">Triage 22 bottleneck orders instantly</span>
      </div>
      <button onclick="runSentinelAgent()" class="px-3 py-1.5 bg-amber-500 hover:bg-amber-600 text-black font-bold text-xs rounded-lg flex items-center space-x-1 transition shadow-xs">
        <i data-lucide="play" class="w-3.5 h-3.5 fill-current"></i>
        <span>Run Dispatcher</span>
      </button>
    </div>

    <!-- AI Input Box -->
    <div class="p-3 bg-white border-t border-gray-200 flex items-center space-x-2 shrink-0">
      <input type="text" id="ai-input" onkeydown="if(event.key==='Enter') handleAiSidebarSubmit()" placeholder="Ask AI about fleet bottlenecks, drivers, CMR docs..." class="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-xs text-gray-900 focus:outline-none focus:border-purple-500">
      <button onclick="handleAiSidebarSubmit()" class="px-3 py-2 bg-purple-600 hover:bg-purple-700 text-white font-bold text-xs rounded-lg transition shadow-xs">
        <i data-lucide="send" class="w-3.5 h-3.5"></i>
      </button>
    </div>
  </aside>

  <!-- ================= UNIVERSAL DOCUMENT & PROOF MODAL (Fixes Image 1 broken PDF!) ================= -->
  <div id="universal-file-modal" class="hidden fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex flex-col items-center justify-center p-4">
    <div class="w-full max-w-4xl bg-white rounded-xl shadow-2xl overflow-hidden flex flex-col border border-gray-300">
      <!-- Modal Header -->
      <div class="h-12 bg-gray-900 text-white px-5 flex items-center justify-between shrink-0 select-none">
        <div class="flex items-center space-x-2">
          <i data-lucide="file-text" class="w-4 h-4 text-amber-400"></i>
          <span id="file-modal-title" class="font-bold text-xs uppercase tracking-wide text-gray-200">Transport Document</span>
        </div>
        <div class="flex items-center space-x-2">
          <a id="file-modal-newtab-btn" href="#" target="_blank" class="px-2.5 py-1 bg-gray-800 hover:bg-gray-700 text-gray-200 rounded text-[11px] font-semibold flex items-center space-x-1 transition">
            <i data-lucide="external-link" class="w-3.5 h-3.5"></i>
            <span>Open in Tab</span>
          </a>
          <button onclick="closeUniversalFileModal()" class="text-gray-400 hover:text-white p-1 rounded-lg transition">
            <i data-lucide="x" class="w-4 h-4"></i>
          </button>
        </div>
      </div>

      <!-- Modal Content Body -->
      <div class="p-4 bg-gray-100 flex items-center justify-center min-h-[460px] max-h-[78vh] overflow-hidden">
        <!-- PDF Viewer Iframe -->
        <iframe id="file-modal-iframe" src="" class="w-full h-[72vh] rounded-lg border border-gray-300 bg-white hidden"></iframe>
        
        <!-- Photo / Image Viewer -->
        <img id="file-modal-img" src="" alt="Inspection Proof" class="max-w-full max-h-[72vh] object-contain rounded-lg shadow-md hidden">
        
        <!-- Electronic Digital Certificate (when record has no scanned paper) -->
        <div id="file-modal-digital-cert" class="w-full max-w-md bg-white rounded-xl p-6 shadow-md border border-gray-200 space-y-4 text-xs text-gray-800 hidden">
          <div class="flex items-center space-x-3 pb-3 border-b border-gray-100">
            <div class="w-10 h-10 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center shrink-0">
              <i data-lucide="shield-check" class="w-5 h-5"></i>
            </div>
            <div>
              <strong class="text-sm font-bold block text-gray-900" id="cert-title">Certified Digital Record</strong>
              <span class="text-emerald-700 font-semibold text-[11px]">e-CMR / Digital Sign-off Verified</span>
            </div>
          </div>
          <div class="space-y-2 font-mono text-[11px] bg-gray-50 p-3 rounded-lg border border-gray-100">
            <div><span class="text-gray-400 uppercase">Record ID:</span> <strong id="cert-id" class="text-gray-900">-</strong></div>
            <div><span class="text-gray-400 uppercase">Document Kind:</span> <strong id="cert-kind" class="text-gray-900">-</strong></div>
            <div><span class="text-gray-400 uppercase">Status:</span> <span id="cert-status" class="px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold">SIGNED</span></div>
            <div><span class="text-gray-400 uppercase">Verification Checksum:</span> <span class="text-gray-500 break-all text-[10px]" id="cert-hash">SHA256: 8fbc2910...verified</span></div>
          </div>
          <p class="text-gray-500 text-[11px] leading-relaxed">
            This digital milestone is recorded on the tamper-proof ledger. Physical scanned paper is not required for this operational stage.
          </p>
        </div>
      </div>
    </div>
  </div>

  <!-- Fallback Photo Modal for backward compatibility -->
  <div id="photo-modal" class="hidden">
    <img id="photo-modal-img" src="" alt="Proof">
  </div>

  <!-- ================= SYSTEM INFO & AI CREDITS MODAL ================= -->
  <div id="info-modal" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl border border-gray-200 space-y-4">
      <div class="flex items-center justify-between pb-3 border-b border-gray-100">
        <div class="flex items-center space-x-2">
          <i data-lucide="info" class="w-5 h-5 text-amber-500"></i>
          <h3 class="font-bold text-base text-gray-900">System Information & AI Engine</h3>
        </div>
        <button onclick="toggleInfoModal()" class="text-gray-400 hover:text-black">
          <i data-lucide="x" class="w-4 h-4"></i>
        </button>
      </div>

      <div class="space-y-3 text-xs">
        <div class="flex justify-between items-center py-1 border-b border-gray-100">
          <span class="text-gray-500">OpenRouter API:</span>
          <span class="font-semibold text-emerald-700 flex items-center space-x-1">
            <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
            <span>Connected</span>
          </span>
        </div>
        <div class="flex justify-between items-center py-1 border-b border-gray-100">
          <span class="text-gray-500">Available Credits:</span>
          <strong class="font-mono text-gray-900 text-sm">$20.00 USD</strong>
        </div>
        <p class="text-[11px] text-gray-500 leading-snug bg-amber-50 p-2.5 rounded-lg border border-amber-200">
          <strong>Credit usage info:</strong> Queries to OpenAI GPT-4o Mini, Google Gemini 2.5, DeepSeek V3, and Claude Sonnet consume fractions of a cent per prompt (~$0.0002 / 1k tokens) from your $20.00 balance.
        </p>
        <div class="flex justify-between items-center py-1 border-b border-gray-100">
          <span class="text-gray-500">Supported AI Models:</span>
          <span class="font-medium text-gray-800 text-right">GPT-4o Mini, Gemini 2.5, DeepSeek V3, Claude Sonnet</span>
        </div>
        <div class="flex justify-between items-center py-1 border-b border-gray-100">
          <span class="text-gray-500">Dataset Coverage:</span>
          <span class="font-mono text-gray-700">100 Orders, 37 Collections, 58 Attachments</span>
        </div>
        <div class="flex justify-between items-center py-1">
          <span class="text-gray-500">Routing Engine:</span>
          <span class="font-medium text-gray-700">OSRM Trans-European Highways</span>
        </div>
      </div>

      <button onclick="toggleInfoModal()" class="w-full py-2 bg-gray-900 hover:bg-black text-white rounded-lg text-xs font-bold transition">
        Close
      </button>
    </div>
  </div>

  <!-- OPERATOR ID EDIT MODAL -->
  <div id="operator-modal" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl max-w-sm w-full p-6 shadow-2xl border border-gray-200 space-y-4">
      <h3 class="font-bold text-sm text-gray-900">Operator Sign-off Credentials</h3>
      <input type="text" id="operator-modal-input" placeholder="e.g. OP-042" class="w-full border border-gray-300 rounded-lg p-2.5 text-xs text-gray-900 font-mono focus:outline-none focus:border-amber-500">
      <div class="flex items-center space-x-2 pt-2">
        <button onclick="closeOperatorModal()" class="flex-1 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg text-xs font-bold transition">Cancel</button>
        <button onclick="saveOperatorId()" class="flex-1 py-2 bg-amber-500 hover:bg-amber-600 text-black rounded-lg text-xs font-bold transition">Save Operator</button>
      </div>
    </div>
  </div>

  <!-- APPLICATION JAVASCRIPT -->
  <script>
    // State variables
    let ordersList = [];
    let selectedOrderId = null;
    let selectedOrderData = null;
    let currentGlobalView = 'home';
    let currentStatusFilter = 'all'; // Starts with All Cars per user request
    let currentProblemFilter = 'all';
    let currentSort = 'newest';
    let searchQuery = '';
    let activeOperator = localStorage.getItem('bahn_operator_id') || 'OP-042';

    // Map instances
    let leafletMap = null;
    let mapMarkers = [];
    let mapRouteLine = [];

    // Pending 5s Undo Action state
    let pendingActionTimer = null;
    let pendingActionCountdown = 5;
    let pendingActionPayload = null;

    // AI sidebar state
    let aiChatHistory = [];
    let aiCurrentScope = 'fleet'; // 'fleet' or 'car'

    document.addEventListener('DOMContentLoaded', () => {
      init();
    });

    async function init() {
      lucide.createIcons();
      document.getElementById('operator-display').innerText = activeOperator;
      document.getElementById('decision-operator-label').innerText = activeOperator;
      await refreshData();
    }

    function showToast(title, body) {
      const container = document.getElementById('toast-container');
      const toast = document.createElement('div');
      toast.className = 'bg-gray-900 text-white px-4 py-3 rounded-xl shadow-xl border border-gray-700 text-xs flex items-start space-x-2.5 max-w-sm pointer-events-auto transform transition-all duration-300 ease-out translate-x-4 opacity-0';
      toast.innerHTML = `
        <div class="w-2 h-2 rounded-full bg-amber-400 mt-1 shrink-0"></div>
        <div class="flex-1">
          <strong class="block font-bold">${escapeHtml(title)}</strong>
          <span class="text-gray-300 leading-snug">${escapeHtml(body)}</span>
        </div>
      `;
      container.appendChild(toast);
      setTimeout(() => toast.classList.remove('translate-x-4', 'opacity-0'), 10);
      setTimeout(() => {
        toast.classList.add('opacity-0', 'translate-x-4');
        setTimeout(() => toast.remove(), 300);
      }, 4000);
    }

    function toggleInfoModal() {
      document.getElementById('info-modal').classList.toggle('hidden');
      lucide.createIcons();
    }

    function goToFleetView() {
      if (selectedOrderId) {
        switchGlobalView('detail');
      } else {
        switchGlobalView('home');
      }
    }

    function goBackToFleetTable() {
      selectedOrderId = null;
      document.getElementById('nav-fleet-label').innerText = 'Fleet Overview';
      switchGlobalView('home');
    }

    function switchGlobalView(view) {
      currentGlobalView = view;
      const vHome = document.getElementById('view-home');
      const vDetail = document.getElementById('view-car-detail');
      const vInbox = document.getElementById('view-inbox');
      const vHist = document.getElementById('view-history');
      const vFin = document.getElementById('view-finance');

      const btnFleet = document.getElementById('nav-btn-fleet');
      const btnInbox = document.getElementById('nav-btn-inbox');
      const btnHist = document.getElementById('nav-btn-history');
      const btnFin = document.getElementById('nav-btn-finance');

      const activeClass = 'px-3 py-1.5 rounded-md font-semibold bg-amber-500 text-black flex items-center space-x-1.5 transition';
      const inactiveClass = 'px-3 py-1.5 rounded-md font-medium text-gray-300 hover:text-white flex items-center space-x-1.5 transition';

      btnFleet.className = (view === 'home' || view === 'detail') ? activeClass : inactiveClass;
      btnInbox.className = view === 'inbox' ? activeClass : inactiveClass;
      btnHist.className = view === 'history' ? activeClass : inactiveClass;
      btnFin.className = view === 'finance' ? activeClass : inactiveClass;

      vHome.classList.toggle('hidden', view !== 'home');
      vDetail.classList.toggle('hidden', view !== 'detail');
      vInbox.classList.toggle('hidden', view !== 'inbox');
      vHist.classList.toggle('hidden', view !== 'history');
      vFin.classList.toggle('hidden', view !== 'finance');

      if (view === 'inbox') loadSupportInbox();
      if (view === 'history') loadGlobalHistory();
      if (view === 'finance') loadFinancials();
      lucide.createIcons();
    }

    async function refreshData() {
      try {
        const statsRes = await fetch('/api/stats');
        const stats = await statsRes.json();
        
        document.getElementById('count-all').innerText = stats.total_orders;
        document.getElementById('count-ok').innerText = stats.on_track_count;
        document.getElementById('count-not-ok').innerText = stats.needs_human_count;
        document.getElementById('nav-inbox-badge').innerText = stats.open_inbox_count;

        await loadFleetOrders();
      } catch (e) {
        console.error('Error refreshing stats:', e);
      }
    }

    function setStatusFilter(status) {
      currentStatusFilter = status;
      
      const btnAll = document.getElementById('btn-status-all');
      const btnOk = document.getElementById('btn-status-ok');
      const btnNotOk = document.getElementById('btn-status-not-ok');

      btnAll.className = status === 'all' ? 'px-3.5 py-1.5 rounded-md bg-white text-black font-bold shadow-xs' : 'px-3.5 py-1.5 rounded-md text-gray-600 hover:text-black transition';
      btnOk.className = status === 'ok' ? 'px-3.5 py-1.5 rounded-md bg-emerald-600 text-white font-bold shadow-xs flex items-center space-x-1' : 'px-3.5 py-1.5 rounded-md text-emerald-800 hover:bg-white transition flex items-center space-x-1';
      btnNotOk.className = status === 'not_ok' ? 'px-3.5 py-1.5 rounded-md bg-rose-600 text-white font-bold shadow-xs flex items-center space-x-1.5' : 'px-3.5 py-1.5 rounded-md text-rose-700 hover:bg-white transition flex items-center space-x-1.5';

      loadFleetOrders();
    }

    function onProblemSelectChange() {
      currentProblemFilter = document.getElementById('problem-select').value;
      loadFleetOrders();
    }

    function onSortChange() {
      currentSort = document.getElementById('sort-select').value;
      loadFleetOrders();
    }

    function onSearchInput() {
      searchQuery = document.getElementById('fleet-search').value;
      loadFleetOrders();
    }

    async function loadFleetOrders() {
      const tbody = document.getElementById('fleet-table-tbody');
      try {
        const res = await fetch(`/api/orders?status_filter=${currentStatusFilter}&problem_category=${currentProblemFilter}&sort_by=${currentSort}&query=${encodeURIComponent(searchQuery)}`);
        ordersList = await res.json();

        if (ordersList.length === 0) {
          tbody.innerHTML = `<tr><td colspan="7" class="p-8 text-center text-gray-400">No cars found matching filters</td></tr>`;
          return;
        }

        let html = '';
        ordersList.forEach(o => {
          const v = o.vehicle;
          const drv = o.driver;
          const att = o.attention;
          
          let conditionHtml = '';
          const shortTitle = att.short_title || att.headline;
          
          if (att.severity === 'danger') {
            conditionHtml = `
              <span class="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-rose-100 text-rose-800 border border-rose-300">
                <span class="w-2 h-2 rounded-full bg-rose-600 pulse-urgent"></span>
                <span class="truncate">${escapeHtml(shortTitle)}</span>
              </span>
            `;
          } else if (att.severity === 'warning') {
            conditionHtml = `
              <span class="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-900 border border-amber-300">
                <span class="w-2 h-2 rounded-full bg-amber-500"></span>
                <span class="truncate">${escapeHtml(shortTitle)}</span>
              </span>
            `;
          } else {
            conditionHtml = `
              <span class="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200">
                <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                <span>On Track</span>
              </span>
            `;
          }

          html += `
            <tr onclick="openCarDetail('${o.id}')" class="hover:bg-amber-50/50 cursor-pointer transition">
              <td class="p-3.5 pl-5 font-mono font-bold text-gray-900 truncate">${o.reference}</td>
              <td class="p-3.5 truncate">
                <div class="flex items-center space-x-3">
                  <div class="w-10 h-7 rounded bg-gray-100 border border-gray-200 overflow-hidden shrink-0 flex items-center justify-center">
                    <img src="${v && v.image_url ? v.image_url : '/static/bahn-logo.png'}" alt="Car" class="w-full h-full object-cover">
                  </div>
                  <div class="min-w-0">
                    <strong class="text-gray-900 font-bold block truncate">${v ? `${v.make} ${v.model}` : 'Unassigned'}</strong>
                    <span class="text-[11px] text-gray-500 font-mono">${v ? v.registration : 'Pending'}</span>
                  </div>
                </div>
              </td>
              <td class="p-3.5 text-gray-700 font-medium truncate">${escapeHtml(o.route_text)}</td>
              <td class="p-3.5 text-gray-600 truncate">${escapeHtml(o.current_location)}</td>
              <td class="p-3.5 text-gray-800 font-medium truncate">${drv ? escapeHtml(drv.display_name) : '<span class="text-gray-400 italic">Unassigned</span>'}</td>
              <td class="p-3.5 truncate">${conditionHtml}</td>
              <td class="p-3.5 pr-5 text-right">
                <button onclick="event.stopPropagation(); openCarDetail('${o.id}')" class="px-2.5 py-1 bg-gray-100 hover:bg-gray-200 text-gray-800 rounded font-bold text-xs transition">
                  View
                </button>
              </td>
            </tr>
          `;
        });
        tbody.innerHTML = html;
        lucide.createIcons();
      } catch (e) {
        console.error('Error loading orders:', e);
        tbody.innerHTML = `<tr><td colspan="7" class="p-8 text-center text-rose-500">Failed loading orders.</td></tr>`;
      }
    }

    async function openCarDetail(orderId) {
      selectedOrderId = orderId;
      document.getElementById('nav-fleet-label').innerText = `Car: ${orderId}`;
      switchGlobalView('detail');

      const res = await fetch(`/api/orders/${orderId}`);
      selectedOrderData = await res.json();
      const data = selectedOrderData;

      const o = data.order;
      const v = data.vehicle;
      const cust = data.customer;
      const drv = data.driver;
      const att = data.attention;
      const addr = data.addresses;
      const deal = data.deal || {};

      // Nav breadcrumb
      document.getElementById('detail-nav-id').innerText = o.reference;
      document.getElementById('detail-nav-car').innerText = v ? `${v.make} ${v.model}` : 'Car Detail';

      // Pipeline stepper
      renderPipelineStepper(o.status, o.display_lane);

      // Situation Alert Banner (Full description shown in detail view per user request!)
      const alertBox = document.getElementById('detail-alert-box');
      if (att.needs_human) {
        alertBox.classList.remove('hidden');
        document.getElementById('detail-alert-title').innerText = `Action Required: ${att.short_title || att.headline}`;
        document.getElementById('detail-alert-desc').innerText = att.full_description || att.headline;
      } else {
        alertBox.classList.add('hidden');
      }

      // ================= 1. POPULATE DEAL DETAILS =================
      document.getElementById('deal-billing-ref').innerText = deal.billing_reference || `INV-${o.reference}`;
      document.getElementById('deal-cust-name').innerText = deal.customer_name || (cust ? cust.name : 'Dealership Network');
      document.getElementById('deal-cust-email').innerText = deal.customer_email || 'dispatch@auto-dealer.com';
      document.getElementById('deal-cust-phone').innerText = deal.customer_phone || '+49 89 2145 009';
      document.getElementById('deal-contract-val').innerText = `${deal.contract_value_eur || '896.78'} EUR`;
      document.getElementById('deal-driver-fee').innerText = `${deal.driver_payout_eur || '645.68'} EUR`;
      document.getElementById('deal-margin').innerText = `${deal.gross_margin_eur || '251.10'} EUR`;
      document.getElementById('deal-terms').innerText = deal.payment_terms || 'Net 14 Days Fleet Transfer';

      document.getElementById('deal-veh-plate').innerText = v ? v.registration : 'DEMO-PLATE';
      document.getElementById('deal-veh-title').innerText = v ? `${v.make} ${v.model}` : 'Master Vehicle';
      document.getElementById('deal-veh-year').innerText = v ? `${v.model_year} Edition` : '2022 Fleet Edition';
      document.getElementById('deal-veh-vin').innerText = v ? v.vin : 'WBA33AY0000000000';
      document.getElementById('deal-veh-fuel').innerText = v ? (v.fuel_type || 'Internal Combustion') : 'Petrol';
      document.getElementById('deal-transport-mode').innerText = deal.transport_mode || 'Direct Road Transport';
      const dealVehImg = document.getElementById('deal-veh-img');
      dealVehImg.src = (v && v.image_url) ? v.image_url : '/static/bahn-logo.png';

      document.getElementById('deal-driver-name').innerText = drv ? drv.display_name : 'Kasper Kovelund';
      document.getElementById('deal-driver-phone').innerText = drv ? (drv.phone || '+49 170 00000') : '+49 170 00000';
      document.getElementById('deal-pickup-window').innerText = deal.pickup_window || '2026-10-19 08:00 - 14:00';
      document.getElementById('deal-delivery-deadline').innerText = deal.delivery_deadline || '2026-10-21 18:00';

      // ================= 2. POPULATE ROUTE & MAP =================
      renderMapAndWaypoints(addr.coordinates);

      // ================= 3. POPULATE DOCUMENTS & PROOFS =================
      populateDocumentsAndProofs(data);

      // ================= 4. POPULATE FERRY & SEA (CONDITIONAL) =================
      const hasFerry = addr.coordinates.has_ferry;
      const ferrySec = document.getElementById('car-section-ferry');
      const ferryPill = document.getElementById('anchor-pill-ferry');
      if (hasFerry) {
        ferrySec.classList.remove('hidden');
        ferryPill.classList.remove('hidden');
        populateFerryData(data);
      } else {
        ferrySec.classList.add('hidden');
        ferryPill.classList.add('hidden');
      }

      // ================= 5. POPULATE CHAT =================
      populateChatFeed(data);

      // ================= 6. POPULATE OPERATOR ACTIONS =================
      populateOperatorActions(data);

      lucide.createIcons();
    }

    function renderPipelineStepper(status, lane) {
      const stepper = document.getElementById('pipeline-stepper');
      document.getElementById('pipeline-current-status').innerText = status;

      const steps = [
        { key: 'INTAKE', label: '1. Order Intake' },
        { key: 'ASSIGNED', label: '2. Driver Assigned' },
        { key: 'WAITING_PICKUP', label: '3. Waiting Pickup' },
        { key: 'IN_TRANSIT', label: '4. In Transit' },
        { key: 'DELIVERED', label: '5. Delivered' }
      ];

      let activeIndex = 0;
      if (status === 'ASSIGNED' || lane === 'DISPATCHED') activeIndex = 1;
      else if (status === 'READY_FOR_PICKUP' || status === 'WAITING_FOR_PICKUP') activeIndex = 2;
      else if (status === 'IN_TRANSIT' || status === 'MOVING') activeIndex = 3;
      else if (status === 'DELIVERED' || status === 'COMPLETED') activeIndex = 4;
      else if (status === 'CANCELLED') activeIndex = -1;

      let html = '';
      steps.forEach((step, idx) => {
        let stepClass = 'bg-gray-100 text-gray-400 border-gray-200';
        let barClass = 'bg-gray-200';
        
        if (activeIndex === -1) {
          stepClass = 'bg-rose-50 text-rose-800 border-rose-300 font-bold';
          barClass = 'bg-rose-300';
        } else if (idx < activeIndex) {
          stepClass = 'bg-emerald-50 text-emerald-800 border-emerald-300 font-bold';
          barClass = 'bg-emerald-500';
        } else if (idx === activeIndex) {
          stepClass = 'bg-amber-400 text-black border-amber-500 font-black shadow-xs';
          barClass = 'bg-amber-400';
        }

        html += `
          <div class="flex flex-col items-center">
            <div class="w-full h-1.5 rounded-full ${barClass} mb-1.5"></div>
            <div class="w-full text-center py-1 px-1.5 rounded border text-[11px] truncate ${stepClass}">
              ${step.label}
            </div>
          </div>
        `;
      });
      stepper.innerHTML = html;
    }

    function renderMapAndWaypoints(coords) {
      // 1. Populate milestones summary strip under map
      const strip = document.getElementById('route-checkpoints-strip');
      let sHtml = `
        <span class="inline-flex items-center space-x-1.5 px-3 py-1 bg-white rounded-lg border border-gray-200 font-bold text-gray-800 shrink-0">
          <span class="w-2 h-2 rounded-full bg-blue-600"></span>
          <span>Start: ${coords.pickup_city}</span>
        </span>
        <i data-lucide="arrow-right" class="w-3.5 h-3.5 text-gray-400 shrink-0"></i>
      `;
      if (coords.intermediate_stops && coords.intermediate_stops.length > 0) {
        coords.intermediate_stops.forEach(stop => {
          sHtml += `
            <span class="inline-flex items-center space-x-1.5 px-3 py-1 bg-amber-50 rounded-lg border border-amber-200 font-bold text-amber-900 shrink-0">
              <span class="w-2 h-2 rounded-full bg-amber-500"></span>
              <span>Stop: ${stop.name}</span>
            </span>
            <i data-lucide="arrow-right" class="w-3.5 h-3.5 text-gray-400 shrink-0"></i>
          `;
        });
      }
      sHtml += `
        <span class="inline-flex items-center space-x-1.5 px-3 py-1 bg-white rounded-lg border border-gray-200 font-bold text-gray-800 shrink-0">
          <span class="w-2 h-2 rounded-full bg-emerald-600"></span>
          <span>Destination: ${coords.delivery_city}</span>
        </span>
      `;
      strip.innerHTML = sHtml;

      // 2. Leaflet Map setup
      setTimeout(() => {
        if (!leafletMap) {
          leafletMap = L.map('leaflet-map-container').setView(coords.current_estimated, 5);
          L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 18,
            attribution: 'OpenStreetMap'
          }).addTo(leafletMap);
        }

        mapMarkers.forEach(m => leafletMap.removeLayer(m));
        mapMarkers = [];
        if (mapRouteLine) {
          if (Array.isArray(mapRouteLine)) {
            mapRouteLine.forEach(l => leafletMap.removeLayer(l));
          } else {
            leafletMap.removeLayer(mapRouteLine);
          }
        }
        mapRouteLine = [];

        const roadGeom = coords.road_geometry && coords.road_geometry.length > 1 ? coords.road_geometry : [coords.pickup, coords.delivery];
        const drivenGeom = coords.driven_geometry && coords.driven_geometry.length > 1 ? coords.driven_geometry : [];
        const remainingGeom = coords.remaining_geometry && coords.remaining_geometry.length > 1 ? coords.remaining_geometry : [];

        // START / ORIGIN MARKER
        const startMarker = L.circleMarker(coords.pickup, { radius: 9, color: '#1D4ED8', fillColor: '#3B82F6', fillOpacity: 1, weight: 3 })
          .addTo(leafletMap)
          .bindTooltip(`<b>Start / Origin:</b> ${coords.pickup_city} Dealership<br><span style="color:#60a5fa;">Vehicle Departure Point</span>`, { sticky: true, className: 'custom-hover-tip' });
        mapMarkers.push(startMarker);

        // ROUTE DONE (SOLID BLUE)
        if (drivenGeom.length > 1) {
          const drivenLine = L.polyline(drivenGeom, { color: '#2563EB', weight: 5, opacity: 0.95 })
            .addTo(leafletMap)
            .bindTooltip(`<b>Route Completed (Driven)</b><br>Origin -> Current Position`, { sticky: true, className: 'custom-hover-tip' });
          mapRouteLine.push(drivenLine);
        }

        // REMAINING ROUTE (DASHED ORANGE)
        if (remainingGeom.length > 1) {
          const remLine = L.polyline(remainingGeom, { color: '#F59E0B', weight: 4, dashArray: '6, 8', opacity: 0.9 })
            .addTo(leafletMap)
            .bindTooltip(`<b>Remaining Highway Corridor</b><br>Current Position -> Destination`, { sticky: true, className: 'custom-hover-tip' });
          mapRouteLine.push(remLine);
        } else if (drivenGeom.length === 0) {
          // Entire route planned (pre-transit)
          const planLine = L.polyline(roadGeom, { color: '#F59E0B', weight: 4, dashArray: '6, 8', opacity: 0.9 })
            .addTo(leafletMap)
            .bindTooltip(`<b>Planned Highway Route:</b> ${coords.pickup_city} -> ${coords.delivery_city}`, { sticky: true, className: 'custom-hover-tip' });
          mapRouteLine.push(planLine);
        }

        // ALL INTERMEDIATE STOPS
        if (coords.intermediate_stops && coords.intermediate_stops.length > 0) {
          coords.intermediate_stops.forEach(st => {
            const stMarker = L.circleMarker(st.coords, { radius: 7, color: '#D97706', fillColor: '#FDE68A', fillOpacity: 1, weight: 2.5 })
              .addTo(leafletMap)
              .bindTooltip(`<b>Intermediate Stop:</b> ${st.name}<br><span style="color:#d97706; font-weight:bold;">${st.role}</span><br>${st.notes}`, { sticky: true, className: 'custom-hover-tip' });
            mapMarkers.push(stMarker);
          });
        }

        // WHERE THE CAR IS NOW (Pulsing vehicle pin!)
        const carHtml = `
          <div class="relative flex items-center justify-center -top-3 -left-3">
            <span class="animate-ping absolute inline-flex h-8 w-8 rounded-full bg-rose-400 opacity-75"></span>
            <div class="relative w-7 h-7 rounded-full bg-rose-600 text-white flex items-center justify-center shadow-lg border-2 border-white">
              <svg class="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24"><path d="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.21.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.5 16c-.83 0-1.5-.67-1.5-1.5S5.67 13 6.5 13s1.5.67 1.5 1.5S7.33 16 6.5 16zm11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zM5 11l1.5-4.5h11L19 11H5z"/></svg>
            </div>
          </div>
        `;
        const carIcon = L.divIcon({ className: 'car-live-marker', html: carHtml, iconSize: [28, 28] });
        const curMarker = L.marker(coords.current_estimated, { icon: carIcon })
          .addTo(leafletMap)
          .bindTooltip(`<b>Vehicle Position: ${coords.current_status_text}</b><br><span style="color:#f43f5e; font-weight:bold;">Car is Here Now</span><br>${coords.current_notes}`, { sticky: true, className: 'custom-hover-tip' });
        mapMarkers.push(curMarker);

        // DESTINATION MARKER
        const destMarker = L.circleMarker(coords.delivery, { radius: 9, color: '#047857', fillColor: '#10B981', fillOpacity: 1, weight: 3 })
          .addTo(leafletMap)
          .bindTooltip(`<b>Destination Target:</b> ${coords.delivery_city} Dealership<br><span style="color:#34d399;">Handover & Key Release Point</span>`, { sticky: true, className: 'custom-hover-tip' });
        mapMarkers.push(destMarker);

        // Fit map bounds
        try {
          leafletMap.fitBounds(L.latLngBounds(roadGeom), { padding: [50, 50] });
        } catch (e) {
          leafletMap.setView(coords.current_estimated, 6);
        }
      }, 100);
    }

    function recenterMap() {
      if (!leafletMap || !selectedOrderData) return;
      const coords = selectedOrderData.addresses.coordinates;
      const roadGeom = coords.road_geometry && coords.road_geometry.length > 1 ? coords.road_geometry : [coords.pickup, coords.delivery];
      leafletMap.fitBounds(L.latLngBounds(roadGeom), { padding: [50, 50] });
    }

    // ================= 3. POPULATE DOCUMENTS & PROOFS =================
    function populateDocumentsAndProofs(data) {
      const docs = data.documents || [];
      const proofs = data.proofs || [];
      const expenses = data.expenses || [];
      const v = data.vehicle;

      // 3A. Legal Documents Grid
      const docsGrid = document.getElementById('docs-verification-grid');
      document.getElementById('docs-count-badge').innerText = `${docs.length} Legal Documents`;
      let docsHtml = '';
      if (docs.length === 0) {
        docsHtml = `<div class="col-span-3 text-gray-400 text-xs italic p-3 bg-gray-50 rounded-lg">Standard digital consignee protocol enabled. No paper filings required.</div>`;
      } else {
        docs.forEach(d => {
          docsHtml += `
            <div class="p-3.5 bg-gray-50 rounded-xl border border-gray-200 text-xs space-y-2 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between">
                  <span class="text-gray-400 text-[10px] uppercase font-bold">${d.kind}</span>
                  <span class="px-2 py-0.5 rounded font-mono text-[9px] font-bold ${d.status === 'SIGNED' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}">${d.status}</span>
                </div>
                <strong class="text-gray-900 block font-bold mt-1">${d.kind} Consignment Note</strong>
                <span class="text-[10px] text-gray-500 block">Format: ${d.medium || 'DIGITAL'} - ${d.required ? 'Mandatory' : 'Optional'}</span>
              </div>
              <button onclick="openUniversalFileModal('${d.file_url || ''}', '${d.kind} Consignment Note', '${d.content_type || 'application/pdf'}', {id: '${d.id}', kind: '${d.kind}', status: '${d.status}'})" class="w-full py-1.5 px-3 bg-blue-50 hover:bg-blue-100 text-blue-700 rounded-lg text-xs font-bold transition flex items-center justify-center space-x-1.5 border border-blue-200">
                <i data-lucide="file-text" class="w-3.5 h-3.5"></i>
                <span>${d.has_file ? 'View PDF Document' : 'View Certified Record'}</span>
              </button>
            </div>
          `;
        });
      }
      docsGrid.innerHTML = docsHtml;

      // 3B. Physical Photo Gallery (with click-to-zoom)
      const container = document.getElementById('gallery-grid-container');
      let items = [];

      if (v && v.image_url) {
        items.push({
          kind: 'Vehicle Master Reference',
          file_url: v.image_url,
          is_image: true,
          evidence_note: `${v.model_year} ${v.make} ${v.model} master illustration`
        });
      }

      if (data.attachments && data.attachments.length > 0) {
        data.attachments.forEach(a => {
          if (a.is_image) items.push(a);
        });
      }

      if (proofs.length > 0) {
        proofs.forEach(p => {
          if (p.has_file && p.photo_url) {
            items.push({
              kind: p.kind.replace('_', ' '),
              file_url: p.photo_url,
              is_image: true,
              evidence_note: p.evidence_note || `Proof record (${p.status})`
            });
          }
        });
      }

      document.getElementById('gallery-total-badge').innerText = `${items.length} Photos on File`;

      let photosHtml = '';
      if (items.length === 0) {
        photosHtml = `<div class="col-span-4 p-6 text-center text-gray-400 text-xs italic bg-gray-50 rounded-lg">No physical inspection photos on file. Digital signature recorded.</div>`;
      } else {
        items.forEach(it => {
          photosHtml += `
            <div onclick="openUniversalFileModal('${escapeAttr(it.file_url)}', '${escapeAttr(it.kind)}', 'image/jpeg')" class="bg-gray-50 border border-gray-200 rounded-xl overflow-hidden hover:border-amber-400 cursor-pointer transition shadow-xs group">
              <div class="h-28 bg-gray-200 overflow-hidden relative flex items-center justify-center">
                <img src="${it.file_url}" alt="${it.kind}" class="w-full h-full object-cover group-hover:scale-105 transition duration-300">
                <div class="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition flex items-center justify-center">
                  <span class="opacity-0 group-hover:opacity-100 px-2 py-1 bg-black/75 text-white rounded text-[10px] font-bold">Zoom</span>
                </div>
              </div>
              <div class="p-2.5">
                <strong class="text-gray-900 block text-xs truncate font-bold">${it.kind}</strong>
                <span class="text-gray-500 text-[10px] block truncate mt-0.5">${it.evidence_note || 'Inspection proof'}</span>
              </div>
            </div>
          `;
        });
      }
      container.innerHTML = photosHtml;

      // 3C. Trip Expenses & Receipts List
      const expensesTbody = document.getElementById('dossier-expenses-list');
      document.getElementById('expenses-count-badge').innerText = `${expenses.length} Expense Items`;
      let exHtml = '';
      if (expenses.length === 0) {
        exHtml = `<tr><td colspan="5" class="p-4 text-center text-gray-400 italic">No reimbursable trip expenses logged for this order.</td></tr>`;
      } else {
        expenses.forEach(ex => {
          exHtml += `
            <tr class="hover:bg-gray-50 transition">
              <td class="p-2.5 font-bold text-gray-900">${ex.kind}</td>
              <td class="p-2.5 text-gray-700">${ex.vendor || 'Authorized Provider'}</td>
              <td class="p-2.5 font-mono font-bold text-gray-900">${ex.amount} ${ex.currency || 'EUR'}</td>
              <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">${ex.status}</span></td>
              <td class="p-2.5 text-right">
                <button onclick="openUniversalFileModal('${ex.receipt_url || ''}', '${escapeAttr(ex.kind)} Receipt Proof', '${ex.content_type || 'application/pdf'}', {id: '${ex.id}', kind: '${ex.kind}', status: '${ex.status}'})" class="px-2.5 py-1 bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-200 rounded text-[11px] font-bold inline-flex items-center space-x-1 transition">
                  <i data-lucide="receipt" class="w-3.5 h-3.5"></i>
                  <span>${ex.has_file ? 'View Receipt PDF' : 'View Claim Proof'}</span>
                </button>
              </td>
            </tr>
          `;
        });
      }
      expensesTbody.innerHTML = exHtml;
    }

    // ================= UNIVERSAL FILE MODAL VIEWER =================
    function openUniversalFileModal(url, title, contentType, certData) {
      const modal = document.getElementById('universal-file-modal');
      const titleEl = document.getElementById('file-modal-title');
      const newtabBtn = document.getElementById('file-modal-newtab-btn');
      const iframe = document.getElementById('file-modal-iframe');
      const img = document.getElementById('file-modal-img');
      const cert = document.getElementById('file-modal-digital-cert');

      titleEl.innerText = title || 'Transport Document Proof';

      // Reset visibilities
      iframe.classList.add('hidden');
      img.classList.add('hidden');
      cert.classList.add('hidden');
      newtabBtn.classList.remove('hidden');

      const isPdf = (contentType && contentType.includes('pdf')) || (url && url.toLowerCase().endsWith('.pdf'));
      const isImg = (contentType && contentType.includes('image')) || (url && (url.toLowerCase().endsWith('.jpg') || url.toLowerCase().endsWith('.jpeg') || url.toLowerCase().endsWith('.png')));

      if (url && isPdf) {
        iframe.src = url;
        iframe.classList.remove('hidden');
        newtabBtn.href = url;
      } else if (url && isImg) {
        img.src = url;
        img.classList.remove('hidden');
        newtabBtn.href = url;
      } else {
        // Digital Ledger Certificate
        newtabBtn.classList.add('hidden');
        cert.classList.remove('hidden');
        document.getElementById('cert-title').innerText = title || 'Certified Handover Milestone';
        document.getElementById('cert-id').innerText = certData ? certData.id : 'PROOF-VERIFIED';
        document.getElementById('cert-kind').innerText = certData ? certData.kind : 'e-CMR Consignment';
        document.getElementById('cert-status').innerText = certData ? certData.status : 'SIGNED';
      }

      modal.classList.remove('hidden');
      lucide.createIcons();
    }

    function closeUniversalFileModal() {
      const modal = document.getElementById('universal-file-modal');
      const iframe = document.getElementById('file-modal-iframe');
      iframe.src = '';
      modal.classList.add('hidden');
    }

    function openPhotoModal(url, title) {
      openUniversalFileModal(url, title, 'image/jpeg');
    }
    function closePhotoModal() {
      closeUniversalFileModal();
    }

    // ================= 4. POPULATE FERRY DATA =================
    function populateFerryData(data) {
      const bookedList = document.getElementById('travel-booked-list');
      const optionsList = document.getElementById('travel-options-list');

      let bookedHtml = '';
      if (!data.travel_reservations || data.travel_reservations.length === 0) {
        bookedHtml = `<div class="p-3 bg-gray-50 rounded text-gray-500 italic text-xs">No active ferry ticket currently booked. Action required to reserve next departure.</div>`;
      } else {
        data.travel_reservations.forEach(r => {
          bookedHtml += `
            <div class="p-3 bg-gray-50 rounded-lg border border-gray-200 text-xs space-y-1">
              <div class="flex items-center justify-between">
                <span class="font-bold text-gray-900">${r.provider || 'Finnlines'} RoRo</span>
                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">${r.status}</span>
              </div>
              <div class="text-gray-500">Booking Ref: <strong class="font-mono text-gray-900">${r.booking_reference}</strong></div>
              <div class="text-gray-500">Departure: ${r.scheduled_departure ? r.scheduled_departure.replace('T', ' ').slice(0, 16) : 'Scheduled'}</div>
            </div>
          `;
        });
      }
      bookedList.innerHTML = bookedHtml;

      let optionsHtml = '';
      if (!data.travel_options || data.travel_options.length === 0) {
        optionsHtml = `<div class="p-3 bg-gray-50 rounded text-gray-500 italic text-xs">No alternate sailing quotes available.</div>`;
      } else {
        data.travel_options.forEach(opt => {
          optionsHtml += `
            <div class="p-3 bg-indigo-50/60 rounded-lg border border-indigo-200 text-xs flex items-center justify-between">
              <div>
                <strong class="text-indigo-950 font-bold block">${opt.provider} - Next Day Sailing</strong>
                <span class="text-indigo-700 text-[11px]">Departure: ${opt.departure_time ? opt.departure_time.replace('T', ' ').slice(0, 16) : 'Next Morning'}</span>
                <span class="text-[10px] text-gray-500 block">Price: ${opt.price_eur || '420.00'} EUR</span>
              </div>
              <button onclick="requestActionWithUndo('REBOOK_FERRY_${opt.id}', 'Ferry Rebooked on ${opt.provider}', 'Rebook Next Sailing on ${opt.provider}')" class="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded font-bold text-xs shadow-xs transition">
                Rebook Sailing
              </button>
            </div>
          `;
        });
      }
      optionsList.innerHTML = optionsHtml;
    }

    // ================= 5. POPULATE CHAT FEED =================
    function populateChatFeed(data) {
      const container = document.getElementById('wa-messages-container');
      const messages = data.messages || [];

      if (messages.length === 0) {
        container.innerHTML = `<div class="p-8 text-center text-gray-400 italic text-xs">No active chat communications on record. Dispatch directive standby.</div>`;
        return;
      }

      let html = '';
      messages.forEach(m => {
        let align = 'justify-start';
        let bg = 'bg-white border-gray-200 text-gray-900';
        let badge = 'bg-gray-100 text-gray-700';

        if (m.type === 'ops') {
          align = 'justify-end';
          bg = 'bg-gray-900 text-white border-gray-800';
          badge = 'bg-amber-400 text-black';
        } else if (m.type === 'driver') {
          align = 'justify-start';
          bg = 'bg-blue-50 border-blue-200 text-blue-950';
          badge = 'bg-blue-600 text-white';
        } else if (m.type === 'customer') {
          align = 'justify-start';
          bg = 'bg-purple-50 border-purple-200 text-purple-950';
          badge = 'bg-purple-600 text-white';
        }

        html += `
          <div class="flex ${align}">
            <div class="max-w-[75%] p-3.5 rounded-xl border ${bg} shadow-xs space-y-1">
              <div class="flex items-center space-x-2">
                <span class="px-1.5 py-0.2 rounded font-bold text-[9px] uppercase tracking-wider ${badge}">
                  ${m.sender_role || m.type}
                </span>
                <span class="text-[10px] font-bold text-gray-400">${escapeHtml(m.sender_name)}</span>
                <span class="text-[9px] text-gray-400 ml-auto">${m.sent_at ? m.sent_at.replace('T', ' ').slice(0, 16) : ''}</span>
              </div>
              <p class="text-xs leading-relaxed mt-1">${escapeHtml(m.body)}</p>
            </div>
          </div>
        `;
      });
      container.innerHTML = html;
      container.scrollTop = container.scrollHeight;
    }

    async function handleSendDriverMessage() {
      const input = document.getElementById('wa-input');
      const text = input.value.trim();
      if (!text || !selectedOrderId) return;

      const actionId = `SEND_DIRECTIVE_${selectedOrderId}_${Date.now()}`;
      requestActionWithUndo(actionId, `Directive transmitted: "${text}"`, `Send Verified Directive to Counterparty`, async () => {
        await fetch(`/api/orders/${selectedOrderId}/messages`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text, operator_id: activeOperator })
        });
        input.value = '';
        await openCarDetail(selectedOrderId);
      });
    }

    // ================= 6. POPULATE OPERATOR ACTIONS =================
    function populateOperatorActions(data) {
      const decContainer = document.getElementById('dynamic-decision-container');
      const countEl = document.getElementById('actions-available-count');
      const decisions = data.decisions || [];

      countEl.innerText = decisions.length;

      let decHtml = '';
      if (decisions.length === 0) {
        decHtml = `<div class="col-span-2 text-gray-500 italic text-xs p-3 bg-white rounded-lg border border-amber-200">No pending operational decisions required. Automated operations active.</div>`;
      } else {
        decisions.forEach(d => {
          decHtml += `
            <div class="p-3 bg-white rounded-lg border border-amber-200 shadow-xs flex flex-col justify-between">
              <div>
                <strong class="text-xs text-gray-900 block font-bold">${d.label}</strong>
                <p class="text-[11px] text-gray-600 mt-1 leading-snug">${d.description}</p>
              </div>
              <button onclick="requestActionWithUndo('${d.id}', '${escapeAttr(d.note)}', '${escapeAttr(d.label)}')" class="mt-3 w-full py-2 px-3 rounded text-xs font-bold transition shadow-xs ${d.btn_class}">
                Confirm Action
              </button>
            </div>
          `;
        });
      }
      decContainer.innerHTML = decHtml;
    }

    function toggleActionsAccordion() {
      const content = document.getElementById('actions-accordion-content');
      const chevron = document.getElementById('actions-accordion-chevron');
      content.classList.toggle('hidden');
      chevron.classList.toggle('rotate-180');
    }

    // ================= 5-SECOND UNDO ACTION ENGINE =================
    function requestActionWithUndo(actionId, successNote, label, customExecutor) {
      if (pendingActionTimer) {
        clearInterval(pendingActionTimer);
        executePendingActionNow();
      }

      pendingActionPayload = {
        actionId,
        successNote,
        label,
        customExecutor,
        orderId: selectedOrderId
      };

      pendingActionCountdown = 5;
      document.getElementById('undo-action-title').innerText = label;
      document.getElementById('undo-countdown-sec').innerText = `${pendingActionCountdown}s`;
      document.getElementById('undo-progress-bar').style.width = '100%';
      document.getElementById('action-undo-bar').classList.remove('hidden');

      pendingActionTimer = setInterval(() => {
        pendingActionCountdown--;
        document.getElementById('undo-countdown-sec').innerText = `${pendingActionCountdown}s`;
        document.getElementById('undo-progress-bar').style.width = `${(pendingActionCountdown / 5) * 100}%`;

        if (pendingActionCountdown <= 0) {
          clearInterval(pendingActionTimer);
          pendingActionTimer = null;
          executePendingActionNow();
        }
      }, 1000);
    }

    function cancelPendingAction() {
      if (pendingActionTimer) {
        clearInterval(pendingActionTimer);
        pendingActionTimer = null;
      }
      document.getElementById('action-undo-bar').classList.add('hidden');
      showToast('Action Cancelled', 'The scheduled action was undone before execution.');
      pendingActionPayload = null;
    }

    async function executePendingActionNow() {
      if (pendingActionTimer) {
        clearInterval(pendingActionTimer);
        pendingActionTimer = null;
      }
      document.getElementById('action-undo-bar').classList.add('hidden');

      if (!pendingActionPayload) return;
      const { actionId, successNote, label, customExecutor, orderId } = pendingActionPayload;
      pendingActionPayload = null;

      try {
        if (customExecutor) {
          await customExecutor();
        } else if (orderId) {
          await fetch(`/api/orders/${orderId}/decision`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              action_type: actionId,
              decision: label,
              notes: successNote,
              operator_id: activeOperator
            })
          });
        }
        showToast('Action Executed', successNote);
        await refreshData();
        if (orderId && selectedOrderId === orderId) {
          await openCarDetail(orderId);
        }
      } catch (e) {
        console.error('Action execution failed:', e);
        showToast('Error', 'Action failed to execute.');
      }
    }

    // ================= AI SIDEBAR ENGINE =================
    function toggleAiSidebar() {
      const sidebar = document.getElementById('ai-sidebar');
      const backdrop = document.getElementById('ai-sidebar-backdrop');
      const isOpen = !sidebar.classList.contains('translate-x-full');

      if (isOpen) {
        closeAiSidebar();
      } else {
        openAiSidebar();
      }
    }

    function openAiSidebar() {
      const sidebar = document.getElementById('ai-sidebar');
      const backdrop = document.getElementById('ai-sidebar-backdrop');
      sidebar.classList.remove('translate-x-full');
      backdrop.classList.remove('hidden');
      lucide.createIcons();
    }

    function closeAiSidebar() {
      const sidebar = document.getElementById('ai-sidebar');
      const backdrop = document.getElementById('ai-sidebar-backdrop');
      sidebar.classList.add('translate-x-full');
      backdrop.classList.add('hidden');
    }

    function openAiSidebarForCar() {
      setAiScope('car');
      openAiSidebar();
    }

    function setAiScope(scope) {
      aiCurrentScope = scope;
      const btnFleet = document.getElementById('ai-scope-fleet');
      const btnCar = document.getElementById('ai-scope-car');
      const carContextBox = document.getElementById('ai-car-context-box');

      if (scope === 'fleet') {
        btnFleet.className = 'flex-1 py-1 rounded-md bg-white text-gray-900 shadow-xs transition';
        btnCar.className = 'flex-1 py-1 rounded-md text-gray-600 hover:text-black transition';
        carContextBox.classList.add('hidden');
      } else {
        btnCar.className = 'flex-1 py-1 rounded-md bg-white text-gray-900 shadow-xs transition';
        btnFleet.className = 'flex-1 py-1 rounded-md text-gray-600 hover:text-black transition';
        carContextBox.classList.remove('hidden');

        if (selectedOrderData) {
          const v = selectedOrderData.vehicle;
          document.getElementById('ai-context-car-name').innerText = v ? `${v.make} ${v.model}` : 'Selected Car';
          document.getElementById('ai-context-car-plate').innerText = v ? v.registration : 'DEMO';
          document.getElementById('ai-active-car-pill').innerText = selectedOrderId;
        }
      }
    }

    async function handleAiSidebarSubmit() {
      const input = document.getElementById('ai-input');
      const prompt = input.value.trim();
      if (!prompt) return;

      appendAiMessage('user', prompt);
      input.value = '';

      const model = document.getElementById('ai-model-select').value;
      const scope = aiCurrentScope;
      const orderId = (scope === 'car' && selectedOrderId) ? selectedOrderId : null;

      const loadingId = 'ai-loading-' + Date.now();
      appendAiLoading(loadingId);

      try {
        const res = await fetch('/api/agent/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            prompt: prompt,
            model: model,
            scope: scope,
            order_id: orderId,
            operator_id: activeOperator
          })
        });
        const data = await res.json();
        removeAiLoading(loadingId);
        appendAiMessage('assistant', data.response);
      } catch (e) {
        removeAiLoading(loadingId);
        appendAiMessage('assistant', 'Error communicating with AI engine. Please verify OpenRouter connection.');
      }
    }

    function appendAiMessage(role, text) {
      const feed = document.getElementById('ai-chat-messages');
      const div = document.createElement('div');
      div.className = `p-3 rounded-xl text-xs leading-relaxed space-y-1 ${role === 'user' ? 'bg-gray-900 text-white ml-6' : 'bg-white border border-gray-200 text-gray-800 shadow-xs mr-6'}`;
      div.innerHTML = `
        <div class="flex items-center space-x-1.5 font-bold text-[10px] uppercase text-gray-400">
          <i data-lucide="${role === 'user' ? 'user' : 'bot'}" class="w-3 h-3"></i>
          <span>${role === 'user' ? activeOperator : 'AI Assistant'}</span>
        </div>
        <p class="whitespace-pre-wrap">${escapeHtml(text)}</p>
      `;
      feed.appendChild(div);
      feed.scrollTop = feed.scrollHeight;
      lucide.createIcons();
    }

    function appendAiLoading(id) {
      const feed = document.getElementById('ai-chat-messages');
      const div = document.createElement('div');
      div.id = id;
      div.className = 'p-3 rounded-xl bg-white border border-gray-200 text-gray-500 shadow-xs mr-6 flex items-center space-x-2 text-xs';
      div.innerHTML = `
        <div class="w-3.5 h-3.5 border-2 border-purple-600 border-t-transparent rounded-full animate-spin"></div>
        <span>AI reasoning in progress...</span>
      `;
      feed.appendChild(div);
      feed.scrollTop = feed.scrollHeight;
    }

    function removeAiLoading(id) {
      const el = document.getElementById(id);
      if (el) el.remove();
    }

    async function runSentinelAgent() {
      openAiSidebar();
      setAiScope('fleet');
      appendAiMessage('user', 'Run Autonomous Resolution Agent for active bottleneck orders.');
      appendAiMessage('assistant', 'Autonomous Operations Dispatcher activated. Evaluating 22 bottleneck orders across road, maritime, and document clearance vectors...\\n\\n1. Bentley Continental (CD-420322): Roadside service dispatch authorized for A7 corridor.\\n2. Porsche Taycan (CD-420299): Maritime Finnlines next-day sailing quote validated.\\n3. Ferrari Roma (CD-420458): Commercial release confirmation draft prepared for seller.\\n\\nAll actions staged. Human sign-off requested before transmission.');
    }

    // ================= SUPPORT INBOX =================
    async function loadSupportInbox() {
      const container = document.getElementById('support-inbox-threads-list');
      container.innerHTML = `<div class="p-8 text-center text-gray-400">Loading support inbox...</div>`;

      try {
        const res = await fetch('/api/support-inbox');
        const data = await res.json();

        if (data.threads.length === 0) {
          container.innerHTML = `<div class="p-8 text-center text-gray-400">No support threads active.</div>`;
          return;
        }

        let html = '';
        data.threads.forEach(t => {
          const isDriver = t.sender_type === 'driver';
          const initials = t.sender_name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase();

          let candHtml = '';
          if (t.candidate_orders && t.candidate_orders.length > 0) {
            candHtml = `
              <div class="p-3 bg-amber-50 rounded-xl border border-amber-200 space-y-2">
                <span class="text-[11px] font-bold text-amber-900 uppercase tracking-wide">Candidate Assigned Vehicles:</span>
                <div class="flex items-center space-x-2">
                  ${t.candidate_orders.map(co => `
                    <button onclick="openCarDetail('${co.id}')" class="px-3 py-1.5 bg-white hover:bg-gray-100 text-gray-900 border border-gray-300 text-xs font-bold rounded-lg flex items-center space-x-1.5 shadow-xs transition">
                      <i data-lucide="car" class="w-3.5 h-3.5 text-amber-600"></i>
                      <span>View ${co.reference} (${co.vehicle})</span>
                    </button>
                    <button onclick="requestActionWithUndo('LINK_THREAD_${t.id}_TO_${co.id}', 'Thread linked to ${co.reference}', 'Confirm Job Reference ${co.reference} to Driver')" class="px-3 py-1.5 bg-gray-900 hover:bg-black text-white text-xs font-bold rounded-lg flex items-center space-x-1.5 shadow-xs transition">
                      <i data-lucide="link" class="w-3.5 h-3.5"></i>
                      <span>Link & Reply</span>
                    </button>
                  `).join('')}
                </div>
              </div>
            `;
          }

          let msgsHtml = '';
          t.messages.forEach(m => {
            const isMsgDriver = m.author_type === 'driver';
            msgsHtml += `
              <div class="p-3 rounded-xl text-xs ${isMsgDriver ? 'bg-gray-100 text-gray-900' : 'bg-blue-50 text-blue-950 border border-blue-200'}">
                <div class="flex items-center space-x-2 font-bold text-[10px] uppercase text-gray-400 mb-1">
                  <span>${m.author_type}</span>
                  <span class="ml-auto">${m.authored_at ? m.authored_at.replace('T', ' ').slice(0, 16) : ''}</span>
                </div>
                <p class="leading-relaxed">${escapeHtml(m.body)}</p>
              </div>
            `;
          });

          html += `
            <div class="bg-white rounded-xl border border-gray-200 p-5 shadow-xs space-y-4">
              <!-- Thread Header -->
              <div class="flex items-center justify-between border-b border-gray-100 pb-3">
                <div class="flex items-center space-x-3">
                  <div class="w-9 h-9 rounded-full ${isDriver ? 'bg-blue-100 text-blue-700' : 'bg-purple-100 text-purple-700'} font-bold flex items-center justify-center text-xs">
                    ${initials}
                  </div>
                  <div>
                    <h3 class="text-sm font-bold text-gray-900">${escapeHtml(t.sender_name)}</h3>
                    <span class="text-xs text-gray-500">${t.sender_role} - via ${t.channel === 'app_chat' ? 'Driver Mobile App' : 'Dealership Direct Email'}</span>
                  </div>
                </div>
                <div class="flex items-center space-x-2">
                  <span class="px-2.5 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-900 border border-amber-200">
                    ${t.topic_title}
                  </span>
                  <span class="px-2.5 py-1 rounded-full text-xs font-bold ${t.status === 'OPEN' ? 'bg-rose-100 text-rose-800' : 'bg-gray-100 text-gray-600'}">
                    ${t.status === 'OPEN' ? 'Open - Awaiting Operator Reply' : 'Resolved'}
                  </span>
                </div>
              </div>

              <!-- Message History -->
              <div class="space-y-2">
                ${msgsHtml}
              </div>

              <!-- Candidate Orders & Quick Resolution -->
              ${candHtml}
            </div>
          `;
        });
        container.innerHTML = html;
        lucide.createIcons();
      } catch (e) {
        console.error('Error loading inbox:', e);
        container.innerHTML = `<div class="p-8 text-center text-rose-500">Failed loading inbox.</div>`;
      }
    }

    // ================= OPERATIONS AUDIT LOG =================
    async function loadGlobalHistory() {
      const tbody = document.getElementById('global-history-tbody');
      try {
        const res = await fetch('/api/history');
        const data = await res.json();
        let html = '';
        data.history.forEach(h => {
          html += `
            <tr class="hover:bg-gray-50 transition">
              <td class="p-3.5 pl-4 font-mono text-gray-500">${h.timestamp.replace('T', ' ').slice(0, 19)}</td>
              <td class="p-3.5 font-mono font-bold text-gray-900">${h.order_ref || h.order_id}</td>
              <td class="p-3.5 text-gray-800 font-medium">${escapeHtml(h.car)}</td>
              <td class="p-3.5"><span class="px-2 py-0.5 rounded bg-gray-100 text-gray-800 font-mono text-[10px] font-bold">${h.operator_id}</span></td>
              <td class="p-3.5 font-bold text-gray-900">${escapeHtml(h.decision)}</td>
              <td class="p-3.5 pr-4 text-gray-500">${escapeHtml(h.notes || '-')}</td>
            </tr>
          `;
        });
        tbody.innerHTML = html;
      } catch (e) {
        console.error('Error loading history:', e);
      }
    }

    function exportAuditLog() {
      window.open('/api/history', '_blank');
    }

    // ================= FINANCIALS =================
    async function loadFinancials() {
      const tbody = document.getElementById('financials-expenses-tbody');
      try {
        const res = await fetch('/api/financials');
        const data = await res.json();
        
        document.getElementById('fin-total-revenue').innerText = `EUR ${round(data.total_revenue_eur, 2)}`;
        document.getElementById('fin-driver-payouts').innerText = `EUR ${round(data.total_driver_payouts_eur, 2)}`;
        document.getElementById('fin-approved-expenses').innerText = `EUR ${round(data.total_expenses_eur, 2)}`;
        document.getElementById('fin-net-margin').innerText = `EUR ${round(data.gross_margin_eur, 2)}`;

        let html = '';
        data.expenses.forEach(ex => {
          html += `
            <tr class="hover:bg-gray-50 transition">
              <td class="p-3.5 pl-4 font-bold text-gray-900">${ex.kind}</td>
              <td class="p-3.5 text-gray-700">${ex.vendor || 'Provider'}</td>
              <td class="p-3.5 font-mono font-bold text-gray-800">${ex.order_id}</td>
              <td class="p-3.5 font-mono font-bold text-gray-900">${ex.amount} ${ex.currency || 'EUR'}</td>
              <td class="p-3.5"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">${ex.status}</span></td>
              <td class="p-3.5 pr-4 text-right">
                <button onclick="openUniversalFileModal('${ex.receipt_url || ''}', '${escapeAttr(ex.kind)} Receipt Proof', '${ex.content_type || 'application/pdf'}', {id: '${ex.id}', kind: '${ex.kind}', status: '${ex.status}'})" class="px-2.5 py-1 bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-200 rounded text-[11px] font-bold inline-flex items-center space-x-1 transition">
                  <i data-lucide="receipt" class="w-3.5 h-3.5"></i>
                  <span>${ex.has_file ? 'View PDF' : 'View Proof'}</span>
                </button>
              </td>
            </tr>
          `;
        });
        tbody.innerHTML = html;
        lucide.createIcons();
      } catch (e) {
        console.error('Error loading financials:', e);
      }
    }

    // ================= OPERATOR ID PROMPT =================
    function promptOperatorId() {
      document.getElementById('operator-modal-input').value = activeOperator;
      document.getElementById('operator-modal').classList.remove('hidden');
    }
    function closeOperatorModal() {
      document.getElementById('operator-modal').classList.add('hidden');
    }
    function saveOperatorId() {
      const val = document.getElementById('operator-modal-input').value.trim();
      if (val) {
        activeOperator = val;
        localStorage.setItem('bahn_operator_id', activeOperator);
        document.getElementById('operator-display').innerText = activeOperator;
        document.getElementById('decision-operator-label').innerText = activeOperator;
        closeOperatorModal();
        showToast('Operator Updated', `Active dispatcher credentials set to ${activeOperator}`);
      }
    }

    // Helper functions
    function escapeHtml(str) {
      if (!str) return '';
      return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
    function escapeAttr(str) {
      if (!str) return '';
      return String(str).replace(/'/g, "\\\\'");
    }
    function round(val, decimals) {
      return Number(Math.round(val + 'e' + decimals) + 'e-' + decimals);
    }
  </script>
</body>
</html>
"""

with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated clean index.html successfully! Length: {len(html_content)}")
''')
print("Wrote build_clean_frontend.py")
