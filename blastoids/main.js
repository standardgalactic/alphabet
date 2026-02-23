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
  cockpit: true,
  asteroids: [],
  bullets: [],
  reticle: { x: 0, y: 0 },
  score: 0,
  overheat: 0,
  spawnTimer: 0,
  spawnRate: 0.7
};

canvas.addEventListener("mousemove", e=>{
  state.reticle.x = e.clientX;
  state.reticle.y = e.clientY;
});

window.addEventListener("keydown", e=>{
  if(!introState.active && !state.running){
    state.running = true;
  }
  if(e.code === "Space") fire();
  if(e.key === "c" || e.key === "C"){
    state.cockpit = !state.cockpit;
  }
});

canvas.addEventListener("mousedown", fire);

function fire(){
  if(!state.running) return;
  if(state.overheat > 1) return;

  fireSound();
  state.overheat += 0.12;

  const leftX = W*0.4;
  const rightX = W*0.6;
  const originY = H*0.8;

  state.bullets.push(
    makeBullet(leftX, originY),
    makeBullet(rightX, originY)
  );
}

function makeBullet(x,y){
  return {
    x,
    y,
    vx:(state.reticle.x - x)*3,
    vy:(state.reticle.y - y)*3
  };
}

function makeAsteroid(){
  const shape = [];
  const points = 8 + Math.floor(Math.random()*5);
  for(let i=0;i<points;i++){
    const angle = (Math.PI*2/points)*i;
    const radius = 0.7 + Math.random()*0.6;
    shape.push({angle, radius});
  }

  state.asteroids.push({
    x:(Math.random()-0.5)*2,
    y:(Math.random()-0.5)*2,
    z:Math.random()*1 + 0.2,
    shape,
    spin:(Math.random()-0.5)*2
  });
}

let last=0;
function loop(ts){
  const dt=(ts-last)/1000;
  last=ts;
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
      overlay.innerText = "PRESS ANY KEY";
    }
    return;
  }

  if(!state.running) return;

  state.spawnTimer+=dt;
  if(state.spawnTimer>state.spawnRate){
    state.spawnTimer=0;
    makeAsteroid();
  }

  state.overheat=Math.max(0,state.overheat-dt*0.4);

  for(const a of state.asteroids){
    a.z -= dt*0.5;
    a.spin += dt;
  }

  state.asteroids = state.asteroids.filter(a=>a.z>0);

  for(const b of state.bullets){
    b.x+=b.vx*dt;
    b.y+=b.vy*dt;
  }

  state.bullets = state.bullets.filter(b=>b.y>-50 && b.y<H+50);

  overlay.innerText =
    `SCORE ${state.score}   HEAT ${(state.overheat*100|0)}%`;
}

function draw(){

  if(introState.active){
    drawIntro(ctx,W,H);
    return;
  }

  ctx.fillStyle="#020304";
  ctx.fillRect(0,0,W,H);

  drawCRT();

  ctx.strokeStyle="#66ff9a";
  ctx.lineWidth=2;

  drawAsteroids();
  drawBullets();
  drawReticle();

  if(state.cockpit) drawCockpit();
}

function project(x,y,z){
  const f=400;
  const scale=f/z;
  return {
    x:W/2 + x*scale,
    y:H/2 + y*scale,
    scale
  };
}

function drawAsteroids(){
  for(const a of state.asteroids){
    const p = project(a.x,a.y,a.z);
    const size = 60 * p.scale*0.01;

    ctx.beginPath();
    for(let i=0;i<a.shape.length;i++){
      const s=a.shape[i];
      const angle=s.angle + a.spin;
      const r=size*s.radius;
      const x=p.x + Math.cos(angle)*r;
      const y=p.y + Math.sin(angle)*r;
      if(i===0) ctx.moveTo(x,y);
      else ctx.lineTo(x,y);
    }
    ctx.closePath();
    ctx.stroke();
  }
}

function drawBullets(){
  for(const b of state.bullets){
    ctx.beginPath();
    ctx.moveTo(b.x,b.y);
    ctx.lineTo(b.x,b.y+8);
    ctx.stroke();
  }
}

function drawReticle(){
  const x=state.reticle.x;
  const y=state.reticle.y;
  ctx.beginPath();
  ctx.arc(x,y,15,0,Math.PI*2);
  ctx.stroke();
}

function drawCockpit(){
  ctx.strokeStyle="#66ff9a";
  ctx.lineWidth=2;

  ctx.beginPath();
  ctx.moveTo(W*0.2,H);
  ctx.lineTo(W*0.35,H*0.75);
  ctx.lineTo(W*0.65,H*0.75);
  ctx.lineTo(W*0.8,H);
  ctx.stroke();

  ctx.beginPath();
  ctx.arc(W*0.4,H*0.85,20,0,Math.PI*2);
  ctx.stroke();

  ctx.beginPath();
  ctx.arc(W*0.6,H*0.85,20,0,Math.PI*2);
  ctx.stroke();
}

function drawCRT(){
  ctx.fillStyle="rgba(0,255,120,0.03)";
  ctx.fillRect(0,0,W,H);
  ctx.fillStyle="rgba(0,0,0,0.25)";
  for(let i=0;i<H;i+=4){
    ctx.fillRect(0,i,W,2);
  }
}
