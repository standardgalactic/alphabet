import {FieldSim} from "./sim.js";
import {StarSystem} from "./stars.js";
import {detectCorridors} from "./corridors.js";
import {Fleet} from "./fleets.js";
import {computeTravelTime} from "./movement.js";
import {buildInfluenceMap,drawStars} from "./viz.js";

const canvas=document.getElementById("canvas");
const ctx=canvas.getContext("2d");
canvas.width=256;
canvas.height=256;

const sim=new FieldSim(256);

const systems=[];
for(let i=0;i<30;i++){
  systems.push(new StarSystem(i,Math.random()*256|0,Math.random()*256|0));
}

const factions=[[90,170,255],[255,120,120]];
systems[0].owner=0;
systems[1].owner=1;

let influenceMap=buildInfluenceMap(sim,systems);

function loop(){
  sim.step();
  influenceMap=buildInfluenceMap(sim,systems);
  render();
  requestAnimationFrame(loop);
}

function render(){
  const img=ctx.createImageData(256,256);
  for(let i=0;i<sim.size;i++){
    const v=Math.max(0,Math.min(1,sim.phi[i]*2));
    const c=(v*255)|0;
    const j=i*4;
    img.data[j]=c;
    img.data[j+1]=c;
    img.data[j+2]=c;
    img.data[j+3]=255;
  }
  ctx.putImageData(img,0,0);
  drawStars(ctx,systems,factions);
}

loop();
