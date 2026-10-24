with open("control_room_app/static/index.html", "r", encoding="utf-8") as f:
    text = f.read()

target = '<button onclick="toggleAiSidebar()" class="text-gray-400 hover:text-white p-1 rounded-lg transition">\n        <i data-lucide="x" class="w-5 h-5"></i>\n      </button>'
if target not in text:
    target = target.replace("\n", "\r\n")

replacement = """<div class="flex items-center space-x-2">
        <button onclick="openInfoModal()" title="System Information & Credits" class="px-2.5 py-1 rounded-md bg-gray-800/90 hover:bg-gray-700 text-amber-400 border border-gray-700 flex items-center space-x-1 text-[11px] font-bold transition">
          <i data-lucide="info" class="w-3.5 h-3.5"></i>
          <span>Credits: $20.00</span>
        </button>
        <button onclick="toggleAiSidebar()" class="text-gray-400 hover:text-white p-1 rounded-lg transition">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>"""

if "\r\n" in text:
    replacement = replacement.replace("\n", "\r\n")

assert target in text, "Target button not found"
text = text.replace(target, replacement, 1)

with open("control_room_app/static/index.html", "w", encoding="utf-8") as f:
    f.write(text)

print("Placed (i) button inside AI sidebar header successfully!")
