export const introState = {
  active: true,
  phase: 0,
  timer: 0,
  duration: [3, 2.5, 2.5, 3]
};

export function updateIntro(dt){
  introState.timer += dt;
  if (introState.timer > introState.duration[introState.phase]){
    introState.timer = 0;
    introState.phase++;
    if (introState.phase >= introState.duration.length){
      introState.active = false;
    }
  }
}

export function drawIntro(ctx, W, H){
  ctx.fillStyle="#030506";
  ctx.fillRect(0,0,W,H);

  switch(introState.phase){
    case 0: roadside(ctx,W,H); break;
    case 1: foldingCar(ctx,W,H,introState.timer/introState.duration[1]); break;
    case 2: briefcase(ctx,W,H,introState.timer/introState.duration[2]); break;
    case 3: monitorBoot(ctx,W,H,introState.timer/introState.duration[3]); break;
  }
}

function roadside(ctx,W,H){
  ctx.strokeStyle="#66ff9a";
  ctx.lineWidth=2;
  ctx.beginPath();
  ctx.moveTo(0,H*0.65);
  ctx.lineTo(W,H*0.65);
  ctx.stroke();

  ctx.beginPath();
  ctx.moveTo(W*0.3,H*0.62);
  ctx.lineTo(W*0.45,H*0.62);
  ctx.lineTo(W*0.5,H*0.57);
  ctx.lineTo(W*0.42,H*0.53);
  ctx.lineTo(W*0.32,H*0.53);
  ctx.closePath();
  ctx.stroke();

  ctx.fillStyle="#66ff9a";
  ctx.font="18px monospace";
  ctx.fillText("1956 — FIELD TEST SITE",W*0.28,H*0.8);
}

function foldingCar(ctx,W,H,t){
  ctx.strokeStyle="#66ff9a";
  ctx.lineWidth=2;
  const scale=1-t*0.7;
  ctx.save();
  ctx.translate(W*0.5,H*0.55);
  ctx.scale(scale,scale);
  ctx.beginPath();
  ctx.moveTo(-120,30);
  ctx.lineTo(80,30);
  ctx.lineTo(110,-10);
  ctx.lineTo(-80,-10);
  ctx.closePath();
  ctx.stroke();
  ctx.restore();
  if(t>0.5){
    ctx.strokeRect(W*0.45,H*0.5,100,60);
  }
}

function briefcase(ctx,W,H,t){
  ctx.strokeStyle="#66ff9a";
  ctx.lineWidth=2;
  const x=W*0.45;
  const y=H*0.55;
  ctx.strokeRect(x,y,110,70);
  const angle=-Math.PI/2*t;
  ctx.save();
  ctx.translate(x,y);
  ctx.rotate(angle);
  ctx.strokeRect(0,-70,110,70);
  ctx.restore();
  ctx.fillStyle="#66ff9a";
  ctx.font="16px monospace";
  ctx.fillText("PORTABLE VECTOR DEFENSE SYSTEM",W*0.25,H*0.8);
}

function monitorBoot(ctx,W,H,t){
  ctx.strokeStyle="#66ff9a";
  ctx.lineWidth=2;
  ctx.strokeRect(W*0.3,H*0.25,W*0.4,H*0.4);
  const lines=[
    "BLASTOIDS DEFENSE GRID",
    "VECTOR PROCESSOR ONLINE",
    "ASTEROID TRAJECTORY LINK",
    "COCKPIT READY"
  ];
  ctx.fillStyle="#66ff9a";
  ctx.font="20px monospace";
  const visible=Math.floor(t*lines.length);
  for(let i=0;i<visible;i++){
    ctx.fillText(lines[i],W*0.34,H*0.35+i*30);
  }
}
