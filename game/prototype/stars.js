export class StarSystem {
  constructor(id,x,y,radius=6){
    this.id=id;
    this.x=x;
    this.y=y;
    this.radius=radius;

    this.owner=null;
    this.population=0;
    this.infrastructure=0;

    this.cached={phi:0,S:0,coherence:0};
  }

  sample(sim){
    const N=sim.N;
    let sumPhi=0,sumS=0,sumVX=0,sumVY=0,count=0;

    for(let dy=-this.radius;dy<=this.radius;dy++){
      for(let dx=-this.radius;dx<=this.radius;dx++){
        if(dx*dx+dy*dy>this.radius*this.radius)continue;
        const x=(this.x+dx+N)%N;
        const y=(this.y+dy+N)%N;
        const i=y*N+x;
        sumPhi+=sim.phi[i];
        sumS+=sim.S[i];
        sumVX+=sim.vx[i];
        sumVY+=sim.vy[i];
        count++;
      }
    }

    this.cached.phi=sumPhi/count;
    this.cached.S=sumS/count;
    this.cached.coherence=Math.sqrt(sumVX*sumVX+sumVY*sumVY)/count;
  }

  isHabitable(){
    return this.cached.phi>0.12 && this.cached.S<0.45;
  }

  power(){
    if(!this.owner)return 0;
    const stability=Math.max(0,this.cached.phi-0.6*this.cached.S);
    return Math.max(0.02,stability*(1+this.infrastructure));
  }

  colonize(faction){
    if(this.owner||!this.isHabitable())return false;
    this.owner=faction;
    this.population=1;
    this.infrastructure=0.2;
    return true;
  }
}
