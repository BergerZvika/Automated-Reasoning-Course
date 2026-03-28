<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ackermanization Engine</title>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>

    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f8fafc;
            overflow: hidden;
            perspective: 1200px;
        }
        
        .mono { font-family: 'JetBrains Mono', monospace; }

        /* --- 3D & Glass Styles --- */
        .glass-panel {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.9);
            box-shadow: 
                0 4px 6px -1px rgba(0, 0, 0, 0.05),
                0 20px 40px -6px rgba(148, 163, 184, 0.3),
                inset 0 1px 0 rgba(255,255,255,0.6);
            transform-style: preserve-3d;
            transition: all 0.5s ease-out;
        }
        
        /* Specific style for the reference box */
        .ref-box {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(99, 102, 241, 0.2);
            box-shadow: 0 10px 20px -5px rgba(0,0,0,0.1);
        }

        #stage-container {
            transform-style: preserve-3d;
            transition: transform 0.1s ease-out;
        }

        /* --- Animations --- */
        .step-content {
            display: none;
            opacity: 0;
            transform: translateY(20px) scale(0.95);
            transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .step-content.active {
            display: flex;
            opacity: 1;
            transform: translateY(0) scale(1);
        }

        .anim-item {
            opacity: 0;
            transform: translateY(20px) rotateX(10deg);
            transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
        }
        
        .active .anim-item {
            opacity: 1;
            transform: translateY(0) rotateX(0deg);
        }

        /* Input Styling */
        .formula-input {
            background: rgba(255, 255, 255, 0.5);
            border: 2px solid #e2e8f0;
            transition: all 0.3s ease;
        }
        .formula-input:focus {
            background: white;
            border-color: #6366f1;
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
            outline: none;
        }

        /* Live Tags Animation */
        .tag-pop {
            animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
            opacity: 0;
            transform: scale(0.8);
        }
        @keyframes popIn {
            to { opacity: 1; transform: scale(1); }
        }
    </style>
</head>
<body class="h-screen w-screen flex flex-col items-center justify-center bg-gradient-to-br from-slate-50 via-slate-100 to-indigo-50">

    <div class="absolute inset-0 overflow-hidden opacity-20 pointer-events-none">
        <div class="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] rounded-full bg-blue-300 blur-[120px]"></div>
        <div class="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] rounded-full bg-purple-300 blur-[120px]"></div>
    </div>

    <div class="absolute top-10 z-50">
        <div class="flex gap-2 p-2 bg-white/50 backdrop-blur-md rounded-full shadow-sm border border-white/50" id="progress-container"></div>
    </div>

    <div id="stage-container" class="relative w-[900px] h-[700px] flex items-center justify-center">

        <div id="step-0" class="step-content absolute inset-0 flex-col items-center justify-center">
            <div class="glass-panel p-10 rounded-3xl max-w-3xl w-full transform-style-3d text-center flex flex-col gap-6">
                <div class="anim-item">
                    <h1 class="text-3xl font-extrabold text-slate-900 tracking-tight">Ackermanization Engine</h1>
                    <p class="text-slate-500 mt-2">Enter a logic formula. We will flatten it.</p>
                </div>
                <div class="anim-item delay-100 relative group">
                    <div class="absolute -inset-1 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-xl opacity-20 group-hover:opacity-40 transition duration-500 blur"></div>
                    <input type="text" id="user-input" 
                        value="g(f(x)) = 10 & f(x) = y"
                        class="relative formula-input w-full text-center text-3xl mono font-bold text-slate-700 py-6 px-6 rounded-xl"
                        placeholder="g(f(x)) = f(f(f(y)))"
                        autocomplete="off">
                </div>
                <div class="anim-item delay-200 border-t border-slate-200 pt-6">
                    <div class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Live Detection</div>
                    <div id="live-preview" class="flex flex-wrap justify-center gap-3 min-h-[60px]"></div>
                </div>
            </div>
        </div>

        <div id="step-1" class="step-content absolute inset-0 flex-col items-center justify-center gap-8">
            <div class="text-center space-y-2 anim-item">
                <h2 class="text-2xl font-bold text-slate-800">Step 1: Identified Functions</h2>
                <p class="text-slate-500">The engine has locked onto these terms.</p>
            </div>
            <div id="step1-display" class="glass-panel p-8 rounded-2xl flex flex-wrap justify-center gap-4 items-center max-w-3xl anim-item delay-100 min-h-[120px]"></div>
            <div id="step1-stats" class="flex gap-4 anim-item delay-300"></div>
        </div>

        <div id="step-2" class="step-content absolute inset-0 flex-col items-center justify-center w-full">
            <div class="text-center space-y-2 mb-6 anim-item">
                <h2 class="text-2xl font-bold text-slate-800">Step 2: Fresh Variables</h2>
                <p class="text-slate-500">Mapping complex terms to simple symbols.</p>
            </div>
            <div id="step2-grid" class="grid grid-cols-2 gap-6 w-full max-w-3xl overflow-y-auto max-h-[400px] p-4"></div>
        </div>

        <div id="step-3" class="step-content absolute inset-0 flex-col items-center justify-center w-full relative">
            
            <div class="absolute left-0 top-10 anim-item delay-500 z-20">
                <div class="ref-box rounded-xl p-4 w-56 flex flex-col gap-2 transform -rotate-2 hover:rotate-0 transition-transform duration-300">
                    <div class="text-[10px] font-bold text-indigo-500 uppercase tracking-wider mb-1 flex items-center gap-1">
                        <i data-lucide="list" class="w-3 h-3"></i> Mapping Reference
                    </div>
                    <div id="step3-ref-list" class="flex flex-col gap-2 max-h-[300px] overflow-y-auto pr-1">
                        </div>
                </div>
            </div>

            <div class="text-center space-y-2 mb-4 anim-item">
                <h2 class="text-2xl font-bold text-slate-800">Step 3: Congruence Axioms</h2>
                <p class="text-slate-500">Enforcing functional consistency.</p>
            </div>
            <div id="step3-list" class="flex flex-col gap-4 w-full max-w-2xl items-center overflow-y-auto max-h-[450px] p-2 z-10"></div>
        </div>

        <div id="step-4" class="step-content absolute inset-0 flex-col items-center justify-center text-center w-full max-w-5xl">
            <div class="mb-4 anim-item">
                <h2 class="text-3xl font-bold text-slate-800 bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">Transformation Complete</h2>
            </div>
            <div class="glass-panel p-8 rounded-3xl shadow-2xl flex flex-col gap-4 items-center border-t-4 border-indigo-500 anim-item delay-100 w-full">
                <div class="w-full text-left anim-item delay-200">
                    <div class="text-xs font-bold text-slate-400 uppercase mb-2 ml-1">Original Input</div>
                    <div class="w-full bg-slate-50/50 rounded-xl p-4 border border-slate-200 text-left overflow-x-auto">
                        <code id="original-formula" class="text-lg mono font-medium text-slate-500 leading-relaxed"></code>
                    </div>
                </div>
                <div class="anim-item delay-300">
                    <i data-lucide="arrow-down" class="text-indigo-300 w-6 h-6"></i>
                </div>
                <div class="w-full text-left anim-item delay-300">
                    <div class="text-xs font-bold text-indigo-500 uppercase mb-2 ml-1">Ackermanized Output</div>
                    <div class="w-full bg-indigo-50/30 rounded-xl p-5 border border-indigo-100 shadow-inner text-left overflow-x-auto">
                        <code id="final-formula" class="text-xl mono font-bold text-slate-800 leading-relaxed"></code>
                    </div>
                </div>
                <div class="grid grid-cols-3 gap-4 w-full text-left anim-item delay-400 mt-2">
                     <div class="p-3 rounded-xl bg-white border border-slate-100 shadow-sm">
                        <div class="text-xs font-bold text-slate-400 uppercase">Logic</div>
                        <div class="text-indigo-600 font-bold">QF_LIA</div>
                     </div>
                     <div class="p-3 rounded-xl bg-white border border-slate-100 shadow-sm">
                        <div class="text-xs font-bold text-slate-400 uppercase">Vars Added</div>
                        <div id="stat-vars" class="text-indigo-600 font-bold">0</div>
                     </div>
                     <div class="p-3 rounded-xl bg-white border border-slate-100 shadow-sm">
                        <div class="text-xs font-bold text-slate-400 uppercase">Axioms</div>
                        <div id="stat-axioms" class="text-indigo-600 font-bold">0</div>
                     </div>
                </div>
            </div>
        </div>
    </div>

    <div class="absolute bottom-10 z-50 flex gap-4">
        <button id="prev-btn" class="flex items-center gap-2 px-6 py-3 bg-white text-slate-600 rounded-full font-semibold shadow-md shadow-slate-200 hover:bg-slate-50 hover:scale-105 active:scale-95 transition-all opacity-0 pointer-events-none">
            <i data-lucide="arrow-left" class="w-4 h-4"></i>
            Back
        </button>
        <button id="next-btn" class="group flex items-center gap-2 px-8 py-3 bg-indigo-600 text-white rounded-full font-semibold shadow-lg shadow-indigo-200 hover:bg-indigo-700 hover:scale-105 active:scale-95 transition-all">
            <span id="btn-text">Start Process</span>
            <i data-lucide="arrow-right" class="w-4 h-4 group-hover:translate-x-1 transition-transform"></i>
        </button>
    </div>

    <script>
        const Engine = {
            rawFormula: "",
            ufs: [],
            axioms: [],
            finalStr: "",

            reset() {
                this.ufs = [];
                this.axioms = [];
                this.finalStr = "";
            },

            parse(input) {
                this.reset();
                this.rawFormula = input;
                const foundSet = new Set();
                let counter = 0;

                for (let i = 0; i < input.length; i++) {
                    if (/[a-zA-Z_]/.test(input[i])) {
                        let j = i;
                        while(j < input.length && /\w/.test(input[j])) j++;
                        
                        if (j < input.length && input[j] === '(') {
                            const funcName = input.substring(i, j);
                            const startParen = j;
                            
                            let depth = 1;
                            let k = startParen + 1;
                            while (k < input.length && depth > 0) {
                                if (input[k] === '(') depth++;
                                if (input[k] === ')') depth--;
                                k++;
                            }
                            
                            if (depth === 0) {
                                const fullText = input.substring(i, k);
                                const argsInner = input.substring(startParen + 1, k - 1);
                                
                                if (!foundSet.has(fullText)) {
                                    foundSet.add(fullText);
                                    const args = this.splitArgs(argsInner);
                                    this.ufs.push({
                                        id: counter++,
                                        text: fullText,
                                        func: funcName,
                                        args: args,
                                        freshVar: `ack_${funcName}_${counter}` 
                                    });
                                }
                            }
                        }
                    }
                }

                const counts = {};
                this.ufs.forEach(u => {
                    if(!counts[u.func]) counts[u.func] = 0;
                    u.freshVar = `ack_${u.func}_${counts[u.func]++}`;
                });
            },

            splitArgs(innerStr) {
                const args = [];
                let depth = 0;
                let start = 0;
                for (let i = 0; i < innerStr.length; i++) {
                    if (innerStr[i] === '(') depth++;
                    if (innerStr[i] === ')') depth--;
                    if (innerStr[i] === ',' && depth === 0) {
                        args.push(innerStr.substring(start, i).trim());
                        start = i + 1;
                    }
                }
                args.push(innerStr.substring(start).trim());
                return args.filter(s => s.length > 0);
            },

            generateAxioms() {
                const groups = {};
                this.ufs.forEach(u => {
                    if (!groups[u.func]) groups[u.func] = [];
                    groups[u.func].push(u);
                });

                for (const func in groups) {
                    const list = groups[func];
                    for (let i = 0; i < list.length; i++) {
                        for (let j = i + 1; j < list.length; j++) {
                            const A = list[i];
                            const B = list[j];
                            const conditions = A.args.map((arg, idx) => `${arg} = ${B.args[idx]}`);
                            const condStr = conditions.join(" ∧ ");
                            
                            this.axioms.push({
                                condition: condStr,
                                consequence: `${A.freshVar} = ${B.freshVar}`,
                            });
                        }
                    }
                }
            },

            rewrite() {
                let temp = this.rawFormula;
                const sortedUfs = [...this.ufs].sort((a,b) => b.text.length - a.text.length);
                
                sortedUfs.forEach(u => {
                    const esc = u.text.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
                    const re = new RegExp(esc, 'g');
                    temp = temp.replace(re, u.freshVar);
                });

                this.axioms.forEach(ax => {
                    let cond = ax.condition;
                    sortedUfs.forEach(u => {
                        const esc = u.text.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
                        const re = new RegExp(esc, 'g');
                        cond = cond.replace(re, u.freshVar);
                    });
                    ax.finalCondition = cond;
                });

                const axiomStrs = this.axioms.map(ax => `(${ax.finalCondition} → ${ax.consequence})`);
                if (axiomStrs.length > 0) {
                    temp = "(" + axiomStrs.join(" ∧ ") + ") -> " + temp;
                }
                this.finalStr = temp;
            }
        };

        let currentStep = 0;
        const totalSteps = 5; 
        const nextBtn = document.getElementById('next-btn');
        const prevBtn = document.getElementById('prev-btn');
        const btnText = document.getElementById('btn-text');
        const inputField = document.getElementById('user-input');
        const livePreview = document.getElementById('live-preview');

        lucide.createIcons();
        renderDots();

        function updateLivePreview() {
            const val = inputField.value;
            Engine.parse(val);
            
            livePreview.innerHTML = '';
            if (Engine.ufs.length === 0) {
                livePreview.innerHTML = '<span class="text-slate-300 italic text-sm">No functions detected... try typing f(x)</span>';
            } else {
                Engine.ufs.forEach((u, i) => {
                    const tag = document.createElement('div');
                    tag.className = 'tag-pop px-3 py-1 bg-indigo-100 text-indigo-700 rounded-lg text-sm font-mono font-bold border border-indigo-200 shadow-sm';
                    tag.style.animationDelay = `${i * 50}ms`;
                    tag.innerText = u.text;
                    livePreview.appendChild(tag);
                });
            }
        }

        inputField.addEventListener('input', updateLivePreview);
        setTimeout(updateLivePreview, 100);

        function resetApp() {
            inputField.value = "";
            updateLivePreview();
        }

        nextBtn.onclick = () => {
            if (currentStep === 0) {
                const input = inputField.value;
                Engine.parse(input);
                Engine.generateAxioms();
                Engine.rewrite();
                populateUI();
            }
            let next = currentStep + 1;
            if (next >= totalSteps) {
                next = 0;
                resetApp();
            }
            setStep(next);
        };

        prevBtn.onclick = () => {
            if (currentStep > 0) setStep(currentStep - 1);
        };

        function populateUI() {
            const s1Container = document.getElementById('step1-display');
            s1Container.innerHTML = '';
            Engine.ufs.forEach((u, i) => {
                const el = document.createElement('div');
                el.className = `px-4 py-2 rounded-lg border-b-4 bg-indigo-600 text-white border-indigo-800 shadow-xl mono font-bold text-lg flex flex-col items-center anim-item`;
                el.style.animationDelay = `${i * 100}ms`;
                el.innerHTML = `<span class="text-[10px] mb-1 text-indigo-200 uppercase tracking-wider">UF</span>${u.text}`;
                s1Container.appendChild(el);
            });
            document.getElementById('step1-stats').innerHTML = `<div class="px-4 py-2 bg-indigo-100 text-indigo-700 rounded-lg text-sm font-semibold shadow-sm">Functions: ${Engine.ufs.length}</div>`;

            const s2Grid = document.getElementById('step2-grid');
            s2Grid.innerHTML = '';
            Engine.ufs.forEach((u, i) => {
                const card = document.createElement('div');
                card.className = "glass-panel p-4 rounded-2xl flex items-center justify-between anim-item hover:translate-z-10";
                card.style.transitionDelay = `${i * 100}ms`;
                card.innerHTML = `
                    <div class="flex flex-col items-center">
                        <span class="text-xs text-slate-400 uppercase tracking-widest mb-1">Original</span>
                        <span class="text-xl mono font-bold text-slate-700">${u.text}</span>
                    </div>
                    <i data-lucide="arrow-right" class="text-indigo-400"></i>
                    <div class="flex flex-col items-center">
                        <span class="text-xs text-indigo-400 uppercase tracking-widest mb-1">Fresh Var</span>
                        <span class="text-xl mono font-bold text-indigo-600 bg-indigo-50 px-3 py-1 rounded-lg">${u.freshVar}</span>
                    </div>
                `;
                s2Grid.appendChild(card);
            });

            // Populate Step 3 Main List
            const s3List = document.getElementById('step3-list');
            s3List.innerHTML = '';
            if(Engine.axioms.length === 0) {
                 s3List.innerHTML = '<div class="text-slate-400 italic mt-10">No repeated functions found.</div>';
            } else {
                Engine.axioms.forEach((ax, i) => {
                    const row = document.createElement('div');
                    row.className = "glass-panel w-full p-6 rounded-xl flex items-center justify-around anim-item";
                    row.style.transitionDelay = `${i * 100}ms`;
                    row.innerHTML = `
                        <div class="flex flex-col items-center">
                            <span class="text-xs text-amber-600 font-bold mb-1">IF INPUTS</span>
                            <span class="mono font-bold text-slate-700">${ax.finalCondition}</span>
                        </div>
                        <div class="h-1 bg-slate-300 w-16 rounded-full relative">
                            <div class="absolute -top-4 left-1/2 -translate-x-1/2 text-[10px] text-slate-400 font-bold">IMPLIES</div>
                        </div>
                        <div class="flex flex-col items-center">
                            <span class="text-xs text-emerald-600 font-bold mb-1">THEN OUTPUTS</span>
                            <span class="mono font-bold text-slate-700">${ax.consequence}</span>
                        </div>
                    `;
                    s3List.appendChild(row);
                });
            }

            // NEW: Populate Step 3 Reference Box
            const refList = document.getElementById('step3-ref-list');
            refList.innerHTML = '';
            Engine.ufs.forEach(u => {
                const item = document.createElement('div');
                item.className = "flex justify-between items-center text-xs p-1 border-b border-slate-100 last:border-0";
                item.innerHTML = `
                    <span class="mono text-slate-600 font-semibold">${u.text}</span>
                    <i data-lucide="arrow-right" class="w-3 h-3 text-slate-300"></i>
                    <span class="mono text-indigo-600 bg-indigo-50 px-1 rounded">${u.freshVar}</span>
                `;
                refList.appendChild(item);
            });

            document.getElementById('original-formula').innerText = Engine.rawFormula;
            document.getElementById('final-formula').innerText = Engine.finalStr;
            document.getElementById('stat-vars').innerText = Engine.ufs.length;
            document.getElementById('stat-axioms').innerText = Engine.axioms.length;
            lucide.createIcons();
        }

        function setStep(step) {
            currentStep = step;
            document.querySelectorAll('.step-content').forEach(el => el.classList.remove('active'));
            setTimeout(() => {
                const target = document.getElementById(`step-${currentStep}`);
                if(target) {
                    target.classList.add('active');
                    lucide.createIcons();
                }
            }, 50);
            renderDots();
            
            if(currentStep === 0) {
                btnText.innerText = "Start Process";
                prevBtn.style.opacity = '0';
                prevBtn.style.pointerEvents = 'none';
            } else if (currentStep === totalSteps - 1) {
                btnText.innerText = "New Formula";
                prevBtn.style.opacity = '1';
                prevBtn.style.pointerEvents = 'auto';
            } else {
                btnText.innerText = "Next Step";
                prevBtn.style.opacity = '1';
                prevBtn.style.pointerEvents = 'auto';
            }
        }

        function renderDots() {
            const container = document.getElementById('progress-container');
            container.innerHTML = '';
            for(let i=0; i<totalSteps; i++) {
                const dot = document.createElement('button');
                const isActive = i === currentStep;
                dot.className = `h-3 rounded-full transition-all duration-300 ${isActive ? 'bg-indigo-600 w-8' : 'bg-slate-300 w-3 hover:bg-slate-400'}`;
                if (i <= currentStep || (currentStep > 0 && i < currentStep)) {
                   dot.onclick = () => setStep(i);
                   dot.style.cursor = 'pointer';
                } else dot.style.cursor = 'default';
                container.appendChild(dot);
            }
        }

        const stage = document.getElementById('stage-container');
        document.addEventListener('mousemove', (e) => {
            const x = (window.innerWidth / 2 - e.pageX) / 50;
            const y = (window.innerHeight / 2 - e.pageY) / 50;
            stage.style.transform = `rotateY(${-x}deg) rotateX(${y}deg)`;
        });

    </script>
</body>
</html>