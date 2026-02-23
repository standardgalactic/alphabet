import { FieldSim } from "./sim.js";
import { StarSystem } from "./stars.js";
import { Fleet } from "./fleets.js";
import { computeTravelTime } from "./movement.js";
import { buildInfluenceMap } from "./viz.js";

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const N = 256;
const sim = new FieldSim(N);

// ---- Resize Logic ----
function resize() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
window.addEventListener("resize", resize);
resize();

// ---- View State ----
let zoom = Math.min(canvas.width, canvas.height) / N;
let offsetX = (canvas.width - N * zoom) / 2;
let offsetY = (canvas.height - N * zoom) / 2;

// ---- Galaxy Setup ----
const systems = [];
for (let i = 0; i < 40; i++) {
  systems.push(new StarSystem(
    i,
    (Math.random() * N) | 0,
    (Math.random() * N) | 0
  ));
}

const factions = [
  [90, 170, 255],
  [255, 120, 120]
];

systems[0].owner = 0;
systems[1].owner = 1;

const fleets = [];
let nextFleetId = 0;
let influenceMap = buildInfluenceMap(sim, systems);

let selectedStar = null;

// ---- Coordinate Conversion ----
function worldToScreen(x, y) {
  return [
    x * zoom + offsetX,
    y * zoom + offsetY
  ];
}

function screenToWorld(x, y) {
  return [
    (x - offsetX) / zoom,
    (y - offsetY) / zoom
  ];
}

// ---- Zoom (Centered on Mouse) ----
canvas.addEventListener("wheel", e => {
  e.preventDefault();

  const mouseX = e.clientX;
  const mouseY = e.clientY;

  const [wx, wy] = screenToWorld(mouseX, mouseY);

  const factor = e.deltaY > 0 ? 0.9 : 1.1;
  zoom *= factor;
  zoom = Math.max(0.5, Math.min(8, zoom));

  offsetX = mouseX - wx * zoom;
  offsetY = mouseY - wy * zoom;
});

// ---- Drag To Pan ----
let dragging = false;
let lastX = 0;
let lastY = 0;

canvas.addEventListener("mousedown", e => {
  if (e.button === 1 || e.button === 2) {
    dragging = true;
    lastX = e.clientX;
    lastY = e.clientY;
  }
});

canvas.addEventListener("mousemove", e => {
  if (!dragging) return;

  const dx = e.clientX - lastX;
  const dy = e.clientY - lastY;

  offsetX += dx;
  offsetY += dy;

  lastX = e.clientX;
  lastY = e.clientY;
});

canvas.addEventListener("mouseup", () => dragging = false);
canvas.addEventListener("contextmenu", e => e.preventDefault());

// ---- Left Click Select / Launch ----
canvas.addEventListener("click", e => {
  const [wx, wy] = screenToWorld(e.clientX, e.clientY);

  const star = systems.find(s =>
    Math.hypot(s.x - wx, s.y - wy) < 4
  );

  if (!star) return;

  if (!selectedStar) {
    selectedStar = star;
  } else {
    if (selectedStar.owner === 0) {
      const fleet = new Fleet(nextFleetId++, 0, selectedStar);
      const time = computeTravelTime(selectedStar, star);
      fleet.launch(star, time);
      fleets.push(fleet);
    }
    selectedStar = null;
  }
});

// ---- Main Loop ----
function loop() {
  sim.step(0.08);

  systems.forEach(s => s.sample(sim));
  influenceMap = buildInfluenceMap(sim, systems);
  fleets.forEach(f => f.update(0.1));

  render();
  requestAnimationFrame(loop);
}

// ---- Render ----
function render() {
  ctx.fillStyle = "black";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Draw Field
  for (let y = 0; y < N; y++) {
    for (let x = 0; x < N; x++) {
      const i = y * N + x;
      const phi = sim.phi[i];

      const brightness = Math.max(0, Math.min(1, phi * 4));
      const c = brightness * 255;

      const [sx, sy] = worldToScreen(x, y);

      ctx.fillStyle = `rgb(${c},${c},${c})`;
      ctx.fillRect(sx, sy, zoom + 0.5, zoom + 0.5);
    }
  }

  // Draw Stars
  systems.forEach(s => {
    const [sx, sy] = worldToScreen(s.x, s.y);

    ctx.fillStyle = s.owner !== null
      ? `rgb(${factions[s.owner].join(",")})`
      : "white";

    ctx.beginPath();
    ctx.arc(sx, sy, Math.max(3, zoom * 0.8), 0, Math.PI * 2);
    ctx.fill();

    if (s === selectedStar) {
      ctx.strokeStyle = "yellow";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(sx, sy, Math.max(8, zoom * 2), 0, Math.PI * 2);
      ctx.stroke();
    }
  });

  // Draw Fleet Routes
  fleets.forEach(f => {
    if (!f.targetStar) return;

    const [ax, ay] = worldToScreen(
      f.currentStar.x,
      f.currentStar.y
    );
    const [bx, by] = worldToScreen(
      f.targetStar.x,
      f.targetStar.y
    );

    ctx.strokeStyle = "lime";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(ax, ay);
    ctx.lineTo(bx, by);
    ctx.stroke();
  });
}

loop();
