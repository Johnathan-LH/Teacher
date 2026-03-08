import os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json

def generate():
    all_lessons = []
    hierarchy = {}
    
    # 1. 掃描目錄
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.html') and file != 'index.html':
                file_path = os.path.join(root, file)
                display_path = file_path.replace('./', '').replace('\\', '/')
                path_parts = display_path.split('/')
                
                main_subject = "其他"
                sub_category = "全部"
                
                if len(path_parts) > 2:
                    main_subject = path_parts[0].upper()
                    sub_category = path_parts[1].upper()
                elif len(path_parts) == 2:
                    main_subject = path_parts[0].upper()
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        soup = BeautifulSoup(f, 'html.parser')
                        title = soup.title.string if soup.title else file
                except:
                    title = file

                lesson_data = {
                    "title": str(title).strip(),
                    "url": display_path,
                    "subject": main_subject,
                    "sub": sub_category,
                    "path": display_path
                }
                all_lessons.append(lesson_data)
                
                if main_subject not in hierarchy:
                    hierarchy[main_subject] = set()
                hierarchy[main_subject].add(sub_category)

    # 2. 計算時間 (HKT)
    now_utc = datetime.utcnow()
    now_hkt = now_utc + timedelta(hours=8)
    update_time = now_hkt.strftime('%Y-%m-%d %H:%M:%S')

    # 3. 數據準備
    lessons_json = json.dumps(all_lessons)
    
    # 科技感左側樹狀圖 (Tree Directory)
    sidebar_html = f'''
    <div class="mb-6">
        <button onclick="filterBy('ALL', 'ALL')" id="btn-ALL-ALL" class="filter-btn w-full text-left px-4 py-3 bg-cyan-500/10 border border-cyan-500 text-cyan-400 font-['Orbitron'] tracking-[0.2em] text-sm uppercase transition-all shadow-[0_0_15px_rgba(6,182,212,0.3)] hover:bg-cyan-500/20 cyber-clip flex items-center group">
            <i class="fas fa-network-wired mr-3 group-hover:animate-pulse"></i> SYS.ROOT_DIR
        </button>
    </div>
    <div class="space-y-6 font-['Share_Tech_Mono']">
    '''
    
    sorted_main = sorted(hierarchy.keys())
    for main in sorted_main:
        subs = sorted(list(hierarchy[main]))
        
        sub_items_html = ""
        for idx, s in enumerate(subs):
            is_last = (idx == len(subs) - 1)
            display_name = "VIEW_ALL" if s == "全部" else s
            tree_branch = "└──" if is_last else "├──"
            
            sub_items_html += f'''
            <div class="flex items-center text-slate-500 mt-2">
                <span class="mr-2 text-cyan-800">{tree_branch}</span>
                <button onclick="filterBy('{main}', '{s}')" id="btn-{main}-{s}" class="filter-btn flex-1 text-left px-3 py-1.5 rounded bg-transparent border border-transparent text-xs font-bold text-slate-400 hover:text-cyan-300 hover:border-cyan-500/30 hover:bg-cyan-500/5 transition-all flex items-center group">
                    <i class="fas fa-folder mr-2 opacity-50 group-hover:opacity-100 group-hover:text-cyan-400"></i> {display_name}
                </button>
            </div>
            '''
            
        sidebar_html += f'''
        <div>
            <div class="text-sm font-bold text-cyan-600 uppercase tracking-widest px-2 flex items-center bg-slate-900/50 py-1 border-l-2 border-cyan-600">
                <i class="fas fa-database mr-2 text-xs"></i> {main}
            </div>
            <div class="pl-2 ml-1 border-l border-slate-800/80">
                {sub_items_html}
            </div>
        </div>
        '''
    sidebar_html += "</div>"

    # 4. 生成極致未來感 HTML
    full_html = f'''
    <!DOCTYPE html>
    <html lang="zh-Hant">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>JOHNATHAN // NEXUS_LAB</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <!-- 引入科幻字體 -->
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
        
        <style>
            :root {{
                --neon-cyan: #06b6d4;
                --neon-purple: #8b5cf6;
                --dark-bg: #030712;
            }}
            body {{
                background-color: var(--dark-bg);
                color: #e2e8f0;
                font-family: 'Share Tech Mono', monospace;
                overflow-x: hidden;
            }}
            h1, h2, h3, .orbitron {{ font-family: 'Orbitron', sans-serif; }}
            
            #bg-canvas {{ position: fixed; top: 0; left: 0; z-index: -1; width: 100%; height: 100%; pointer-events: none; }}
            
            /* 掃描線特效 */
            .scanlines {{
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,0) 50%, rgba(0,0,0,0.2) 50%, rgba(0,0,0,0.2));
                background-size: 100% 4px; z-index: 50; pointer-events: none; opacity: 0.3;
            }}
            
            /* HUD 玻璃面板 */
            .cyber-panel {{
                background: rgba(3, 7, 18, 0.7); backdrop-filter: blur(10px);
                border: 1px solid rgba(6, 182, 212, 0.2);
                box-shadow: inset 0 0 20px rgba(6, 182, 212, 0.05);
            }}
            
            /* 賽博切角設計 */
            .cyber-clip {{ clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px); }}
            
            /* 課件卡片特效 */
            .data-card {{
                transition: all 0.3s ease; position: relative;
                border: 1px solid rgba(6, 182, 212, 0.3);
                background: linear-gradient(135deg, rgba(15,23,42,0.9) 0%, rgba(3,7,18,0.9) 100%);
            }}
            .data-card:hover {{
                border-color: var(--neon-cyan);
                box-shadow: 0 0 20px rgba(6, 182, 212, 0.2), inset 0 0 15px rgba(6, 182, 212, 0.1);
                transform: translateY(-5px);
            }}
            .data-card::before {{
                content: ''; position: absolute; top: -1px; left: -1px; width: 20px; height: 20px;
                border-top: 2px solid var(--neon-cyan); border-left: 2px solid var(--neon-cyan);
                transition: all 0.3s ease;
            }}
            .data-card:hover::before {{ width: 100%; height: 100%; border-color: var(--neon-cyan); opacity: 0.5; }}
            
            /* 閃爍游標 */
            .blinking-cursor {{ animation: blink 1s step-end infinite; }}
            @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
            
            /* 活躍按鈕狀態 */
            .filter-btn.active {{ color: var(--neon-cyan); border-color: var(--neon-cyan); background: rgba(6, 182, 212, 0.1); text-shadow: 0 0 8px var(--neon-cyan); }}
            
            ::-webkit-scrollbar {{ width: 4px; }}
            ::-webkit-scrollbar-track {{ background: #0f172a; }}
            ::-webkit-scrollbar-thumb {{ background: #06b6d4; }}
        </style>
    </head>
    <body class="flex flex-col min-h-screen">
        <div class="scanlines"></div>
        <canvas id="bg-canvas"></canvas>

        <div class="flex-1 w-full max-w-screen-2xl mx-auto p-4 md:p-6 flex flex-col h-screen z-10 relative">
            
            <!-- 頂部遙測儀表板 (Telemetry HUD) -->
            <header class="mb-6 flex flex-col md:flex-row justify-between items-start md:items-end gap-4 shrink-0 border-b border-cyan-900/50 pb-4">
                <div class="flex items-center gap-4">
                    <div class="w-16 h-16 bg-cyan-950 border border-cyan-500 flex items-center justify-center rounded cyber-clip shadow-[0_0_15px_rgba(6,182,212,0.2)]">
                        <i class="fas fa-satellite-dish text-cyan-400 text-2xl animate-pulse"></i>
                    </div>
                    <div>
                        <h1 class="text-3xl md:text-4xl font-black tracking-widest text-white orbitron">
                            J0HNATHAN <span class="text-cyan-400">//</span> LAB<span class="blinking-cursor text-cyan-400">_</span>
                        </h1>
                        <p class="text-cyan-600 font-bold text-[10px] tracking-[0.3em] uppercase mt-1">Global Learning Network Node &bull; Authorized Access Only</p>
                    </div>
                </div>
                
                <div class="flex gap-3">
                    <div class="cyber-panel px-4 py-2 border-cyan-500/30">
                        <div class="text-[8px] text-cyan-500 uppercase tracking-widest mb-1">Status</div>
                        <div class="text-emerald-400 text-xs font-bold tracking-widest flex items-center">
                            <span class="w-1.5 h-1.5 bg-emerald-400 rounded-full mr-2 shadow-[0_0_5px_#34d399]"></span>ONLINE
                        </div>
                    </div>
                    <div class="cyber-panel px-4 py-2 border-cyan-500/30">
                        <div class="text-[8px] text-cyan-500 uppercase tracking-widest mb-1">Last Sync (HKT)</div>
                        <div class="text-cyan-300 text-xs font-bold tracking-widest">{update_time}</div>
                    </div>
                </div>
            </header>

            <!-- 核心終端機介面 -->
            <main class="flex-1 cyber-panel flex flex-col md:flex-row overflow-hidden relative cyber-clip border-cyan-800">
                
                <!-- 裝飾用角標 -->
                <div class="absolute top-0 right-0 w-20 h-20 border-t-4 border-r-4 border-cyan-500/30 m-1 pointer-events-none"></div>
                <div class="absolute bottom-0 left-0 w-20 h-20 border-b-4 border-l-4 border-cyan-500/30 m-1 pointer-events-none"></div>

                <!-- 左側資料夾樹 (Sidebar) -->
                <aside class="w-full md:w-64 bg-slate-950/80 border-r border-cyan-900/50 p-6 overflow-y-auto shrink-0 z-10">
                    <div class="text-[10px] text-cyan-500 mb-6 font-bold tracking-widest border-b border-cyan-900/50 pb-2">
                        > DIRECTORY_TREE
                    </div>
                    {sidebar_html}
                </aside>

                <!-- 右側數據顯示區 -->
                <section class="flex-1 flex flex-col relative overflow-hidden z-10">
                    
                    <!-- 指令搜尋列 -->
                    <div class="p-4 border-b border-cyan-900/50 flex flex-col sm:flex-row justify-between items-center bg-slate-900/50 shrink-0 gap-4">
                        <div class="text-xs font-bold text-cyan-500 tracking-widest flex items-center">
                            <i class="fas fa-terminal mr-2"></i> 
                            <span class="text-white mr-2">QUERY:</span> 
                            <span id="file-count" class="text-cyan-300">0</span> DATABLOCKS FOUND
                        </div>
                        <div class="relative w-full sm:w-80">
                            <span class="absolute left-3 top-1/2 -translate-y-1/2 text-cyan-500 font-bold">>_</span>
                            <input type="text" id="search-input" placeholder="ENTER SEARCH PARAMETER..." oninput="handleSearch()"
                                   class="w-full pl-9 pr-4 py-2 bg-slate-950 border border-cyan-800 focus:outline-none focus:border-cyan-400 focus:shadow-[0_0_10px_rgba(6,182,212,0.3)] transition-all text-xs font-bold text-cyan-100 placeholder-cyan-800 cyber-clip">
                        </div>
                    </div>

                    <!-- 課件數據網格 -->
                    <div class="p-6 overflow-y-auto flex-1 bg-gradient-to-br from-slate-900/50 to-transparent">
                        <div id="lessons-grid" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                            <!-- JS 動態生成 -->
                        </div>
                        
                        <!-- 找不到檔案 -->
                        <div id="empty-state" class="hidden h-full flex flex-col items-center justify-center opacity-50">
                            <i class="fas fa-exclamation-triangle text-6xl mb-6 text-red-500 shadow-[0_0_30px_#ef4444]"></i>
                            <h3 class="text-2xl font-bold text-red-500 orbitron tracking-[0.2em] mb-2">ERR_404</h3>
                            <p class="text-cyan-600 tracking-widest text-sm">NO CORRESPONDING DATA BLOCKS LOCATED.</p>
                        </div>
                    </div>
                </section>
            </main>
            
            <footer class="mt-4 flex justify-between items-center text-cyan-700 text-[10px] font-bold uppercase tracking-[0.3em] shrink-0">
                <span>> SYS.MAINTAINER: JOHNATHAN-LH</span>
                <span>SECURE CONNECTION ESTABLISHED // PORT 443</span>
            </footer>
        </div>

        <script>
            // --- 量子引力粒子系統 (Quantum Gravity Mesh) ---
            const canvas = document.getElementById('bg-canvas');
            const ctx = canvas.getContext('2d');
            let particles = [];
            const mouse = {{ x: null, y: null, radius: 250 }}; // 擴大引力範圍

            window.addEventListener('mousemove', (e) => {{ mouse.x = e.x; mouse.y = e.y; }});
            window.addEventListener('mouseout', () => {{ mouse.x = null; mouse.y = null; }});

            class Particle {{
                constructor() {{
                    this.x = Math.random() * canvas.width;
                    this.y = Math.random() * canvas.height;
                    this.size = Math.random() * 2 + 0.5;
                    this.baseX = this.x;
                    this.baseY = this.y;
                    this.density = (Math.random() * 30) + 1;
                    this.speedX = (Math.random() - 0.5) * 0.8;
                    this.speedY = (Math.random() - 0.5) * 0.8;
                }}
                draw() {{
                    ctx.fillStyle = 'rgba(6, 182, 212, 0.8)'; // 明亮的青色
                    ctx.beginPath();
                    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                    ctx.fill();
                    // 發光效果
                    ctx.shadowBlur = 10;
                    ctx.shadowColor = '#06b6d4';
                }}
                update() {{
                    // 1. 基本移動
                    this.x += this.speedX; this.y += this.speedY;
                    if (this.x > canvas.width || this.x < 0) this.speedX *= -1;
                    if (this.y > canvas.height || this.y < 0) this.speedY *= -1;

                    // 2. 磁吸引力互動 (Magnetic Attraction)
                    if (mouse.x != null) {{
                        let dx = mouse.x - this.x;
                        let dy = mouse.y - this.y;
                        let distance = Math.sqrt(dx * dx + dy * dy);
                        let forceDirectionX = dx / distance;
                        let forceDirectionY = dy / distance;
                        let maxDistance = mouse.radius;
                        let force = (maxDistance - distance) / maxDistance;
                        let directionX = forceDirectionX * force * this.density;
                        let directionY = forceDirectionY * force * this.density;

                        if (distance < mouse.radius) {{
                            this.x += directionX * 0.05; // 吸向鼠標
                            this.y += directionY * 0.05;
                        }}
                    }}
                }}
            }}

            function init() {{
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
                particles = [];
                let numberOfParticles = Math.floor((canvas.width * canvas.height) / 10000);
                if(numberOfParticles > 150) numberOfParticles = 150; 
                for (let i = 0; i < numberOfParticles; i++) particles.push(new Particle());
            }}

            function animate() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                for (let i = 0; i < particles.length; i++) {{
                    particles[i].update(); 
                    particles[i].draw();
                    
                    // 粒子間的網路連線
                    for (let j = i; j < particles.length; j++) {{
                        let dx = particles[i].x - particles[j].x;
                        let dy = particles[i].y - particles[j].y;
                        let distance = Math.sqrt(dx * dx + dy * dy);
                        if (distance < 100) {{
                            ctx.beginPath();
                            ctx.strokeStyle = `rgba(6, 182, 212, ${{0.3 - distance/333}})`;
                            ctx.lineWidth = 1;
                            ctx.moveTo(particles[i].x, particles[i].y); 
                            ctx.lineTo(particles[j].x, particles[j].y);
                            ctx.stroke();
                        }}
                    }}
                    
                    // 鼠標雷射連線
                    if (mouse.x != null && mouse.y != null) {{
                        let dxMouse = mouse.x - particles[i].x;
                        let dyMouse = mouse.y - particles[i].y;
                        let distMouse = Math.sqrt(dxMouse * dxMouse + dyMouse * dyMouse);
                        if (distMouse < mouse.radius * 0.8) {{
                            ctx.beginPath();
                            ctx.strokeStyle = `rgba(6, 182, 212, ${{0.8 - distMouse/mouse.radius}})`;
                            ctx.lineWidth = 1.5;
                            ctx.moveTo(particles[i].x, particles[i].y); 
                            ctx.lineTo(mouse.x, mouse.y);
                            ctx.stroke();
                        }}
                    }}
                }}
                requestAnimationFrame(animate);
            }}

            window.addEventListener('resize', init);
            init(); animate();

            // --- 檔案系統渲染邏輯 ---
            const lessons = {lessons_json};
            let currentMain = 'ALL';
            let currentSub = 'ALL';
            let searchQuery = '';

            function render() {{
                const grid = document.getElementById('lessons-grid');
                const empty = document.getElementById('empty-state');
                const countDisplay = document.getElementById('file-count');
                grid.innerHTML = '';
                
                const filtered = lessons.filter(l => {{
                    const matchMain = currentMain === 'ALL' || l.subject === currentMain;
                    const matchSub = currentSub === 'ALL' || l.sub === currentSub;
                    const matchSearch = l.title.toLowerCase().includes(searchQuery) || l.path.toLowerCase().includes(searchQuery);
                    return matchMain && matchSub && matchSearch;
                }});

                countDisplay.innerText = filtered.length;

                if (filtered.length === 0) {{
                    empty.classList.remove('hidden');
                }} else {{
                    empty.classList.add('hidden');
                    filtered.forEach(l => {{
                        // 修復：在 Python f-string 內部要輸出 JS 的 template literal 變數，必須雙寫大括號，如 ${{l.title}}
                        grid.innerHTML += `
                            <div class="data-card p-6 cyber-clip group flex flex-col justify-between h-48">
                                <div>
                                    <div class="flex justify-between items-start mb-4">
                                        <div class="text-[8px] text-cyan-500 font-bold uppercase tracking-widest bg-cyan-950 px-2 py-1 border border-cyan-800">
                                            ID: ${{l.subject}}-${{l.sub}}
                                        </div>
                                        <i class="fas fa-satellite-dish text-slate-600 group-hover:text-cyan-400 group-hover:animate-ping transition-colors text-[10px]"></i>
                                    </div>
                                    <h3 class="text-lg orbitron font-bold text-white mb-2 group-hover:text-cyan-300 transition-colors leading-snug line-clamp-2">${{l.title}}</h3>
                                    <p class="text-[10px] text-cyan-700 font-mono truncate">>${{l.path}}</p>
                                </div>
                                <div class="mt-4 pt-4 border-t border-cyan-900/50 flex justify-between items-center opacity-70 group-hover:opacity-100 transition-opacity">
                                    <div class="text-[8px] text-cyan-600 tracking-widest uppercase">Size: 4.2KB</div>
                                    <a href="${{l.url}}" target="_blank" rel="noopener noreferrer" class="text-xs font-bold text-cyan-400 hover:text-white hover:bg-cyan-600 px-3 py-1.5 border border-cyan-500 transition-all cyber-clip shadow-[0_0_10px_rgba(6,182,212,0.2)]">
                                        EXECUTE <i class="fas fa-play ml-1 text-[8px]"></i>
                                    </a>
                                </div>
                            </div>
                        `;
                    }});
                }}
            }}

            function filterBy(main, sub) {{
                currentMain = main;
                currentSub = sub;
                
                // 重設按鈕樣式
                document.querySelectorAll('.filter-btn').forEach(btn => {{
                    btn.classList.remove('active', 'text-cyan-300', 'bg-cyan-500/10', 'border-cyan-500/50');
                    if(btn.id !== 'btn-ALL-ALL') btn.classList.remove('text-cyan-300'); 
                }});

                const activeId = main === 'ALL' ? 'btn-ALL-ALL' : `btn-${{main}}-${{sub}}`;
                const activeBtn = document.getElementById(activeId);
                
                if (activeBtn) {{
                    activeBtn.classList.add('active');
                    if (main !== 'ALL') {{
                        activeBtn.classList.add('text-cyan-300', 'bg-cyan-500/10', 'border-cyan-500/50');
                    }}
                }}

                render();
            }}

            function handleSearch() {{
                searchQuery = document.getElementById('search-input').value.toLowerCase();
                render();
            }}

            window.onload = render;
        </script>
    </body>
    </html>
    '''
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(full_html)

if __name__ == "__main__":
    generate()