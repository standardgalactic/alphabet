export class Fleet{
  constructor(id,owner,origin){
    this.id=id;
    this.owner=owner;
    this.currentStar=origin;
    this.targetStar=null;
    this.progress=0;
    this.travelTime=0;
  }

  launch(target,time){
    this.targetStar=target;
    this.travelTime=time;
    this.progress=0;
  }

  update(dt){
    if(!this.targetStar)return;
    this.progress+=dt;
    if(this.progress>=this.travelTime){
      this.currentStar=this.targetStar;
      this.targetStar=null;
    }
  }
}
