export function computeTravelTime(a,b){
  const dx=a.x-b.x;
  const dy=a.y-b.y;
  const dist=Math.sqrt(dx*dx+dy*dy);
  return dist/8;
}
