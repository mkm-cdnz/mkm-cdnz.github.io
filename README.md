<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Keyword Network — DeepSeek-r1 (G:Y)</title>
<style>
  html, body { height: 100%; margin: 0; }
  body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; background: #0b0f14; color: #e2e8f0; }
  header { padding: 12px 16px; display:flex; gap: 16px; align-items: center; border-bottom: 1px solid #1f2937; background:#0d1218; position: sticky; top:0; z-index: 10; }
  header h1 { margin: 0; font-size: 16px; font-weight: 600; }
  header .meta { font-size: 12px; color: #94a3b8; }
  .controls { display:flex; gap: 16px; align-items: center; flex-wrap: wrap; }
  .controls label { font-size: 12px; color: #cbd5e1; }
  .pill { background:#111827; border:1px solid #1f2937; padding:6px 10px; border-radius: 999px; font-size: 12px; }
  #graph { width: 100%; height: calc(100vh - 60px); }
  .tooltip { position: absolute; pointer-events: none; background: rgba(15,23,42,0.95); color:#e2e8f0; border:1px solid #334155; padding:6px 8px; border-radius:8px; font-size:12px; }
  .legend { display:flex; gap: 12px; align-items:center; font-size:12px; color:#94a3b8; }
  .legend .swatch { width: 12px; height: 12px; border-radius: 3px; background:#94a3b8; display:inline-block; }
  a.btn { color:#e2e8f0; text-decoration:none; border:1px solid #334155; padding:6px 10px; border-radius:8px; }
  a.btn:hover { background:#111827; }
</style>
</head>
<body>
  <header>
    <div>
      <h1>Keyword Network — DeepSeek‑r1 (Columns G:Y)</h1>
      <div class="meta">Nodes: 19 · Links: 146 · Built from boolean keyword matrix</div>
    </div>
    <div class="controls" style="margin-left:auto;">
      <label>Min co-occurrence: <span id="threshVal" class="pill">1</span></label>
      <input id="threshold" type="range" min="1" max="79" value="1" step="1"/>
      <label>Zoom: scroll · Drag nodes to pin</label>
      <a class="btn" href="keyword_cooccurrence.csv" download>Download co-occurrence CSV</a>
    </div>
  </header>
  <div id="graph"></div>
  <div id="tooltip" class="tooltip" style="opacity:0;"></div>

  <script src="https://d3js.org/d3.v7.min.js"></script>
  <script>
  const data = {
    "nodes": [{"id": "Yarvin|Moldbug", "group": 1, "count": 36}, {"id": "Thiel", "group": 1, "count": 43}, {"id": "Vance", "group": 1, "count": 79}, {"id": "Altman", "group": 1, "count": 25}, {"id": "Musk", "group": 1, "count": 85}, {"id": "Srinivasan|Balaji", "group": 1, "count": 12}, {"id": "Andreessen", "group": 1, "count": 19}, {"id": "Trump", "group": 1, "count": 126}, {"id": "FVEY", "group": 1, "count": 2}, {"id": "NSA", "group": 1, "count": 44}, {"id": "Palantir", "group": 1, "count": 19}, {"id": "Groyper", "group": 1, "count": 20}, {"id": "Karp", "group": 1, "count": 12}, {"id": "Bannon", "group": 1, "count": 15}, {"id": "Fuentes", "group": 1, "count": 25}, {"id": "Kirk", "group": 1, "count": 19}, {"id": "fascist|fascism", "group": 1, "count": 28}, {"id": "Israel", "group": 1, "count": 54}, {"id": "genocide|genocidal", "group": 1, "count": 9}],
    "links": [{"source": "Altman", "target": "Vance", "value": 12}, {"source": "Altman", "target": "Yarvin|Moldbug", "value": 6}, {"source": "Vance", "target": "Yarvin|Moldbug", "value": 30}, {"source": "Altman", "target": "NSA", "value": 10}, {"source": "Altman", "target": "Thiel", "value": 5}, {"source": "NSA", "target": "Thiel", "value": 13}, {"source": "NSA", "target": "Vance", "value": 25}, {"source": "NSA", "target": "Yarvin|Moldbug", "value": 12}, {"source": "Thiel", "target": "Vance", "value": 34}, {"source": "Thiel", "target": "Yarvin|Moldbug", "value": 26}, {"source": "Altman", "target": "fascist|fascism", "value": 3}, {"source": "NSA", "target": "fascist|fascism", "value": 13}, {"source": "Vance", "target": "fascist|fascism", "value": 22}, {"source": "Yarvin|Moldbug", "target": "fascist|fascism", "value": 15}, {"source": "Bannon", "target": "Musk", "value": 10}, {"source": "Bannon", "target": "Thiel", "value": 11}, {"source": "Bannon", "target": "Trump", "value": 14}, {"source": "Bannon", "target": "Vance", "value": 12}, {"source": "Bannon", "target": "Yarvin|Moldbug", "value": 10}, {"source": "Bannon", "target": "fascist|fascism", "value": 9}, {"source": "Musk", "target": "Thiel", "value": 29}, {"source": "Musk", "target": "Trump", "value": 79}, {"source": "Musk", "target": "Vance", "value": 54}, {"source": "Musk", "target": "Yarvin|Moldbug", "value": 20}, {"source": "Musk", "target": "fascist|fascism", "value": 13}, {"source": "Thiel", "target": "Trump", "value": 36}, {"source": "Thiel", "target": "fascist|fascism", "value": 14}, {"source": "Trump", "target": "Vance", "value": 67}, {"source": "Trump", "target": "Yarvin|Moldbug", "value": 30}, {"source": "Trump", "target": "fascist|fascism", "value": 23}, {"source": "NSA", "target": "Trump", "value": 32}, {"source": "Bannon", "target": "Israel", "value": 6}, {"source": "Bannon", "target": "NSA", "value": 9}, {"source": "Bannon", "target": "Srinivasan|Balaji", "value": 3}, {"source": "Israel", "target": "NSA", "value": 14}, {"source": "Israel", "target": "Srinivasan|Balaji", "value": 3}, {"source": "Israel", "target": "Thiel", "value": 10}, {"source": "Israel", "target": "Trump", "value": 53}, {"source": "Israel", "target": "Vance", "value": 25}, {"source": "Israel", "target": "Yarvin|Moldbug", "value": 9}, {"source": "Israel", "target": "fascist|fascism", "value": 13}, {"source": "NSA", "target": "Srinivasan|Balaji", "value": 6}, {"source": "Srinivasan|Balaji", "target": "Thiel", "value": 7}, {"source": "Srinivasan|Balaji", "target": "Trump", "value": 10}, {"source": "Srinivasan|Balaji", "target": "Vance", "value": 7}, {"source": "Srinivasan|Balaji", "target": "Yarvin|Moldbug", "value": 6}, {"source": "Srinivasan|Balaji", "target": "fascist|fascism", "value": 4}, {"source": "Altman", "target": "Israel", "value": 7}, {"source": "Altman", "target": "Karp", "value": 1}, {"source": "Altman", "target": "Musk", "value": 18}, {"source": "Altman", "target": "Palantir", "value": 2}, {"source": "Altman", "target": "Trump", "value": 16}, {"source": "Israel", "target": "Karp", "value": 5}, {"source": "Israel", "target": "Musk", "value": 26}, {"source": "Israel", "target": "Palantir", "value": 7}, {"source": "Karp", "target": "Musk", "value": 6}, {"source": "Karp", "target": "Palantir", "value": 12}, {"source": "Karp", "target": "Thiel", "value": 7}, {"source": "Karp", "target": "Trump", "value": 10}, {"source": "Karp", "target": "Vance", "value": 5}, {"source": "Karp", "target": "Yarvin|Moldbug", "value": 2}, {"source": "Karp", "target": "fascist|fascism", "value": 2}, {"source": "Musk", "target": "Palantir", "value": 12}, {"source": "Palantir", "target": "Thiel", "value": 13}, {"source": "Palantir", "target": "Trump", "value": 16}, {"source": "Palantir", "target": "Vance", "value": 10}, {"source": "Palantir", "target": "Yarvin|Moldbug", "value": 4}, {"source": "Palantir", "target": "fascist|fascism", "value": 4}, {"source": "Andreessen", "target": "NSA", "value": 8}, {"source": "Andreessen", "target": "Srinivasan|Balaji", "value": 9}, {"source": "Andreessen", "target": "Trump", "value": 16}, {"source": "Andreessen", "target": "Musk", "value": 15}, {"source": "Andreessen", "target": "Thiel", "value": 8}, {"source": "Andreessen", "target": "Vance", "value": 12}, {"source": "Andreessen", "target": "Yarvin|Moldbug", "value": 7}, {"source": "Andreessen", "target": "genocide|genocidal", "value": 2}, {"source": "Musk", "target": "NSA", "value": 18}, {"source": "Musk", "target": "genocide|genocidal", "value": 4}, {"source": "NSA", "target": "genocide|genocidal", "value": 6}, {"source": "Thiel", "target": "genocide|genocidal", "value": 3}, {"source": "Trump", "target": "genocide|genocidal", "value": 8}, {"source": "Vance", "target": "genocide|genocidal", "value": 5}, {"source": "Yarvin|Moldbug", "target": "genocide|genocidal", "value": 3}, {"source": "Musk", "target": "Srinivasan|Balaji", "value": 7}, {"source": "Altman", "target": "Andreessen", "value": 5}, {"source": "Groyper", "target": "Thiel", "value": 2}, {"source": "Groyper", "target": "Trump", "value": 19}, {"source": "Groyper", "target": "Vance", "value": 8}, {"source": "Groyper", "target": "Yarvin|Moldbug", "value": 3}, {"source": "Altman", "target": "Srinivasan|Balaji", "value": 2}, {"source": "Andreessen", "target": "Palantir", "value": 3}, {"source": "Andreessen", "target": "fascist|fascism", "value": 3}, {"source": "NSA", "target": "Palantir", "value": 6}, {"source": "Palantir", "target": "Srinivasan|Balaji", "value": 2}, {"source": "Altman", "target": "Bannon", "value": 1}, {"source": "Andreessen", "target": "Bannon", "value": 3}, {"source": "Altman", "target": "Fuentes", "value": 1}, {"source": "Andreessen", "target": "Fuentes", "value": 1}, {"source": "Fuentes", "target": "Musk", "value": 8}, {"source": "Bannon", "target": "Fuentes", "value": 2}, {"source": "Bannon", "target": "Groyper", "value": 1}, {"source": "Bannon", "target": "Kirk", "value": 2}, {"source": "Bannon", "target": "genocide|genocidal", "value": 3}, {"source": "Fuentes", "target": "Groyper", "value": 17}, {"source": "Fuentes", "target": "Israel", "value": 21}, {"source": "Fuentes", "target": "Kirk", "value": 18}, {"source": "Fuentes", "target": "Trump", "value": 24}, {"source": "Fuentes", "target": "Yarvin|Moldbug", "value": 2}, {"source": "Fuentes", "target": "fascist|fascism", "value": 7}, {"source": "Fuentes", "target": "genocide|genocidal", "value": 4}, {"source": "Groyper", "target": "Israel", "value": 15}, {"source": "Groyper", "target": "Kirk", "value": 15}, {"source": "Groyper", "target": "fascist|fascism", "value": 7}, {"source": "Groyper", "target": "genocide|genocidal", "value": 4}, {"source": "Israel", "target": "Kirk", "value": 16}, {"source": "Israel", "target": "genocide|genocidal", "value": 7}, {"source": "Kirk", "target": "Trump", "value": 18}, {"source": "Kirk", "target": "Yarvin|Moldbug", "value": 2}, {"source": "Kirk", "target": "fascist|fascism", "value": 7}, {"source": "Kirk", "target": "genocide|genocidal", "value": 4}, {"source": "fascist|fascism", "target": "genocide|genocidal", "value": 4}, {"source": "FVEY", "target": "Israel", "value": 2}, {"source": "FVEY", "target": "NSA", "value": 2}, {"source": "FVEY", "target": "Trump", "value": 2}, {"source": "Karp", "target": "NSA", "value": 4}, {"source": "FVEY", "target": "genocide|genocidal", "value": 1}, {"source": "Andreessen", "target": "Israel", "value": 2}, {"source": "Andreessen", "target": "Karp", "value": 1}, {"source": "Bannon", "target": "Karp", "value": 1}, {"source": "Bannon", "target": "Palantir", "value": 1}, {"source": "Karp", "target": "Srinivasan|Balaji", "value": 1}, {"source": "Karp", "target": "genocide|genocidal", "value": 1}, {"source": "Palantir", "target": "genocide|genocidal", "value": 1}, {"source": "Srinivasan|Balaji", "target": "genocide|genocidal", "value": 1}, {"source": "Fuentes", "target": "NSA", "value": 4}, {"source": "Fuentes", "target": "Vance", "value": 8}, {"source": "Kirk", "target": "NSA", "value": 4}, {"source": "Kirk", "target": "Vance", "value": 6}, {"source": "Kirk", "target": "Musk", "value": 5}, {"source": "Fuentes", "target": "Srinivasan|Balaji", "value": 1}, {"source": "Groyper", "target": "Musk", "value": 6}, {"source": "Groyper", "target": "Srinivasan|Balaji", "value": 1}, {"source": "Kirk", "target": "Srinivasan|Balaji", "value": 1}, {"source": "Groyper", "target": "NSA", "value": 2}, {"source": "Fuentes", "target": "Thiel", "value": 1}, {"source": "Kirk", "target": "Thiel", "value": 1}]
  };

  // Basic dimensions
  const container = document.getElementById('graph');
  const width = container.clientWidth;
  const height = container.clientHeight;

  const tooltip = d3.select("#tooltip");

  const svg = d3.select("#graph")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .call(d3.zoom().on("zoom", (event) => g.attr("transform", event.transform)));

  const g = svg.append("g");

  // Scales
  const linkValueExtent = d3.extent(data.links, d => d.value);
  const linkWidth = d3.scaleLinear().domain(linkValueExtent).range([0.5, 6]);
  const nodeSize = d3.scaleSqrt().domain([0, d3.max(data.nodes, d => d.count)||1]).range([4, 18]);
  const nodeColor = d3.scaleLinear().domain([0, d3.max(data.nodes, d => d.count)||1]).range(["#60a5fa", "#f97316"]);

  // Forces
  let simulation = d3.forceSimulation(data.nodes)
      .force("link", d3.forceLink(data.links).id(d => d.id).distance(d => 80 - Math.min(50, d.value*2)).strength(d => Math.min(1, 0.05 + d.value*0.02)))
      .force("charge", d3.forceManyBody().strength(-160))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collide", d3.forceCollide().radius(d => nodeSize(d.count)+4));

  let link = g.append("g")
      .attr("stroke", "#475569")
      .attr("stroke-opacity", 0.6)
    .selectAll("line")
    .data(data.links)
    .join("line")
      .attr("stroke-width", d => linkWidth(d.value));

  let node = g.append("g")
      .attr("stroke", "#0b0f14")
      .attr("stroke-width", 1.2)
    .selectAll("circle")
    .data(data.nodes)
    .join("circle")
      .attr("r", d => nodeSize(d.count))
      .attr("fill", d => nodeColor(d.count))
      .call(drag(simulation))
      .on("mouseover", (event, d) => showTooltip(event, d))
      .on("mousemove", (event, d) => moveTooltip(event, d))
      .on("mouseout", hideTooltip);

  let labels = g.append("g")
    .selectAll("text")
    .data(data.nodes)
    .join("text")
      .text(d => d.id)
      .attr("font-size", "11px")
      .attr("fill", "#cbd5e1")
      .attr("stroke", "#0b0f14")
      .attr("stroke-width", 3)
      .attr("paint-order", "stroke")
      .attr("dx", 10)
      .attr("dy", 4)
      .style("pointer-events", "none");

  simulation.on("tick", () => {
    link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

    node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);

    labels
        .attr("x", d => d.x)
        .attr("y", d => d.y);
  });

  function drag(simulation) {
    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }
    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }
    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      // keep pinned after drag; comment next two lines to unpin on release
      // d.fx = null;
      // d.fy = null;
    }
    return d3.drag().on("start", dragstarted).on("drag", dragged).on("end", dragended);
  }

  function showTooltip(event, d) {
    const deg = neighborsOf(d.id);
    tooltip
      .style("opacity", 1)
      .html(`<div><strong>${d.id}</strong></div>
             <div>Mentions: ${d.count}</div>
             <div>Neighbors: ${deg.size}</div>`);
    // highlight
    node.attr("opacity", n => (n.id === d.id || deg.has(n.id)) ? 1 : 0.15);
    labels.attr("opacity", n => (n.id === d.id || deg.has(n.id)) ? 1 : 0.1);
    link.attr("stroke-opacity", l => (l.source.id === d.id || l.target.id === d.id) ? 0.9 : 0.05)
        .attr("stroke", l => (l.source.id === d.id || l.target.id === d.id) ? "#eab308" : "#475569");
  }
  function moveTooltip(event, d) {
    tooltip.style("left", (event.pageX + 12) + "px")
           .style("top", (event.pageY + 12) + "px");
  }
  function hideTooltip() {
    tooltip.style("opacity", 0);
    node.attr("opacity", 1);
    labels.attr("opacity", 1);
    link.attr("stroke-opacity", 0.6).attr("stroke", "#475569");
  }

  // Build neighbor map
  const neighborMap = new Map();
  function neighborsOf(id) {
    if (neighborMap.has(id)) return neighborMap.get(id);
    const set = new Set();
    data.links.forEach(l => {
      const a = (typeof l.source === 'object') ? l.source.id : l.source;
      const b = (typeof l.target === 'object') ? l.target.id : l.target;
      if (a === id) set.add(b);
      else if (b === id) set.add(a);
    });
    neighborMap.set(id, set);
    return set;
  }

  // Threshold filtering
  const slider = document.getElementById('threshold');
  const threshVal = document.getElementById('threshVal');
  slider.addEventListener('input', () => {
    const t = +slider.value;
    threshVal.textContent = t;
    const filteredLinks = data.links.filter(d => d.value >= t);
    // Update simulation links
    simulation.force("link").links(filteredLinks);
    // Update link selection
    link = link.data(filteredLinks, d => d.source.id + "-" + d.target.id).join(
      enter => enter.append("line")
                    .attr("stroke", "#475569")
                    .attr("stroke-opacity", 0.6)
                    .attr("stroke-width", d => linkWidth(d.value)),
      update => update,
      exit => exit.remove()
    );
    neighborMap.clear();
    simulation.alpha(0.6).restart();
  });
  </script>
</body>
</html>
