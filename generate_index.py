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
    
    # 科技感左側樹狀圖 (Tree Directory) - 支援顏色分類
    sidebar_html = f'''
    <div class="mb-6">
        <button onclick="filterBy('ALL', 'ALL')" id="btn-ALL-ALL" class="filter-btn w-full text-left px-4 py-3 bg-slate-800/50 border border-slate-500 text-slate-200 font-black tracking-[0.1em] text-sm uppercase transition-all shadow-[0_0_15px_rgba(255,255,255,0.1)] hover:bg-slate-700 cyber-clip flex items-center group active-all">
            <i class="fas fa-network-wired mr-3 group-hover:animate-pulse text-emerald-400"></i> SYS.ROOT_DIR
        </button>
    </div>
    <div class="space-y-6 font-mono">
    '''
    
    sorted_main = sorted(hierarchy.keys())
    for main in sorted_main:
        subs = sorted(list(hierarchy[main]))
        
        # 根據科目決定 UI 顏色 (ICT = Cyan, MATH = Purple, 預設 = Blue)
        color_theme = "blue"
        if main == "ICT":
            color_theme = "cyan"
        elif main == "MATH":
            color_theme = "purple"
            
        sub_items_html = ""
        for idx, s in enumerate(subs):
            is_last = (idx == len(subs) - 1)
            display_name = "VIEW_ALL" if s == "全部" else s
            tree_branch = "└──" if is_last else "├──"
            
            sub_items_html += f'''
            <div class="flex items-center text-slate-600 mt-2">
                <span class="mr-2 text-{color_theme}-900">{tree_branch}</span>
                <button onclick="filterBy('{main}', '{s}')" id="btn-{main}-{s}" class="filter-btn flex-1 text-left px-3 py-1.5 rounded bg-transparent border border-transparent text-xs font-bold text-slate-400 hover:text-{color_theme}-300 hover:border-{color_theme}-500/30 hover:bg-{color_theme}-500/10 transition-all flex items-center group" data-color="{color_theme}">
                    <i class="fas fa-folder mr-2 opacity-50 group-hover:opacity-100 group-hover:text-{color_theme}-400"></i> {display_name}
                </button>
            </div>
            '''
            
        sidebar_html += f'''
        <div>
            <div class="text-sm font-black text-{color_theme}-500 uppercase tracking-widest px-2 flex items-center bg-slate-900/80 py-1 border-l-2 border-{color_theme}-500">
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
        
        <style>
            :root {{
                --dark-bg: #030712;
            }}
            body {{
                background-color: var(--dark-bg);
                color: #e2e8f0;
                overflow-x: hidden;
            }}
            
            #bg-canvas {{ position: fixed; top: 0; left: 0; z-index: -1; width: 100%; height: 100%; pointer-events: none; }}
            
            .scanlines {{
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,0) 50%, rgba(0,0,0,0.25) 50%, rgba(0,0,0,0.25));
                background-size: 100% 4px; z-index: 50; pointer-events: none; opacity: 0.4;
            }}
            
            .cyber-panel {{
                background: rgba(3, 7, 18, 0.75); backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .cyber-clip {{ clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px); }}
            
            /* 動態顏色卡片 */
            .data-card {{
                transition: all 0.3s ease; position: relative;
                border: 1px solid var(--theme-dim);
                background: linear-gradient(135deg, rgba(15,23,42,0.9) 0%, rgba(3,7,18,0.9) 100%);
            }}
            .data-card:hover {{
                border-color: var(--theme-color);
                box-shadow: 0 0 20px var(--theme-glow), inset 0 0 15px var(--theme-dim);
                transform: translateY(-4px);
            }}
            .data-card::before {{
                content: ''; position: absolute; top: -1px; left: -1px; width: 20px; height: 20px;
                border-top: 2px solid var(--theme-color); border-left: 2px solid var(--theme-color);
                transition: all 0.3s ease;
            }}
            .data-card:hover::before {{ width: 100%; height: 100%; opacity: 0.3; }}
            
            .blinking-cursor {{ animation: blink 1s step-end infinite; }}
            @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
            
            /* 側邊欄活躍按鈕動態顏色 */
            .filter-btn.active-cyan {{ color: #22d3ee; border-color: #06b6d4; background: rgba(6, 182, 212, 0.15); text-shadow: 0 0 8px #06b6d4; }}
            .filter-btn.active-purple {{ color: #d8b4fe; border-color: #a855f7; background: rgba(168, 85, 247, 0.15); text-shadow: 0 0 8px #a855f7; }}
            .filter-btn.active-blue {{ color: #93c5fd; border-color: #3b82f6; background: rgba(59, 130, 246, 0.15); text-shadow: 0 0 8px #3b82f6; }}
            
            ::-webkit-scrollbar {{ width: 4px; }}
            ::-webkit-scrollbar-track {{ background: #0f172a; }}
            ::-webkit-scrollbar-thumb {{ background: #475569; }}
        </style>
    </head>
    <body class="flex flex-col min-h-screen font-sans">
        <div class="scanlines"></div>
        <canvas id="bg-canvas"></canvas>

        <div class="flex-1 w-full max-w-screen-2xl mx-auto p-4 md:p-6 flex flex-col h-screen z-10 relative">
            
            <!-- 頂部遙測儀表板 -->
            <header class="mb-6 flex flex-col md:flex-row justify-between items-start md:items-end gap-4 shrink-0 border-b border-slate-800 pb-4">
                <div class="flex items-center gap-4">
                    <div class="w-16 h-16 bg-slate-900 border border-slate-600 flex items-center justify-center rounded cyber-clip shadow-lg">
                        <i class="fas fa-satellite-dish text-slate-300 text-2xl animate-pulse"></i>
                    </div>
                    <div>
                        <h1 class="text-3xl md:text-4xl font-black tracking-widest text-white">
                            JOHNATHAN <span class="text-slate-500">//</span> LAB<span class="blinking-cursor text-slate-500">_</span>
                        </h1>
                        <p class="text-slate-400 font-bold text-[10px] tracking-[0.3em] uppercase mt-1 font-mono">Global Learning Network Node &bull; Authorized Access Only</p>
                    </div>
                </div>
                
                <div class="flex gap-3">
                    <div class="cyber-panel px-4 py-2 font-mono">
                        <div class="text-[8px] text-slate-400 uppercase tracking-widest mb-1">System Status</div>
                        <div class="text-emerald-400 text-xs font-bold tracking-widest flex items-center">
                            <span class="w-1.5 h-1.5 bg-emerald-400 rounded-full mr-2 shadow-[0_0_5px_#34d399]"></span>ONLINE
                        </div>
                    </div>
                    <div class="cyber-panel px-4 py-2 font-mono">
                        <div class="text-[8px] text-slate-400 uppercase tracking-widest mb-1">Last Sync (HKT)</div>
                        <div class="text-slate-300 text-xs font-bold tracking-widest">{update_time}</div>
                    </div>
                </div>
            </header>

            <main class="flex-1 cyber-panel flex flex-col md:flex-row overflow-hidden relative cyber-clip border-slate-700">
                
                <aside class="w-full md:w-64 bg-slate-950/90 border-r border-slate-800 p-6 overflow-y-auto shrink-0 z-10">
                    <div class="text-[10px] text-slate-500 mb-6 font-bold tracking-widest border-b border-slate-800 pb-2 font-mono">
                        > DIRECTORY_TREE
                    </div>
                    {sidebar_html}
                </aside>

                <section class="flex-1 flex flex-col relative overflow-hidden z-10">
                    
                    <div class="p-4 border-b border-slate-800 flex flex-col sm:flex-row justify-between items-center bg-slate-900/60 shrink-0 gap-4 font-mono">
                        <div class="text-xs font-bold text-slate-400 tracking-widest flex items-center">
                            <i class="fas fa-terminal mr-2 text-slate-500"></i> 
                            <span class="text-white mr-2">QUERY:</span> 
                            <span id="file-count" class="text-slate-300">0</span> DATABLOCKS FOUND
                        </div>
                        <div class="relative w-full sm:w-80">
                            <span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 font-bold">>_</span>
                            <input type="text" id="search-input" placeholder="ENTER SEARCH PARAMETER..." oninput="handleSearch()"
                                   class="w-full pl-9 pr-4 py-2 bg-slate-950 border border-slate-700 focus:outline-none focus:border-slate-400 transition-all text-xs font-bold text-white placeholder-slate-700 cyber-clip">
                        </div>
                    </div>

                    <div class="p-6 overflow-y-auto flex-1 bg-gradient-to-br from-slate-900/30 to-transparent">
                        <div id="lessons-grid" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                            <!-- JS 動態生成 -->
                        </div>
                        
                        <div id="empty-state" class="hidden h-full flex flex-col items-center justify-center opacity-40">
                            <i class="fas fa-exclamation-triangle text-6xl mb-6 text-red-500"></i>
                            <h3 class="text-2xl font-black text-red-500 tracking-[0.2em] mb-2 font-mono">ERR_404</h3>
                            <p class="text-slate-400 tracking-widest text-sm font-mono">NO CORRESPONDING DATA BLOCKS LOCATED.</p>
                        </div>
                    </div>
                </section>
            </main>
            
            <footer class="mt-4 flex justify-between items-center text-slate-600 text-[10px] font-bold uppercase tracking-[0.3em] shrink-0 font-mono">
                <span>> SYS.MAINTAINER: JOHNATHAN-LH</span>
                <span>SECURE CONNECTION ESTABLISHED // PORT 443</span>
            </footer>
        </div>

        <script>
            // --- 高效能粒子系統 (FPS Optimized) ---
            const canvas = document.getElementById('bg-canvas');
            const ctx = canvas.getContext('2d');
            let particles = [];
            const mouse = {{ x: null, y: null, radius: 200 }};

            window.addEventListener('mousemove', (e) => {{ mouse.x = e.x; mouse.y = e.y; }});
            window.addEventListener('mouseout', () => {{ mouse.x = null; mouse.y = null; }});

            class Particle {{
                constructor() {{
                    this.x = Math.random() * canvas.width;
                    this.y = Math.random() * canvas.height;
                    this.size = Math.random() * 1.5 + 0.5;
                    this.speedX = (Math.random() - 0.5) * 0.5; 
                    this.speedY = (Math.random() - 0.5) * 0.5;
                }}
                draw() {{
                    ctx.fillStyle = 'rgba(99, 102, 241, 0.6)'; 
                    ctx.beginPath();
                    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                    ctx.fill();
                }}
                update() {{
                    this.x += this.speedX; this.y += this.speedY;
                    if (this.x > canvas.width || this.x < 0) this.speedX *= -1;
                    if (this.y > canvas.height || this.y < 0) this.speedY *= -1;

                    if (mouse.x != null) {{
                        let dx = mouse.x - this.x;
                        let dy = mouse.y - this.y;
                        if (Math.abs(dx) < mouse.radius && Math.abs(dy) < mouse.radius) {{
                            let distance = Math.sqrt(dx * dx + dy * dy);
                            if (distance < mouse.radius) {{
                                this.x += dx * 0.01;
                                this.y += dy * 0.01;
                            }}
                        }}
                    }}
                }}
            }}

            function init() {{
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
                particles = [];
                let numberOfParticles = Math.floor((canvas.width * canvas.height) / 15000);
                if(numberOfParticles > 70) numberOfParticles = 70; 
                for (let i = 0; i < numberOfParticles; i++) particles.push(new Particle());
            }}

            function animate() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                for (let i = 0; i < particles.length; i++) {{
                    particles[i].update(); 
                    particles[i].draw();
                    
                    for (let j = i + 1; j < particles.length; j++) {{
                        let dx = particles[i].x - particles[j].x;
                        let dy = particles[i].y - particles[j].y;
                        
                        if (Math.abs(dx) > 120 || Math.abs(dy) > 120) continue;
                        
                        let distance = Math.sqrt(dx * dx + dy * dy);
                        if (distance < 120) {{
                            ctx.beginPath();
                            ctx.strokeStyle = `rgba(99, 102, 241, ${{0.2 - distance/600}})`;
                            ctx.lineWidth = 0.5;
                            ctx.moveTo(particles[i].x, particles[i].y); 
                            ctx.lineTo(particles[j].x, particles[j].y);
                            ctx.stroke();
                        }}
                    }}
                    
                    if (mouse.x != null) {{
                        let dxMouse = mouse.x - particles[i].x;
                        let dyMouse = mouse.y - particles[i].y;
                        if (Math.abs(dxMouse) < mouse.radius && Math.abs(dyMouse) < mouse.radius) {{
                            let distMouse = Math.sqrt(dxMouse * dxMouse + dyMouse * dyMouse);
                            if (distMouse < mouse.radius * 0.7) {{
                                ctx.beginPath();
                                ctx.strokeStyle = `rgba(6, 182, 212, ${{0.6 - distMouse/mouse.radius}})`;
                                ctx.lineWidth = 1;
                                ctx.moveTo(particles[i].x, particles[i].y); 
                                ctx.lineTo(mouse.x, mouse.y);
                                ctx.stroke();
                            }}
                        }}
                    }}
                }}
                requestAnimationFrame(animate);
            }}

            let resizeTimer;
            window.addEventListener('resize', () => {{
                clearTimeout(resizeTimer);
                resizeTimer = setTimeout(init, 200); 
            }});
            init(); animate();

            // --- 色彩管理與渲染邏輯 ---
            const lessons = {lessons_json};
            let currentMain = 'ALL';
            let currentSub = 'ALL';
            let searchQuery = '';

            const themeMap = {{
                'ICT': {{ color: '#06b6d4', dim: 'rgba(6,182,212,0.3)', glow: 'rgba(6,182,212,0.2)', bg: 'rgba(6,182,212,0.1)' }},   
                'MATH': {{ color: '#a855f7', dim: 'rgba(168,85,247,0.3)', glow: 'rgba(168,85,247,0.2)', bg: 'rgba(168,85,247,0.1)' }}, 
                'DEFAULT': {{ color: '#3b82f6', dim: 'rgba(59,130,246,0.3)', glow: 'rgba(59,130,246,0.2)', bg: 'rgba(59,130,246,0.1)' }} 
            }};

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
                        const theme = themeMap[l.subject] || themeMap['DEFAULT'];
                        
                        // 修復重點：使用 ${{l.變數}} 來讓 Javascript 正確解析範本字串
                        grid.innerHTML += `
                            <div class="data-card p-6 cyber-clip group flex flex-col justify-between h-48" 
                                 style="--theme-color: ${{theme.color}}; --theme-dim: ${{theme.dim}}; --theme-glow: ${{theme.glow}}; --theme-bg: ${{theme.bg}};">
                                <div>
                                    <div class="flex justify-between items-start mb-4">
                                        <div class="text-[9px] font-bold uppercase tracking-widest px-2 py-1 border font-mono" 
                                             style="color: ${{theme.color}}; border-color: ${{theme.color}}; background: ${{theme.bg}};">
                                            SYS_${{l.subject}} / ${{l.sub}}
                                        </div>
                                        <i class="fas fa-file-code opacity-40 group-hover:opacity-100 transition-all text-lg" style="color: ${{theme.color}};"></i>
                                    </div>
                                    <h3 class="text-xl font-black text-white mb-2 transition-colors leading-snug line-clamp-2" 
                                        style="text-shadow: 0 0 10px ${{theme.glow}};">${{l.title}}</h3>
                                    <p class="text-[10px] text-slate-500 font-mono truncate">>${{l.path}}</p>
                                </div>
                                <div class="mt-4 pt-4 border-t border-slate-800 flex justify-between items-center opacity-70 group-hover:opacity-100 transition-opacity">
                                    <div class="text-[8px] text-slate-500 tracking-widest uppercase font-mono">DATABLOCK_READY</div>
                                    <a href="${{l.url}}" target="_blank" rel="noopener noreferrer" 
                                       class="text-xs font-black tracking-widest px-4 py-2 border transition-all cyber-clip font-mono"
                                       style="color: ${{theme.color}}; border-color: ${{theme.color}};"
                                       onmouseover="this.style.backgroundColor='${{theme.color}}'; this.style.color='#fff';"
                                       onmouseout="this.style.backgroundColor='transparent'; this.style.color='${{theme.color}}';">
                                        EXECUTE <i class="fas fa-play ml-2 text-[10px]"></i>
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
                
                document.querySelectorAll('.filter-btn').forEach(btn => {{
                    btn.classList.remove('active-cyan', 'active-purple', 'active-blue', 'bg-slate-700');
                    if(btn.id === 'btn-ALL-ALL') btn.classList.remove('shadow-[0_0_15px_rgba(255,255,255,0.1)]');
                }});

                const activeId = main === 'ALL' ? 'btn-ALL-ALL' : `btn-${{main}}-${{sub}}`;
                const activeBtn = document.getElementById(activeId);
                
                if (activeBtn) {{
                    if (main === 'ALL') {{
                        activeBtn.classList.add('bg-slate-700', 'shadow-[0_0_15px_rgba(255,255,255,0.1)]');
                    }} else {{
                        const colorTheme = activeBtn.getAttribute('data-color') || 'blue';
                        activeBtn.classList.add(`active-${{colorTheme}}`);
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
