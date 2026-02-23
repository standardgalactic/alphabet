import { introState, updateIntro, drawIntro } from "./intro.js";
import { initAudio, bootTone, fireSound } from "./audio.js";

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const overlay = document.getElementById("overlay");

let W, H;
function resize(){
  W = canvas.width = window.innerWidth;
  H = canvas.height = window.innerHeight;
}
resize();
window.addEventListener("resize", resize);

initAudio();

const state = {
  running: false,
  asteroids: [],
  bullets: [],
  reticle: { x: 0, y: 0 },
  score: 0,
  combo: 0,
  overheat: 0,
  spawnTimer: 0,
  spawnRate: 0.6  // faster spawn
};

canvas.addEventListener("mousemove", e=>{
  state.reticle.x = e.clientX;
  state.reticle.y = e.clientY;
});

canvas.addEventListener("mousedown", ()=>{
  fire();
});

window.addEventListener("keydown", e=>{
  if(e.key === "Enter" && !introState.active){
    state.running = true;
  }
  if(e.code === "Space"){
    fire();
  }
});

function fire(){
  if(!state.running) return;
  if(state.overheat > 1) return;

  fireSound();
  state.overheat += 0.15;

  state.bullets.push({
    x: W/2,
    y: H * 0.85,
    vx: (state.reticle.x - W/2) * 4,
    vy: (state.reticle.y - H*0.85) * 4
  });
}

function makeAsteroid(){
  const shard = Math.random() < 0.35;
  const size = shard ? 15 : 40;
  const speed = shard ? 250 : 120;

  state.asteroids.push({
    x: Math.random() * W,
    y: -50,
    vx: (Math.random()-0.5)*40,
    vy: speed,
    r: size,
    hp: shard ? 1 : 3,
    shard
  });
}

let last = 0;
function loop(ts){
  const dt = (ts - last) / 1000;
  last = ts;

  update(dt);
  draw();

  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);

function update(dt){

  if(introState.active){
    updateIntro(dt);
    if(!introState.active){
      bootTone();
      overlay.innerText = "PRESS ENTER TO ENGAGE";
    }
    return;
  }

  if(!state.running) return;

  state.spawnTimer += dt;
  if(state.spawnTimer > state.spawnRate){
    state.spawnTimer = 0;
    makeAsteroid();
  }

  state.overheat = Math.max(0, state.overheat - dt * 0.4);

  for(const a of state.asteroids){
    a.x += a.vx * dt;
    a.y += a.vy * dt;
  }

  for(const b of state.bullets){
    b.x += b.vx * dt;
    b.y += b.vy * dt;
  }

  // Remove offscreen
  state.asteroids = state.asteroids.filter(a => a.y < H + 100);
  state.bullets = state.bullets.filter(b => b.y > -100 && b.x > -100 && b.x < W+100);

  // Collision
  for(const a of state.asteroids){
    for(const b of state.bullets){
      const d = Math.hypot(a.x - b.x, a.y - b.y);
      if(d < a.r){
        a.hp--;
        b.dead = true;
        if(a.hp <= 0){
          state.score += a.shard ? 100 : 200;
          state.combo++;
          a.dead = true;
        }
      }
    }
  }

  state.bullets = state.bullets.filter(b => !b.dead);
  state.asteroids = state.asteroids.filter(a => !a.dead);

  overlay.innerText =
    `SCORE ${state.score}   COMBO ${state.combo}   HEAT ${(state.overheat*100|0)}%`;
}

function draw(){

  if(introState.active){
    drawIntro(ctx, W, H);
    return;
  }

  ctx.fillStyle = "#020304";
  ctx.fillRect(0,0,W,H);

  drawCRT();

  ctx.strokeStyle = "#66ff9a";
  ctx.lineWidth = 2;

  // Asteroids
  for(const a of state.asteroids){
    ctx.beginPath();
    ctx.arc(a.x, a.y, a.r, 0, Math.PI*2);
    ctx.stroke();
  }

  // Bullets
  for(const b of state.bullets){
    ctx.beginPath();
    ctx.moveTo(b.x, b.y);
    ctx.lineTo(b.x, b.y+12);
    ctx.stroke();
  }

  drawReticle();
}

function drawReticle(){
  const x = state.reticle.x;
  const y = state.reticle.y;

  ctx.strokeStyle = "#66ff9a";
  ctx.beginPath();
  ctx.arc(x, y, 18, 0, Math.PI*2);
  ctx.stroke();
}

function drawCRT(){
  ctx.fillStyle = "rgba(0,255,120,0.03)";
  ctx.fillRect(0,0,W,H);

  ctx.fillStyle = "rgba(0,0,0,0.25)";
  for(let i=0;i<H;i+=4){
    ctx.fillRect(0,i,W,2);
  }
}
