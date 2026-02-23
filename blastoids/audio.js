let ctxAudio;

export function initAudio(){
  ctxAudio = new (window.AudioContext || window.webkitAudioContext)();
}

export function bootTone(){
  const osc = ctxAudio.createOscillator();
  const gain = ctxAudio.createGain();
  osc.type="square";
  osc.frequency.value=120;
  gain.gain.value=0.05;
  osc.connect(gain);
  gain.connect(ctxAudio.destination);
  osc.start();
  osc.frequency.exponentialRampToValueAtTime(600, ctxAudio.currentTime+1.2);
  osc.stop(ctxAudio.currentTime+1.2);
}

export function fireSound(){
  const osc = ctxAudio.createOscillator();
  const gain = ctxAudio.createGain();
  osc.type="triangle";
  osc.frequency.value=800;
  gain.gain.value=0.04;
  osc.connect(gain);
  gain.connect(ctxAudio.destination);
  osc.start();
  osc.stop(ctxAudio.currentTime+0.08);
}
