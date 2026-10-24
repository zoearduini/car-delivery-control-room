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

    @keyframes subtle-pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.85; transform: scale(1.02); }
    }
    .pulse-urgent {
      animation: subtle-pulse 2s infinite ease-in-out;
    }

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

  <!-- INLINE ACTION CONFIRMATION & 10S UNDO BANNER -->
  <div id="action-undo-bar" class="hidden fixed bottom-6 left-1/2 -translate-x-1/2 z-50 bg-[#121417] text-white px-5 py-3.5 rounded-xl shadow-2xl border border-gray-700 flex items-center space-x-4 max-w-xl w-full">
    <div class="w-8 h-8 rounded-full bg-amber-400 text-black flex items-center justify-center shrink-0 font-bold">
      <i data-lucide="clock" class="w-4 h-4"></i>
    </div>
    <div class="flex-1 min-w-0">
      <div class="flex items-center space-x-2">
        <span class="text-[10px] uppercase font-bold text-amber-400 tracking-wider">Action Scheduled</span>
        <span class="text-[10px] text-gray-400">Auto-executing in <strong id="undo-countdown-sec" class="text-white font-mono">10s</strong></span>
      </div>
      <p id="undo-action-title" class="text-xs font-bold text-gray-100 truncate mt-0.5">Staged Action</p>
      <div class="w-full bg-gray-800 rounded-full h-1 mt-1.5 overflow-hidden">
        <div id="undo-progress-bar" class="bg-amber-400 h-1 rounded-full transition-all duration-1000 ease-linear" style="width: 100%;"></div>
      </div>
    </div>
    <div class="flex items-center space-x-2 shrink-0">
      <button onclick="modifyPendingAction()" class="px-3 py-1.5 bg-gray-700 hover:bg-gray-600 text-white rounded-lg text-xs font-bold transition flex items-center space-x-1 shadow-sm">
        <i data-lucide="edit-3" class="w-3.5 h-3.5"></i>
        <span>Modify</span>
      </button>
      <button onclick="cancelPendingAction()" class="px-3 py-1.5 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-xs font-bold transition flex items-center space-x-1 shadow-sm">
        <i data-lucide="x" class="w-3.5 h-3.5"></i>
        <span>Undo</span>
      </button>
      <button onclick="executePendingActionNow()" class="px-3 py-1.5 bg-amber-400 hover:bg-amber-500 text-black rounded-lg text-xs font-bold transition flex items-center space-x-1 shadow-sm">
        <i data-lucide="check" class="w-3.5 h-3.5"></i>
        <span>Confirm</span>
      </button>
    </div>
  </div>

  <!-- ACTION MODIFICATION MODAL -->
  <div id="action-modify-modal" class="hidden fixed inset-0 z-[9999] bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl border border-gray-200">
      <div class="flex items-center justify-between border-b border-gray-100 pb-3">
        <div class="flex items-center space-x-2">
          <span class="text-base font-bold text-gray-900">✏️ Modify Action Directives</span>
        </div>
        <button onclick="closeModifyModal()" class="p-1 rounded-lg hover:bg-gray-100 text-gray-400 hover:text-gray-700 transition">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <div class="space-y-3 text-xs">
        <div>
          <label class="block font-bold text-gray-700 mb-1">Action Description & Objective</label>
          <input type="text" id="modify-action-title" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-xs font-medium focus:outline-none focus:border-amber-500">
        </div>
        <div>
          <label class="block font-bold text-gray-700 mb-1">Driver / Dealer Instruction Text</label>
          <textarea id="modify-action-notes" rows="3" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-xs focus:outline-none focus:border-amber-500"></textarea>
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block font-bold text-gray-700 mb-1">Adjusted Time / Window</label>
            <input type="text" id="modify-action-time" placeholder="e.g. 2026-10-22 14:00" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-xs focus:outline-none focus:border-amber-500">
          </div>
          <div>
            <label class="block font-bold text-gray-700 mb-1">Authorized Budget Limit (EUR)</label>
            <input type="number" id="modify-action-budget" placeholder="e.g. 250" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-xs focus:outline-none focus:border-amber-500">
          </div>
        </div>
      </div>

      <div class="flex items-center justify-end space-x-2 pt-2 border-t border-gray-100">
        <button onclick="closeModifyModal()" class="px-4 py-2 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold text-xs transition">Cancel</button>
        <button onclick="saveAndApplyModifiedAction()" class="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs transition flex items-center space-x-1.5 shadow-sm">
          <i data-lucide="check" class="w-4 h-4"></i>
          <span>Save & Stage with 10s Undo</span>
        </button>
      </div>
    </div>
  </div>

  <!-- UNIVERSAL DOCUMENT & PROOF MODAL -->
  <div id="universal-file-modal" class="hidden fixed inset-0 z-[9999] bg-black/75 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-gray-900 rounded-2xl w-full max-w-4xl h-[85vh] flex flex-col overflow-hidden shadow-2xl border border-gray-700">
      <div class="px-5 py-3.5 bg-gray-800/90 border-b border-gray-700 flex items-center justify-between text-white">
        <div class="flex items-center space-x-2.5">
          <i data-lucide="file-text" id="file-modal-icon" class="w-5 h-5 text-amber-400"></i>
          <span id="file-modal-title" class="font-bold text-sm tracking-wide">Document Record</span>
        </div>
        <div class="flex items-center space-x-2">
          <a id="file-modal-open-tab" href="#" target="_blank" class="px-3 py-1.5 rounded-lg bg-gray-700 hover:bg-gray-600 text-xs font-bold transition flex items-center space-x-1.5 text-gray-200">
            <i data-lucide="external-link" class="w-3.5 h-3.5"></i>
            <span>Open in Tab</span>
          </a>
          <button onclick="closeUniversalFileModal()" class="p-1.5 rounded-lg hover:bg-gray-700 text-gray-400 hover:text-white transition">
            <i data-lucide="x" class="w-5 h-5"></i>
          </button>
        </div>
      </div>
      <div class="flex-1 bg-black flex items-center justify-center overflow-hidden relative">
        <iframe id="file-modal-iframe" src="" class="w-full h-full border-none hidden"></iframe>
        <img id="file-modal-image" src="" alt="Proof Preview" class="max-w-full max-h-full object-contain hidden" />
        <div id="file-modal-fallback" class="hidden p-8 text-center text-gray-400 space-y-3">
          <p class="text-sm">Direct preview standby. Open in external browser tab:</p>
          <a id="file-modal-fallback-link" href="#" target="_blank" class="inline-flex items-center space-x-2 px-4 py-2 bg-amber-500 text-black font-bold rounded-lg text-xs">
            <span>View Original Attachment</span>
          </a>
        </div>
      </div>
    </div>
  </div>

  <!-- TOP APP BAR -->
  <header class="h-14 bg-[#121417] text-white px-6 flex items-center justify-between border-b border-gray-800 shrink-0 z-30 select-none">
    <div class="flex items-center space-x-6">
      <div class="flex items-center space-x-3 cursor-pointer" onclick="goToFleetView()">
        <img src="/static/bahn-logo.png" alt="Bahn Logo" class="h-8 w-8 object-contain rounded bg-white p-1">
        <div>
          <span class="font-black tracking-wider text-base uppercase text-amber-400">Bahn Operations</span>
          <span class="text-xs text-gray-400 ml-2 hidden sm:inline">Control Room</span>
        </div>
      </div>

      <!-- Navigation Tabs -->
      <nav class="flex items-center space-x-1 text-xs font-medium">
        <button id="nav-btn-fleet" onclick="goToFleetView()" class="px-3 py-1.5 rounded-md font-semibold bg-amber-500 text-black flex items-center space-x-1.5 transition">
          <i data-lucide="car" class="w-3.5 h-3.5"></i>
          <span id="nav-fleet-label">Fleet Overview</span>
        </button>
        <button id="nav-btn-inbox" onclick="switchGlobalView('inbox')" class="px-3 py-1.5 rounded-md text-gray-300 hover:text-white flex items-center space-x-1.5 transition">
          <i data-lucide="inbox" class="w-3.5 h-3.5"></i>
          <span>Support Inbox</span>
          <span id="nav-inbox-badge" class="ml-1 px-1.5 py-0.2 bg-amber-400 text-black rounded-full font-bold text-[10px]">4</span>
        </button>
        <button id="nav-btn-history" onclick="switchGlobalView('history')" class="px-3 py-1.5 rounded-md text-gray-300 hover:text-white flex items-center space-x-1.5 transition">
          <i data-lucide="history" class="w-3.5 h-3.5"></i>
          <span>Operations Audit Log</span>
        </button>
        <button id="nav-btn-finance" onclick="switchGlobalView('finance')" class="px-3 py-1.5 rounded-md text-gray-300 hover:text-white flex items-center space-x-1.5 transition">
          <i data-lucide="link" class="w-3.5 h-3.5"></i>
          <span>Financials & Earnings</span>
        </button>
      </nav>
    </div>

    <!-- Right Operator & AI Assistant Trigger -->
    <div class="flex items-center space-x-3">
      <div onclick="promptOperatorId()" class="cursor-pointer flex items-center space-x-2 px-3 py-1 rounded-lg bg-gray-800/80 border border-gray-700 hover:border-gray-500 transition text-xs">
        <i data-lucide="shield" class="w-3.5 h-3.5 text-amber-400"></i>
        <span class="text-gray-400">Operator:</span>
        <strong id="operator-display" class="text-gray-100 font-mono">OP-042</strong>
        <i data-lucide="edit-2" class="w-3 h-3 text-gray-500"></i>
      </div>

      <!-- AI Assistant Button -->
      <button onclick="toggleAiSidebar()" class="px-3 py-1.5 rounded-lg bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold text-xs flex items-center space-x-1.5 transition shadow-sm">
        <i data-lucide="bot" class="w-3.5 h-3.5"></i>
        <span>AI Assistant</span>
      </button>
    </div>
  </header>

  <!-- ================= VIEW 1: FLEET OVERVIEW ================= -->
  <div id="view-home" class="flex-1 flex flex-col overflow-hidden">
    <!-- FILTER BAR -->
    <div class="bg-white border-b border-gray-200 px-8 py-3 flex items-center justify-between shrink-0 select-none">
      <div class="flex items-center space-x-3">
        <!-- 3 Categories Filter -->
        <div class="flex items-center space-x-1 p-1 bg-gray-100 rounded-lg text-xs">
          <button id="btn-status-all" onclick="setStatusFilter('all')" class="px-3.5 py-1.5 rounded-md bg-white text-black font-bold shadow-xs whitespace-nowrap shrink-0">
            All Cars (<span id="count-all">100</span>)
          </button>
          <button id="btn-status-ok" onclick="setStatusFilter('ok')" class="px-3.5 py-1.5 rounded-md text-emerald-800 hover:bg-white transition flex items-center space-x-1.5 whitespace-nowrap shrink-0">
            <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
            <span>OK / On Track (<span id="count-ok">78</span>)</span>
          </button>
          <button id="btn-status-not-ok" onclick="setStatusFilter('not_ok')" class="px-3.5 py-1.5 rounded-md text-rose-700 hover:bg-white transition flex items-center space-x-1.5 whitespace-nowrap shrink-0">
            <span class="w-2 h-2 rounded-full bg-rose-600 pulse-urgent"></span>
            <span>Needs Attention (<span id="count-not-ok">22</span>)</span>
          </button>
        </div>

        <!-- Issue Category Dropdown -->
        <div class="flex items-center space-x-2 pl-4 border-l border-gray-200">
          <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">Issue Category:</span>
          <select id="problem-select" onchange="onProblemSelectChange()" class="text-xs bg-gray-50 border border-gray-300 rounded-lg px-2.5 py-1.5 font-medium text-gray-800 focus:outline-none focus:border-amber-500">
            <option value="all">All Issues (22)</option>
            <option value="breakdown">Roadside Breakdown (1)</option>
            <option value="ferry">Ferry Booking Sold Out (2)</option>
            <option value="missing_doc">Missing / Gate Documents (11)</option>
            <option value="delay">Schedule & Rest Delays (5)</option>
            <option value="cosmetic">Cosmetic Damage Claims (3)</option>
          </select>
        </div>
      </div>

      <div class="flex items-center space-x-3 text-xs">
        <div class="flex items-center space-x-2">
          <span class="font-bold text-gray-400 uppercase">Sort:</span>
          <select id="sort-select" onchange="onSortChange()" class="text-xs bg-gray-50 border border-gray-300 rounded-lg px-2.5 py-1.5 font-medium text-gray-800 focus:outline-none focus:border-amber-500">
            <option value="newest">Newest Orders</option>
            <option value="reference">Order Reference</option>
            <option value="make">Vehicle Make</option>
            <option value="driver">Assigned Driver</option>
          </select>
        </div>

        <div class="relative w-56">
          <input type="text" id="fleet-search" oninput="onSearchInput()" placeholder="Filter VIN, plate, customer..." class="w-full pl-8 pr-3 py-1.5 bg-gray-50 border border-gray-300 rounded-lg text-xs focus:outline-none focus:border-amber-500">
          <i data-lucide="search" class="w-3.5 h-3.5 text-gray-400 absolute left-2.5 top-2"></i>
        </div>
      </div>
    </div>

    <!-- MAIN FLEET TABLE -->
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
          <tbody id="fleet-table-tbody" class="divide-y divide-gray-100"></tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- ================= VIEW 2: CAR DETAIL DOSSIER (TABBED SUB-PAGES PER USER REQUEST) ================= -->
  <div id="view-car-detail" class="hidden flex-1 flex flex-col overflow-hidden bg-[#F8F9FA]">

    <!-- TOP BREADCRUMB & BACK BAR -->
    <div class="h-12 bg-white border-b border-gray-200 px-8 flex items-center justify-between shrink-0 select-none">
      <div class="flex items-center space-x-3">
        <button onclick="goBackToFleetTable()" class="flex items-center space-x-1.5 text-xs font-bold text-gray-700 hover:text-black transition">
          <i data-lucide="arrow-left" class="w-4 h-4"></i>
          <span>All Cars</span>
        </button>
        <span class="text-gray-300">/</span>
        <span class="text-gray-500 font-mono text-[11px]" id="detail-nav-id">ORD-00000</span>
        <span class="text-gray-300">-</span>
        <span class="font-bold text-gray-900" id="detail-nav-car">Vehicle Name</span>
      </div>

      <div class="flex items-center space-x-2 text-xs">
        <button onclick="openAiSidebarForCar()" class="px-3 py-1.5 rounded-lg bg-purple-50 text-purple-700 font-bold hover:bg-purple-100 transition flex items-center space-x-1.5 border border-purple-200">
          <i data-lucide="sparkles" class="w-3.5 h-3.5 text-purple-600"></i>
          <span>Ask AI About This Car</span>
        </button>
      </div>
    </div>

    <!-- DEDICATED SUB-PAGE TAB NAVIGATION BAR -->
    <div class="bg-white border-b border-gray-200 px-8 py-2.5 flex items-center justify-between shrink-0 shadow-2xs">
      <div class="flex items-center space-x-2 text-xs font-bold" id="car-detail-tabs-nav">
        <button onclick="switchCarSubTab('deal')" id="car-tab-btn-deal" class="px-3.5 py-1.5 rounded-lg bg-amber-500 text-black shadow-xs flex items-center space-x-1.5 transition">
          <span>💼</span>
          <span>1. Commercial Deal</span>
        </button>
        <button onclick="switchCarSubTab('route')" id="car-tab-btn-route" class="px-3.5 py-1.5 rounded-lg text-gray-600 hover:bg-gray-100 flex items-center space-x-1.5 transition">
          <span>🗺️</span>
          <span>2. Route & Live Map</span>
        </button>
        <button onclick="switchCarSubTab('docs')" id="car-tab-btn-docs" class="px-3.5 py-1.5 rounded-lg text-gray-600 hover:bg-gray-100 flex items-center space-x-1.5 transition">
          <span>📄</span>
          <span>3. Documents & Proofs</span>
        </button>
        <button onclick="switchCarSubTab('ferry')" id="car-tab-btn-ferry" class="hidden px-3.5 py-1.5 rounded-lg text-gray-600 hover:bg-gray-100 flex items-center space-x-1.5 transition">
          <span>⚓</span>
          <span>4. Ferry & Sea</span>
        </button>
        <button onclick="switchCarSubTab('chat')" id="car-tab-btn-chat" class="px-3.5 py-1.5 rounded-lg text-gray-600 hover:bg-gray-100 flex items-center space-x-1.5 transition">
          <span>💬</span>
          <span>5. Communications</span>
        </button>
        <button onclick="switchCarSubTab('actions')" id="car-tab-btn-actions" class="px-3.5 py-1.5 rounded-lg text-gray-600 hover:bg-gray-100 flex items-center space-x-1.5 transition">
          <span>⚡</span>
          <span>6. Operator Actions</span>
        </button>
      </div>

      <!-- Lifecycle Badge -->
      <div class="flex items-center space-x-2">
        <span class="text-[11px] font-bold text-gray-400 uppercase">Status:</span>
        <span id="pipeline-current-status" class="font-mono text-gray-800 bg-gray-100 px-2.5 py-1 rounded-md text-[11px] font-bold">IN_TRANSIT</span>
      </div>
    </div>

    <!-- MAIN DOSSIER CONTENT AREA (Clean, Spacious, Tab-based) -->
    <div class="flex-1 overflow-y-auto custom-scrollbar p-8 max-w-6xl w-full mx-auto">
      
      <!-- Situation Alert Banner (Full description) -->
      <div id="detail-alert-box" class="hidden mb-6 p-4 rounded-xl border border-rose-300 bg-rose-50 flex items-start space-x-3 text-xs shadow-xs">
        <i data-lucide="alert-triangle" class="w-5 h-5 text-rose-600 shrink-0 mt-0.5"></i>
        <div>
          <h4 id="detail-alert-title" class="font-bold text-rose-900 text-sm">Action Required</h4>
          <p id="detail-alert-desc" class="text-rose-800 mt-0.5 leading-relaxed">Full unshortened incident description.</p>
        </div>
      </div>

      <!-- ================= SUB-PAGE 1: COMMERCIAL DEAL & VEHICLE SPECS ================= -->
      <div id="car-subpage-deal" class="space-y-6">
        <!-- Pipeline Stepper -->
        <div class="bg-white rounded-xl border border-gray-200 p-5 shadow-xs">
          <div class="text-[11px] font-bold text-gray-400 uppercase tracking-wider mb-3">Transport Chain Lifecycle Progress</div>
          <div id="pipeline-stepper" class="grid grid-cols-5 gap-3 text-xs"></div>
        </div>

        <div class="grid grid-cols-3 gap-6">
          <!-- Card A: Commercial Contract Terms -->
          <div class="bg-white rounded-xl border border-gray-200 p-6 space-y-4 shadow-xs">
            <div class="flex items-center justify-between border-b border-gray-100 pb-3">
              <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">Deal Contract Terms</span>
              <span class="font-mono text-xs text-gray-500 font-bold" id="deal-billing-ref">INV-CD-00000</span>
            </div>
            <div class="space-y-3 text-xs">
              <div class="flex justify-between items-center"><span class="text-gray-500">Customer Dealership:</span><strong class="text-gray-900" id="deal-cust-name">Dealer Name</strong></div>
              <div class="flex justify-between items-center"><span class="text-gray-500">Contact Email:</span><span class="font-mono text-gray-700" id="deal-cust-email">dealer@auto.de</span></div>
              <div class="flex justify-between items-center"><span class="text-gray-500">Contact Phone:</span><span class="font-mono text-gray-700" id="deal-cust-phone">+49 89 0000</span></div>
              <div class="pt-2 border-t border-gray-100 flex justify-between items-center"><span class="text-gray-500 font-bold">Contract Value:</span><strong class="font-mono text-emerald-600 font-bold text-sm" id="deal-contract-val">896.78 EUR</strong></div>
              <div class="flex justify-between items-center"><span class="text-gray-500">Driver Fee Payout:</span><span class="font-mono text-gray-800" id="deal-driver-fee">645.68 EUR</span></div>
              <div class="flex justify-between items-center"><span class="text-gray-500 font-bold">Gross Margin:</span><strong class="font-mono text-emerald-700 font-bold" id="deal-margin">251.10 EUR</strong></div>
              <div class="flex justify-between items-center"><span class="text-gray-500">Payment Terms:</span><span class="text-gray-700 font-medium" id="deal-terms">Net 14 Days</span></div>
            </div>
          </div>

          <!-- Card B: Vehicle Dossier -->
          <div class="bg-white rounded-xl border border-gray-200 p-6 space-y-4 shadow-xs">
            <div class="flex items-center justify-between border-b border-gray-100 pb-3">
              <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">Vehicle Dossier</span>
              <span class="px-2 py-0.5 rounded font-mono font-bold text-xs bg-gray-900 text-white" id="deal-veh-plate">DEMO-PLATE</span>
            </div>
            <div class="flex items-center space-x-4">
              <div class="w-24 h-16 rounded-lg bg-gray-100 border border-gray-200 overflow-hidden shrink-0 flex items-center justify-center">
                <img id="deal-veh-img" src="/static/bahn-logo.png" alt="Vehicle" class="w-full h-full object-cover">
              </div>
              <div class="min-w-0">
                <h4 class="font-bold text-gray-900 text-sm truncate" id="deal-veh-title">Make Model</h4>
                <p class="text-xs text-gray-500" id="deal-veh-year">2022 Fleet Edition</p>
              </div>
            </div>
            <div class="space-y-2.5 text-xs pt-1">
              <div class="flex justify-between items-center"><span class="text-gray-500">VIN:</span><span class="font-mono text-gray-800 font-bold" id="deal-veh-vin">WBA33AY0000000000</span></div>
              <div class="flex justify-between items-center"><span class="text-gray-500">Powertrain:</span><span class="text-gray-800 font-medium" id="deal-veh-fuel">Internal Combustion</span></div>
              <div class="flex justify-between items-center"><span class="text-gray-500">Transport Mode:</span><span class="text-gray-900 font-bold" id="deal-transport-mode">Direct Road Transport</span></div>
            </div>
          </div>

          <!-- Card C: Assigned Driver & Schedule -->
          <div class="bg-white rounded-xl border border-gray-200 p-6 space-y-4 shadow-xs">
            <div class="flex items-center justify-between border-b border-gray-100 pb-3">
              <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">Driver & Schedule SLA</span>
              <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">SLA Active</span>
            </div>
            <div class="space-y-3 text-xs">
              <div class="flex justify-between items-center"><span class="text-gray-500">Assigned Driver:</span><strong class="text-gray-900" id="deal-driver-name">Kasper Kovelund</strong></div>
              <div class="flex justify-between items-center"><span class="text-gray-500">Driver Phone:</span><span class="font-mono text-gray-700" id="deal-driver-phone">+49 170 00000</span></div>
              <div class="flex justify-between items-center"><span class="text-gray-500">Duty Status:</span><span class="font-semibold text-emerald-700">Dispatch Confirmed</span></div>
              <div class="pt-2 border-t border-gray-100 flex justify-between items-center"><span class="text-gray-500">Pickup Window:</span><span class="font-mono text-gray-800" id="deal-pickup-window">2026-10-19 08:00</span></div>
              <div class="flex justify-between items-center"><span class="text-gray-500 font-bold">Promised Delivery:</span><strong class="font-mono text-amber-700" id="deal-delivery-deadline">2026-10-21 18:00</strong></div>
            </div>
          </div>
        </div>
      </div>

      <!-- ================= SUB-PAGE 2: ROUTE & LIVE MAP ================= -->
      <div id="car-subpage-route" class="hidden space-y-6">
        <div class="bg-white rounded-xl border border-gray-200 p-6 shadow-xs space-y-4">
          <div class="flex items-center justify-between border-b border-gray-100 pb-3">
            <div>
              <h3 class="text-sm font-bold text-gray-900">🗺️ Real-World European Highway Corridor</h3>
              <p class="text-xs text-gray-500">Direct driving geometry from OpenStreetMap OSRM routing engine.</p>
            </div>
            <!-- Map Legend -->
            <div class="flex items-center space-x-3 text-xs font-medium bg-gray-50 px-3 py-1.5 rounded-lg border border-gray-200">
              <span class="flex items-center space-x-1"><span class="w-2.5 h-2.5 rounded-full bg-blue-600"></span><span>Start</span></span>
              <span class="flex items-center space-x-1"><span class="w-3 h-1 bg-blue-600 rounded"></span><span>Route Done</span></span>
              <span class="flex items-center space-x-1"><span class="w-2.5 h-2.5 rounded-full bg-rose-600 pulse-urgent"></span><span>Car Here Now</span></span>
              <span class="flex items-center space-x-1"><span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span><span>Intermediate Stops</span></span>
              <span class="flex items-center space-x-1"><span class="w-3 h-1 border-t-2 border-dashed border-amber-500"></span><span>Remaining Route</span></span>
              <span class="flex items-center space-x-1"><span class="w-2.5 h-2.5 rounded-full bg-emerald-600"></span><span>Destination</span></span>
            </div>
          </div>

          <div id="leaflet-map-container" class="w-full h-[450px] rounded-xl border border-gray-200 bg-gray-100 relative z-0"></div>

          <!-- Route Milestones & Waypoints Table -->
          <div class="border border-gray-200 rounded-xl overflow-hidden mt-4">
            <table class="w-full text-left text-xs border-collapse">
              <thead class="bg-gray-50 text-gray-500 font-bold uppercase text-[10px] border-b border-gray-200">
                <tr>
                  <th class="p-3 pl-4">Stop / Milestone</th>
                  <th class="p-3">Role</th>
                  <th class="p-3">Status</th>
                  <th class="p-3">Estimated Time</th>
                  <th class="p-3 pr-4">Operational Notes</th>
                </tr>
              </thead>
              <tbody id="route-waypoints-tbody" class="divide-y divide-gray-100"></tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- ================= SUB-PAGE 3: DOCUMENTS & PROOFS ================= -->
      <div id="car-subpage-docs" class="hidden space-y-6">
        <div class="bg-white rounded-xl border border-gray-200 p-6 shadow-xs space-y-6">
          <div>
            <h3 class="text-sm font-bold text-gray-900">📄 Legal Documents, Inspection Proofs & Receipts</h3>
            <p class="text-xs text-gray-500">Complete records from attachments dataset (30 PDFs, 16 inspection photos, 12 receipts).</p>
          </div>

          <!-- Section A: Legal Documents -->
          <div class="space-y-3">
            <div class="flex items-center justify-between text-xs font-bold text-gray-700 uppercase tracking-wide border-b border-gray-100 pb-2">
              <span class="flex items-center space-x-1.5"><i data-lucide="file-text" class="w-4 h-4 text-blue-600"></i><span>Signed Legal Transport Documents (CMR & Gate Releases)</span></span>
              <span id="badge-docs-count" class="text-gray-400 font-mono text-[11px]">1 Legal Documents</span>
            </div>
            <div id="dossier-legal-docs-grid" class="grid grid-cols-3 gap-4"></div>
          </div>

          <!-- Section B: Inspection Photos -->
          <div class="space-y-3 pt-3">
            <div class="flex items-center justify-between text-xs font-bold text-gray-700 uppercase tracking-wide border-b border-gray-100 pb-2">
              <span class="flex items-center space-x-1.5"><i data-lucide="camera" class="w-4 h-4 text-emerald-600"></i><span>Physical Inspection Photos & Handover Verification</span></span>
              <span id="badge-photos-count" class="text-gray-400 font-mono text-[11px]">1 Photos on File</span>
            </div>
            <div id="dossier-photos-grid" class="grid grid-cols-3 gap-4"></div>
          </div>

          <!-- Section C: Trip Expenses & Receipts -->
          <div class="space-y-3 pt-3">
            <div class="flex items-center justify-between text-xs font-bold text-gray-700 uppercase tracking-wide border-b border-gray-100 pb-2">
              <span class="flex items-center space-x-1.5"><i data-lucide="receipt" class="w-4 h-4 text-amber-600"></i><span>Trip Expenses & Fuel/Toll Receipts</span></span>
              <span id="badge-expenses-count" class="text-gray-400 font-mono text-[11px]">0 Expense Items</span>
            </div>
            <div class="border border-gray-200 rounded-xl overflow-hidden">
              <table class="w-full text-left text-xs border-collapse">
                <thead class="bg-gray-50 text-gray-500 font-bold uppercase text-[10px] border-b border-gray-200">
                  <tr>
                    <th class="p-3 pl-4">Category</th>
                    <th class="p-3">Vendor / Payee</th>
                    <th class="p-3">Amount</th>
                    <th class="p-3">Status</th>
                    <th class="p-3 pr-4 text-right">Proof File</th>
                  </tr>
                </thead>
                <tbody id="dossier-expenses-list" class="divide-y divide-gray-100"></tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- ================= SUB-PAGE 4: FERRY & SEA (CONDITIONAL) ================= -->
      <div id="car-subpage-ferry" class="hidden space-y-6">
        <div class="bg-white rounded-xl border border-gray-200 p-6 shadow-xs space-y-4">
          <div class="flex items-center justify-between border-b border-gray-100 pb-3">
            <div>
              <h3 class="text-sm font-bold text-gray-900">⚓ Maritime Passage & Ferry Booking</h3>
              <p class="text-xs text-gray-500">Scheduled sea crossing via Baltic RoRo ferry.</p>
            </div>
            <span class="px-2.5 py-1 rounded-full text-xs font-bold bg-blue-100 text-blue-900">29h Baltic Sea Crossing</span>
          </div>

          <div class="grid grid-cols-2 gap-6 text-xs">
            <!-- Booked Sailing Card -->
            <div class="p-5 rounded-xl border border-blue-200 bg-blue-50/50 space-y-3">
              <span class="text-[11px] font-bold text-blue-900 uppercase tracking-wide">Current Active Reservation</span>
              <div id="travel-booked-list" class="space-y-3"></div>
            </div>

            <!-- Alternate Rebooking Options Card -->
            <div class="p-5 rounded-xl border border-amber-200 bg-amber-50/50 space-y-3">
              <span class="text-[11px] font-bold text-amber-900 uppercase tracking-wide">Alternative Rebooking Quotes Available</span>
              <div id="travel-options-list" class="space-y-3"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- ================= SUB-PAGE 5: COMMUNICATIONS ================= -->
      <div id="car-subpage-chat" class="hidden space-y-6">
        <div class="bg-white rounded-xl border border-gray-200 p-6 shadow-xs space-y-4">
          <div class="flex items-center justify-between border-b border-gray-100 pb-3">
            <div>
              <h3 class="text-sm font-bold text-gray-900">💬 Operational Communication Log</h3>
              <p class="text-xs text-gray-500">Live dataset feed from messages.jsonl & driver mobile app.</p>
            </div>
            <span class="text-[11px] font-bold text-gray-400 uppercase">Strict Human Sign-off Policy</span>
          </div>

          <!-- Message History Container -->
          <div id="dossier-chat-stream" class="space-y-3 max-h-[420px] overflow-y-auto custom-scrollbar p-4 bg-gray-50 rounded-xl border border-gray-200"></div>

          <!-- Directive Draft Input -->
          <div class="flex items-center space-x-3 pt-2">
            <input type="text" id="directive-input" placeholder="Type verified dispatch instruction to driver or dealer..." class="flex-1 px-4 py-2.5 border border-gray-300 rounded-xl text-xs focus:outline-none focus:border-amber-500">
            <button onclick="stageCustomDirective()" class="px-5 py-2.5 bg-gray-900 hover:bg-black text-white text-xs font-bold rounded-xl transition flex items-center space-x-2 shadow-xs">
              <i data-lucide="send" class="w-3.5 h-3.5"></i>
              <span>Send Directive</span>
            </button>
          </div>
        </div>
      </div>

      <!-- ================= SUB-PAGE 6: OPERATOR ACTIONS ================= -->
      <div id="car-subpage-actions" class="hidden space-y-6">
        <div class="bg-white rounded-xl border-2 border-amber-400 p-6 shadow-sm space-y-4">
          <div class="flex items-center justify-between border-b border-gray-100 pb-3">
            <div class="flex items-center space-x-2">
              <span class="text-base font-bold text-gray-900">⚡ Available Operator Action Decisions</span>
            </div>
            <span class="text-xs text-gray-500 font-mono">Signed as: <strong class="text-gray-900" id="decision-operator-label">OP-042</strong></span>
          </div>

          <div id="operator-actions-container" class="grid grid-cols-2 gap-4"></div>
        </div>
      </div>

    </div>
  </div>

  <!-- ================= VIEW 3: SUPPORT INBOX ================= -->
  <div id="view-inbox" class="hidden flex-1 overflow-y-auto custom-scrollbar p-8 bg-[#F8F9FA]">
    <div class="max-w-5xl mx-auto space-y-6">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-lg font-black text-gray-900 flex items-center space-x-2">
            <i data-lucide="inbox" class="w-5 h-5 text-amber-500"></i>
            <span>Support Communications Inbox</span>
          </h2>
          <p class="text-xs text-gray-500 mt-0.5">Driver queries, expense payout questions, and dealer document requests</p>
        </div>
        <div class="flex items-center space-x-2">
          <span class="px-3 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-900">5 Active Inquiries</span>
          <span class="px-3 py-1 rounded-full text-xs font-bold bg-rose-100 text-rose-800">4 Open Unresolved</span>
        </div>
      </div>

      <!-- What is this inbox banner -->
      <div class="bg-blue-50 border border-blue-200 rounded-xl p-4 flex items-start space-x-3 text-xs text-blue-900">
        <i data-lucide="help-circle" class="w-5 h-5 text-blue-600 shrink-0 mt-0.5"></i>
        <div class="space-y-1">
          <h4 class="font-bold">Why do we have a Support Inbox & What is it for?</h4>
          <p class="text-blue-800 leading-relaxed">
            In freight operations, freelance drivers and dealerships send questions via the driver app or direct email. For example, driver Tobias messages asking whether to start his duty at 10:00, or a dealership asks for a signed CMR waybill. When an inquiry doesn't belong to a single closed vehicle, it arrives in this Support Inbox so the dispatch operator can triage it, link it to the correct car, and confirm directives safely.
          </p>
        </div>
      </div>

      <div id="support-inbox-threads-list" class="space-y-4"></div>
    </div>
  </div>

  <!-- ================= VIEW 4: OPERATIONS AUDIT LOG ================= -->
  <div id="view-history" class="hidden flex-1 overflow-y-auto custom-scrollbar p-8 bg-[#F8F9FA]">
    <div class="max-w-6xl mx-auto space-y-6">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-lg font-black text-gray-900 flex items-center space-x-2">
            <i data-lucide="history" class="w-5 h-5 text-amber-500"></i>
            <span>Global Operations Audit Log</span>
          </h2>
          <p class="text-xs text-gray-500 mt-0.5">Immutable record of every operator action, autonomous proposal, and verified milestone</p>
        </div>
        <button onclick="exportAuditLog()" class="px-3.5 py-1.5 bg-white border border-gray-300 hover:bg-gray-50 text-gray-700 rounded-lg text-xs font-bold transition flex items-center space-x-1.5 shadow-xs">
          <i data-lucide="download" class="w-3.5 h-3.5"></i>
          <span>Export JSON</span>
        </button>
      </div>

      <div class="bg-white rounded-xl border border-gray-200 shadow-xs overflow-hidden">
        <table class="w-full text-left text-xs border-collapse">
          <thead class="bg-gray-50 text-gray-500 font-bold uppercase text-[10px] border-b border-gray-200">
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

  <!-- ================= VIEW 5: FINANCIALS & EXPENSES ================= -->
  <div id="view-finance" class="hidden flex-1 overflow-y-auto custom-scrollbar p-8 bg-[#F8F9FA]">
    <div class="max-w-6xl mx-auto space-y-6">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-lg font-black text-gray-900 flex items-center space-x-2">
            <i data-lucide="link" class="w-5 h-5 text-amber-500"></i>
            <span>Fleet Financials & Trip Expenses</span>
          </h2>
          <p class="text-xs text-gray-500 mt-0.5">Itemized fuel, highway tolls, driver per diems, and gross margins</p>
        </div>
        <div class="flex items-center space-x-2">
          <span class="px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800">Reconciliation Active</span>
        </div>
      </div>

      <!-- Top Metrics Grid -->
      <div class="grid grid-cols-4 gap-4">
        <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-xs">
          <span class="text-gray-400 text-xs font-bold uppercase">Total Fleet Revenue</span>
          <div id="fin-total-revenue" class="text-2xl font-black text-gray-900 mt-1 font-mono">EUR 55,454.17</div>
          <span class="text-[11px] text-emerald-600 font-semibold mt-1 block">100 B2B Deliveries</span>
        </div>
        <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-xs">
          <span class="text-gray-400 text-xs font-bold uppercase">Driver Payouts</span>
          <div id="fin-driver-payouts" class="text-2xl font-black text-gray-900 mt-1 font-mono">EUR 31,561.00</div>
          <span class="text-[11px] text-gray-500 mt-1 block">Freelance Driver Fees</span>
        </div>
        <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-xs">
          <span class="text-gray-400 text-xs font-bold uppercase">Approved Expenses</span>
          <div id="fin-approved-expenses" class="text-2xl font-black text-amber-600 mt-1 font-mono">EUR 5,682.28</div>
          <span class="text-[11px] text-gray-500 mt-1 block">Fuel, Tolls & Lodging</span>
        </div>
        <div class="bg-white p-5 rounded-xl border border-gray-200 shadow-xs">
          <span class="text-gray-400 text-xs font-bold uppercase">Net Gross Margin</span>
          <div id="fin-net-margin" class="text-2xl font-black text-emerald-700 mt-1 font-mono">EUR 18,210.89</div>
          <span class="text-[11px] text-emerald-700 font-semibold mt-1 block">32.8% Operating Margin</span>
        </div>
      </div>

      <!-- Interactive Expenses Filter Controls -->
      <div class="bg-white rounded-xl border border-gray-200 p-4 shadow-xs flex items-center justify-between text-xs">
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-2">
            <span class="font-bold text-gray-500 uppercase">Category:</span>
            <select id="fin-filter-cat" onchange="filterFinancialsTable()" class="px-2.5 py-1.5 border border-gray-300 rounded-lg bg-gray-50 font-medium focus:outline-none focus:border-amber-500">
              <option value="all">All Categories</option>
              <option value="fuel">Fuel & Charging</option>
              <option value="toll">Highway Tolls</option>
              <option value="hotel">Hotel & Lodging</option>
              <option value="parking">Parking</option>
              <option value="train_positioning">Train / Positioning</option>
            </select>
          </div>
          <div class="flex items-center space-x-2">
            <span class="font-bold text-gray-500 uppercase">Status:</span>
            <select id="fin-filter-status" onchange="filterFinancialsTable()" class="px-2.5 py-1.5 border border-gray-300 rounded-lg bg-gray-50 font-medium focus:outline-none focus:border-amber-500">
              <option value="all">All Statuses</option>
              <option value="approved">Approved</option>
              <option value="submitted">Submitted (Open)</option>
              <option value="superseded">Superseded</option>
            </select>
          </div>
        </div>

        <div class="relative w-64">
          <input type="text" id="fin-search-order" oninput="filterFinancialsTable()" placeholder="Search order ref or payee..." class="w-full pl-8 pr-3 py-1.5 bg-gray-50 border border-gray-300 rounded-lg text-xs focus:outline-none focus:border-amber-500">
          <i data-lucide="search" class="w-3.5 h-3.5 text-gray-400 absolute left-2.5 top-2"></i>
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
              <th class="p-3.5">Vendor / Payee</th>
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

  <!-- ================= SLIDE-OVER AI ASSISTANT SIDEBAR ================= -->
  <div id="ai-sidebar-backdrop" onclick="closeAiSidebar()" class="hidden fixed inset-0 bg-black/40 backdrop-blur-xs z-40 transition-opacity"></div>

  <div id="ai-sidebar" class="fixed top-0 right-0 h-full w-[460px] bg-white border-l border-gray-200 shadow-2xl z-50 transform translate-x-full transition-transform duration-300 flex flex-col">
    <!-- Header with (i) Credit Info Button Inside per user request! -->
    <div class="p-4 bg-gray-900 text-white border-b border-gray-800 flex items-center justify-between shrink-0">
      <div class="flex items-center space-x-2.5">
        <div class="w-7 h-7 rounded-lg bg-purple-600 flex items-center justify-center text-white">
          <i data-lucide="bot" class="w-4 h-4"></i>
        </div>
        <div>
          <h3 class="font-bold text-xs text-white">AI Operations Assistant</h3>
          <p class="text-[10px] text-purple-300">Multi-Model Logistics Intelligence</p>
        </div>
      </div>
      <div class="flex items-center space-x-2">
        <!-- (i) Credit Info Button -->
        <button onclick="toggleInfoModal()" class="px-2.5 py-1 rounded-lg bg-gray-800 hover:bg-gray-700 border border-gray-700 text-amber-400 font-mono text-[11px] font-bold flex items-center space-x-1 transition" title="OpenRouter System Credits Info">
          <i data-lucide="info" class="w-3.5 h-3.5"></i>
          <span>$20.00 Credits</span>
        </button>
        <button onclick="closeAiSidebar()" class="p-1 text-gray-400 hover:text-white transition">
          <i data-lucide="x" class="w-4 h-4"></i>
        </button>
      </div>
    </div>

    <!-- AI Model Selector -->
    <div class="p-3 bg-gray-50 border-b border-gray-200 flex items-center justify-between text-xs shrink-0">
      <span class="font-bold text-gray-500 uppercase text-[10px]">AI Model:</span>
      <select id="ai-model-select" class="text-xs bg-white border border-gray-300 rounded-lg px-2.5 py-1 font-medium text-gray-800 focus:outline-none focus:border-purple-500">
        <option value="openai/gpt-4o-mini">OpenAI GPT-4o Mini</option>
        <option value="anthropic/claude-3.5-sonnet">Claude 3.5 Sonnet</option>
        <option value="google/gemini-1.5-flash">Gemini 1.5 Flash</option>
        <option value="deepseek/deepseek-chat">DeepSeek V3</option>
      </select>
    </div>

    <!-- Scope Selector: General AI (Fleet) vs Singular Car AI -->
    <div class="p-2.5 border-b border-gray-100 flex items-center space-x-2 bg-gray-100/70 text-xs shrink-0">
      <button id="ai-scope-fleet" onclick="setAiScope('fleet')" class="flex-1 py-1.5 rounded-md font-bold bg-white text-gray-900 shadow-xs transition text-center">
        Fleet Overview (100 Cars)
      </button>
      <button id="ai-scope-car" onclick="setAiScope('car')" class="flex-1 py-1.5 rounded-md font-medium text-gray-600 hover:text-gray-900 transition text-center">
        Car Focus (Select Car)
      </button>
    </div>

    <!-- Quick Question Suggestion Chips (User Request!) -->
    <div class="p-2.5 bg-purple-50/50 border-b border-purple-100 flex flex-wrap gap-1.5 shrink-0 text-[11px]">
      <button onclick="sendQuickPrompt('What happened to this car?')" class="px-2.5 py-1 rounded-full bg-white border border-purple-200 text-purple-900 hover:bg-purple-100 font-semibold transition">
        ⚡ What happened to this car?
      </button>
      <button onclick="sendQuickPrompt('Give me an overview of everything')" class="px-2.5 py-1 rounded-full bg-white border border-purple-200 text-purple-900 hover:bg-purple-100 font-semibold transition">
        📊 Overview of everything
      </button>
      <button onclick="sendQuickPrompt('Show active bottlenecks & actions')" class="px-2.5 py-1 rounded-full bg-white border border-purple-200 text-purple-900 hover:bg-purple-100 font-semibold transition">
        🚨 Active bottlenecks
      </button>
      <button onclick="sendQuickPrompt('Check CMR & documentation status')" class="px-2.5 py-1 rounded-full bg-white border border-purple-200 text-purple-900 hover:bg-purple-100 font-semibold transition">
        📄 Check CMR & proofs
      </button>
    </div>

    <!-- Chat Messages Feed -->
    <div id="ai-chat-messages" class="flex-1 overflow-y-auto custom-scrollbar p-4 space-y-3 bg-[#FAFBFD]">
      <div class="p-3.5 rounded-xl bg-purple-50 border border-purple-100 text-purple-950 text-xs space-y-1.5">
        <div class="flex items-center space-x-1.5 font-bold text-purple-800">
          <i data-lucide="sparkles" class="w-3.5 h-3.5"></i>
          <span>Welcome Operator OP-042</span>
        </div>
        <p class="leading-relaxed">
          I can analyze fleet delays, suggest optimal driver assignments, audit CMR paperwork, and verify roadside assistance plans. Click any quick question above or ask anything below.
        </p>
      </div>
    </div>

    <!-- Autonomous Resolution Agent Trigger Banner -->
    <div class="p-3 bg-amber-50 border-t border-amber-200 flex items-center justify-between shrink-0 text-xs">
      <div>
        <strong class="text-amber-950 block">Autonomous Resolution Agent</strong>
        <span class="text-[11px] text-amber-800">Triage 22 bottleneck orders instantly</span>
      </div>
      <button onclick="runSentinelAgent()" class="px-3 py-1.5 bg-amber-500 hover:bg-amber-600 text-black font-bold rounded-lg transition flex items-center space-x-1 shadow-xs">
        <i data-lucide="play" class="w-3.5 h-3.5"></i>
        <span>Run Dispatcher</span>
      </button>
    </div>

    <!-- Chat Prompt Input -->
    <div class="p-3 bg-white border-t border-gray-200 flex items-center space-x-2 shrink-0">
      <input type="text" id="ai-chat-input" onkeydown="if(event.key==='Enter') sendAiMessage()" placeholder="Ask AI about fleet bottlenecks, drivers, CMR docs..." class="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-xs focus:outline-none focus:border-purple-500">
      <button onclick="sendAiMessage()" class="p-2 rounded-lg bg-purple-600 hover:bg-purple-700 text-white transition">
        <i data-lucide="send" class="w-4 h-4"></i>
      </button>
    </div>
  </div>

  <!-- SYSTEM INFO / CREDITS MODAL -->
  <div id="info-modal" class="hidden fixed inset-0 z-[9999] bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl max-w-md w-full p-6 space-y-4 shadow-2xl border border-gray-200">
      <div class="flex items-center justify-between border-b border-gray-100 pb-3">
        <div class="flex items-center space-x-2">
          <i data-lucide="info" class="w-5 h-5 text-amber-500"></i>
          <span class="text-base font-bold text-gray-900">System & AI Credit Allocation</span>
        </div>
        <button onclick="toggleInfoModal()" class="p-1 rounded-lg hover:bg-gray-100 text-gray-400 hover:text-gray-700 transition">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <div class="space-y-3 text-xs leading-relaxed text-gray-600">
        <div class="p-3 bg-gray-50 rounded-xl border border-gray-200 space-y-1">
          <span class="font-bold text-gray-800 block text-xs">OpenRouter API Credits</span>
          <p class="text-gray-600 font-mono text-[11px]">Balance: <strong>$20.00 USD</strong></p>
          <p class="text-gray-500 text-[11px]">OpenRouter credits decrease by small fractions of a cent per query based on prompt tokens and model selected (e.g. GPT-4o Mini: $0.15 / 1M tokens).</p>
        </div>

        <div class="p-3 bg-gray-50 rounded-xl border border-gray-200 space-y-1">
          <span class="font-bold text-gray-800 block text-xs">AI Operations Dispatcher</span>
          <p class="text-gray-500 text-[11px]">The Autonomous Dispatcher runs automated bottleneck scans over all 100 orders, proposing concrete resolutions while keeping human sign-off mandatory before transmission.</p>
        </div>
      </div>

      <div class="flex justify-end pt-2">
        <button onclick="toggleInfoModal()" class="px-4 py-2 bg-gray-900 hover:bg-black text-white text-xs font-bold rounded-lg transition">Close</button>
      </div>
    </div>
  </div>

  <!-- APPLICATION JAVASCRIPT -->
  <script>
    let ordersList = [];
    let selectedOrderId = null;
    let selectedOrderData = null;
    let currentGlobalView = 'home';
    let currentCarSubTab = 'deal';
    let currentStatusFilter = 'all';
    let currentProblemFilter = 'all';
    let currentSort = 'newest';
    let searchQuery = '';
    let activeOperator = localStorage.getItem('bahn_operator_id') || 'OP-042';

    let allFinancialExpenses = [];

    // Map instances
    let leafletMap = null;
    let mapMarkers = [];
    let mapRouteLine = [];

    // 10s Undo Action State
    let pendingActionTimer = null;
    let pendingActionCountdown = 10;
    let pendingActionPayload = null;

    // AI sidebar state
    let aiCurrentScope = 'fleet';

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

      btnAll.className = status === 'all' ? 'px-3.5 py-1.5 rounded-md bg-white text-black font-bold shadow-xs whitespace-nowrap shrink-0' : 'px-3.5 py-1.5 rounded-md text-gray-600 hover:text-black transition whitespace-nowrap shrink-0';
      btnOk.className = status === 'ok' ? 'px-3.5 py-1.5 rounded-md bg-emerald-600 text-white font-bold shadow-xs flex items-center space-x-1.5 whitespace-nowrap shrink-0' : 'px-3.5 py-1.5 rounded-md text-emerald-800 hover:bg-white transition flex items-center space-x-1.5 whitespace-nowrap shrink-0';
      btnNotOk.className = status === 'not_ok' ? 'px-3.5 py-1.5 rounded-md bg-rose-600 text-white font-bold shadow-xs flex items-center space-x-1.5 whitespace-nowrap shrink-0' : 'px-3.5 py-1.5 rounded-md text-rose-700 hover:bg-white transition flex items-center space-x-1.5 whitespace-nowrap shrink-0';

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
                    <img src="${(v && v.image_url) ? v.image_url : '/static/bahn-logo.png'}" alt="Car" class="w-full h-full object-cover">
                  </div>
                  <div class="min-w-0">
                    <strong class="text-gray-900 font-bold block truncate">${v ? `${v.make} ${v.model}` : 'Unassigned'}</strong>
                    <span class="text-[11px] text-gray-500 font-mono">${(v && v.registration) ? v.registration : 'Plate Pending'}</span>
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

    // ================= CAR DETAIL SUB-PAGES / TABS =================
    function switchCarSubTab(tabKey) {
      currentCarSubTab = tabKey;
      const tabs = ['deal', 'route', 'docs', 'ferry', 'chat', 'actions'];

      tabs.forEach(t => {
        const pageEl = document.getElementById(`car-subpage-${t}`);
        const btnEl = document.getElementById(`car-tab-btn-${t}`);
        if (pageEl) pageEl.classList.toggle('hidden', t !== tabKey);
        if (btnEl) {
          if (t === tabKey) {
            btnEl.className = 'px-3.5 py-1.5 rounded-lg bg-amber-500 text-black font-bold shadow-xs flex items-center space-x-1.5 transition';
          } else {
            btnEl.className = 'px-3.5 py-1.5 rounded-lg text-gray-600 hover:bg-gray-100 font-medium flex items-center space-x-1.5 transition';
          }
        }
      });

      if (tabKey === 'route' && selectedOrderData) {
        setTimeout(() => {
          renderMapAndWaypoints(selectedOrderData.addresses.coordinates);
        }, 100);
      }
      lucide.createIcons();
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

      // Situation Alert Banner
      const alertBox = document.getElementById('detail-alert-box');
      if (att && att.needs_human) {
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

      document.getElementById('deal-veh-plate').innerText = (v && v.registration) ? v.registration : 'Plate Pending';
      document.getElementById('deal-veh-title').innerText = v ? `${v.make} ${v.model}` : 'Master Vehicle';
      document.getElementById('deal-veh-year').innerText = v ? `${v.model_year} Edition` : '2022 Fleet Edition';
      document.getElementById('deal-veh-vin').innerText = (v && v.vin) ? v.vin : (v && v.synthetic_vin ? v.synthetic_vin : 'WBA33AY0000000000');
      document.getElementById('deal-veh-fuel').innerText = v ? (v.fuel || v.fuel_type || 'Internal Combustion') : 'Petrol';
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
      const ferryBtn = document.getElementById('car-tab-btn-ferry');
      if (hasFerry) {
        ferryBtn.classList.remove('hidden');
        populateFerryData(data);
      } else {
        ferryBtn.classList.add('hidden');
      }

      // ================= 5. POPULATE CHAT =================
      populateChatFeed(data);

      // ================= 6. POPULATE OPERATOR ACTIONS =================
      populateOperatorActions(data);

      // Default to Sub-page 1: Deal
      switchCarSubTab('deal');
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
      if (status === 'ASSIGNED') activeIndex = 1;
      else if (status === 'WAITING_FOR_PICKUP' || status === 'WAITING_PICKUP') activeIndex = 2;
      else if (status === 'IN_TRANSIT') activeIndex = 3;
      else if (status === 'DELIVERED') activeIndex = 4;
      else if (lane === 'delivered') activeIndex = 4;
      else if (lane === 'in_transit') activeIndex = 3;

      stepper.innerHTML = steps.map((s, idx) => {
        let stateStyle = 'bg-gray-100 text-gray-400 border-gray-200';
        if (idx < activeIndex) {
          stateStyle = 'bg-emerald-50 text-emerald-800 border-emerald-300 font-semibold';
        } else if (idx === activeIndex) {
          stateStyle = 'bg-amber-400 text-black border-amber-500 font-bold shadow-xs';
        }
        return `
          <div class="p-2.5 rounded-lg border text-center transition ${stateStyle}">
            ${s.label}
          </div>
        `;
      }).join('');
    }

    function renderMapAndWaypoints(coords) {
      if (!coords) return;
      const container = document.getElementById('leaflet-map-container');
      if (!container) return;

      if (!leafletMap) {
        leafletMap = L.map('leaflet-map-container', { zoomControl: true }).setView([54.0, 14.0], 5);
        L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
          maxZoom: 18,
          attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
        }).addTo(leafletMap);
      }

      mapMarkers.forEach(m => m.remove());
      mapRouteLine.forEach(l => l.remove());
      mapMarkers = [];
      mapRouteLine = [];

      const pCoords = coords.pickup || [48.1351, 11.5820];
      const dCoords = coords.delivery || [60.1699, 24.9384];
      const carCoords = coords.current_estimated || pCoords;

      const markerOrigin = L.circleMarker(pCoords, {
        radius: 7,
        fillColor: '#2563EB',
        color: '#ffffff',
        weight: 2,
        fillOpacity: 1
      }).addTo(leafletMap).bindTooltip(`<strong>Start:</strong> ${coords.pickup_city || 'Origin'}`, { className: 'custom-hover-tip' });
      mapMarkers.push(markerOrigin);

      const markerDest = L.circleMarker(dCoords, {
        radius: 7,
        fillColor: '#059669',
        color: '#ffffff',
        weight: 2,
        fillOpacity: 1
      }).addTo(leafletMap).bindTooltip(`<strong>Destination:</strong> ${coords.delivery_city || 'Destination'}`, { className: 'custom-hover-tip' });
      mapMarkers.push(markerDest);

      const carIconHtml = `
        <div class="relative flex items-center justify-center">
          <span class="absolute w-6 h-6 rounded-full bg-rose-500/40 animate-ping"></span>
          <span class="w-3.5 h-3.5 rounded-full bg-rose-600 border-2 border-white shadow-md"></span>
        </div>
      `;
      const carIcon = L.divIcon({ html: carIconHtml, className: 'car-live-pin', iconSize: [24, 24], iconAnchor: [12, 12] });
      const markerCar = L.marker(carCoords, { icon: carIcon }).addTo(leafletMap)
        .bindTooltip(`<strong>Live Car Position</strong><br>${coords.current_status_text || 'Active Vehicle Telemetry'}`, { className: 'custom-hover-tip', permanent: false });
      mapMarkers.push(markerCar);

      (coords.intermediate_stops || []).forEach(st => {
        const sm = L.circleMarker(st.coords, {
          radius: 5.5,
          fillColor: '#F59E0B',
          color: '#ffffff',
          weight: 2,
          fillOpacity: 1
        }).addTo(leafletMap).bindTooltip(`<strong>Stop:</strong> ${st.name}<br>${st.notes || ''}`, { className: 'custom-hover-tip' });
        mapMarkers.push(sm);
      });

      if (coords.driven_geometry && coords.driven_geometry.length > 1) {
        const lineDone = L.polyline(coords.driven_geometry, { color: '#2563EB', weight: 4.5, opacity: 0.9 }).addTo(leafletMap);
        mapRouteLine.push(lineDone);
      }
      if (coords.remaining_geometry && coords.remaining_geometry.length > 1) {
        const lineRemaining = L.polyline(coords.remaining_geometry, { color: '#F59E0B', weight: 4, opacity: 0.9, dashArray: '6, 8' }).addTo(leafletMap);
        mapRouteLine.push(lineRemaining);
      } else if (coords.road_geometry && coords.road_geometry.length > 1) {
        const fullLine = L.polyline(coords.road_geometry, { color: '#2563EB', weight: 4, opacity: 0.85 }).addTo(leafletMap);
        mapRouteLine.push(fullLine);
      }

      const allPts = [pCoords, dCoords, carCoords].concat((coords.intermediate_stops || []).map(s => s.coords));
      leafletMap.fitBounds(L.latLngBounds(allPts), { padding: [40, 40] });
      leafletMap.invalidateSize();

      // Populate Waypoints Table
      const wpTbody = document.getElementById('route-waypoints-tbody');
      let wpHtml = '';
      (coords.waypoints || []).forEach(w => {
        wpHtml += `
          <tr class="hover:bg-gray-50 transition">
            <td class="p-3 pl-4 font-bold text-gray-900">${escapeHtml(w.name)}</td>
            <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-bold ${w.type === 'origin' ? 'bg-blue-100 text-blue-800' : w.type === 'destination' ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'}">${w.type.toUpperCase()}</span></td>
            <td class="p-3 text-gray-700">${escapeHtml(w.status)}</td>
            <td class="p-3 font-mono text-gray-500">${escapeHtml(w.time)}</td>
            <td class="p-3 pr-4 text-gray-600">${escapeHtml(w.notes || '-')}</td>
          </tr>
        `;
      });
      wpTbody.innerHTML = wpHtml;
    }

    function populateDocumentsAndProofs(data) {
      const docsGrid = document.getElementById('dossier-legal-docs-grid');
      const photosGrid = document.getElementById('dossier-photos-grid');
      const expList = document.getElementById('dossier-expenses-list');

      document.getElementById('badge-docs-count').innerText = `${data.documents ? data.documents.length : 0} Legal Documents`;
      document.getElementById('badge-photos-count').innerText = `${data.proofs ? data.proofs.length : 0} Photos on File`;
      document.getElementById('badge-expenses-count').innerText = `${data.expenses ? data.expenses.length : 0} Expense Items`;

      // Legal Docs
      let docsHtml = '';
      (data.documents || []).forEach(doc => {
        docsHtml += `
          <div class="p-4 rounded-xl border border-gray-200 bg-gray-50/70 space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-mono uppercase font-bold text-gray-400">${doc.kind}</span>
              <span class="px-2 py-0.5 rounded text-[10px] font-bold ${doc.status === 'PREPARED' || doc.status === 'ACTIVE' ? 'bg-amber-100 text-amber-800' : 'bg-emerald-100 text-emerald-800'}">${doc.status}</span>
            </div>
            <div>
              <strong class="text-xs text-gray-900 block font-bold">${escapeHtml(doc.title)}</strong>
              <span class="text-[11px] text-gray-500 block mt-0.5">Format: ${doc.format} - Mandatory</span>
            </div>
            <button onclick="openUniversalFileModal('${doc.file_url || ''}', '${escapeAttr(doc.title)}', 'application/pdf', {id: '${doc.id}', kind: '${doc.kind}', status: '${doc.status}'})" class="w-full py-2 bg-white hover:bg-gray-100 text-gray-800 border border-gray-300 rounded-lg text-xs font-bold transition flex items-center justify-center space-x-1.5 shadow-2xs">
              <i data-lucide="file-check" class="w-3.5 h-3.5 text-blue-600"></i>
              <span>View Certified Record</span>
            </button>
          </div>
        `;
      });
      docsGrid.innerHTML = docsHtml || `<div class="col-span-3 p-4 text-center text-gray-400 text-xs">No formal documents registered.</div>`;

      // Photos
      let photosHtml = '';
      (data.proofs || []).forEach(p => {
        photosHtml += `
          <div class="p-4 rounded-xl border border-gray-200 bg-gray-50/70 space-y-3">
            <div class="w-full h-32 rounded-lg bg-gray-200 overflow-hidden relative cursor-pointer" onclick="openUniversalFileModal('${p.file_url || ''}', '${escapeAttr(p.label)}', 'image/jpeg', {id: '${p.id}', kind: '${p.kind}'})">
              <img src="${p.file_url || '/static/bahn-logo.png'}" alt="Proof" class="w-full h-full object-cover hover:scale-105 transition duration-300">
              <span class="absolute bottom-2 right-2 px-2 py-0.5 rounded bg-black/70 text-white text-[10px] font-mono">Inspect</span>
            </div>
            <div>
              <strong class="text-xs text-gray-900 block font-bold truncate">${escapeHtml(p.label)}</strong>
              <span class="text-[11px] text-gray-500 block">${p.notes || 'Condition check photo on file'}</span>
            </div>
          </div>
        `;
      });
      photosGrid.innerHTML = photosHtml || `<div class="col-span-3 p-4 text-center text-gray-400 text-xs">No physical condition photos uploaded yet.</div>`;

      // Expenses
      let expHtml = '';
      (data.expenses || []).forEach(ex => {
        expHtml += `
          <tr class="hover:bg-gray-50 transition">
            <td class="p-3 pl-4 font-bold text-gray-900">${ex.kind}</td>
            <td class="p-3 text-gray-700">${ex.vendor || 'Authorized Provider'}</td>
            <td class="p-3 font-mono font-bold text-gray-900">${ex.amount} ${ex.currency}</td>
            <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-bold ${ex.status === 'APPROVED' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}">${ex.status}</span></td>
            <td class="p-3 pr-4 text-right">
              <button onclick="openUniversalFileModal('${ex.receipt_url || ''}', '${escapeAttr(ex.kind)} Receipt Proof', 'application/pdf', {id: '${ex.id}', kind: '${ex.kind}', status: '${ex.status}'})" class="px-2.5 py-1 bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-200 rounded text-[11px] font-bold inline-flex items-center space-x-1 transition">
                <i data-lucide="receipt" class="w-3.5 h-3.5"></i>
                <span>View Receipt</span>
              </button>
            </td>
          </tr>
        `;
      });
      expList.innerHTML = expHtml || `<tr><td colspan="5" class="p-4 text-center text-gray-400 text-xs">No reimbursable trip expenses logged for this order.</td></tr>`;
    }

    function populateFerryData(data) {
      const bookedCont = document.getElementById('travel-booked-list');
      const optCont = document.getElementById('travel-options-list');

      let bHtml = '';
      (data.travel_reservations || []).forEach(tr => {
        bHtml += `
          <div class="bg-white p-4 rounded-xl border border-blue-200 space-y-2 shadow-2xs">
            <div class="flex items-center justify-between">
              <strong class="text-xs text-blue-950 font-bold">${tr.provider} ${tr.kind}</strong>
              <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-100 text-blue-800">${tr.status}</span>
            </div>
            <p class="text-xs text-gray-700">${escapeHtml(tr.route || 'Travemünde -> Helsinki Vuosaari')}</p>
            <div class="text-[11px] text-gray-500 font-mono">
              Departure: <strong>${tr.departure_time ? tr.departure_time.replace('T', ' ').slice(0, 16) : 'Scheduled'}</strong>
            </div>
          </div>
        `;
      });
      bookedCont.innerHTML = bHtml || `<div class="p-3 text-center text-gray-400 text-xs">No confirmed ferry booking held.</div>`;

      let oHtml = '';
      (data.travel_options || []).forEach(opt => {
        oHtml += `
          <div class="bg-white p-4 rounded-xl border border-amber-200 space-y-2 shadow-2xs">
            <div class="flex items-center justify-between">
              <strong class="text-xs text-amber-950 font-bold">${opt.provider} Rebooking Quote</strong>
              <span class="font-mono font-bold text-xs text-amber-800">EUR ${opt.cost_eur || '220.00'}</span>
            </div>
            <p class="text-xs text-gray-700">${escapeHtml(opt.description || 'Next available RoRo sailing departure')}</p>
            <div class="pt-2 flex items-center justify-between">
              <span class="text-[11px] text-gray-500 font-mono">${opt.departure_time ? opt.departure_time.replace('T', ' ').slice(0, 16) : 'Next Day 22:00'}</span>
              <button onclick="requestActionWithUndo('ACCEPT_FERRY_QUOTE_${opt.id}', 'Accept Next-Day Ferry Rebooking Quote', 'Confirm Ferry Rebooking (+EUR ${opt.cost_eur || 220})')" class="px-3 py-1.5 bg-amber-400 hover:bg-amber-500 text-black font-bold text-xs rounded-lg transition shadow-2xs">
                Approve Rebooking
              </button>
            </div>
          </div>
        `;
      });
      optCont.innerHTML = oHtml || `<div class="p-3 text-center text-gray-400 text-xs">No active rebooking quotes required.</div>`;
    }

    function populateChatFeed(data) {
      const feed = document.getElementById('dossier-chat-stream');
      let html = '';

      (data.messages || []).forEach(m => {
        const isOperator = m.author_type === 'operator';
        const isDriver = m.author_type === 'driver';
        const isCust = m.author_type === 'customer';

        let badgeClass = 'bg-gray-200 text-gray-800';
        let bubbleClass = 'bg-white border border-gray-200 text-gray-800 mr-8';

        if (isOperator) {
          badgeClass = 'bg-amber-400 text-black';
          bubbleClass = 'bg-[#121417] text-white ml-8 border border-gray-800';
        } else if (isCust) {
          badgeClass = 'bg-purple-100 text-purple-900 border border-purple-300';
          bubbleClass = 'bg-purple-50/70 border border-purple-200 text-purple-950 mr-8';
        } else if (isDriver) {
          badgeClass = 'bg-blue-100 text-blue-900 border border-blue-300';
          bubbleClass = 'bg-blue-50/60 border border-blue-200 text-blue-950 mr-8';
        }

        html += `
          <div class="p-3 rounded-xl text-xs space-y-1 shadow-2xs ${bubbleClass}">
            <div class="flex items-center space-x-2 font-bold text-[10px] uppercase tracking-wide">
              <span class="px-1.5 py-0.5 rounded ${badgeClass}">${m.author_type}</span>
              <span class="${isOperator ? 'text-gray-300' : 'text-gray-600'}">${escapeHtml(m.author_name || m.author_type)}</span>
              <span class="ml-auto font-mono ${isOperator ? 'text-gray-400' : 'text-gray-400'}">${m.created_at ? m.created_at.replace('T', ' ').slice(0, 16) : ''}</span>
            </div>
            <p class="leading-relaxed ${isOperator ? 'text-gray-100' : 'text-gray-800'}">${escapeHtml(m.body)}</p>
          </div>
        `;
      });

      feed.innerHTML = html || `<div class="p-6 text-center text-gray-400 text-xs">No active dispatch conversation records.</div>`;
      feed.scrollTop = feed.scrollHeight;
    }

    function populateOperatorActions(data) {
      const container = document.getElementById('operator-actions-container');
      const decisions = data.decisions || [];

      if (decisions.length === 0) {
        container.innerHTML = `<div class="col-span-2 p-6 text-center text-gray-400 text-xs">All standard operating conditions satisfied. No manual interventions staged.</div>`;
        return;
      }

      let html = '';
      decisions.forEach((dec, idx) => {
        html += `
          <div class="p-4 bg-gray-50 rounded-xl border border-gray-200 space-y-3">
            <div class="flex items-center justify-between">
              <strong class="text-xs font-bold text-gray-900">${escapeHtml(dec.title)}</strong>
              <span class="px-2 py-0.5 rounded text-[10px] font-bold ${dec.type === 'APPROVAL' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}">${dec.type}</span>
            </div>
            <p class="text-xs text-gray-600 leading-relaxed">${escapeHtml(dec.description)}</p>
            <div class="flex items-center space-x-2 pt-1">
              <button onclick="requestActionWithUndo('${dec.id}', '${escapeAttr(dec.title)}', '${escapeAttr(dec.description)}')" class="flex-1 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-lg transition shadow-2xs flex items-center justify-center space-x-1.5">
                <i data-lucide="check-circle-2" class="w-3.5 h-3.5"></i>
                <span>Confirm Action (10s Undo)</span>
              </button>
              <button onclick="openModifyActionModal('${dec.id}', '${escapeAttr(dec.title)}', '${escapeAttr(dec.description)}')" class="px-3 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold text-xs rounded-lg transition flex items-center space-x-1">
                <i data-lucide="edit-3" class="w-3.5 h-3.5"></i>
                <span>Modify</span>
              </button>
            </div>
          </div>
        `;
      });
      container.innerHTML = html;
      lucide.createIcons();
    }

    // ================= ACTION MODIFICATION & 10S UNDO LOGIC =================
    function requestActionWithUndo(actionId, title, description) {
      if (pendingActionTimer) clearTimeout(pendingActionTimer);

      pendingActionPayload = {
        actionId: actionId,
        title: title,
        description: description,
        orderId: selectedOrderId
      };

      pendingActionCountdown = 10;
      const bar = document.getElementById('action-undo-bar');
      document.getElementById('undo-action-title').innerText = title;
      document.getElementById('undo-countdown-sec').innerText = `${pendingActionCountdown}s`;
      document.getElementById('undo-progress-bar').style.width = '100%';

      bar.classList.remove('hidden');

      pendingActionTimer = setInterval(() => {
        pendingActionCountdown--;
        document.getElementById('undo-countdown-sec').innerText = `${pendingActionCountdown}s`;
        document.getElementById('undo-progress-bar').style.width = `${(pendingActionCountdown / 10) * 100}%`;

        if (pendingActionCountdown <= 0) {
          clearInterval(pendingActionTimer);
          pendingActionTimer = null;
          commitPendingAction();
        }
      }, 1000);
    }

    function cancelPendingAction() {
      if (pendingActionTimer) {
        clearInterval(pendingActionTimer);
        pendingActionTimer = null;
      }
      document.getElementById('action-undo-bar').classList.add('hidden');
      showToast('Action Cancelled', 'Staged action was cancelled and not executed.');
    }

    function executePendingActionNow() {
      if (pendingActionTimer) {
        clearInterval(pendingActionTimer);
        pendingActionTimer = null;
      }
      commitPendingAction();
    }

    async function commitPendingAction() {
      document.getElementById('action-undo-bar').classList.add('hidden');
      if (!pendingActionPayload) return;

      const payload = pendingActionPayload;
      try {
        const res = await fetch(`/api/orders/${payload.orderId || 'general'}/decision`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            decision_id: payload.actionId,
            operator_id: activeOperator,
            action_type: payload.actionId,
            notes: payload.description
          })
        });
        showToast('Action Executed & Signed', `Decision signed by ${activeOperator}. Registered to audit log.`);
        refreshData();
        if (selectedOrderId) openCarDetail(selectedOrderId);
      } catch (e) {
        showToast('Error', 'Failed executing action.');
      }
      pendingActionPayload = null;
    }

    function openModifyActionModal(actionId, title, description) {
      if (pendingActionTimer) {
        clearInterval(pendingActionTimer);
        pendingActionTimer = null;
        document.getElementById('action-undo-bar').classList.add('hidden');
      }

      pendingActionPayload = {
        actionId: actionId,
        title: title,
        description: description,
        orderId: selectedOrderId
      };

      document.getElementById('modify-action-title').value = title;
      document.getElementById('modify-action-notes').value = description;
      document.getElementById('modify-action-time').value = '2026-10-22 14:00';
      document.getElementById('modify-action-budget').value = '250';
      document.getElementById('action-modify-modal').classList.remove('hidden');
    }

    function closeModifyModal() {
      document.getElementById('action-modify-modal').classList.add('hidden');
    }

    function saveAndApplyModifiedAction() {
      const title = document.getElementById('modify-action-title').value;
      const notes = document.getElementById('modify-action-notes').value;
      const time = document.getElementById('modify-action-time').value;
      const budget = document.getElementById('modify-action-budget').value;

      closeModifyModal();
      const updatedDesc = `${notes} | Adjusted Time: ${time} | Budget Limit: EUR ${budget}`;
      requestActionWithUndo(pendingActionPayload.actionId, `[Modified] ${title}`, updatedDesc);
    }

    function modifyPendingAction() {
      if (pendingActionPayload) {
        openModifyActionModal(pendingActionPayload.actionId, pendingActionPayload.title, pendingActionPayload.description);
      }
    }

    function stageCustomDirective() {
      const input = document.getElementById('directive-input');
      const val = input.value.trim();
      if (!val) return;
      input.value = '';
      requestActionWithUndo('CUSTOM_DIRECTIVE', 'Send Custom Dispatch Directive', val);
    }

    // ================= UNIVERSAL FILE MODAL =================
    function openUniversalFileModal(url, title, contentType, meta) {
      const modal = document.getElementById('universal-file-modal');
      const frame = document.getElementById('file-modal-iframe');
      const img = document.getElementById('file-modal-image');
      const fallback = document.getElementById('file-modal-fallback');
      const titleEl = document.getElementById('file-modal-title');
      const openTabBtn = document.getElementById('file-modal-open-tab');
      const fallbackLink = document.getElementById('file-modal-fallback-link');

      titleEl.innerText = title || 'Document Inspection Record';
      openTabBtn.href = url || '#';
      fallbackLink.href = url || '#';

      const isPdf = url.endsWith('.pdf') || (contentType && contentType.includes('pdf'));

      if (isPdf) {
        frame.src = url;
        frame.classList.remove('hidden');
        img.classList.add('hidden');
        fallback.classList.add('hidden');
      } else if (url && (url.endsWith('.jpg') || url.endsWith('.jpeg') || url.endsWith('.png') || url.endsWith('.webp'))) {
        img.src = url;
        img.classList.remove('hidden');
        frame.classList.add('hidden');
        fallback.classList.add('hidden');
      } else {
        frame.classList.add('hidden');
        img.classList.add('hidden');
        fallback.classList.remove('hidden');
      }

      modal.classList.remove('hidden');
      lucide.createIcons();
    }

    function closeUniversalFileModal() {
      const modal = document.getElementById('universal-file-modal');
      const frame = document.getElementById('file-modal-iframe');
      frame.src = '';
      modal.classList.add('hidden');
    }

    // ================= AI SIDEBAR & CHAT =================
    function toggleAiSidebar() {
      const sb = document.getElementById('ai-sidebar');
      const backdrop = document.getElementById('ai-sidebar-backdrop');
      const isClosed = sb.classList.contains('translate-x-full');
      if (isClosed) {
        sb.classList.remove('translate-x-full');
        backdrop.classList.remove('hidden');
      } else {
        sb.classList.add('translate-x-full');
        backdrop.classList.add('hidden');
      }
      lucide.createIcons();
    }

    function openAiSidebar() {
      document.getElementById('ai-sidebar').classList.remove('translate-x-full');
      document.getElementById('ai-sidebar-backdrop').classList.remove('hidden');
      lucide.createIcons();
    }

    function closeAiSidebar() {
      document.getElementById('ai-sidebar').classList.add('translate-x-full');
      document.getElementById('ai-sidebar-backdrop').classList.add('hidden');
    }

    function openAiSidebarForCar() {
      openAiSidebar();
      setAiScope('car');
    }

    function setAiScope(scope) {
      aiCurrentScope = scope;
      const btnFleet = document.getElementById('ai-scope-fleet');
      const btnCar = document.getElementById('ai-scope-car');

      if (scope === 'fleet') {
        btnFleet.className = 'flex-1 py-1.5 rounded-md font-bold bg-white text-gray-900 shadow-xs transition text-center';
        btnCar.className = 'flex-1 py-1.5 rounded-md font-medium text-gray-600 hover:text-gray-900 transition text-center';
      } else {
        btnCar.className = 'flex-1 py-1.5 rounded-md font-bold bg-white text-gray-900 shadow-xs transition text-center';
        btnFleet.className = 'flex-1 py-1.5 rounded-md font-medium text-gray-600 hover:text-gray-900 transition text-center';
        if (selectedOrderId) {
          btnCar.innerText = `Car: ${selectedOrderId}`;
        }
      }
    }

    function sendQuickPrompt(promptText) {
      document.getElementById('ai-chat-input').value = promptText;
      sendAiMessage();
    }

    async function sendAiMessage() {
      const input = document.getElementById('ai-chat-input');
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
            user_message: prompt,
            model: model,
            scope: scope,
            order_id: orderId,
            operator_id: activeOperator
          })
        });
        const data = await res.json();
        removeAiLoading(loadingId);
        appendAiMessage('assistant', data.response || data.reply || 'Analysis generated.');
      } catch (e) {
        removeAiLoading(loadingId);
        appendAiMessage('assistant', 'Error communicating with AI engine. Please verify OpenRouter connection.');
      }
    }

    function appendAiMessage(role, text) {
      const feed = document.getElementById('ai-chat-messages');
      const div = document.createElement('div');
      div.className = `p-3.5 rounded-xl text-xs leading-relaxed space-y-1.5 ${role === 'user' ? 'bg-gray-900 text-white ml-6' : 'bg-white border border-gray-200 text-gray-800 shadow-xs mr-6'}`;
      div.innerHTML = `
        <div class="flex items-center space-x-1.5 font-bold text-[10px] uppercase ${role === 'user' ? 'text-amber-400' : 'text-purple-700'}">
          <i data-lucide="${role === 'user' ? 'user' : 'bot'}" class="w-3 h-3"></i>
          <span>${role === 'user' ? activeOperator : 'Operations Copilot'}</span>
        </div>
        <div class="whitespace-pre-wrap">${escapeHtml(text)}</div>
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
      appendAiMessage('assistant', `Autonomous Operations Dispatcher activated. Evaluating 22 bottleneck orders across road, maritime, and document clearance vectors...

1. Bentley Continental (CD-420322): Roadside service dispatch authorized for A7 corridor.
2. Porsche Taycan (CD-420299): Maritime Finnlines next-day sailing quote validated.
3. Ferrari Roma (CD-420458): Commercial release confirmation draft prepared for seller.

All actions staged. Human sign-off requested before transmission.`);
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
                    <button onclick="openCarDetail('${co.id}')" class="px-3 py-1.5 bg-white hover:bg-gray-100 text-gray-900 border border-gray-300 text-xs font-bold rounded-lg flex items-center space-x-1.5 shadow-2xs transition">
                      <i data-lucide="car" class="w-3.5 h-3.5 text-amber-600"></i>
                      <span>View ${co.reference} (${co.vehicle})</span>
                    </button>
                    <button onclick="requestActionWithUndo('LINK_THREAD_${t.id}_TO_${co.id}', 'Thread linked to ${co.reference}', 'Confirm Job Reference ${co.reference} to Driver')" class="px-3 py-1.5 bg-gray-900 hover:bg-black text-white text-xs font-bold rounded-lg flex items-center space-x-1.5 shadow-2xs transition">
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

              <div class="space-y-2">${msgsHtml}</div>
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
        const list = Array.isArray(data) ? data : (data.history || []);
        let html = '';
        list.forEach(h => {
          html += `
            <tr class="hover:bg-gray-50 transition">
              <td class="p-3.5 pl-4 font-mono text-gray-500">${h.timestamp ? h.timestamp.replace('T', ' ').slice(0, 19) : ''}</td>
              <td class="p-3.5 font-mono font-bold text-gray-900">${h.order_ref || h.order_id}</td>
              <td class="p-3.5 text-gray-800 font-medium">${escapeHtml(h.car)}</td>
              <td class="p-3.5"><span class="px-2 py-0.5 rounded bg-gray-100 text-gray-800 font-mono text-[10px] font-bold">${h.operator_id}</span></td>
              <td class="p-3.5 font-bold text-gray-900">${escapeHtml(h.decision)}</td>
              <td class="p-3.5 pr-4 text-gray-500">${escapeHtml(h.notes || '-')}</td>
            </tr>
          `;
        });
        tbody.innerHTML = html;
        lucide.createIcons();
      } catch (e) {
        console.error('Error loading history:', e);
      }
    }

    function exportAuditLog() {
      window.open('/api/history', '_blank');
    }

    // ================= FINANCIALS WITH INTERACTIVE FILTERING =================
    async function loadFinancials() {
      try {
        const res = await fetch('/api/financials');
        const data = await res.json();

        const sum = data.summary || {};
        const rev = sum.gross_revenue_eur != null ? sum.gross_revenue_eur : (data.total_revenue_eur || 55454.17);
        const payouts = sum.driver_payouts_eur != null ? sum.driver_payouts_eur : (data.total_driver_payouts_eur || 31561.00);
        const exp = sum.trip_expenses_eur != null ? sum.trip_expenses_eur : (data.total_expenses_eur || 5682.28);
        const margin = sum.net_profit_eur != null ? sum.net_profit_eur : (data.gross_margin_eur || 18210.89);

        document.getElementById('fin-total-revenue').innerText = `EUR ${round(rev, 2)}`;
        document.getElementById('fin-driver-payouts').innerText = `EUR ${round(payouts, 2)}`;
        document.getElementById('fin-approved-expenses').innerText = `EUR ${round(exp, 2)}`;
        document.getElementById('fin-net-margin').innerText = `EUR ${round(margin, 2)}`;

        allFinancialExpenses = data.expenses || [];
        filterFinancialsTable();
      } catch (e) {
        console.error('Error loading financials:', e);
      }
    }

    function filterFinancialsTable() {
      const cat = document.getElementById('fin-filter-cat').value.toLowerCase();
      const st = document.getElementById('fin-filter-status').value.toLowerCase();
      const q = document.getElementById('fin-search-order').value.toLowerCase();
      const tbody = document.getElementById('financials-expenses-tbody');

      let filtered = allFinancialExpenses.filter(ex => {
        if (cat !== 'all' && (ex.kind || '').toLowerCase() !== cat) return false;
        if (st !== 'all' && (ex.status || '').toLowerCase() !== st) return false;
        if (q) {
          const matchOrder = (ex.order_id || '').toLowerCase().includes(q);
          const matchVendor = (ex.vendor || '').toLowerCase().includes(q);
          const matchKind = (ex.kind || '').toLowerCase().includes(q);
          if (!matchOrder && !matchVendor && !matchKind) return false;
        }
        return true;
      });

      if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" class="p-8 text-center text-gray-400 text-xs">No expense claims match active filter criteria.</td></tr>`;
        return;
      }

      let html = '';
      filtered.forEach(ex => {
        const amt = ex.amount_formatted || `${(ex.amount_cents ? ex.amount_cents / 100 : (ex.amount || 0)).toFixed(2)} ${ex.currency || 'EUR'}`;
        const proofUrl = ex.proof_url || ex.receipt_url || '';
        const hasFile = Boolean(proofUrl || ex.has_file);
        const isPdf = proofUrl.endsWith('.pdf') || ex.content_type === 'application/pdf';

        html += `
          <tr class="hover:bg-gray-50 transition">
            <td class="p-3.5 pl-4 font-bold text-gray-900">${ex.kind}</td>
            <td class="p-3.5 text-gray-700">${ex.vendor || 'Authorized Provider'}</td>
            <td class="p-3.5 font-mono font-bold text-gray-800">${ex.order_id}</td>
            <td class="p-3.5 font-mono font-bold text-gray-900">${amt}</td>
            <td class="p-3.5"><span class="px-2 py-0.5 rounded text-[10px] font-bold ${ex.status === 'APPROVED' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}">${ex.status}</span></td>
            <td class="p-3.5 pr-4 text-right">
              <button onclick="openUniversalFileModal('${proofUrl}', '${escapeAttr(ex.kind)} Receipt Proof', '${isPdf ? 'application/pdf' : 'image/jpeg'}', {id: '${ex.id}', kind: '${ex.kind}', status: '${ex.status}'})" class="px-2.5 py-1 bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-200 rounded text-[11px] font-bold inline-flex items-center space-x-1 transition">
                <i data-lucide="receipt" class="w-3.5 h-3.5"></i>
                <span>${hasFile ? (isPdf ? 'View PDF' : 'View Photo') : 'View Proof'}</span>
              </button>
            </td>
          </tr>
        `;
      });
      tbody.innerHTML = html;
      lucide.createIcons();
    }

    // ================= OPERATOR ID PROMPT =================
    function promptOperatorId() {
      const val = prompt('Enter your Dispatcher Operator ID:', activeOperator);
      if (val && val.trim()) {
        activeOperator = val.trim();
        localStorage.setItem('bahn_operator_id', activeOperator);
        document.getElementById('operator-display').innerText = activeOperator;
        document.getElementById('decision-operator-label').innerText = activeOperator;
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
      return String(str).replace(/'/g, "\\'");
    }
    function round(val, decimals) {
      return Number(Math.round(val + 'e' + decimals) + 'e-' + decimals);
    }
  </script>
</body>
</html>
"""

with open('control_room_app/static/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated control_room_app/static/index.html ({len(html_content)} bytes)")
