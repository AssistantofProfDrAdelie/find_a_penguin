const $=selector=>document.querySelector(selector);
const fileInput=$("#fileInput"),dropZone=$("#dropZone"),intro=$("#intro"),encounter=$("#encounter");
const source=$("#sourceCanvas"),visitor=$("#visitorCanvas"),srcCtx=source.getContext("2d"),visitorCtx=visitor.getContext("2d");
const encounterButton=$("#encounterButton"),saveButton=$("#saveButton"),status=$("#status");
const professor=new Image();
const professorCrop={x:114,y:1035,width:1866,height:2485};
professor.src="assets/professor-adelie-owner-approved.png";
let loaded=false,professorReady=false,running=false,encounterCount=0,animationFrame=0,fileStem="penguin-encounter",savePrepared=false,saveUrl="";
professor.onload=()=>{professorReady=true;if(loaded)encounterButton.disabled=false;};

const prefersReducedMotion=()=>window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const ease=value=>value<.5?4*value*value*value:1-Math.pow(-2*value+2,3)/2;

function loadFile(file){
  if(!file||!file.type.startsWith("image/"))return;
  cancelAnimationFrame(animationFrame);running=false;saveButton.hidden=true;visitorCtx.clearRect(0,0,visitor.width,visitor.height);
  const image=new Image(),url=URL.createObjectURL(file);
  image.onload=()=>{const max=1800,scale=Math.min(1,max/Math.max(image.width,image.height));source.width=visitor.width=Math.round(image.width*scale);source.height=visitor.height=Math.round(image.height*scale);srcCtx.drawImage(image,0,0,source.width,source.height);visitorCtx.clearRect(0,0,visitor.width,visitor.height);URL.revokeObjectURL(url);loaded=true;fileStem=(file.name.replace(/\.[^.]+$/,"")||"photograph")+"-professor-adelie";saveButton.download=`${fileStem}.png`;$("#fileName").textContent=file.name;status.textContent=professorReady?"The photograph is ready.":"Professor Adelie is getting ready.";encounterButton.disabled=!professorReady;intro.hidden=true;encounter.hidden=false;encounter.scrollIntoView({behavior:"smooth",block:"start"});};
  image.onerror=()=>{URL.revokeObjectURL(url);alert("That photograph could not be opened. Please try another.");};image.src=url;
}

function placement(side,progress){
  const ratio=professorCrop.width/professorCrop.height,maxWidth=source.width*.46;let height=source.height*.68,width=height*ratio;if(width>maxWidth){width=maxWidth;height=width/ratio;}
  const y=Math.max(source.height*.2,source.height-height*.97),hidden=side==="right"?source.width+width*.035:-width*1.035,visible=side==="right"?source.width-width*.64:-width*.36;
  return{x:hidden+(visible-hidden)*progress,y,width,height};
}

function drawProfessor(side,progress){
  visitorCtx.clearRect(0,0,visitor.width,visitor.height);if(progress<=0)return;
  const{x,y,width,height}=placement(side,progress),lift=Math.sin(progress*Math.PI)*source.height*.006,lean=(1-progress)*.012*(side==="right"?-1:1);visitorCtx.save();
  visitorCtx.translate(x+width/2,y+height+lift);visitorCtx.rotate(lean);
  const draw=()=>visitorCtx.drawImage(professor,professorCrop.x,professorCrop.y,professorCrop.width,professorCrop.height,-width/2,-height,width,height);
  if(side==="left"){visitorCtx.scale(-1,1);draw();}else draw();
  visitorCtx.restore();
}

function animateEncounter(){
  if(!loaded||!professorReady||running)return;
  running=true;savePrepared=false;encounterButton.disabled=true;saveButton.hidden=true;status.textContent="Stay with the photograph for a moment.";
  const reduced=prefersReducedMotion(),pause=reduced?300:850,enter=reduced?350:1600,hold=reduced?3400:5000,leave=reduced?350:1600,total=pause+enter+hold+leave;
  const side=encounterCount++%2===0?"right":"left",started=performance.now();
  function frame(now){
    const elapsed=now-started;let progress=0;
    if(elapsed<pause)progress=0;
    else if(elapsed<pause+enter)progress=ease((elapsed-pause)/enter);
    else if(elapsed<pause+enter+hold)progress=1;
    else if(elapsed<total)progress=1-ease((elapsed-pause-enter-hold)/leave);
    drawProfessor(side,progress);
    const visiting=elapsed>=pause+enter&&elapsed<pause+enter+hold;
    if(visiting&&!savePrepared){savePrepared=true;prepareSave();}
    if(!visiting&&elapsed>=pause+enter+hold)saveButton.hidden=true;
    if(visiting)status.textContent="Professor Adelie is visiting.";
    else if(elapsed>=pause+enter+hold)status.textContent="Professor Adelie is leaving.";
    if(elapsed<total)animationFrame=requestAnimationFrame(frame);else{drawProfessor(side,0);saveButton.hidden=true;running=false;encounterButton.disabled=false;status.textContent="Until next time.";}
  }
  animationFrame=requestAnimationFrame(frame);
}

function prepareSave(){
  const output=document.createElement("canvas"),ctx=output.getContext("2d");output.width=source.width;output.height=source.height;ctx.drawImage(source,0,0);ctx.drawImage(visitor,0,0);
  output.toBlob(blob=>{if(!blob||!running)return;if(saveUrl)URL.revokeObjectURL(saveUrl);saveUrl=URL.createObjectURL(blob);saveButton.href=saveUrl;saveButton.hidden=false;},"image/png");
}

fileInput.addEventListener("change",event=>loadFile(event.target.files[0]));
["dragenter","dragover"].forEach(type=>dropZone.addEventListener(type,event=>{event.preventDefault();dropZone.classList.add("dragging");}));
["dragleave","drop"].forEach(type=>dropZone.addEventListener(type,event=>{event.preventDefault();dropZone.classList.remove("dragging");}));
dropZone.addEventListener("drop",event=>loadFile(event.dataTransfer.files[0]));
encounterButton.addEventListener("click",animateEncounter);
$("#changeButton").addEventListener("click",()=>{fileInput.value="";fileInput.click();});
