/* NEXPLAY — The Monolith. An original procedural 3D architectural scene.
   Canvas is an optional enhancement: accessible content is independent. */
(async function(){
const canvas=document.querySelector('#nexus-3d');const hero=document.querySelector('.hero-reborn');
if(!canvas||!hero||matchMedia('(prefers-reduced-motion: reduce)').matches||navigator.connection?.saveData||document.body.classList.contains('motion-off')||matchMedia('(max-width: 700px)').matches)return;
let THREE;try{THREE=await import('https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js')}catch(e){return}
let renderer;try{renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:true,powerPreference:'high-performance'});}catch(e){return}
renderer.setPixelRatio(Math.min(devicePixelRatio||1,1.5));renderer.outputColorSpace=THREE.SRGBColorSpace;
renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.0;
const scene=new THREE.Scene();scene.fog=new THREE.FogExp2(0x060e15,.021);
const camera=new THREE.PerspectiveCamera(42,1,.1,180);
camera.position.set(0,3.1,21);
const mat=(color,metalness=.4,roughness=.6)=>new THREE.MeshStandardMaterial({color,metalness,roughness,side:THREE.DoubleSide});
const dark=mat(0x101c27,.84,.36),dark2=mat(0x15212a,.87,.33),edge=mat(0x31434d,.74,.4),rock=mat(0x0e1a22,.15,.98);
const glow=new THREE.MeshBasicMaterial({color:0x86f9e5,transparent:true,opacity:.9,depthWrite:false});
function mesh(g,m,x,y,z,rotY=0){const o=new THREE.Mesh(g,m);o.position.set(x,y,z);o.rotation.y=rotY;scene.add(o);return o}
function slab(w,h,d,x,y,z,m=dark,ry=0){return mesh(new THREE.BoxGeometry(w,h,d),m,x,y,z,ry)}
// The architecture is staged as a forced-perspective temple, not disconnected decorations.
for(let i=0;i<14;i++){
 const z=10-i*5.8,wide=15+i*1.25;
 slab(2.1,18,3.1,-wide/2,5,z,i%2?dark:dark2,-.04);
 slab(2.1,18,3.1,wide/2,5,z,i%2?dark:dark2,.04);
 slab(wide+4,2.0,3.2,0,14,z,dark2);
 slab(wide-2,.08,.22,0,12.95,z,edge);
 // narrow edge luminaires create rhythm, scale and distant depth
 const strip=new THREE.MeshBasicMaterial({color:0x1aaea6,transparent:true,opacity:Math.max(.12,.4-i*.013)});
 slab(.05,8,.04,-wide/2+1,2.7,z+1.58,strip);
 slab(.05,8,.04,wide/2-1,2.7,z+1.58,strip);
}
// Elevated central causeway with illuminated perspective seams.
slab(11.5,.5,105,0,-3,-15,rock);
for(let i=0;i<28;i++){
 const z=13-i*4;
 slab(11.5,.025,.035,0,-2.71,z,edge);
}
for(const x of [-5.6,5.6]){
 slab(.045,.025,105,x,-2.67,-15,glow);
 slab(.6,.34,105,x,-2.93,-15,dark);
}
// A dimensional monolith: asymmetrical split shell, hidden heart and moving signal.
const monolith=new THREE.Group();monolith.position.set(0,2,-18);scene.add(monolith);
const physical=new THREE.MeshPhysicalMaterial({color:0x17262d,metalness:.92,roughness:.19,clearcoat:1,clearcoatRoughness:.14});
const shellL=new THREE.Mesh(new THREE.BoxGeometry(2.1,15,2.9),physical);shellL.position.x=-2.5;shellL.rotation.z=-.055;monolith.add(shellL);
const shellR=new THREE.Mesh(new THREE.BoxGeometry(2.1,15,2.9),physical);shellR.position.x=2.5;shellR.rotation.z=.055;monolith.add(shellR);
const cap=new THREE.Mesh(new THREE.BoxGeometry(7.5,1.1,3.4),physical);cap.position.y=7.1;monolith.add(cap);
const base=new THREE.Mesh(new THREE.BoxGeometry(9,1.1,4.6),physical);base.position.y=-7.3;monolith.add(base);
const lightMat=new THREE.MeshBasicMaterial({color:0x83faee,transparent:true,opacity:.92,depthWrite:false});
const signal=new THREE.Mesh(new THREE.PlaneGeometry(3.25,12),new THREE.ShaderMaterial({transparent:true,depthWrite:false,uniforms:{t:{value:0}},vertexShader:'varying vec2 uvv;void main(){uvv=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',fragmentShader:'varying vec2 uvv;uniform float t;void main(){float x=abs(uvv.x-.5);float core=pow(max(0.,1.-x*1.9),4.);float bands=.63+.37*sin(uvv.y*70.-t*2.7+sin(uvv.y*20.+t)*3.);float fade=smoothstep(0.,.12,uvv.y)*smoothstep(1.,.87,uvv.y);vec3 c=mix(vec3(.03,.23,.25),vec3(.55,1.,.9),core);gl_FragColor=vec4(c,core*bands*fade*.83);}' }));signal.position.z=1.61;monolith.add(signal);
const coreLight=new THREE.PointLight(0x58ffdf,55,38,1.5);coreLight.position.set(0,2,-14);scene.add(coreLight);
const rimLight=new THREE.PointLight(0xff9b68,12,32,1.8);rimLight.position.set(15,10,-12);scene.add(rimLight);
scene.add(new THREE.AmbientLight(0xb3d5e4,.45));
const hemi=new THREE.HemisphereLight(0x597587,0x090c12,1.1);scene.add(hemi);
// Fine atmospheric dust and long-distance depth.
const count=450,points=new Float32Array(count*3);let seed=41;const rnd=()=>{seed=(1664525*seed+1013904223)>>>0;return seed/4294967296};
for(let i=0;i<count;i++){points[i*3]=(rnd()-.5)*65;points[i*3+1]=(rnd()-.5)*25;points[i*3+2]=(rnd()-.5)*110}
const dustG=new THREE.BufferGeometry();dustG.setAttribute('position',new THREE.BufferAttribute(points,3));
const dust=new THREE.Points(dustG,new THREE.PointsMaterial({color:0x8dc8c7,size:.055,transparent:true,opacity:.4,depthWrite:false}));scene.add(dust);
let mx=0,my=0,sx=0,sy=0,visible=true,dead=false;
function resize(){let w=hero.clientWidth,h=hero.clientHeight;camera.aspect=w/h;camera.fov=w<750?58:42;camera.updateProjectionMatrix();renderer.setSize(w,h,false)}
resize();const ro=new ResizeObserver(resize);ro.observe(hero);const io=new IntersectionObserver(es=>visible=!!es[0]?.isIntersecting);io.observe(hero);
hero.addEventListener('pointermove',e=>{let r=hero.getBoundingClientRect();mx=(e.clientX/r.width-.5);my=(e.clientY/r.height-.5)},{passive:true});
hero.addEventListener('pointerleave',()=>{mx=0;my=0});
const clock=new THREE.Clock();function frame(){if(dead)return;requestAnimationFrame(frame);if(!visible||document.hidden||document.body.classList.contains('motion-off'))return;
const t=clock.getElapsedTime();sx+=(mx-sx)*.025;sy+=(my-sy)*.025;
camera.position.x=sx*3.8;camera.position.y=3.1-sy*1.6;camera.lookAt(0,1,-18);
signal.material.uniforms.t.value=t;coreLight.intensity=48+8*Math.sin(t*.9);monolith.position.y=2+Math.sin(t*.3)*.07;
renderer.render(scene,camera)}
hero.classList.add('scene-ready');requestAnimationFrame(frame);
addEventListener('pagehide',()=>{dead=true;io.disconnect();ro.disconnect();renderer.dispose()},{once:true});
})();
