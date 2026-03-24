export function detectCorridors(sim,threshold=0.25){
  const N=sim.N;
  const visited=new Uint8Array(N*N);
  const corridors=[];
  const idx=(x,y)=>y*N+x;

  for(let y=0;y<N;y++){
    for(let x=0;x<N;x++){
      const i=idx(x,y);
      if(visited[i]||sim.S[i]>threshold)continue;

      const stack=[[x,y]];
      const region=[];

      while(stack.length){
        const [cx,cy]=stack.pop();
        const ci=idx(cx,cy);
        if(visited[ci])continue;
        visited[ci]=1;
        if(sim.S[ci]>threshold)continue;
        region.push(ci);

        [[1,0],[-1,0],[0,1],[0,-1]].forEach(d=>{
          const nx=(cx+d[0]+N)%N;
          const ny=(cy+d[1]+N)%N;
          stack.push([nx,ny]);
        });
      }

      if(region.length>150)corridors.push(region);
    }
  }
  return corridors;
}
