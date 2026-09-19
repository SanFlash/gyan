(()=>{const canvas=document.getElementById("gyanpath-3d");if(!canvas||typeof THREE==="undefined"||matchMedia("(prefers-reduced-motion: reduce)").matches)return;
const scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(50,innerWidth/innerHeight,.1,100);camera.position.z=6;
const renderer=new THREE.WebGLRenderer({canvas,alpha:true,antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));renderer.setSize(innerWidth,innerHeight);
const group=new THREE.Group();
const knot=new THREE.Mesh(new THREE.TorusKnotGeometry(1.35,.055,140,14),new THREE.MeshBasicMaterial({color:0xeac878,transparent:true,opacity:.42}));
const ring=new THREE.Mesh(new THREE.TorusGeometry(2.05,.014,14,120),new THREE.MeshBasicMaterial({color:0xc96545,transparent:true,opacity:.38}));ring.rotation.x=1.1;
const ring2=new THREE.Mesh(new THREE.TorusGeometry(2.55,.008,10,120),new THREE.MeshBasicMaterial({color:0xf1bd75,transparent:true,opacity:.24}));ring2.rotation.y=.7;
group.add(knot,ring,ring2);scene.add(group);
const stars=new THREE.BufferGeometry(),count=260,positions=new Float32Array(count*3);
for(let i=0;i<count*3;i+=3){positions[i]=(Math.random()-.5)*11;positions[i+1]=(Math.random()-.5)*7;positions[i+2]=(Math.random()-.5)*5;}
stars.setAttribute("position",new THREE.BufferAttribute(positions,3));
const points=new THREE.Points(stars,new THREE.PointsMaterial({color:0xeac878,size:.018,transparent:true,opacity:.65}));scene.add(points);
const onResize=()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight)};addEventListener("resize",onResize,{passive:true});
let t=0;const tick=()=>{t+=.008;group.rotation.x+=.0012;group.rotation.y+=.002;ring.rotation.z-=.0012;ring2.rotation.z+=.0007;points.rotation.y+=.00035;points.position.y=Math.sin(t)*.06;renderer.render(scene,camera);requestAnimationFrame(tick)};tick()})();