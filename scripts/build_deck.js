/* Pitch deck template "Northstar" — 12 slides, Midnight Executive palette.
   Build: node scripts/build_deck.js  → templates/pitch-deck/pitch-deck.pptx */
const pptxgen = require("pptxgenjs");
const NAVY="1E2761", ICE="CADCFC", WHT="FFFFFF", INKL="2A2E3A", MUT="6B7280", LITE="F4F7FE";
const HF="Georgia", BF="Calibri";
let P = new pptxgen();
P.layout="LAYOUT_16x9"; P.author="murzi.studio"; P.title="Northstar Pitch Deck";

const W=10,H=5.625;
function darkSlide(){let s=P.addSlide();s.background={color:NAVY};return s}
function lightSlide(kicker,title){
  let s=P.addSlide();s.background={color:WHT};
  s.addText(kicker.toUpperCase(),{x:.55,y:.42,w:6,h:.3,fontFace:BF,fontSize:11,bold:true,color:MUT,charSpacing:3,margin:0});
  s.addText(title,{x:.5,y:.72,w:9,h:.75,fontFace:HF,fontSize:30,bold:true,color:NAVY,margin:0});
  s.addText("NORTHSTAR",{x:8.1,y:5.22,w:1.5,h:.25,fontFace:BF,fontSize:8,color:MUT,charSpacing:2,align:"right"});
  return s;
}
function numDot(s,x,y,n,dark=false){
  s.addShape(P.shapes.OVAL,{x,y,w:.42,h:.42,fill:{color:dark?ICE:NAVY}});
  s.addText(String(n),{x,y:y-0.005,w:.42,h:.42,align:"center",valign:"middle",fontFace:BF,fontSize:14,bold:true,color:dark?NAVY:WHT,margin:0});
}

/* 1 — Cover (dark) */
let s=darkSlide();
s.addShape(P.shapes.OVAL,{x:7.1,y:-1.6,w:4.6,h:4.6,fill:{color:"253070"}});
s.addShape(P.shapes.OVAL,{x:8.2,y:3.9,w:2.6,h:2.6,fill:{color:"253070"}});
s.addText("NORTHSTAR",{x:.6,y:.55,w:4,h:.3,fontFace:BF,fontSize:13,bold:true,color:ICE,charSpacing:4,margin:0});
s.addText("Navigation for\nteams in the dark.",{x:.55,y:1.7,w:7.5,h:1.9,fontFace:HF,fontSize:44,bold:true,color:WHT,margin:0});
s.addText("Seed round · 2026",{x:.6,y:3.85,w:4,h:.3,fontFace:BF,fontSize:14,color:ICE,margin:0});
s.addText("Replace this tagline with one sentence about your company.",{x:.6,y:4.7,w:5.6,h:.35,fontFace:BF,fontSize:11,italic:true,color:"8E97C9",margin:0});

/* 2 — Problem */
s=lightSlide("The problem","Teams fly blind between meetings.");
const probs=[["73%","of projects slip because status lives in someone's head."],
["11 hrs","per week wasted reconstructing who is doing what."],
["$47B","lost annually to misalignment in mid-size companies."]];
probs.forEach((p,i)=>{const x=.55+i*3.15;
  s.addShape(P.shapes.ROUNDED_RECTANGLE,{x,y:1.85,w:2.85,h:2.9,fill:{color:LITE},rectRadius:.08});
  s.addText(p[0],{x:x+.25,y:2.15,w:2.4,h:.85,fontFace:HF,fontSize:40,bold:true,color:NAVY,margin:0});
  s.addText(p[1],{x:x+.25,y:3.15,w:2.4,h:1.3,fontFace:BF,fontSize:13,color:INKL,margin:0});});

/* 3 — Solution */
s=lightSlide("The solution","One quiet source of truth.");
s.addShape(P.shapes.ROUNDED_RECTANGLE,{x:5.6,y:1.7,w:3.9,h:3.3,fill:{color:NAVY},rectRadius:.1});
s.addText("Drop your product\nscreenshot here",{x:5.6,y:1.7,w:3.9,h:3.3,align:"center",valign:"middle",fontFace:BF,fontSize:13,italic:true,color:"8E97C9"});
const sol=[["Connect","Plugs into the tools your team already uses in under five minutes."],
["Understand","Builds a live map of work, owners and blockers automatically."],
["Act","Sends the right nudge to the right person before things slip."]];
sol.forEach((p,i)=>{const y=1.8+i*1.05;
  numDot(s,.6,y,i+1);
  s.addText(p[0],{x:1.2,y:y-0.04,w:4.1,h:.35,fontFace:BF,fontSize:15,bold:true,color:NAVY,margin:0});
  s.addText(p[1],{x:1.2,y:y+.3,w:4.1,h:.6,fontFace:BF,fontSize:12,color:INKL,margin:0});});

