/* ── File Viewer with Syntax Highlighting ──────────────────────────────────
   Intercepts clicks on .file-row links for .py / .cnf / .smt2 files and
   shows them in a full-screen modal with syntax highlighting.
   Include once per lab:  <script src="../viewer.js"></script>
   ────────────────────────────────────────────────────────────────────────── */
(function () {
'use strict';

// ── STYLES ───────────────────────────────────────────────────────────────────
const CSS = `
#fv-overlay {
  position:fixed;inset:0;z-index:99999;
  background:rgba(7,10,18,.88);backdrop-filter:blur(6px);
  display:flex;align-items:center;justify-content:center;
  animation:fv-in .15s ease;
}
@keyframes fv-in{from{opacity:0}to{opacity:1}}
@keyframes fv-out{from{opacity:1}to{opacity:0}}
#fv-modal {
  background:#0d1117;border:1px solid #2a3148;border-radius:14px;
  width:min(96vw,960px);height:min(92vh,860px);
  display:flex;flex-direction:column;
  box-shadow:0 32px 96px rgba(0,0,0,.8);
  animation:fv-slide .2s cubic-bezier(.16,1,.3,1);overflow:hidden;
}
@keyframes fv-slide{from{transform:translateY(22px) scale(.98);opacity:0}to{transform:none;opacity:1}}
#fv-hdr {
  display:flex;align-items:center;gap:10px;
  padding:10px 16px;background:#111827;
  border-bottom:1px solid #1e2d45;flex-shrink:0;
}
#fv-back {
  display:flex;align-items:center;gap:6px;
  background:rgba(99,102,241,.12);border:1px solid rgba(99,102,241,.28);
  color:#818cf8;border-radius:7px;padding:6px 13px;
  font-size:.78rem;font-weight:700;cursor:pointer;
  transition:background .15s,border-color .15s;white-space:nowrap;
  font-family:inherit;
}
#fv-back:hover{background:rgba(99,102,241,.24);border-color:rgba(99,102,241,.5);}
#fv-fname {
  flex:1;font-family:'SF Mono','Cascadia Code',Consolas,monospace;
  font-size:.82rem;color:#94a3b8;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
}
#fv-badge {
  font-size:.62rem;font-weight:800;padding:3px 9px;
  border-radius:5px;letter-spacing:.07em;flex-shrink:0;
}
#fv-copy {
  background:transparent;border:1px solid #2a3148;color:#4a5568;
  border-radius:7px;padding:6px 13px;font-size:.75rem;cursor:pointer;
  transition:all .15s;font-family:inherit;flex-shrink:0;
}
#fv-copy:hover{background:#1e2535;color:#94a3b8;border-color:#4a5568;}
#fv-copy.ok{color:#22c55e;border-color:#22c55e40;}
#fv-body {
  flex:1;overflow:auto;display:flex;align-items:flex-start;
  font-family:'SF Mono','Cascadia Code',Consolas,'Courier New',monospace;
  font-size:.8rem;line-height:1.65;background:#0d1117;
}
#fv-body::-webkit-scrollbar{width:7px;height:7px;}
#fv-body::-webkit-scrollbar-track{background:#0a0e16;}
#fv-body::-webkit-scrollbar-thumb{background:#2a3148;border-radius:4px;}
#fv-nums {
  padding:18px 0;text-align:right;user-select:none;
  color:#30405a;min-width:54px;flex-shrink:0;
  background:#0d1117;position:sticky;left:0;z-index:1;
  box-shadow:1px 0 0 #1a2233;
}
#fv-nums span{display:block;padding:0 14px 0 8px;}
#fv-code {
  flex:1;margin:0;padding:18px 24px;
  white-space:pre;color:#c9d1d9;background:transparent;
  min-width:0;overflow:visible;
}
.fv-load {
  flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;
  color:#475569;font-size:.88rem;gap:10px;
}
.fv-load a{color:#818cf8;}

/* ── Token colours (VS Code Dark+ palette) ────────────────────────── */
.k {color:#569cd6}          /* keyword */
.fn{color:#dcdcaa}          /* function / command */
.s {color:#ce9178}          /* string */
.cm{color:#6a9955}          /* comment */
.n {color:#b5cea8}          /* number */
.op{color:#d4d4d4}          /* operator / punct */
.dc{color:#c586c0}          /* decorator */
.sp{color:#9cdcfe}          /* identifier / special */
.ty{color:#4ec9b0}          /* type */
.hd{color:#4fc1ff}          /* header (CNF p line) */
.ng{color:#f97583}          /* negative literal */

/* ── Lab Files button (injected into .hdr) ────────────────────────── */
#fv-lf-btn {
  display:inline-flex;align-items:center;gap:7px;
  padding:9px 18px;
  background:linear-gradient(160deg,#1a2535 0%,#111827 100%);
  border:1px solid rgba(99,102,241,.25);border-bottom-color:rgba(0,0,0,.4);
  border-radius:12px;color:#818cf8;font-size:.78rem;font-weight:700;
  letter-spacing:.06em;text-transform:uppercase;cursor:pointer;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.06),0 4px 0 #070b14,0 5px 12px rgba(0,0,0,.5);
  transform:translateY(0);transition:all .13s cubic-bezier(.2,.8,.4,1);
  position:relative;overflow:hidden;font-family:inherit;flex-shrink:0;
}
#fv-lf-btn::after{content:'';position:absolute;top:0;left:-60%;width:40%;height:100%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.06),transparent);
  transform:skewX(-20deg);transition:left .4s ease}
#fv-lf-btn:hover::after{left:120%}
#fv-lf-btn:hover{color:#a5b4fc;border-color:rgba(99,102,241,.5);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.1),0 6px 0 #070b14,0 8px 20px rgba(0,0,0,.6),0 0 24px rgba(99,102,241,.15);
  transform:translateY(-3px)}
#fv-lf-btn:active{transform:translateY(3px);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.04),0 1px 0 #070b14,0 2px 6px rgba(0,0,0,.4)}

/* ── Lab Files explorer (split panel) ────────────────────────────── */
#fv-lf-overlay {
  position:fixed;inset:0;z-index:99998;
  background:rgba(7,10,18,.82);backdrop-filter:blur(5px);
  display:flex;align-items:center;justify-content:center;
  animation:fv-in .15s ease;
}
#fv-lf-modal {
  background:#0d1117;border:1px solid #2a3148;border-radius:14px;
  width:min(96vw,1100px);height:min(92vh,860px);
  display:flex;flex-direction:column;
  box-shadow:0 32px 96px rgba(0,0,0,.85);
  animation:fv-slide .2s cubic-bezier(.16,1,.3,1);overflow:hidden;
}
#fv-lf-hdr {
  display:flex;align-items:center;gap:10px;
  padding:11px 16px;background:#111827;
  border-bottom:1px solid #1e2d45;flex-shrink:0;
}
#fv-lf-title {
  font-size:.82rem;font-weight:700;color:#e2e8f0;
  display:flex;align-items:center;gap:7px;flex-shrink:0;
}
#fv-lf-title svg{flex-shrink:0;opacity:.6}
#fv-lf-active {
  flex:1;display:flex;align-items:center;gap:8px;
  font-family:'SF Mono','Cascadia Code',Consolas,monospace;
  font-size:.8rem;color:#64748b;padding-left:4px;
  overflow:hidden;white-space:nowrap;text-overflow:ellipsis;
}
#fv-lf-active-badge{font-size:.6rem;font-weight:800;padding:2px 7px;border-radius:4px;letter-spacing:.06em;flex-shrink:0}
#fv-lf-copy {
  background:transparent;border:1px solid #2a3148;color:#4a5568;
  border-radius:7px;padding:5px 12px;font-size:.72rem;cursor:pointer;
  transition:all .15s;font-family:inherit;flex-shrink:0;
}
#fv-lf-copy:hover{background:#1e2535;color:#94a3b8;border-color:#4a5568;}
#fv-lf-copy.ok{color:#22c55e;border-color:#22c55e40;}
#fv-lf-close {
  background:transparent;border:1px solid #2a3148;color:#4a5568;
  border-radius:6px;width:28px;height:28px;cursor:pointer;
  font-size:.85rem;transition:all .15s;font-family:inherit;
  display:flex;align-items:center;justify-content:center;flex-shrink:0;
}
#fv-lf-close:hover{background:#1e2535;color:#94a3b8;border-color:#4a5568;}
/* split body */
#fv-lf-split {
  flex:1;display:flex;overflow:hidden;
}
/* left sidebar */
#fv-lf-sidebar {
  width:230px;min-width:180px;flex-shrink:0;
  overflow-y:auto;border-right:1px solid #1a2233;
  background:#0a0e16;padding:12px 8px;display:flex;flex-direction:column;gap:10px;
}
#fv-lf-sidebar::-webkit-scrollbar{width:4px;}
#fv-lf-sidebar::-webkit-scrollbar-track{background:transparent;}
#fv-lf-sidebar::-webkit-scrollbar-thumb{background:#2a3148;border-radius:3px;}
.fv-lf-group-title {
  font-size:.62rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;
  color:#2d3d52;margin-bottom:4px;padding:0 6px;
}
.fv-lf-file {
  display:flex;align-items:center;gap:8px;
  padding:7px 8px;border-radius:7px;cursor:pointer;
  border:1px solid transparent;transition:background .1s,border-color .1s;
}
.fv-lf-file:hover{background:#111c2e;border-color:#1e2d45;}
.fv-lf-file.active{background:#131c2e;border-color:rgba(99,102,241,.35);}
.fv-lf-file.active .fv-lf-name{color:#c5d0e0;}
.fv-lf-name {
  flex:1;font-family:'SF Mono','Cascadia Code',Consolas,monospace;
  font-size:.72rem;color:#64748b;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;min-width:0;
}
.fv-lf-file:hover .fv-lf-name{color:#94a3b8;}
.fv-lf-badge {
  font-size:.57rem;font-weight:800;padding:2px 6px;border-radius:4px;
  letter-spacing:.05em;flex-shrink:0;
}
.fv-lf-badge.py {background:rgba(34,197,94,.1);color:#4ade80;border:1px solid rgba(34,197,94,.2)}
.fv-lf-badge.cnf{background:rgba(168,85,247,.1);color:#c084fc;border:1px solid rgba(168,85,247,.2)}
.fv-lf-badge.smt2{background:rgba(59,130,246,.1);color:#60a5fa;border:1px solid rgba(59,130,246,.2)}
/* right content pane */
#fv-lf-pane {
  flex:1;overflow:auto;display:flex;align-items:flex-start;
  font-family:'SF Mono','Cascadia Code',Consolas,'Courier New',monospace;
  font-size:.8rem;line-height:1.65;background:#0d1117;
}
#fv-lf-pane::-webkit-scrollbar{width:7px;height:7px;}
#fv-lf-pane::-webkit-scrollbar-track{background:#0a0e16;}
#fv-lf-pane::-webkit-scrollbar-thumb{background:#2a3148;border-radius:4px;}
#fv-lf-nums {
  padding:18px 0;text-align:right;user-select:none;color:#30405a;
  min-width:54px;flex-shrink:0;background:#0d1117;
  position:sticky;left:0;z-index:1;box-shadow:1px 0 0 #1a2233;
}
#fv-lf-nums span{display:block;padding:0 14px 0 8px;}
#fv-lf-code {
  flex:1;margin:0;padding:18px 24px;white-space:pre;
  color:#c9d1d9;background:transparent;min-width:0;overflow:visible;
}
#fv-lf-empty {
  flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;
  color:#2d3d52;font-size:.85rem;gap:10px;font-family:inherit;
}
#fv-lf-empty svg{opacity:.3}

/* Hide the original bottom files section */
.files-section{display:none!important}
`;

// ── HELPERS ──────────────────────────────────────────────────────────────────
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function t(cls,s){return `<span class="${cls}">${s}</span>`;}

// ── PYTHON HIGHLIGHTER ───────────────────────────────────────────────────────
const PY_KW = new Set(['False','None','True','and','as','assert','async','await',
  'break','class','continue','def','del','elif','else','except','finally','for',
  'from','global','if','import','in','is','lambda','nonlocal','not','or','pass',
  'raise','return','try','while','with','yield']);
const PY_BI = new Set(['abs','all','any','bool','bytes','callable','chr','dict',
  'dir','divmod','enumerate','eval','exec','filter','float','format','frozenset',
  'getattr','globals','hasattr','hash','help','hex','id','input','int','isinstance',
  'issubclass','iter','len','list','locals','map','max','min','next','object','open',
  'ord','pow','print','property','range','repr','reversed','round','set','setattr',
  'slice','sorted','staticmethod','str','sum','super','tuple','type','vars','zip']);

function hlPython(src){
  const lines=src.split('\n');
  let inTriple=false,tripleQ='';
  const out=[];
  for(let li=0;li<lines.length;li++){
    let line=lines[li],res='',i=0;
    if(inTriple){
      const end=line.indexOf(tripleQ);
      if(end===-1){out.push(t('s',esc(line)));continue;}
      res+=t('s',esc(line.slice(0,end+3)));
      i=end+3;inTriple=false;
    }
    while(i<line.length){
      const c=line[i];
      if(c==='#'){res+=t('cm',esc(line.slice(i)));i=line.length;continue;}
      // triple-quoted string
      if((c==='"'||c==="'")&&line[i+1]===c&&line[i+2]===c){
        const q=c+c+c,end=line.indexOf(q,i+3);
        if(end===-1){res+=t('s',esc(line.slice(i)));inTriple=true;tripleQ=q;i=line.length;}
        else{res+=t('s',esc(line.slice(i,end+3)));i=end+3;}
        continue;
      }
      // single-quoted string
      if(c==='"'||c==="'"){
        let j=i+1;
        while(j<line.length&&line[j]!==c){if(line[j]==='\\')j++;j++;}
        res+=t('s',esc(line.slice(i,j+1)));i=j+1;continue;
      }
      // decorator
      if(c==='@'){
        let j=i+1;while(j<line.length&&/[\w.]/.test(line[j]))j++;
        res+=t('dc',esc(line.slice(i,j)));i=j;continue;
      }
      // number
      if(/[0-9]/.test(c)&&(i===0||/\W/.test(line[i-1]))){
        let j=i;while(j<line.length&&/[0-9._xXbBoOeEfFlLjJ]/.test(line[j]))j++;
        res+=t('n',esc(line.slice(i,j)));i=j;continue;
      }
      // identifier
      if(/[a-zA-Z_]/.test(c)){
        let j=i;while(j<line.length&&/\w/.test(line[j]))j++;
        const w=line.slice(i,j);
        if(PY_KW.has(w))res+=t('k',esc(w));
        else if(PY_BI.has(w)||line[j]==='(')res+=t('fn',esc(w));
        else res+=esc(w);
        i=j;continue;
      }
      if(/[+\-*\/=<>!&|^~%:,;.[\]{}()]/.test(c)){res+=t('op',esc(c));i++;continue;}
      res+=esc(c);i++;
    }
    out.push(res);
  }
  return out.join('\n');
}

// ── DIMACS CNF HIGHLIGHTER ───────────────────────────────────────────────────
function hlCNF(src){
  return src.split('\n').map(line=>{
    const tr=line.trim();
    if(!tr)return '';
    if(tr[0]==='c')return t('cm',esc(line));
    if(tr.startsWith('p ')){
      return line.replace(/^(\s*)(p)(\s+)(cnf|sat)(\s+)(\d+)(\s+)(\d+)(.*)/,
        (_,ws,p,s1,kw,s2,v,s3,cl,rest)=>
          esc(ws)+t('hd',esc(p))+esc(s1)+t('k',esc(kw))+esc(s2)+
          t('n',esc(v))+esc(s3)+t('n',esc(cl))+esc(rest));
    }
    return line.replace(/(-?\d+)/g,m=>{
      const n=parseInt(m);
      if(n===0)return t('op','0');
      if(n<0)return t('ng',esc(m));
      return t('n',esc(m));
    });
  }).join('\n');
}

// ── SMT-LIB2 HIGHLIGHTER ────────────────────────────────────────────────────
const SMT_CMD=new Set(['set-logic','set-option','set-info','declare-sort','declare-fun',
  'declare-const','define-sort','define-fun','define-fun-rec','assert','check-sat',
  'check-sat-assuming','get-model','get-value','get-assignment','push','pop','exit',
  'echo','reset','reset-assertions','get-info','get-option','get-proof','get-unsat-core']);
const SMT_OP=new Set(['=','not','and','or','xor','=>','iff','<','<=','>','>=','+','-','*',
  '/','mod','div','abs','to_int','to_real','is_int','ite','let','forall','exists',
  'concat','extract','bvadd','bvsub','bvmul','bvudiv','bvsdiv','bvurem','bvsrem',
  'bvshl','bvlshr','bvashr','bvand','bvor','bvxor','bvnot','bvneg',
  'bvule','bvult','bvuge','bvugt','bvsle','bvslt','bvsge','bvsgt',
  'zero_extend','sign_extend','rotate_left','rotate_right','repeat','store','select',
  'distinct','true','false','str.len','str.++','str.substr','str.contains']);
const SMT_TY=new Set(['Int','Bool','Real','String','Array','BitVec','Float','RoundingMode',
  'RegLan']);
const SMT_LG=new Set(['QF_UF','QF_LIA','QF_LRA','QF_NIA','QF_NRA','QF_BV','QF_ABV',
  'QF_AUFLIA','QF_ALIA','QF_UFLRA','QF_UFLIA','LIA','LRA','NIA','NRA','BV','UF',
  'AUFLIA','AUFNIRA','ALL']);
const PC=['#ffd700','#da70d6','#87ceeb','#98fb98','#ff9e64'];

function hlSMT2(src){
  let depth=0;
  return src.split('\n').map(line=>{
    let res='',i=0;
    while(i<line.length){
      const c=line[i];
      if(c===';'){res+=t('cm',esc(line.slice(i)));i=line.length;continue;}
      if(c==='"'){
        let j=i+1;while(j<line.length&&line[j]!=='"'){if(line[j]==='\\')j++;j++;}
        res+=t('s',esc(line.slice(i,j+1)));i=j+1;continue;
      }
      if(c==='|'){
        let j=line.indexOf('|',i+1);if(j===-1)j=line.length-1;
        res+=t('sp',esc(line.slice(i,j+1)));i=j+1;continue;
      }
      if(c==='('){
        const col=PC[depth%PC.length];
        res+=`<span style="color:${col}">(</span>`;depth++;i++;continue;
      }
      if(c===')'){
        depth=Math.max(0,depth-1);
        const col=PC[depth%PC.length];
        res+=`<span style="color:${col}">)</span>`;i++;continue;
      }
      // number
      if(/[0-9]/.test(c)||(c==='-'&&i+1<line.length&&/[0-9]/.test(line[i+1])&&(i===0||/[\s(]/.test(line[i-1])))){
        let j=i+(c==='-'?1:0);while(j<line.length&&/[0-9._bBoOxX]/.test(line[j]))j++;
        res+=t('n',esc(line.slice(i,j)));i=j;continue;
      }
      // #bN... #xN... bit-vector literals
      if(c==='#'&&/[bxBX]/.test(line[i+1])){
        let j=i+2;while(j<line.length&&/[0-9a-fA-F]/.test(line[j]))j++;
        res+=t('n',esc(line.slice(i,j)));i=j;continue;
      }
      // identifier / keyword
      if(/[a-zA-Z_\-!<>=+*%^~?@.]/.test(c)){
        let j=i;
        while(j<line.length&&/[a-zA-Z0-9_\-!<>=+*%^~?@.]/.test(line[j])&&line[j]!=='('&&line[j]!==')')j++;
        const w=line.slice(i,j);
        if(SMT_CMD.has(w))res+=t('fn',esc(w));
        else if(SMT_OP.has(w))res+=t('k',esc(w));
        else if(SMT_TY.has(w))res+=t('ty',esc(w));
        else if(SMT_LG.has(w))res+=t('hd',esc(w));
        else res+=t('sp',esc(w));
        i=j;continue;
      }
      res+=esc(c);i++;
    }
    return res;
  }).join('\n');
}

// ── DETECT LANGUAGE ──────────────────────────────────────────────────────────
function detectLang(url){
  const ext=url.split('.').pop().toLowerCase().split('?')[0];
  if(ext==='py')return 'python';
  if(ext==='cnf')return 'cnf';
  if(ext==='smt2'||ext==='smt')return 'smt2';
  return 'text';
}
function highlight(src,lang){
  if(lang==='python')return hlPython(src);
  if(lang==='cnf')return hlCNF(src);
  if(lang==='smt2')return hlSMT2(src);
  return esc(src);
}
const BADGE={
  python:{label:'Python', bg:'rgba(34,197,94,.12)', color:'#4ade80', border:'rgba(34,197,94,.3)'},
  cnf:   {label:'DIMACS CNF', bg:'rgba(168,85,247,.12)', color:'#c084fc', border:'rgba(168,85,247,.3)'},
  smt2:  {label:'SMT-LIB 2', bg:'rgba(59,130,246,.12)', color:'#60a5fa', border:'rgba(59,130,246,.3)'},
  text:  {label:'Text', bg:'rgba(100,116,139,.12)', color:'#94a3b8', border:'rgba(100,116,139,.3)'},
};

// ── FILE LOADING ─────────────────────────────────────────────────────────────
// Strategy: 1) window.LAB_FILES (pre-embedded, always works)
//           2) fetch (works over HTTP)
//           3) XMLHttpRequest (file:// status===0 on success)
function loadFile(url){
  // 1. Pre-embedded data (most reliable — no network needed)
  if(window.LAB_FILES){
    const key=resolveKey(url);
    if(key!==null&&window.LAB_FILES[key]!==undefined)
      return Promise.resolve(window.LAB_FILES[key]);
  }
  // 2. fetch (HTTP server)
  return fetch(url)
    .then(r=>{if(!r.ok)throw new Error('HTTP '+r.status);return r.text();})
    // 3. XHR fallback
    .catch(()=>new Promise((resolve,reject)=>{
      const xhr=new XMLHttpRequest();
      xhr.open('GET',url,true);
      xhr.responseType='text';
      xhr.onload=()=>{
        if(xhr.status===200||xhr.status===0)resolve(xhr.responseText);
        else reject(new Error('XHR '+xhr.status));
      };
      xhr.onerror=()=>reject(new Error('Could not read file'));
      xhr.send();
    }));
}

// Convert absolute URL back to relative key used in LAB_FILES
function resolveKey(url){
  try{
    // url is like file:///path/to/lab/subdir/file.py
    // We want "subdir/file.py" (relative to the lab's index.html)
    const docBase=window.location.href.replace(/\/[^/]*$/,'/');
    if(url.startsWith(docBase))return decodeURIComponent(url.slice(docBase.length));
    // Also try just the filename
    return decodeURIComponent(url.split('/').pop().split('?')[0]);
  }catch(e){return null;}
}

// ── OPEN VIEWER ──────────────────────────────────────────────────────────────
function openViewer(url){
  injectCSS();
  const lang=detectLang(url);
  const b=BADGE[lang]||BADGE.text;
  const fname=decodeURIComponent(url.split('/').pop().split('?')[0]);

  const overlay=document.createElement('div');
  overlay.id='fv-overlay';
  overlay.innerHTML=`
<div id="fv-modal">
  <div id="fv-hdr">
    <button id="fv-back">&#8592; Back to Tutorial</button>
    <span id="fv-fname">${esc(fname)}</span>
    <span id="fv-badge" style="background:${b.bg};color:${b.color};border:1px solid ${b.border}">${b.label}</span>
    <button id="fv-copy">Copy</button>
  </div>
  <div id="fv-body"><div class="fv-load"><span>Loading&hellip;</span></div></div>
</div>`;

  document.body.appendChild(overlay);
  let rawSrc='';

  function close(){
    overlay.style.animation='fv-out .12s ease forwards';
    setTimeout(()=>overlay.remove(),130);
  }
  overlay.querySelector('#fv-back').onclick=close;
  overlay.addEventListener('click',e=>{if(e.target===overlay)close();});
  function onKey(e){if(e.key==='Escape'){close();document.removeEventListener('keydown',onKey);}}
  document.addEventListener('keydown',onKey);

  loadFile(url)
    .then(src=>{
      rawSrc=src;
      const lineArr=src.split('\n');
      const nums=lineArr.map((_,i)=>`<span>${i+1}</span>`).join('');
      const code=highlight(src,lang);
      const body=overlay.querySelector('#fv-body');
      body.innerHTML=`<div id="fv-nums">${nums}</div><pre id="fv-code">${code}</pre>`;
    })
    .catch(err=>{
      overlay.querySelector('#fv-body').innerHTML=`<div class="fv-load">
        <span style="color:#ef4444">Could not load file: ${esc(err.message)}</span></div>`;
    });

  overlay.querySelector('#fv-copy').onclick=function(){
    if(!rawSrc)return;
    navigator.clipboard.writeText(rawSrc).then(()=>{
      this.textContent='Copied!';this.classList.add('ok');
      setTimeout(()=>{this.textContent='Copy';this.classList.remove('ok');},2000);
    }).catch(()=>{
      // Fallback for HTTP
      const ta=document.createElement('textarea');
      ta.value=rawSrc;ta.style.position='fixed';ta.style.opacity='0';
      document.body.appendChild(ta);ta.select();document.execCommand('copy');
      ta.remove();
      this.textContent='Copied!';this.classList.add('ok');
      setTimeout(()=>{this.textContent='Copy';this.classList.remove('ok');},2000);
    });
  };

  return false;
}

function injectCSS(){
  if(document.getElementById('fv-style'))return;
  const el=document.createElement('style');
  el.id='fv-style';el.textContent=CSS;
  document.head.appendChild(el);
}

// ── LAB FILES EXPLORER (split panel) ─────────────────────────────────────────
function openLabFiles(){
  injectCSS();
  const panels=document.querySelectorAll('.files-panel');
  if(!panels.length)return;

  // Build sidebar file list
  let sidebar='';
  const fileItems=[];
  panels.forEach(panel=>{
    const hdrEl=panel.querySelector('.files-panel-hdr');
    const clone=hdrEl.cloneNode(true);
    clone.querySelectorAll('.chevron').forEach(el=>el.remove());
    const groupLabel=clone.textContent.trim();
    const rows=panel.querySelectorAll('.file-row');
    if(!rows.length)return;
    sidebar+=`<div class="fv-lf-group"><div class="fv-lf-group-title">${esc(groupLabel)}</div>`;
    rows.forEach(row=>{
      const href=row.getAttribute('href')||'';
      const nameEl=row.querySelector('.file-name');
      const name=nameEl?nameEl.textContent.trim():href.split('/').pop();
      const ext=href.split('.').pop().toLowerCase().split('?')[0];
      const badgeCls=ext==='py'?'py':ext==='cnf'?'cnf':'smt2';
      const badgeTxt=ext==='py'?'PY':ext==='cnf'?'CNF':'SMT2';
      const absUrl=new URL(href,document.baseURI).href;
      const idx=fileItems.length;
      fileItems.push({absUrl,name,ext,badgeCls,badgeTxt});
      sidebar+=`<div class="fv-lf-file" data-idx="${idx}">
        <span class="fv-lf-name">${esc(name)}</span>
        <span class="fv-lf-badge ${badgeCls}">${badgeTxt}</span>
      </div>`;
    });
    sidebar+='</div>';
  });

  const overlay=document.createElement('div');
  overlay.id='fv-lf-overlay';
  overlay.innerHTML=`
<div id="fv-lf-modal">
  <div id="fv-lf-hdr">
    <span id="fv-lf-title">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/>
      </svg>Lab Files
    </span>
    <span id="fv-lf-active"><span id="fv-lf-active-name">select a file&hellip;</span></span>
    <button id="fv-lf-copy" style="display:none">Copy</button>
    <button id="fv-lf-close">&#10005;</button>
  </div>
  <div id="fv-lf-split">
    <div id="fv-lf-sidebar">${sidebar}</div>
    <div id="fv-lf-pane">
      <div id="fv-lf-empty">
        <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/>
          <line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>
        </svg>
        <span>Select a file to view</span>
      </div>
    </div>
  </div>
</div>`;

  document.body.appendChild(overlay);
  let rawSrc='', activeIdx=-1;

  function close(){
    overlay.style.animation='fv-out .12s ease forwards';
    setTimeout(()=>overlay.remove(),130);
  }
  overlay.querySelector('#fv-lf-close').onclick=close;
  overlay.addEventListener('click',e=>{if(e.target===overlay)close();});
  function onKey(e){if(e.key==='Escape'){close();document.removeEventListener('keydown',onKey);}}
  document.addEventListener('keydown',onKey);

  const pane=overlay.querySelector('#fv-lf-pane');
  const activeName=overlay.querySelector('#fv-lf-active-name');
  const copyBtn=overlay.querySelector('#fv-lf-copy');

  function loadInPane(idx){
    const f=fileItems[idx];
    if(!f)return;
    rawSrc='';
    activeIdx=idx;

    // Mark active in sidebar
    overlay.querySelectorAll('.fv-lf-file').forEach(el=>el.classList.remove('active'));
    overlay.querySelector(`.fv-lf-file[data-idx="${idx}"]`).classList.add('active');

    // Update header
    activeName.textContent=f.name;
    const b=BADGE[f.ext==='smt'?'smt2':f.ext]||BADGE.text;
    activeName.style.color='#94a3b8';
    let badgeEl=overlay.querySelector('#fv-lf-active-badge');
    if(!badgeEl){
      badgeEl=document.createElement('span');
      badgeEl.id='fv-lf-active-badge';
      overlay.querySelector('#fv-lf-active').prepend(badgeEl);
    }
    badgeEl.textContent=f.badgeTxt;
    badgeEl.style.cssText=`font-size:.6rem;font-weight:800;padding:2px 7px;border-radius:4px;letter-spacing:.06em;flex-shrink:0;background:${b.bg};color:${b.color};border:1px solid ${b.border}`;

    // Show loading
    pane.innerHTML='<div class="fv-load"><span>Loading&hellip;</span></div>';
    copyBtn.style.display='';

    loadFile(f.absUrl)
      .then(src=>{
        rawSrc=src;
        const lang=detectLang(f.absUrl);
        const nums=src.split('\n').map((_,i)=>`<span>${i+1}</span>`).join('');
        const code=highlight(src,lang);
        pane.innerHTML=`<div id="fv-lf-nums">${nums}</div><pre id="fv-lf-code">${code}</pre>`;
      })
      .catch(err=>{
        pane.innerHTML=`<div class="fv-load"><span style="color:#ef4444">Could not load: ${esc(err.message)}</span></div>`;
      });
  }

  // Sidebar clicks
  overlay.querySelectorAll('.fv-lf-file').forEach(el=>{
    el.addEventListener('click',()=>loadInPane(+el.dataset.idx));
  });

  // Copy button
  copyBtn.onclick=function(){
    if(!rawSrc)return;
    navigator.clipboard.writeText(rawSrc).then(()=>{
      this.textContent='Copied!';this.classList.add('ok');
      setTimeout(()=>{this.textContent='Copy';this.classList.remove('ok');},2000);
    }).catch(()=>{
      const ta=document.createElement('textarea');
      ta.value=rawSrc;ta.style.cssText='position:fixed;opacity:0';
      document.body.appendChild(ta);ta.select();document.execCommand('copy');ta.remove();
      this.textContent='Copied!';this.classList.add('ok');
      setTimeout(()=>{this.textContent='Copy';this.classList.remove('ok');},2000);
    });
  };

  // Auto-open first file
  if(fileItems.length)loadInPane(0);
}

// ── INJECT HEADER BUTTON + HIDE BOTTOM SECTION ───────────────────────────────
document.addEventListener('DOMContentLoaded',()=>{
  injectCSS();

  // Inject "Lab Files" button into .hdr if there are file panels
  const hdr=document.querySelector('.hdr');
  const hasPanels=document.querySelector('.files-panel');
  if(hdr&&hasPanels){
    const btn=document.createElement('button');
    btn.id='fv-lf-btn';
    btn.innerHTML=`<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/></svg>Lab Files`;
    btn.onclick=openLabFiles;
    // Group Home + Lab Files together on the left
    const backBtn=hdr.querySelector('.back-btn');
    if(backBtn){
      const group=document.createElement('div');
      group.style.cssText='display:flex;align-items:center;gap:8px;flex-shrink:0';
      backBtn.parentNode.insertBefore(group,backBtn);
      group.appendChild(backBtn);
      group.appendChild(btn);
    }else{
      hdr.prepend(btn);
    }
  }

  // Intercept .file-row link clicks (still needed for any remaining links)
  document.addEventListener('click',e=>{
    const a=e.target.closest('.file-row');
    if(!a||!a.href)return;
    const ext=a.href.split('.').pop().toLowerCase().split('?')[0];
    if(['py','cnf','smt2','smt'].includes(ext)){
      e.preventDefault();
      openViewer(a.href);
    }
  });
});

window.openViewer=openViewer;
})();
