<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Blastoids</title>
  <style>
    html, body {
      margin: 0;
      height: 100%;
      background: black;
      overflow: hidden;
      font-family: 'Share Tech Mono', monospace;
    }

    canvas {
      display: block;
      width: 100vw;
      height: 100vh;
      background-color: black;
    }

    body::before {
      content: "";
      pointer-events: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: repeating-linear-gradient(
        0deg,
        rgba(0, 255, 0, 0.07) 0,
        rgba(0, 255, 0, 0.07) 1px,
        transparent 1px,
        transparent 3px
      );
      z-index: 10;
    }
  </style>
</head>
<body>
  <canvas id="game"></canvas>
  <script type="module">
    const canvas = document.getElementById('game');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    class Asteroid {
      constructor() {
        this.x = Math.random() * canvas.width;
        this.y = -50;
        this.radius = 20 + Math.random() * 30;
        this.speed = 1 + Math.random() * 2;
      }

      update() {
        this.y += this.speed;
      }

      draw() {
        ctx.strokeStyle = '#0f0';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.stroke();
      }

      isHit(missile) {
        const dx = this.x - missile.x;
        const dy = this.y - missile.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        return dist < this.radius;
      }
    }

    class Missile {
      constructor(x, y) {
        this.x = x;
        this.y = y;
        this.speed = 10;
      }

      update() {
        this.y -= this.speed;
      }

      draw() {
        ctx.strokeStyle = '#0f0';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(this.x, this.y);
        ctx.lineTo(this.x, this.y - 10);
        ctx.stroke();
      }
    }

    const ship = {
      x: canvas.width / 2,
      y: canvas.height - 50,
      width: 40,
      draw() {
        ctx.strokeStyle = '#0f0';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(this.x, this.y);
        ctx.lineTo(this.x - this.width / 2, this.y + 30);
        ctx.lineTo(this.x + this.width / 2, this.y + 30);
        ctx.closePath();
        ctx.stroke();
      }
    };

    let asteroids = [];
    let missiles = [];

    function spawnAsteroid() {
      asteroids.push(new Asteroid());
    }

    function fireMissile() {
      missiles.push(new Missile(ship.x, ship.y));
    }

    function update() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ship.draw();

      for (let i = 0; i < asteroids.length; i++) {
        const a = asteroids[i];
        a.update();
        a.draw();
      }

      for (let i = 0; i < missiles.length; i++) {
        const m = missiles[i];
        m.update();
        m.draw();
      }

      // Collision detection
      for (let i = asteroids.length - 1; i >= 0; i--) {
        for (let j = missiles.length - 1; j >= 0; j--) {
          if (asteroids[i].isHit(missiles[j])) {
            asteroids.splice(i, 1);
            missiles.splice(j, 1);
            break;
          }
        }
      }

      requestAnimationFrame(update);
    }

    setInterval(spawnAsteroid, 1000);
    update();

    window.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') {
        ship.x -= 20;
      } else if (e.key === 'ArrowRight') {
        ship.x += 20;
      } else if (e.key === ' ') {
        fireMissile();
      }
    });

    window.addEventListener('resize', () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    });
  </script>
</body>
</html>

