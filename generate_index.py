<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ICT 實作：避障小車任務控制中心</title>
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @keyframes scan {
            0% { transform: translateY(-100%); }
            100% { transform: translateY(100%); }
        }
        .scan-line {
            height: 2px;
            background: linear-gradient(to right, transparent, #38bdf8, transparent);
            animation: scan 3s linear infinite;
        } 
        .neon-border {
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.2);
        }
        .neon-text {
            text-shadow: 0 0 8px rgba(56, 189, 248, 0.5);
        }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }
    </style>
</head>
<body class="bg-[#0f172a] text-slate-200 overflow-x-hidden">
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useRef } = React;

        function App() {
            const [p1, setP1] = useState(600);
            const [p2, setP2] = useState(600);
            const [logs, setLogs] = useState(["系統初始化完畢...", "等待感測器信號..."]);
            const logEndRef = useRef(null);

            const [carState, setCarState] = useState({
                p12: 0, p16: 0, p8: 0, p0: 0,
                statusTitle: 'STANDBY', statusText: '系統待命', actionType: 'stop'
            });

            const addLog = (msg) => {
                setLogs(prev => [...prev.slice(-4), msg]);
            };
            useEffect(() => {
                let newState = {};
                if (p1 > 500 && p2 > 500) {
                    newState = {
                        p12: 0, p16: 0, p8: 500, p0: 500,
                        statusTitle: 'FORWARD', statusText: '全速前進', actionType: 'forward'
                    };
                } else if (p1 > 500 && p2 <= 500) {
                    newState = {
                        p12: 1, p16: 1, p8: 100, p0: 300,
                        statusTitle: 'EVADE RIGHT', statusText: '右側障礙物：向後右轉避讓', actionType: 'back_right'
                    };
                } else if (p1 <= 500 && p2 > 500) {
                    newState = {
                        p12: 1, p16: 1, p8: 300, p0: 100,
                        statusTitle: 'EVADE LEFT', statusText: '左側障礙物：向後左轉避讓', actionType: 'back_left'
                    };
                } else {
                    newState = {
                        p12: 0, p16: 0, p8: 0, p0: 0,
                        statusTitle: 'HALT', statusText: '警告：雙側障礙，緊急停止', actionType: 'stop'
                    };
                }
                
                if (newState.statusTitle !== carState.statusTitle) {
                    addLog(`狀態變更: ${newState.statusTitle}`);
                }
                setCarState(newState);
            }, [p1, p2]);

            useEffect(() => {
                logEndRef.current?.scrollIntoView({ behavior: "smooth" });
            }, [logs]);

            const renderWheelArrow = (speed, dir, startX, startY) => {
                if (speed === 0) return null;
                const length = (speed / 500) * 70;
                const endY = dir === 0 ? startY - length : startY + length;
                const color = dir === 0 ? '#10b981' : '#f43f5e';
                return (
                    <g className="transition-all duration-500">
                        <line x1={startX} y1={startY} x2={startX} y2={endY} stroke={color} strokeWidth="6" strokeLinecap="round" opacity="0.8" />
                        <circle cx={startX} cy={endY} r="3" fill={color} />
                        <text x={startX + (startX > 200 ? 15 : -15)} y={startY + (endY - startY)/2} fill={color} fontSize="14" fontWeight="bold" textAnchor={startX > 200 ? "start" : "end"} className="font-mono">{speed}</text>
                    </g>
                );
            };
            return (
                <div className="min-h-screen flex flex-col p-4 md:p-8">
                    {/* Header */}
                    <header className="flex flex-col md:flex-row justify-between items-center mb-8 border-b border-slate-800 pb-6 gap-4">
                        <div className="flex items-center gap-4">
                            <div className="w-12 h-12 bg-sky-500/10 rounded-lg flex items-center justify-center border border-sky-500/30">
                                <i className="fas fa-satellite-dish text-sky-400 text-xl animate-pulse"></i>
                            </div>
                            <div>
                                <h1 className="text-2xl font-black tracking-tighter neon-text uppercase italic">
                                    Robo-Car Control Unit <span className="text-sky-500">v2.0</span>
                                </h1>
                                <p className="text-[10px] text-slate-500 uppercase tracking-[0.2em] font-bold">Mission Control / Real-time Telemetry</p>
                            </div>
                        </div>
                        <div className="flex gap-2">
                            <div className="px-4 py-2 bg-slate-800/50 rounded border border-slate-700 text-[10px] font-bold">
                                SYSTEM STATUS: <span className="text-emerald-400 ml-2">ONLINE</span>
                            </div>
                            <div className="px-4 py-2 bg-slate-800/50 rounded border border-slate-700 text-[10px] font-bold">
                                DATA RATE: <span className="text-sky-400 ml-2">240 Hz</span>
                            </div>
                        </div>
                    </header>

                    <main className="grid grid-cols-1 lg:grid-cols-12 gap-6 flex-1">
                        {/* Left Control Panel */}
                        <div className="lg:col-span-4 space-y-6">
                            {/* Sensors */}
                            <div className="bg-slate-900/50 rounded-2xl border border-slate-800 p-6 relative overflow-hidden">
                                <div className="scan-line absolute inset-0 opacity-10 pointer-events-none"></div>
                                <h2 className="text-xs font-black text-sky-400 uppercase tracking-widest mb-6 flex items-center gap-2">
                                    <i className="fas fa-radar"></i> 感測器輸入 (Distance Sensors)
                                </h2>
                                <div className="space-y-10">
                                    {[ {id: 'P1', val: p1, set: setP1, label: 'LEFT SENSOR'}, 
                                       {id: 'P2', val: p2, set: setP2, label: 'RIGHT SENSOR'} ].map(s => (
                                        <div key={s.id} className="group">
                                            <div className="flex justify-between items-end mb-3">
                                                <span className="text-[10px] font-black text-slate-500 uppercase tracking-tighter">{s.label}</span>
                                                <span className={`text-2xl font-black font-mono ${s.val <= 500 ? 'text-rose-500' : 'text-emerald-400'}`}>
                                                    {s.val}<span className="text-[10px] ml-1 opacity-50">mv</span>
                                                </span>
                                            </div>
                                            <input type="range" min="0" max="1023" value={s.val} onChange={(e) => s.set(Number(e.target.value))} className="w-full h-1.5 bg-slate-800 rounded-full appearance-none cursor-pointer accent-sky-500" />
                                            <div className="mt-2 flex justify-between text-[10px] font-bold text-slate-600 italic">
                                                <span>RANGE_MIN</span>
                                                <span className={s.val <= 500 ? 'text-rose-500' : ''}>{s.val <= 500 ? 'DETECTED!' : 'CLEAR'}</span>
                                                <span>RANGE_MAX</span>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* Pins Output */}
                            <div className="bg-slate-900/50 rounded-2xl border border-slate-800 p-6">
                                <h2 className="text-xs font-black text-amber-500 uppercase tracking-widest mb-6 flex items-center gap-2">
                                    <i className="fas fa-microchip"></i> 執行器輸出 (Actuator Output)
                                </h2>
                                <div className="grid grid-cols-2 gap-4">
                                    {[ {side: 'LEFT', pinDir: 'P12', dir: carState.p12, pinSpd: 'P8', spd: carState.p8},
                                       {side: 'RIGHT', pinDir: 'P16', dir: carState.p16, pinSpd: 'P0', spd: carState.p0} ].map(m => (
                                        <div key={m.side} className="bg-slate-950 p-4 rounded-xl border border-slate-800">
                                            <div className="text-[10px] font-black text-slate-600 mb-3">{m.side} MOTOR</div>
                                            <div className="space-y-3">
                                                <div className="flex justify-between items-center text-xs">
                                                    <span className="text-slate-500">DIR ({m.pinDir})</span>
                                                    <span className={`font-mono font-bold ${m.dir === 0 ? 'text-emerald-400' : 'text-rose-400'}`}>{m.dir === 0 ? 'F' : 'B'}</span>
                                                </div>
                                                <div className="flex justify-between items-center text-xs">
                                                    <span className="text-slate-500">SPD ({m.pinSpd})</span>
                                                    <span className="font-mono font-bold text-sky-400">{m.spd}</span>
                                                </div>
                                                <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
                                                    <div className="h-full bg-sky-500 transition-all duration-300" style={{width: `${(m.spd/500)*100}%`}}></div>
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* Mini Terminal */}
                            <div className="bg-black/80 rounded-2xl border border-slate-800 p-4 font-mono text-[10px] h-32 overflow-hidden relative">
                                <div className="absolute top-2 right-4 w-2 h-2 bg-emerald-500 rounded-full animate-ping"></div>
                                <div className="text-slate-500 mb-2 border-b border-slate-800 pb-1">CPU THOUGHT_LOG:</div>
                                <div className="space-y-1">
                                    {logs.map((log, i) => (
                                        <div key={i} className="text-emerald-500/80">
                                            <span className="text-emerald-500/30 mr-2">[{new Date().toLocaleTimeString()}]</span>
                                            {log}
                                        </div>
                                    ))}
                                    <div ref={logEndRef} />
                                </div>
                            </div>
                        </div>

                        {/* Right Simulation Canvas */}
                        <div className="lg:col-span-8 flex flex-col gap-6">
                            {/* Visual Display */}
                            <div className="flex-1 bg-slate-950 rounded-3xl border border-slate-800 flex flex-col overflow-hidden relative group">
                                <div className="absolute top-6 left-6 z-10">
                                    <div className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1">Current Action</div>
                                    <div className={`text-4xl font-black italic tracking-tighter ${carState.actionType === 'stop' ? 'text-rose-500' : 'text-emerald-400'} neon-text`}>
                                        {carState.statusTitle}
                                    </div>
                                    <div className="text-xs text-slate-400 mt-2 max-w-xs">{carState.statusText}</div>
                                </div>

                                <div className="flex-1 flex items-center justify-center p-8 bg-[radial-gradient(circle_at_center,_#1e293b_0%,_#0f172a_100%)]">
                                    {/* Grid background */}
                                    <div className="absolute inset-0 opacity-10" style={{backgroundImage: 'radial-gradient(#38bdf8 0.5px, transparent 0.5px)', backgroundSize: '30px 30px'}}></div>
                                    
                                    <svg width="450" height="450" viewBox="0 0 400 400" className="drop-shadow-[0_0_30px_rgba(56,189,248,0.2)]">
                                        <defs>
                                            <marker id="arrow-up" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 10 L 5 0 L 10 10 z" fill="#10b981" /></marker>
                                            <marker id="arrow-down" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 5 10 L 10 0 z" fill="#f43f5e" /></marker>
                                            <filter id="glow">
                                                <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
                                            </filter>
                                        </defs>

                                        {/* Sensor Visuals */}
                                        <g filter="url(#glow)">
                                            <path d="M 120 100 L 70 30 L 170 30 Z" fill={p1 <= 500 ? "#f43f5e" : "#0ea5e9"} opacity={p1 <= 500 ? 0.3 : 0.05} />
                                            <path d="M 280 100 L 230 30 L 330 30 Z" fill={p2 <= 500 ? "#f43f5e" : "#0ea5e9"} opacity={p2 <= 500 ? 0.3 : 0.05} />
                                            <line x1="120" y1="100" x2="120" y2="40" stroke={p1 <= 500 ? "#f43f5e" : "#0ea5e9"} strokeWidth="1" strokeDasharray="4,4" opacity="0.4" />
                                            <line x1="280" y1="100" x2="280" y2="40" stroke={p2 <= 500 ? "#f43f5e" : "#0ea5e9"} strokeWidth="1" strokeDasharray="4,4" opacity="0.4" />
                                        </g>

                                        {/* Car Base - Top Down */}
                                        <rect x="130" y="110" width="140" height="200" fill="#1e293b" rx="25" stroke="#334155" strokeWidth="2" />
                                        <rect x="150" y="130" width="100" height="130" fill="#0f172a" rx="10" />
                                        
                                        {/* PCB Pattern */}
                                        <line x1="200" y1="130" x2="200" y2="260" stroke="#334155" strokeWidth="1" opacity="0.2" />
                                        <circle cx="200" cy="195" r="30" fill="none" stroke="#38bdf8" strokeWidth="0.5" opacity="0.3" />
                                        
                                        {/* Wheels */}
                                        <rect x="115" y="160" width="18" height="80" fill="#020617" rx="4" />
                                        <rect x="267" y="160" width="18" height="80" fill="#020617" rx="4" />
                                        
                                        {/* Dynamic Indicators */}
                                        {renderWheelArrow(carState.p8, carState.p12, 110, 200)}
                                        {renderWheelArrow(carState.p0, carState.p16, 290, 200)}

                                        {/* Sensors On Car */}
                                        <rect x="150" y="100" width="30" height="15" fill="#334155" rx="2" />
                                        <rect x="220" y="100" width="30" height="15" fill="#334155" rx="2" />
                                        <circle cx="165" cy="107" r="4" fill={p1 <= 500 ? "#f43f5e" : "#0ea5e9"} className={p1 <= 500 ? "animate-pulse" : ""} />
                                        <circle cx="235" cy="107" r="4" fill={p2 <= 500 ? "#f43f5e" : "#0ea5e9"} className={p2 <= 500 ? "animate-pulse" : ""} />
                                    </svg>
                                </div>
                            </div>

                            {/* Bottom Info Bar */}
                            <div className="bg-sky-500/10 border border-sky-500/20 rounded-2xl p-6 flex gap-4 items-center">
                                <div className="text-3xl">🧩</div>
                                <div className="text-xs leading-relaxed">
                                    <strong className="text-sky-400 block mb-1 uppercase tracking-wider text-[10px]">邏輯說明 (Internal Logic):</strong>
                                    當感測器讀值低於 <span className="text-white bg-slate-800 px-1 rounded">500</span>，系統將該端判定為障礙物。
                                    避障演算法透過 <span className="text-rose-400 font-bold italic">反向旋轉</span> 其中一個車輪來改變車頭方向，確保安全避開。
                                </div>
                            </div>
                        </div>
                    </main>
                    
                    <footer className="mt-8 text-center text-[10px] text-slate-600 font-bold tracking-[0.3em] uppercase border-t border-slate-800 pt-6">
                        Data provided by Johnathan-LH Learning Hub © 2026
                    </footer>
                </div>
            );
        }

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