/* 4 — Product */
s=lightSlide("Product","See the whole company on one screen.");
s.addShape(P.shapes.ROUNDED_RECTANGLE,{x:.55,y:1.75,w:5.4,h:3.25,fill:{color:NAVY},rectRadius:.1});
s.addText("Product screenshot 16:10",{x:.55,y:1.75,w:5.4,h:3.25,align:"center",valign:"middle",fontFace:BF,fontSize:13,italic:true,color:"8E97C9"});
const feats=[["Live work map","Every project, owner and dependency, always current."],
["Smart nudges","Quiet pings that prevent slips instead of reporting them."],
["Exec digest","A Monday brief your leadership actually reads."]];
feats.forEach((f,i)=>{const y=1.8+i*1.05;
  s.addShape(P.shapes.RECTANGLE,{x:6.25,y:y+.05,w:.14,h:.7,fill:{color:ICE}});
  s.addText(f[0],{x:6.55,y:y-0.04,w:3,h:.35,fontFace:BF,fontSize:15,bold:true,color:NAVY,margin:0});
  s.addText(f[1],{x:6.55,y:y+.3,w:3,h:.62,fontFace:BF,fontSize:12,color:INKL,margin:0});});

/* 5 — Market */
s=lightSlide("Market","A big market getting bigger.");
const rings=[["TAM","$24B",3.2],["SAM","$6.1B",2.3],["SOM","$420M",1.45]];
rings.forEach((r,i)=>{const d=r[2];
  s.addShape(P.shapes.OVAL,{x:1.1+(3.2-d)/2,y:1.95+(3.2-d)/2,w:d,h:d,fill:{color:i==2?NAVY:WHT},line:{color:NAVY,width:1.5,dashType:i==0?"dash":"solid"}});});
s.addText("$420M",{x:1.95,y:3.25,w:1.5,h:.5,align:"center",fontFace:HF,fontSize:20,bold:true,color:WHT,margin:0});
const mk=[["TAM — $24B","All team-coordination software, growing 14% a year."],
["SAM — $6.1B","Mid-market companies, 50 to 2,000 seats."],
["SOM — $420M","Our beachhead: product-led tech companies."]];
mk.forEach((m,i)=>{const y=2+i*.95;
  s.addText(m[0],{x:5.3,y,w:4.2,h:.35,fontFace:BF,fontSize:15,bold:true,color:NAVY,margin:0});
  s.addText(m[1],{x:5.3,y:y+.32,w:4.2,h:.5,fontFace:BF,fontSize:12,color:INKL,margin:0});});

/* 6 — Business model */
s=lightSlide("Business model","Simple per-seat SaaS.");
const tiers=[["Team","$12","per seat / month",LITE,NAVY],["Business","$29","per seat / month",NAVY,WHT],["Enterprise","Custom","SSO, audit, SLA",LITE,NAVY]];
tiers.forEach((t,i)=>{const x=.55+i*3.15;
  s.addShape(P.shapes.ROUNDED_RECTANGLE,{x,y:1.85,w:2.85,h:2.55,fill:{color:t[3]},rectRadius:.08});
  s.addText(t[0],{x:x+.25,y:2.1,w:2.4,h:.3,fontFace:BF,fontSize:13,bold:true,color:t[4]===WHT?ICE:MUT,charSpacing:2,margin:0});
  s.addText(t[1],{x:x+.25,y:2.5,w:2.4,h:.8,fontFace:HF,fontSize:34,bold:true,color:t[4],margin:0});
  s.addText(t[2],{x:x+.25,y:3.35,w:2.4,h:.4,fontFace:BF,fontSize:12,color:t[4]===WHT?ICE:INKL,margin:0});});
s.addText("112% net revenue retention in pilot accounts.",{x:.55,y:4.7,w:9,h:.35,fontFace:BF,fontSize:13,italic:true,color:MUT,margin:0});

