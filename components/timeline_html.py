import json
import base64
from pathlib import Path


def _to_data_uri(path: str) -> str:
    """Read a local file and return a base64 data URI, or empty string if missing."""
    if not path:
        return ""
    p = Path(path)
    if not p.exists():
        return ""
    raw = p.read_bytes()
    b64 = base64.b64encode(raw).decode("utf-8")
    ext = p.suffix.lower()
    mime = {
        ".svg":  "image/svg+xml",
        ".png":  "image/png",
        ".jpg":  "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif":  "image/gif",
        ".webp": "image/webp",
    }.get(ext, "image/png")
    return f"data:{mime};base64,{b64}"


def build_timeline_html(events, links, categories):
    # Convert all image paths to inline base64 data URIs so they work
    # inside Streamlit's components.html() without needing a static file server.
    encoded_events = []
    for ev in events:
        e = dict(ev)
        e["image"]            = _to_data_uri(e.get("image", ""))
        e["event_image_full"] = _to_data_uri(e.get("event_image_full", ""))
        encoded_events.append(e)

    # Serialize data for injection into JS
    events_json     = json.dumps(encoded_events)
    links_json      = json.dumps(links)
    categories_json = json.dumps(categories)

    # Era colors
    era_colors = {
        "Prehistoria":       "rgba(172,46,46,0.15)",
        "Antiguedad":        "rgba(218,136,54,0.12)",
        "Edad Media":        "rgba(41,129,208,0.12)",
        "Era Moderna":       "rgba(60,189,68,0.12)",
        "Era Contemporanea": "rgba(155,48,204,0.12)",
    }

    # Explicit contiguous boundaries — no gaps, no overlaps
    era_boundaries = [
        {"name": "Prehistoria",       "start": -10000, "end": -3200},
        {"name": "Antiguedad",        "start":  -3200, "end":   570},
        {"name": "Edad Media",        "start":    570, "end":  1440},
        {"name": "Era Moderna",       "start":   1440, "end":  1800},
        {"name": "Era Contemporanea", "start":   1800, "end":  2026},
    ]
    for entry in era_boundaries:
        entry["color"] = era_colors.get(entry["name"], "rgba(100,100,100,0.1)")

    era_boundaries_json = json.dumps(era_boundaries)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"/>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    background: #0E1117;
    color: #e2e8f0;
    font-family: 'Segoe UI', system-ui, sans-serif;
    overflow-x: hidden;
  }}

  #controls {{
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 12px 20px;
    background: #0c1320;
    border-bottom: 1px solid #7da3da;
  }}

  #controls label {{
    font-size: 0.8rem;
    color: #94a3b8;
    white-space: nowrap;
  }}

  #slider {{
    flex: 1;
    accent-color: #5ffaf7;
    cursor: pointer;
  }}

  #year-display {{
    font-size: 1rem;
    font-weight: 700;
    color: #5ffaf7;
    min-width: 70px;
    text-align: right;
  }}

  #legend {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    padding: 8px 20px;
    background: #0c1320;
    border-bottom: 1px solid #566a87;
  }}

  .legend-item {{
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 0.75rem;
    color: #94a3b8;
    cursor: pointer;
    padding: 2px 8px;
    border-radius: 999px;
    border: 1px solid #566a87;
    transition: all 0.15s;
  }}
  .legend-item:hover {{ border-color: #5ffaf7; color: #e2e8f0; }}
  .legend-item.inactive {{ opacity: 0.35; }}

  .legend-dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
  }}

  #chart-container {{ position: relative; }}

  svg {{
    display: block;
    width: 100%;
  }}

  .node {{
    cursor: pointer;
    transition: r 0.15s;
  }}
  .node:hover {{ opacity: 0.85; }}

  .axis-label {{
    font-size: 10px;
    fill: #475569;
  }}

  /* ── Side panel ──────────────────────────────────────────────────────────── */
  #panel {{
    display: none;
    position: fixed;
    top: 0; right: 0;
    width: 300px;
    height: 100vh;
    background: #0c1320;
    border-left: 1px solid #566a87;
    overflow-y: auto;
    z-index: 100;
    box-shadow: -4px 0 20px rgba(0,0,0,0.4);
    animation: slideIn 0.2s ease;
  }}

  @keyframes slideIn {{
    from {{ transform: translateX(20px); opacity: 0; }}
    to   {{ transform: translateX(0);    opacity: 1; }}
  }}

  #panel-header {{
    position: sticky;
    top: 0;
    background: #0c1320;
    padding: 14px 16px 10px;
    border-bottom: 1px solid #566a87;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    z-index: 1;
  }}

  #panel-title {{
    font-size: 1.1rem;
    font-weight: 700;
    color: #f1f5f9;
    line-height: 1.3;
    flex: 1;
  }}

  #panel-close {{
    background: none;
    border: none;
    color: #64748b;
    font-size: 1.2rem;
    cursor: pointer;
    padding: 2px 6px;
    border-radius: 4px;
    line-height: 1;
    flex-shrink: 0;
  }}
  #panel-close:hover {{ color: #e2e8f0; background: #566a87; }}

  #panel-body {{ padding: 12px 16px 20px; }}

  #panel-year {{
    font-size: 0.8rem;
    color: #5ffaf7;
    font-weight: 600;
    margin-bottom: 6px;
  }}

  #panel-group {{
    display: inline-block;
    font-size: 0.7rem;
    padding: 2px 8px;
    border-radius: 999px;
    margin-bottom: 10px;
    font-weight: 600;
  }}

  #panel-desc {{
    font-size: 0.85rem;
    color: #94a3b8;
    line-height: 1.6;
    margin-bottom: 14px;
  }}

  #panel-image {{
    width: 100%;
    border-radius: 8px;
    margin-bottom: 14px;
    border: 1px solid #566a87;
  }}

  #panel-link {{
    display: inline-block;
    font-size: 0.85rem;
    color: #5ffaf7;
    text-decoration: none;
    padding: 6px 12px;
    border: 1px solid #3b82f6;
    border-radius: 6px;
    transition: all 0.15s;
    cursor: pointer;
  }}
  #panel-link:hover {{
    background: #3b82f6;
    color: white;
  }}

  /* ── Modal ───────────────────────────────────────────────────────────────── */
  #modal-backdrop {{
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.7);
    z-index: 300;
    backdrop-filter: blur(3px);
    animation: fadeIn 0.2s ease;
  }}
  @keyframes fadeIn {{
    from {{ opacity: 0; }}
    to   {{ opacity: 1; }}
  }}

  #modal {{
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: min(720px, 92vw);
    max-height: 88vh;
    background: #0c1320;
    border: 1px solid #566a87;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    box-shadow: 0 24px 60px rgba(0,0,0,0.6);
    animation: popIn 0.2s ease;
  }}
  @keyframes popIn {{
    from {{ transform: translate(-50%, -48%); opacity: 0; }}
    to   {{ transform: translate(-50%, -50%); opacity: 1; }}
  }}

  #modal-header {{
    padding: 18px 20px 14px;
    border-bottom: 1px solid #566a87;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-shrink: 0;
  }}

  #modal-header-left {{ flex: 1; }}

  #modal-title {{
    font-size: 1.3rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 4px;
  }}

  #modal-meta {{
    font-size: 0.78rem;
    color: #5ffaf7;
    font-weight: 600;
  }}

  #modal-group {{
    display: inline-block;
    font-size: 0.7rem;
    padding: 2px 8px;
    border-radius: 999px;
    font-weight: 600;
    margin-left: 8px;
    vertical-align: middle;
  }}

  #modal-close {{
    background: none;
    border: none;
    color: #64748b;
    font-size: 1.4rem;
    cursor: pointer;
    padding: 2px 8px;
    border-radius: 6px;
    line-height: 1;
    flex-shrink: 0;
    transition: all 0.15s;
  }}
  #modal-close:hover {{ color: #e2e8f0; background: #566a87; }}

  #modal-body {{
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 0;
  }}

  #modal-image {{ display: none; }}

  #modal-details {{
    flex: 1;
    order: 1;
  }}

  #modal-event-image-full {{
    width: 100%;
    border-radius: 8px;
    border: 1px solid #566a87;
    margin: 14px 0;
    display: none;
  }}

  .modal-paragraph {{
    font-size: 0.88rem;
    color: #94a3b8;
    line-height: 1.75;
    margin-bottom: 14px;
  }}
  .modal-paragraph:last-child {{ margin-bottom: 0; }}

  /* ── Tooltip ─────────────────────────────────────────────────────────────── */
  #tooltip {{
    position: fixed;
    background: #0f172a;
    border: 1px solid #566a87;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 0.75rem;
    color: #e2e8f0;
    pointer-events: none;
    display: none;
    z-index: 200;
    max-width: 200px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
  }}
