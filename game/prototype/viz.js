export function buildInfluenceMap(sim,systems){
  const N=sim.N;
  const map=new Int16Array(N*N);
  map.fill(-1);

  for(let y=0;y<N;y++){
    for(let x=0;x<N;x++){
      let best=-1,bestScore=Infinity;
      for(let k=0;k<systems.length;k++){
        const s=systems[k];
        if(!s.owner)continue;
        const dx=x-s.x;
        const dy=y-s.y;
        const d2=dx*dx+dy*dy;
        const score=d2/(s.power()+1e-6);
        if(score<bestScore){
          bestScore=score;
          best=k;
        }
      }
      map[y*N+x]=best;
    }
  }
  return map;
}

export function drawStars(ctx,systems,factions){
  systems.forEach(s=>{
    const col=s.owner!=null?factions[s.owner]:[220,220,220];
    ctx.fillStyle=`rgb(${col[0]},${col[1]},${col[2]})`;
    ctx.beginPath();
    ctx.arc(s.x,s.y,3,0,Math.PI*2);
    ctx.fill();
  });
}