/* 7 — Traction (bar chart) */
s=lightSlide("Traction","Revenue is compounding.");
s.addChart(P.charts.BAR,[{name:"MRR ($k)",labels:["Q1","Q2","Q3","Q4","Q1 '26"],values:[18,31,52,84,128]}],
 {x:.55,y:1.7,w:5.6,h:3.3,barDir:"col",chartColors:[NAVY],catAxisLabelColor:MUT,valAxisLabelColor:MUT,
  dataLabelColor:NAVY,showValue:true,dataLabelPosition:"outEnd",valAxisHidden:true,valGridLine:{style:"none"},catAxisLineColor:"DDDDDD"});
const tr=[["$128k","MRR, growing 22% m/m"],["96","paying companies"],["62","NPS across all plans"]];
tr.forEach((t,i)=>{const y=1.85+i*1.0;
  s.addText(t[0],{x:6.5,y,w:3,h:.5,fontFace:HF,fontSize:26,bold:true,color:NAVY,margin:0});
  s.addText(t[1],{x:6.5,y:y+.5,w:3,h:.3,fontFace:BF,fontSize:12,color:INKL,margin:0});});

/* 8 — Competition 2x2 */
s=lightSlide("Competition","We own the quiet quadrant.");
const cx=3.0,cy=3.45,cw=4.6,ch=2.9;
s.addShape(P.shapes.LINE,{x:cx-cw/2,y:cy,w:cw,h:0,line:{color:"C9CEDC",width:1.5}});
s.addShape(P.shapes.LINE,{x:cx,y:cy-ch/2,w:0,h:ch,line:{color:"C9CEDC",width:1.5}});
s.addText("Proactive",{x:cx-.7,y:cy-ch/2-.34,w:1.4,h:.25,align:"center",fontFace:BF,fontSize:10,color:MUT,margin:0});
s.addText("Reactive",{x:cx-.7,y:cy+ch/2+.08,w:1.4,h:.25,align:"center",fontFace:BF,fontSize:10,color:MUT,margin:0});
s.addText("Simple",{x:cx-cw/2-.85,y:cy-.12,w:.8,h:.25,align:"right",fontFace:BF,fontSize:10,color:MUT,margin:0});
s.addText("Heavy",{x:cx+cw/2+.07,y:cy-.12,w:.8,h:.25,fontFace:BF,fontSize:10,color:MUT,margin:0});
[["Spreadsheets",cx-1.7,cy+.75],["Legacy PM",cx+1.0,cy+.55],["Dashboards",cx+1.15,cy-.95]].forEach(c=>{
  s.addShape(P.shapes.OVAL,{x:c[1],y:c[2],w:.16,h:.16,fill:{color:"9AA3B8"}});
  s.addText(c[0],{x:c[1]+.22,y:c[2]-.06,w:1.4,h:.28,fontFace:BF,fontSize:10.5,color:INKL,margin:0});});
s.addShape(P.shapes.OVAL,{x:cx-1.45,y:cy-1.15,w:.3,h:.3,fill:{color:NAVY}});
s.addText("Northstar",{x:cx-1.08,y:cy-1.12,w:1.4,h:.28,fontFace:BF,fontSize:12,bold:true,color:NAVY,margin:0});
const cm=[["Proactive by default","We prevent slips; others report them after."],
["Five-minute setup","No consultants, no six-week rollout."],
["Loved by ICs","Not another surveillance dashboard."]];
cm.forEach((m,i)=>{const y=1.95+i*1.0;
  s.addText(m[0],{x:6.2,y,w:3.3,h:.35,fontFace:BF,fontSize:14,bold:true,color:NAVY,margin:0});
  s.addText(m[1],{x:6.2,y:y+.32,w:3.3,h:.55,fontFace:BF,fontSize:11.5,color:INKL,margin:0});});

/* 9 — GTM */
s=lightSlide("Go-to-market","Land with teams, expand to companies.");
const gtm=[["Land","Free for squads up to 10. Product-led, zero-touch."],
["Expand","Usage triggers sales-assist at 25+ seats."],
["Embed","Exec digest makes us the company's operating rhythm."]];
gtm.forEach((g,i)=>{const x=.55+i*3.15;
  numDot(s,x,1.95,i+1);
  s.addText(g[0],{x,y:2.55,w:2.85,h:.4,fontFace:HF,fontSize:20,bold:true,color:NAVY,margin:0});
  s.addText(g[1],{x,y:3.05,w:2.75,h:1.2,fontFace:BF,fontSize:13,color:INKL,margin:0});
  if(i<2)s.addText("→",{x:x+2.78,y:1.92,w:.4,h:.5,fontFace:BF,fontSize:22,color:"C9CEDC",margin:0});});