</style>
</head>

<body>

<div id="controls">
  <label>Year</label>
  <input type="range" id="slider" min="-10000" max="2026" step="50" value="2026"/>
  <span id="year-display">2026</span>
</div>

<div id="legend"></div>

<div id="chart-container">
  <svg id="chart" height="470"></svg>
</div>

<!-- Side panel (summary) -->
<div id="panel">
  <div id="panel-header">
    <div id="panel-title"></div>
    <button id="panel-close" onclick="closePanel()">✕</button>
  </div>
  <div id="panel-body">
    <div id="panel-year"></div>
    <div id="panel-group"></div>
    <p id="panel-desc"></p>
    <img id="panel-image" src="" alt="" onerror="this.style.display='none'"/>
    <a id="panel-link" href="#">Read more →</a>
  </div>
</div>

<!-- Modal (full details) -->
<div id="modal-backdrop" onclick="closeModal()">
  <div id="modal" onclick="event.stopPropagation()">
    <div id="modal-header">
      <div id="modal-header-left">
        <div id="modal-title"></div>
        <div id="modal-meta">
          <span id="modal-year"></span>
          <span id="modal-group"></span>
        </div>
      </div>
      <button id="modal-close" onclick="closeModal()">✕</button>
    </div>
    <div id="modal-body">
      <div id="modal-details">
        <img id="modal-event-image-full" src="" alt="" onerror="this.style.display='none'"/>
      </div>
      <img id="modal-image" src="" alt="" onerror="this.style.display='none'"/>
    </div>
  </div>
