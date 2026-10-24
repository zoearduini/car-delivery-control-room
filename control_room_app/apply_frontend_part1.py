import re

html_path = "control_room_app/static/index.html"

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Remove the (i) button from top app header
# Target in header:
old_info_btn = """      <!-- Info Button (Opens Credit & System Status) -->
      <button onclick="toggleInfoModal()" class="w-8 h-8 rounded-lg bg-gray-800 hover:bg-gray-700 border border-gray-700 flex items-center justify-center transition" title="System Info & Credits">
        <i data-lucide="info" class="w-4 h-4 text-amber-400"></i>
      </button>"""

if old_info_btn in html:
    html = html.replace(old_info_btn, "")
    print("1. Removed (i) button from top bar.")
else:
    print("1. Old info button in top bar not found, checking alternatives...")
    html = re.sub(r'<button onclick="toggleInfoModal\(\)"[^>]*>[\s\S]*?<\/button>', '', html, count=1)
    print("1. Removed (i) button via regex.")

# 2. Add the (i) button inside AI sidebar header
old_ai_header = """    <!-- SIDEBAR HEADER -->
    <div class="h-16 px-6 bg-[#121417] text-white flex items-center justify-between border-b border-gray-800 shrink-0">
      <div class="flex items-center space-x-2.5">
        <div class="w-7 h-7 rounded-lg bg-purple-600 flex items-center justify-center">
          <i data-lucide="bot" class="w-4 h-4 text-white"></i>
        </div>
        <div>
          <h2 class="text-xs font-bold uppercase tracking-wider text-purple-400">Bahn AI Assistant</h2>
          <span class="text-[10px] text-gray-400">Fleet & Vehicle Intelligence</span>
        </div>
      </div>
      <button onclick="closeAiSidebar()" class="p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800 transition">
        <i data-lucide="x" class="w-4 h-4"></i>
      </button>
    </div>"""

new_ai_header = """    <!-- SIDEBAR HEADER -->
    <div class="h-16 px-6 bg-[#121417] text-white flex items-center justify-between border-b border-gray-800 shrink-0">
      <div class="flex items-center space-x-2.5">
        <div class="w-7 h-7 rounded-lg bg-purple-600 flex items-center justify-center">
          <i data-lucide="bot" class="w-4 h-4 text-white"></i>
        </div>
        <div>
          <h2 class="text-xs font-bold uppercase tracking-wider text-purple-400">Bahn AI Assistant</h2>
          <span class="text-[10px] text-gray-400">Fleet & Vehicle Intelligence</span>
        </div>
      </div>
      <div class="flex items-center space-x-1.5">
        <!-- Info & Credit Button (Inside AI Assistant per user request) -->
        <button onclick="toggleInfoModal()" class="px-2 py-1 rounded-md bg-gray-800 hover:bg-gray-700 text-amber-400 border border-gray-700 flex items-center space-x-1 text-[11px] font-bold transition" title="System Info & Credits">
          <i data-lucide="info" class="w-3.5 h-3.5"></i>
          <span>Credits</span>
        </button>
        <button onclick="closeAiSidebar()" class="p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800 transition">
          <i data-lucide="x" class="w-4 h-4"></i>
        </button>
      </div>
    </div>"""

if old_ai_header in html:
    html = html.replace(old_ai_header, new_ai_header)
    print("2. Added (i) button inside AI sidebar header.")
else:
    print("2. WARNING: old_ai_header not found.")

# 3. Fix View-Home table layout and table-fixed
old_home_table = """    <!-- MAIN FLEET TABLE -->
    <div class="flex-1 overflow-y-auto custom-scrollbar px-8 py-4">
      <div class="border border-gray-200 rounded-xl overflow-hidden shadow-xs bg-white">
        <table class="w-full text-left border-collapse text-xs">
          <thead class="bg-gray-50/80 border-b border-gray-200 text-gray-500 font-bold uppercase tracking-wider text-[11px] sticky top-0 z-10">
            <tr>
              <th class="p-3.5 pl-4">Order Ref</th>
              <th class="p-3.5">Vehicle</th>
              <th class="p-3.5">Corridor Route</th>
              <th class="p-3.5">Current Position</th>
              <th class="p-3.5">Assigned Driver</th>
              <th class="p-3.5">Operational Condition</th>
              <th class="p-3.5 pr-4 text-right">Action</th>
            </tr>
          </thead>
          <tbody id="fleet-table-tbody" class="divide-y divide-gray-100">
            <!-- Dynamically populated rows -->
          </tbody>
        </table>
      </div>
    </div>"""

new_home_table = """    <!-- MAIN FLEET TABLE (Fixed layout & permanent scrollbar gutter so spaces never shift) -->
    <div class="flex-1 overflow-y-scroll custom-scrollbar px-8 py-4" style="scrollbar-gutter: stable;">
      <div class="border border-gray-200 rounded-xl overflow-hidden shadow-xs bg-white min-h-[540px]">
        <table class="w-full text-left border-collapse text-xs table-fixed">
          <thead class="bg-gray-50/80 border-b border-gray-200 text-gray-500 font-bold uppercase tracking-wider text-[11px] sticky top-0 z-10">
            <tr>
              <th class="w-28 p-3.5 pl-5">Order Ref</th>
              <th class="w-64 p-3.5">Vehicle</th>
              <th class="w-48 p-3.5">Corridor Route</th>
              <th class="w-44 p-3.5">Current Position</th>
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
    </div>"""

if old_home_table in html:
    html = html.replace(old_home_table, new_home_table)
    print("3. Fixed fleet table outline, scrollbar gutter, and table-fixed columns.")
else:
    print("3. WARNING: old_home_table not found.")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Saved first batch of frontend updates.")