s.addText("CAC payback: 7 months · 41% of signups from word of mouth.",{x:.55,y:4.6,w:9,h:.35,fontFace:BF,fontSize:13,italic:true,color:MUT,margin:0});

/* 10 — Team */
s=lightSlide("Team","Operators who lived this problem.");
const team=[["Alex Rivera","CEO · ex-VP Ops, Plenari","Scaled ops 60→540 people."],
["Dana Okonkwo","CTO · ex-Staff Eng, Vela","Built infra for 30M users."],
["Sam Chen","Head of Product · ex-Atlas","Shipped 0→$40M ARR product."]];
team.forEach((t,i)=>{const x=.55+i*3.15;
  s.addShape(P.shapes.OVAL,{x:x+.85,y:1.8,w:1.15,h:1.15,fill:{color:LITE},line:{color:NAVY,width:1.5}});
  s.addText(t[0].split(" ").map(w=>w[0]).join(""),{x:x+.85,y:1.8,w:1.15,h:1.15,align:"center",valign:"middle",fontFace:HF,fontSize:22,bold:true,color:NAVY,margin:0});
  s.addText(t[0],{x,y:3.1,w:2.85,h:.35,align:"center",fontFace:BF,fontSize:15,bold:true,color:NAVY,margin:0});
  s.addText(t[1],{x,y:3.45,w:2.85,h:.3,align:"center",fontFace:BF,fontSize:11,color:MUT,margin:0});
  s.addText(t[2],{x,y:3.8,w:2.85,h:.5,align:"center",fontFace:BF,fontSize:11.5,color:INKL,margin:0});});
s.addText("Backed by angels from Stripe, Figma and Linear.",{x:.55,y:4.65,w:9,h:.35,align:"center",fontFace:BF,fontSize:12,italic:true,color:MUT,margin:0});

/* 11 — Ask */
s=lightSlide("The ask","$3M seed to own the category.");
s.addText("$3.0M",{x:.55,y:1.9,w:3.6,h:1.1,fontFace:HF,fontSize:56,bold:true,color:NAVY,margin:0});
s.addText("18 months runway · to $1M ARR",{x:.6,y:3.05,w:3.6,h:.35,fontFace:BF,fontSize:13,color:INKL,margin:0});
const use=[["45%","Engineering","Ship the platform roadmap"],["30%","Go-to-market","Two AEs + PLG growth"],["25%","Runway","Buffer to Series A metrics"]];
use.forEach((u,i)=>{const y=1.9+i*1.0;
  s.addShape(P.shapes.RECTANGLE,{x:5.0,y:y+.07,w:2.4*(parseInt(u[0])/45),h:.34,fill:{color:i==0?NAVY:ICE}});
  s.addText(u[0],{x:5.0,y:y+.45,w:.8,h:.3,fontFace:BF,fontSize:13,bold:true,color:NAVY,margin:0});
  s.addText(u[1]+" — "+u[2],{x:5.75,y:y+.45,w:4,h:.3,fontFace:BF,fontSize:11.5,color:INKL,margin:0});});

/* 12 — Close (dark) */
s=darkSlide();
s.addShape(P.shapes.OVAL,{x:-1.4,y:3.4,w:4.2,h:4.2,fill:{color:"253070"}});
s.addText("Let's light the way.",{x:.55,y:1.7,w:8.9,h:1.1,fontFace:HF,fontSize:44,bold:true,color:WHT,margin:0});
s.addText("alex@northstar.app   ·   northstar.app   ·   +1 555 0100",{x:.6,y:3.1,w:8,h:.4,fontFace:BF,fontSize:15,color:ICE,margin:0});
s.addText("NORTHSTAR — replace every number and name with yours. Fonts: Georgia + Calibri (built-in).",{x:.6,y:4.95,w:8.8,h:.3,fontFace:BF,fontSize:9,italic:true,color:"8E97C9",margin:0});

P.writeFile({fileName:"templates/pitch-deck/pitch-deck.pptx"}).then(()=>console.log("deck OK"));
