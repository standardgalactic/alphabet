import { introState, updateIntro, drawIntro } from "./intro.js";
import { initAudio, bootTone, fireSound } from "./audio.js";

const canvas=document.getElementById("game");
const ctx=canvas.getContext("2d");
const overlay=document.getElementById("overlay");

let W,H;
function resize(){
  W=canvas.width=window.innerWidth;
  H=canvas.height=window.innerHeight;
}
resize();
window.addEventListener("resize",resize);

initAudio();

const state={
  running:false,
  asteroids:[],
  bullets:[],
  reticle:{x:0,y:0},
  score:0,
  combo:0,
  overheat:0,
  spawnTimer:0,
  spawnRate:1.2
};

canvas.addEventListener("mousemove",e=>{
  state.reticle.x=e.clientX;
  state.reticle.y=e.clientY;
});

window.addEventListener("keydown",e=>{
  if(e.key==="Enter" && !state.running && !introState.active){
    state.running=true;
  }
  if(e.key===" "){
    fire();
  }
});

function fire(){
  if(state.overheat>1) return;
  fireSound();
  state.overheat+=0.15;
  state.bullets.push({
    x:W/2,
    y:H,
    vx:(state.reticle.x-W/2)*3,
    vy:(state.reticle.y-H)*3
  });
}

function makeAsteroid(){
  const shard=Math.random()<0.35;
  const size=shard?Math.random()*12+10:Math.random()*30+30;
  const speed=shard?Math.random()*250+250:Math.random()*120+80;
  state.asteroids.push({
    x:Math.random()*W,
    y:-size,
    vx:0,
    vy:speed,
    r:size,
    hp:shard?1:Math.ceil(size/15),
    shard
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
    if(!introState.active) bootTone();
    return;
  }

  if(!state.running) return;

  state.spawnTimer+=dt;
  if(state.spawnTimer>state.spawnRate){
    state.spawnTimer=0;
    makeAsteroid();
  }

  state.overheat=Math.max(0,state.overheat-dt*0.25);

  for(const a of state.asteroids){
    a.y+=a.vy*dt;
  }

  for(const b of state.bullets){
    b.x+=b.vx*dt;
    b.y+=b.vy*dt;
  }

  state.asteroids=state.asteroids.filter(a=>a.y<H+100);

  for(const a of state.asteroids){
    for(const b of state.bullets){
      const d=Math.hypot(a.x-b.x,a.y-b.y);
      if(d<a.r){
        a.hp--;
        b.dead=true;
        if(a.hp<=0){
          state.score+=a.shard?100:200;
          state.combo++;
          a.dead=true;
        }
      }
    }
  }

  state.bullets=state.bullets.filter(b=>!b.dead);
  state.asteroids=state.asteroids.filter(a=>!a.dead);

  overlay.innerText=`SCORE ${state.score}   COMBO ${state.combo}   HEAT ${(state.overheat*100)|0}%`;
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
  ctx.lineWidth=1;

  for(const a of state.asteroids){
    ctx.beginPath();
    ctx.arc(a.x,a.y,a.r,0,Math.PI*2);
    ctx.stroke();
  }

  for(const b of state.bullets){
    ctx.beginPath();
    ctx.moveTo(b.x,b.y);
    ctx.lineTo(b.x,b.y+10);
    ctx.stroke();
  }

  drawReticle();
}

function drawReticle(){
  const x=state.reticle.x;
  const y=state.reticle.y;
  ctx.strokeStyle="#66ff9a";
  ctx.beginPath();
  ctx.arc(x,y,15,0,Math.PI*2);
  ctx.stroke();
}

function drawCRT(){
  ctx.fillStyle="rgba(0,255,120,0.03)";
  ctx.fillRect(0,0,W,H);
  ctx.fillStyle="rgba(0,0,0,0.2)";
  for(let i=0;i<H;i+=4){
    ctx.fillRect(0,i,W,2);
  }
}
