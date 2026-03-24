export class FieldSim {
  constructor(N = 256) {
    this.N = N;
    this.size = N * N;

    this.phi = new Float32Array(this.size);
    this.S   = new Float32Array(this.size);
    this.vx  = new Float32Array(this.size);
    this.vy  = new Float32Array(this.size);

    this.init();
  }

  init() {
    for (let i = 0; i < this.size; i++) {
      this.phi[i] = 0.15 + 0.02 * (Math.random() - 0.5);
      this.S[i]   = 0.2 + 0.03 * Math.random();
      this.vx[i]  = 0;
      this.vy[i]  = 0;
    }
  }

  idx(x,y) { return y*this.N + x; }

  lap(arr,x,y){
    const N=this.N;
    const xm=(x-1+N)%N, xp=(x+1)%N;
    const ym=(y-1+N)%N, yp=(y+1)%N;
    return arr[this.idx(xp,y)]
         + arr[this.idx(xm,y)]
         + arr[this.idx(x,yp)]
         + arr[this.idx(x,ym)]
         - 4*arr[this.idx(x,y)];
  }

  step(dt=0.12){
    const N=this.N;
    const newPhi=new Float32Array(this.size);
    const newS=new Float32Array(this.size);

    for(let y=0;y<N;y++){
      for(let x=0;x<N;x++){
        const i=this.idx(x,y);

        const Lphi=this.lap(this.phi,x,y);
        const L2phi=this.lap(new Float32Array([Lphi])[0],0,0);

        newPhi[i]=this.phi[i]
          + dt*( -0.4*Lphi -0.2*L2phi - 0.6*this.phi[i]*this.phi[i]*this.phi[i] );

        newS[i]=this.S[i]
          + dt*( 0.3*Math.abs(Lphi) + 0.1*(this.vx[i]*this.vx[i]+this.vy[i]*this.vy[i]) );
      }
    }

    this.phi=newPhi;
    this.S=newS;
  }
}