</div>

<div id="tooltip"></div>

<script>
// ── DATA ────────────────────────────────────────────────────────────────────
const EVENTS         = {events_json};
const LINKS          = {links_json};
const CATEGORIES     = {categories_json};
const ERA_BOUNDARIES = {era_boundaries_json};

// ── CONFIG ──────────────────────────────────────────────────────────────────
const YEAR_MIN = -10000;
const YEAR_MAX = 2026;
const AXIS_Y   = 350;
const ROWS     = 6;
const ROW_GAP  = 45;
const PAD_X    = 60;
const HEIGHT   = 470;

// ── STATE ───────────────────────────────────────────────────────────────────
let currentYear   = YEAR_MAX;
let animFrame     = null;
let activeGroups  = new Set(Object.keys(CATEGORIES));
let selectedEvent = null;

// ── LAYOUT ──────────────────────────────────────────────────────────────────
const svg   = d3.select("#chart");
const width = () => document.getElementById("chart").clientWidth || 1000;

// FIX #5: use width() for the full viewport width so PAD_X margins are
// correctly applied on both sides of the non-linear scale.
function xScale() {{
  const w = width();
  return d3.scaleLinear()
    .domain([-10000, -1000,      1500,      2026])
    .range( [PAD_X,  w * 0.25,  w * 0.60,  w - PAD_X]);
}}

// Compute Y positions once — sorted by year, then round-robin rows
const sortedEvents = [...EVENTS].sort((a, b) => a.year - b.year);
const Y_MAP = {{}};
sortedEvents.forEach((e, i) => {{
  const row = i % ROWS;
  Y_MAP[e.id] = AXIS_Y - 55 - row * ROW_GAP;
}});

// ── LEGEND ──────────────────────────────────────────────────────────────────
const legend = document.getElementById("legend");
Object.entries(CATEGORIES).forEach(([group, color]) => {{
  const item = document.createElement("div");
  item.className = "legend-item";
  item.dataset.group = group;
  item.innerHTML = `<span class="legend-dot" style="background:${{color}}"></span>${{group}}`;
  item.addEventListener("click", () => toggleGroup(group, item));
  legend.appendChild(item);
}});

function toggleGroup(group, el) {{
  if (activeGroups.has(group)) {{
    activeGroups.delete(group);
    el.classList.add("inactive");
  }} else {{
    activeGroups.add(group);
    el.classList.remove("inactive");
  }}
  render();
}}

