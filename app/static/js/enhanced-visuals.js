(()=>{const reduce=matchMedia("(prefers-reduced-motion: reduce)").matches;
const sections=document.querySelectorAll(".motion-section");
if(!reduce&&"IntersectionObserver"in window){const io=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add("is-visible");io.unobserve(e.target)}}),{threshold:.08,rootMargin:"0px 0px -6% 0px"});sections.forEach(e=>io.observe(e));}else sections.forEach(e=>e.classList.add("is-visible"));
if(!reduce&&matchMedia("(pointer:fine)").matches){
document.querySelectorAll(".lift-card,.project-card,.impact-card,.featured-project").forEach(card=>{
card.addEventListener("pointermove",e=>{const r=card.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;card.style.transform="perspective(1000px) rotateX("+(-y*2.2)+"deg) rotateY("+(x*2.2)+"deg) translateY(-7px)"},{passive:true});
card.addEventListener("pointerleave",()=>card.style.transform="",{passive:true});
});
}
const canvas=document.getElementById("gssksAmbientCanvas");
if(!canvas||reduce)return;
const ctx=canvas.getContext("2d",{alpha:true});if(!ctx)return;
let w=0,h=0,dpr=1,raf=0;
const particles=Array.from({length:90},()=>({x:Math.random(),y:Math.random(),r:.5+Math.random()*2.2,vx:(Math.random()-.5)*.00025,vy:(Math.random()-.5)*.00018,a:.15+Math.random()*.45}));
function resize(){dpr=Math.min(devicePixelRatio||1,1.5);w=canvas.clientWidth;h=canvas.clientHeight;canvas.width=w*dpr;canvas.height=h*dpr;ctx.setTransform(dpr,0,0,dpr,0,0)}
function draw(t){ctx.clearRect(0,0,w,h);for(const p of particles){p.x+=p.vx;p.y+=p.vy;if(p.x<0||p.x>1)p.vx*=-1;if(p.y<0||p.y>1)p.vy*=-1;const x=p.x*w,y=p.y*h;ctx.beginPath();ctx.arc(x,y,p.r,0,Math.PI*2);ctx.fillStyle="rgba(234,200,120,"+p.a+")";ctx.fill()}for(let i=0;i<particles.length;i+=1){const a=particles[i];for(let j=i+1;j<Math.min(i+5,particles.length);j++){const b=particles[j],dx=(a.x-b.x)*w,dy=(a.y-b.y)*h,d=Math.hypot(dx,dy);if(d<115){ctx.beginPath();ctx.moveTo(a.x*w,a.y*h);ctx.lineTo(b.x*w,b.y*h);ctx.strokeStyle="rgba(234,200,120,"+(0.07*(1-d/115))+")";ctx.stroke()}}}raf=requestAnimationFrame(draw)}
resize();addEventListener("resize",resize,{passive:true});raf=requestAnimationFrame(draw);
addEventListener("pagehide",()=>cancelAnimationFrame(raf),{once:true});
})();