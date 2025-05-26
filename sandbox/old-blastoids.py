from flask import Flask, Response
app = Flask(__name__)

@app.route('/')
def index():
    return Response('''
<!DOCTYPE html>
<html>
<head>
  <title>Blastoids</title>
  <style>
    html, body {
      margin: 0;
      overflow: hidden;
      background: black;
    }
    canvas {
      display: block;
      background: black;
    }
  </style>
</head>
<body>
<canvas id="game"></canvas>
<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let aimX = canvas.width / 2;
let aimY = canvas.height / 2;
let keys = {};
let missiles = [];

document.addEventListener("mousemove", e => {
  aimX = e.clientX;
  aimY = e.clientY;
});

document.addEventListener("keydown", e => {
  keys[e.key] = true;
  if (e.key === " ") {
    missiles.push({
      x: canvas.width / 2,
      y: canvas.height,
      dx: (aimX - canvas.width / 2) / 50,
      dy: (aimY - canvas.height) / 50
    });
  }
});

document.addEventListener("keyup", e => keys[e.key] = false);

class Asteroid {
  constructor() {
    this.reset();
  }
  reset() {
    const spread = 800;
    this.x = Math.random() * canvas.width;
    this.y = Math.random() * canvas.height;
    this.z = Math.random() * spread + 300;
    this.size = Math.random() * 8 + 4;
    this.speed = 0.3 + Math.random() * 0.2;
    this.alive = true;
  }
  update() {
    this.z -= this.speed;
    if (this.z < 20) this.reset();
  }
  draw(ctx) {
    if (!this.alive) return;
    let scale = 300 / this.z;
    let sx = (this.x - canvas.width / 2) * scale + canvas.width / 2;
    let sy = (this.y - canvas.height / 2) * scale + canvas.height / 2;
    let radius = this.size * scale;

    ctx.beginPath();
    ctx.arc(sx, sy, radius, 0, Math.PI * 2);
    ctx.strokeStyle = "#0f0";
    ctx.lineWidth = 1.5;
    ctx.shadowBlur = 5;
    ctx.shadowColor = "#0f0";
    ctx.stroke();
  }
  checkHit(mx, my) {
    let scale = 300 / this.z;
    let sx = (this.x - canvas.width / 2) * scale + canvas.width / 2;
    let sy = (this.y - canvas.height / 2) * scale + canvas.height / 2;
    let r = this.size * scale;
    let dx = mx - sx;
    let dy = my - sy;
    return (dx*dx + dy*dy) < (r*r);
  }
}

let asteroids = Array.from({length: 60}, () => new Asteroid());

function drawMissiles() {
  ctx.strokeStyle = "#0f0";
  ctx.lineWidth = 1;
  missiles.forEach(m => {
    m.x += m.dx;
    m.y += m.dy;

    // Check for asteroid collisions
    for (let a of asteroids) {
      if (a.alive && a.checkHit(m.x, m.y)) {
        a.alive = false;
        setTimeout(() => a.reset(), 1000);
      }
    }

    ctx.beginPath();
    ctx.moveTo(m.x, m.y);
    ctx.lineTo(m.x - m.dx * 3, m.y - m.dy * 3);
    ctx.stroke();
  });

  missiles = missiles.filter(m => m.y > 0 && m.y < canvas.height && m.x > 0 && m.x < canvas.width);
}

function drawCrosshair(x, y) {
  ctx.strokeStyle = "#0f0";
  ctx.lineWidth = 1;
  ctx.shadowBlur = 4;
  ctx.shadowColor = "#0f0";
  ctx.beginPath();
  ctx.moveTo(x - 8, y);
  ctx.lineTo(x + 8, y);
  ctx.moveTo(x, y - 8);
  ctx.lineTo(x, y + 8);
  ctx.stroke();
}

function drawCockpit() {
  ctx.strokeStyle = "#0f0";
  ctx.lineWidth = 1;
  ctx.shadowBlur = 2;
  ctx.shadowColor = "#0f0";

  ctx.beginPath();
  ctx.moveTo(canvas.width/2 - 60, canvas.height);
  ctx.lineTo(canvas.width/2 - 80, canvas.height - 100);
  ctx.lineTo(canvas.width/2 - 140, canvas.height - 250);
  ctx.moveTo(canvas.width/2 + 60, canvas.height);
  ctx.lineTo(canvas.width/2 + 80, canvas.height - 100);
  ctx.lineTo(canvas.width/2 + 140, canvas.height - 250);
  ctx.stroke();
}

function gameLoop() {
  ctx.fillStyle = "rgba(0,0,0,0.25)";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  if (keys["ArrowLeft"]) aimX -= 5;
  if (keys["ArrowRight"]) aimX += 5;
  if (keys["ArrowUp"]) aimY -= 5;
  if (keys["ArrowDown"]) aimY += 5;

  asteroids.forEach(a => {
    a.update();
    a.draw(ctx);
  });

  drawMissiles();
  drawCrosshair(aimX, aimY);
  drawCockpit();

  requestAnimationFrame(gameLoop);
}

gameLoop();
</script>
</body>
</html>
''', mimetype='text/html')

if __name__ == '__main__':
    app.run(debug=True)