// ── RENDER ──────────────────────────────────────────────────────────────────
function render() {{
  svg.selectAll("*").remove();
  const x = xScale();
  const w = width();

  const visible = EVENTS.filter(e =>
    e.year <= currentYear && activeGroups.has(e.group)
  );

  // Era background bands
  ERA_BOUNDARIES.forEach(era => {{
    const x1 = x(era.start);
    const x2 = x(era.end);
    svg.append("rect")
      .attr("x", x1)
      .attr("y", 0)
      .attr("width", x2 - x1)
      .attr("height", HEIGHT)
      .attr("fill", era.color);
    svg.append("text")
      .attr("x", (x1 + x2) / 2)
      .attr("y", 14)
      .attr("text-anchor", "middle")
      .attr("font-size", "9px")
      .attr("fill", "#64748b")
      .attr("letter-spacing", "0.05em")
      .text(era.name.toUpperCase());
  }});

  // Time axis line
  svg.append("line")
    .attr("x1", PAD_X).attr("x2", w - PAD_X)
    .attr("y1", AXIS_Y).attr("y2", AXIS_Y)
    .attr("stroke", "#566a87").attr("stroke-width", 1.5);

  // Axis tick labels — rotated 45° so dense BC labels don't overlap
  const tickValues = x.ticks(12);
  tickValues.forEach(t => {{
    svg.append("line")
      .attr("x1", x(t)).attr("x2", x(t))
      .attr("y1", AXIS_Y).attr("y2", AXIS_Y + 6)
      .attr("stroke", "#475569");
    svg.append("text")
      .attr("x", x(t))
      .attr("y", AXIS_Y + 10)
      .attr("text-anchor", "end")
      .attr("class", "axis-label")
      .attr("transform", `rotate(-45, ${{x(t)}}, ${{AXIS_Y + 10}})`)
      .text(t < 0 ? `${{Math.abs(t)}} BC` : `${{t}} AD`);
  }});

  // Links (dashed connector lines)
  LINKS.forEach(([a, b]) => {{
    const A = visible.find(e => e.id === a);
    const B = visible.find(e => e.id === b);
    if (!A || !B) return;
    svg.append("line")
      .attr("class", "link")
      .attr("x1", x(A.year)).attr("y1", Y_MAP[A.id])
      .attr("x2", x(B.year)).attr("y2", Y_MAP[B.id])
      .attr("stroke", "#566a87")
      .attr("stroke-dasharray", "3 3")
      .attr("stroke-width", 1);
  }});

  // Vertical drop lines
  visible.forEach(e => {{
    svg.append("line")
      .attr("x1", x(e.year)).attr("x2", x(e.year))
      .attr("y1", Y_MAP[e.id] + 8).attr("y2", AXIS_Y)
      .attr("stroke", CATEGORIES[e.group] || "#aaa")
      .attr("stroke-width", 0.5)
      .attr("opacity", 0.3);
  }});

  // Nodes
  visible.forEach(e => {{
    const isSelected = selectedEvent && selectedEvent.id === e.id;
    const g = svg.append("g").attr("class", "node");

    g.append("circle")
      .attr("cx", x(e.year)).attr("cy", Y_MAP[e.id])
      .attr("r", isSelected ? 10 : 7)
      .attr("fill", CATEGORIES[e.group] || "#aaa")
      .attr("stroke", isSelected ? "#fff" : "none")
      .attr("stroke-width", isSelected ? 2 : 0)
      .attr("opacity", 0.9);

    g.append("text")
      .attr("x", x(e.year))
      .attr("y", Y_MAP[e.id] - 12)
      .attr("text-anchor", "middle")
      .attr("font-size", "9px")
      .attr("fill", "#94a3b8")
      .attr("pointer-events", "none")
      .text(e.name.length > 16 ? e.name.slice(0, 14) + "…" : e.name);

    g.on("click", () => showPanel(e))
     .on("mouseover", (event) => showTooltip(event, e))
     .on("mousemove", (event) => moveTooltip(event))
     .on("mouseout",  () => hideTooltip());
  }});
}}

// ── TOOLTIP ─────────────────────────────────────────────────────────────────
const tooltip = document.getElementById("tooltip");

function showTooltip(event, e) {{
  const yearStr = e.year < 0 ? `${{Math.abs(e.year)}} a.C.` : `${{e.year}} d.C.`;
  tooltip.innerHTML = `<strong>${{e.name}}</strong><br/><span style="color:#94a3b8">${{yearStr}} · ${{e.group}}</span>`;
  tooltip.style.display = "block";
  moveTooltip(event);
}}
function moveTooltip(event) {{
  tooltip.style.left = (event.clientX + 12) + "px";
  tooltip.style.top  = (event.clientY - 28) + "px";
}}
function hideTooltip() {{
  tooltip.style.display = "none";
}}

