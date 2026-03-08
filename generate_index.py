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

    # 2. 計算時間
    now_utc = datetime.utcnow()
    now_hkt = now_utc + timedelta(hours=8)
    update_time = now_hkt.strftime('%Y-%m-%d %H:%M:%S')

    # 3. 數據準備
    lessons_json = json.dumps(all_lessons)
    
    # 生成左側資料夾樹狀圖
    sidebar_html = f'''
    <div class="mb-4">
        <button onclick="filterBy('ALL', 'ALL')" id="btn-ALL-ALL" class="filter-btn w-full text-left px-4 py-3 rounded-xl text-sm font-black tracking-widest transition-all bg-indigo-600 text-white shadow-md flex items-center group">
            <i class="fas fa-server mr-3 group-hover:animate-pulse"></i> ROOT_SYSTEM
        </button>
    </div>
    <div class="space-y-6 mt-6">
    '''
    
    sorted_main = sorted(hierarchy.keys())
    for main in sorted_main:
        subs = sorted(list(hierarchy[main]))
        
        sub_items_html = ""
        for s in subs:
            # 判斷是否為「全部」
            icon = "fa-folder-open" if s == "全部" else "fa-folder"
            display_name = "VIEW ALL" if s == "全部" else s
            sub_items_html += f'''
            <button onclick="filterBy('{main}', '{s}')" id="btn-{main}-{s}" class="filter-btn w-full text-left px-4 py-2 mt-1 rounded-lg text-xs font-bold text-slate-500 hover:bg-indigo-50 hover:text-indigo-600 transition-all flex items-center group">
                <i class="fas {icon} mr-3 opacity-50 group-hover:opacity-100 group-hover:text-indigo-500 transition-colors"></i> {display_name}
            </button>
            '''
            
        sidebar_html += f'''
        <div>
            <div class="text-xs font-black text-slate-400 uppercase tracking-widest mb-2 px-4 flex items-center">
                <i class="fas fa-database mr-2"></i> {main}
            </div>
            <div class="pl-2 border-l-2 border-slate-200/60 ml-5">
                {sub_items_html}
            </div>
        </div>
        '''
    sidebar_html += "</div>"

    # 4. 生成 HTML
    full_html = f'''
    <!DOCTYPE html>
    <html lang="zh-Hant">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Johnathan's OS Lab</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            #bg-canvas {{ position: fixed; top: 0; left: 0; z-index: -1; width: 100%; height: 100%; background: #f0f4f8; pointer-events: none; }}
            .glass-panel {{ background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 25px 50px -12px rgba(0,0,0,0.1); }}
            
            /* 自訂卷軸，讓它看起來像作業系統 */
            ::-webkit-scrollbar {{ width: 6px; }}
            ::-webkit-scrollbar-track {{ background: transparent; }}
            ::-webkit-scrollbar-thumb {{ background: #cbd5e1; border-radius: 10px; }}
            ::-webkit-scrollbar-thumb:hover {{ background: #94a3b8; }}
        </style>
    </head>
    <body class="min-h-screen text-slate-900 font-sans relative overflow-hidden flex flex-col">
        <canvas id="bg-canvas"></canvas>

        <div class="flex-1 w-full max-w-7xl mx-auto p-4 md:p-8 flex flex-col h-screen">
            
            <!-- 標題列 -->
            <header class="mb-6 flex flex-col md:flex-row justify-between items-start md:items-end gap-4 shrink-0">
                <div>
                    <h1 class="text-3xl font-black tracking-tighter text-slate-800 italic flex items-center">
                        <i class="fas fa-terminal text-indigo-600 mr-3"></i> JOHNATHAN'S LAB
                    </h1>
                    <p class="text-slate-500 font-medium text-xs tracking-widest uppercase mt-1">Interactive OS Explorer / v2.0</p>
                </div>
                <div class="text-[10px] text-slate-500 font-mono flex items-center bg-white/60 backdrop-blur-md px-4 py-2 rounded-lg border border-slate-200">
                    <span class="inline-block w-2 h-2 bg-emerald-500 rounded-full mr-2 animate-pulse shadow-[0_0_8px_rgba(16,185,129,0.6)]"></span>
                    SYSTEM SYNC: {update_time} (HKT)
                </div>
            </header>

            <!-- 模擬 OS 視窗主體 -->
            <main class="flex-1 glass-panel rounded-2xl border border-white flex flex-col overflow-hidden shadow-2xl relative">
                
                <!-- 視窗標題列 (Mac Style) -->
                <div class="bg-slate-900 px-4 py-3 border-b border-slate-800 flex items-center justify-between shrink-0">
                    <div class="flex space-x-2">
                        <div class="w-3 h-3 rounded-full bg-red-500 shadow-[0_0_5px_rgba(239,68,68,0.5)]"></div>
                        <div class="w-3 h-3 rounded-full bg-yellow-500 shadow-[0_0_5px_rgba(234,179,8,0.5)]"></div>
                        <div class="w-3 h-3 rounded-full bg-green-500 shadow-[0_0_5px_rgba(34,197,94,0.5)]"></div>
                    </div>
                    <div class="text-[10px] font-mono text-slate-400 font-bold tracking-widest flex items-center" id="window-path">
                        <i class="fas fa-hdd mr-2 text-slate-500"></i> /root/
                    </div>
                    <div class="w-10"></div> <!-- 佔位平衡 -->
                </div>

                <div class="flex flex-col md:flex-row flex-1 overflow-hidden">
                    
                    <!-- 左側資料夾列 -->
                    <aside class="w-full md:w-64 bg-slate-50/50 border-r border-slate-200/60 p-6 overflow-y-auto shrink-0">
                        {sidebar_html}
                    </aside>

                    <!-- 右側檔案列表 -->
                    <section class="flex-1 flex flex-col bg-white/40 relative overflow-hidden">
                        
                        <!-- 搜尋與工具列 -->
                        <div class="p-4 border-b border-slate-200/60 flex justify-between items-center bg-white/50 backdrop-blur-sm shrink-0">
                            <div class="text-xs font-bold text-slate-500 uppercase tracking-widest">
                                <span id="file-count">0</span> Items found
                            </div>
                            <div class="relative w-64">
                                <i class="fas fa-search absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xs"></i>
                                <input type="text" id="search-input" placeholder="Search system files..." oninput="handleSearch()"
                                       class="w-full pl-9 pr-4 py-1.5 bg-white border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-xs font-mono shadow-sm">
                            </div>
                        </div>

                        <!-- 檔案網格 -->
                        <div class="p-6 overflow-y-auto flex-1">
                            <div id="lessons-grid" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                                <!-- 內容由 JS 動態生成 -->
                            </div>
                            
                            <div id="empty-state" class="hidden h-full flex flex-col items-center justify-center opacity-40">
                                <i class="fas fa-ghost text-6xl mb-4 text-slate-400"></i>
                                <h3 class="text-lg font-bold text-slate-600 font-mono">ERR_FILE_NOT_FOUND</h3>
                            </div>
                        </div>
                        
                    </section>
                </div>
            </main>
            
            <footer class="mt-4 text-center text-slate-400 text-[10px] font-bold uppercase tracking-[0.4em] shrink-0">
                Johnathan-LH Lab • Automated File System Interface
            </footer>
        </div>

        <script>
            // --- 背景粒子網路系統 (與之前相同) ---
            const canvas = document.getElementById('bg-canvas');
            const ctx = canvas.getContext('2d');
            let particles = [];
            const mouse = {{ x: null, y: null, radius: 180 }};

            window.addEventListener('mousemove', (e) => {{ mouse.x = e.x; mouse.y = e.y; }});
            window.addEventListener('mouseout', () => {{ mouse.x = null; mouse.y = null; }});

            class Particle {{
                constructor() {{
                    this.x = Math.random() * canvas.width;
                    this.y = Math.random() * canvas.height;
                    this.size = Math.random() * 2 + 1;
                    this.speedX = (Math.random() - 0.5) * 1.2;
                    this.speedY = (Math.random() - 0.5) * 1.2;
                }}
                draw() {{
                    ctx.fillStyle = 'rgba(79, 70, 229, 0.4)';
                    ctx.beginPath();
                    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                    ctx.fill();
                }}
                update() {{
                    this.x += this.speedX; this.y += this.speedY;
                    if (this.x > canvas.width || this.x < 0) this.speedX *= -1;
                    if (this.y > canvas.height || this.y < 0) this.speedY *= -1;
                }}
            }}

            function init() {{
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
                particles = [];
                let numberOfParticles = Math.floor((canvas.width * canvas.height) / 15000);
                if(numberOfParticles > 100) numberOfParticles = 100; 
                for (let i = 0; i < numberOfParticles; i++) particles.push(new Particle());
            }}

            function animate() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                for (let i = 0; i < particles.length; i++) {{
                    particles[i].update(); particles[i].draw();
                    for (let j = i; j < particles.length; j++) {{
                        let dx = particles[i].x - particles[j].x, dy = particles[i].y - particles[j].y;
                        let distance = Math.sqrt(dx * dx + dy * dy);
                        if (distance < 120) {{
                            ctx.beginPath();
                            ctx.strokeStyle = `rgba(148, 163, 184, ${{0.2 - distance/600}})`;
                            ctx.lineWidth = 0.5;
                            ctx.moveTo(particles[i].x, particles[i].y); ctx.lineTo(particles[j].x, particles[j].y);
                            ctx.stroke();
                        }}
                    }}
                    if (mouse.x != null && mouse.y != null) {{
                        let dxMouse = mouse.x - particles[i].x, dyMouse = mouse.y - particles[i].y;
                        let distMouse = Math.sqrt(dxMouse * dxMouse + dyMouse * dyMouse);
                        if (distMouse < mouse.radius) {{
                            ctx.beginPath();
                            ctx.strokeStyle = `rgba(79, 70, 229, ${{0.6 - distMouse/mouse.radius}})`;
                            ctx.lineWidth = 1;
                            ctx.moveTo(particles[i].x, particles[i].y); ctx.lineTo(mouse.x, mouse.y);
                            ctx.stroke();
                        }}
                    }}
                }}
                requestAnimationFrame(animate);
            }}

            window.addEventListener('resize', init);
            init(); animate();

            // --- 模擬檔案系統渲染邏輯 ---
            const lessons = {lessons_json};
            let currentMain = 'ALL';
            let currentSub = 'ALL';
            let searchQuery = '';

            function render() {{
                const grid = document.getElementById('lessons-grid');
                const empty = document.getElementById('empty-state');
                const pathDisplay = document.getElementById('window-path');
                const countDisplay = document.getElementById('file-count');
                grid.innerHTML = '';
                
                // 1. 過濾數據
                const filtered = lessons.filter(l => {{
                    const matchMain = currentMain === 'ALL' || l.subject === currentMain;
                    const matchSub = currentSub === 'ALL' || l.sub === currentSub;
                    const matchSearch = l.title.toLowerCase().includes(searchQuery) || l.path.toLowerCase().includes(searchQuery);
                    return matchMain && matchSub && matchSearch;
                }});

                countDisplay.innerText = filtered.length;

                // 2. 更新終端機路徑
                let pathText = '<i class="fas fa-hdd mr-2 text-slate-500"></i> /root';
                if (currentMain !== 'ALL') pathText += '/' + currentMain.toLowerCase();
                if (currentSub !== 'ALL') pathText += '/' + currentSub.toLowerCase();
                pathDisplay.innerHTML = pathText + '/';

                // 3. 渲染檔案卡片
                if (filtered.length === 0) {{
                    empty.classList.remove('hidden');
                }} else {{
                    empty.classList.add('hidden');
                    filtered.forEach(l => {{
                        grid.innerHTML += `
                            <a href="${{l.url}}" target="_blank" rel="noopener noreferrer" class="group block bg-white border border-slate-200 hover:border-indigo-400 hover:shadow-lg rounded-xl p-4 transition-all duration-300 relative overflow-hidden">
                                <!-- 懸停時左側會出現一個藍色條 -->
                                <div class="absolute left-0 top-0 h-full w-1 bg-indigo-500 transform -translate-x-full group-hover:translate-x-0 transition-transform"></div>
                                
                                <div class="flex items-start gap-4">
                                    <div class="w-12 h-12 rounded-lg bg-slate-50 border border-slate-100 text-indigo-500 flex items-center justify-center text-xl flex-shrink-0 group-hover:bg-indigo-50 transition-colors">
                                        <i class="fas fa-file-code"></i>
                                    </div>
                                    <div class="flex-1 min-w-0 py-1">
                                        <h3 class="text-sm font-black text-slate-800 leading-tight mb-1 truncate group-hover:text-indigo-600 transition-colors">${{l.title}}</h3>
                                        <div class="flex items-center gap-2 mt-2">
                                            <span class="text-[9px] font-mono text-slate-400 bg-slate-100 px-1.5 py-0.5 rounded truncate">
                                                > ${{l.path}}
                                            </span>
                                        </div>
                                    </div>
                                    <div class="text-slate-300 group-hover:text-indigo-500 flex items-center h-12 transition-colors">
                                        <i class="fas fa-arrow-right text-xs"></i>
                                    </div>
                                </div>
                            </a>
                        `;
                    }});
                }}
            }}

            function filterBy(main, sub) {{
                currentMain = main;
                currentSub = sub;
                
                // 重設所有按鈕樣式為非活躍
                document.querySelectorAll('.filter-btn').forEach(btn => {{
                    btn.classList.remove('bg-indigo-600', 'text-white', 'shadow-md');
                    btn.classList.add('text-slate-500');
                    if(btn.id !== 'btn-ALL-ALL') btn.classList.remove('bg-indigo-50'); // 移除子項目的高亮
                }});

                // 設定當前活躍的按鈕樣式
                const activeId = main === 'ALL' ? 'btn-ALL-ALL' : `btn-${{main}}-${{sub}}`;
                const activeBtn = document.getElementById(activeId);
                
                if (activeBtn) {{
                    if (main === 'ALL') {{
                        activeBtn.classList.add('bg-indigo-600', 'text-white', 'shadow-md');
                        activeBtn.classList.remove('text-slate-500');
                    }} else {{
                        // 子目錄的活躍樣式
                        activeBtn.classList.add('bg-indigo-100', 'text-indigo-700');
                        activeBtn.classList.remove('text-slate-500');
                    }}
                }}

                render();
            }}

            function handleSearch() {{
                searchQuery = document.getElementById('search-input').value.toLowerCase();
                render();
            }}

            // 啟動
            window.onload = render;
        </script>
    </body>
    </html>
    '''
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(full_html)

if __name__ == "__main__":
    generate()