// ── PANEL ────────────────────────────────────────────────────────────────────
function showPanel(e) {{
  selectedEvent = e;
  const yearStr = e.year < 0 ? `${{Math.abs(e.year)}} a.C.` : `${{e.year}} d.C.`;
  const color   = CATEGORIES[e.group] || "#aaa";

  document.getElementById("panel-title").textContent = e.name;
  document.getElementById("panel-year").textContent  = yearStr + " · " + e.era;

  const groupEl = document.getElementById("panel-group");
  groupEl.textContent      = e.group;
  groupEl.style.background = color + "33";
  groupEl.style.color      = color;
  groupEl.style.border     = `1px solid ${{color}}55`;

  document.getElementById("panel-desc").textContent = e.desc;

  const img = document.getElementById("panel-image");
  img.src = e.image;
  img.style.display = "block";

  // "Read more" opens the modal with full details
  document.getElementById("panel-link").onclick = (ev) => {{
    ev.preventDefault();
    openModal(e);
  }};

  document.getElementById("panel").style.display = "block";
  render();
}}

function closePanel() {{
  selectedEvent = null;
  document.getElementById("panel").style.display = "none";
  render();
}}

// ── MODAL ────────────────────────────────────────────────────────────────────
function openModal(e) {{
  const yearStr = e.year < 0 ? `${{Math.abs(e.year)}} a.C.` : `${{e.year}} d.C.`;
  const color   = CATEGORIES[e.group] || "#aaa";

  document.getElementById("modal-title").textContent = e.name;
  document.getElementById("modal-year").textContent  = yearStr + " · " + e.era;

  const modalGroup = document.getElementById("modal-group");
  modalGroup.textContent      = e.group;
  modalGroup.style.background = color + "33";
  modalGroup.style.color      = color;
  modalGroup.style.border     = `1px solid ${{color}}55`;

  const modalImg = document.getElementById("modal-image");
  modalImg.style.display = "none";  // images are shown via event_image_full inside the text flow

  // Render each paragraph from details[], inserting event_image_full after paragraph 2
  const detailsEl = document.getElementById("modal-details");
  const imgFull   = document.getElementById("modal-event-image-full");

  // Detach imgFull BEFORE clearing innerHTML so the node isn't destroyed
  if (imgFull.parentNode) imgFull.parentNode.removeChild(imgFull);
  detailsEl.innerHTML = "";

  const paragraphs = Array.isArray(e.details) ? e.details : [e.desc];
  paragraphs.forEach((p, i) => {{
    // After the second paragraph (index 1), insert the full image
    if (i === 2) detailsEl.appendChild(imgFull);
    const el = document.createElement("p");
    el.className = "modal-paragraph";
    el.textContent = p;
    detailsEl.appendChild(el);
  }});
  // If fewer than 2 paragraphs, still append the image at the end
  if (paragraphs.length <= 2) detailsEl.appendChild(imgFull);

  // Show event_image_full if the event has one
  if (e.event_image_full) {{
    imgFull.src = e.event_image_full;
    imgFull.style.display = "block";
  }} else {{
    imgFull.style.display = "none";
  }}

  // FIX #1 & #2: function was never closed AND backdrop was never shown
  document.getElementById("modal-backdrop").style.display = "block";
}}

function closeModal() {{
  document.getElementById("modal-backdrop").style.display = "none";
}}

// Close modal on Escape key
document.addEventListener("keydown", (e) => {{
  if (e.key === "Escape") closeModal();
}});

// ── SLIDER ───────────────────────────────────────────────────────────────────
const yearDisplay = document.getElementById("year-display");

function formatYear(y) {{
  const yr = Math.round(y);
  return yr < 0 ? `${{Math.abs(yr)}} BC` : `${{yr}} AD`;
}}

document.getElementById("slider").addEventListener("input", function() {{
  cancelAnimationFrame(animFrame);
  currentYear = +this.value;
  yearDisplay.textContent = formatYear(currentYear);
  render();
}});

// ── RESIZE ───────────────────────────────────────────────────────────────────
window.addEventListener("resize", () => render());

// ── INIT ─────────────────────────────────────────────────────────────────────
render();
</script>
</body>
</html>
"""
