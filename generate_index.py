import os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json

def generate():
    all_lessons = []
    hierarchy = {}
    
    # 1. 掃描所有目錄
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

    # 2. 計算香港時間 (HKT)
    now_utc = datetime.utcnow()
    now_hkt = now_utc + timedelta(hours=8)
    update_time = now_hkt.strftime('%Y-%m-%d %H:%M:%S')

    # 3. 數據準備
    lessons_json = json.dumps(all_lessons)
    
    nav_html = ""
    sorted_main = sorted(hierarchy.keys())
    for main in sorted_main:
        subs = sorted(list(hierarchy[main]))
        if len(subs) > 1 or (len(subs) == 1 and subs[0] != "全部"):
            sub_items = "".join([
                f'<button onclick="filterBy(\'{main}\', \'{s}\')" class="block w-full text-left px-4 py-2 text-[10px] font-bold text-slate-600 hover:bg-indigo-50 hover:text-indigo-600 transition-colors uppercase tracking-widest">{s}</button>'
                for s in subs
            ])
            nav_html += f'''
            <div class="relative group">
                <button onclick="filterBy('{main}', 'ALL')" class="filter-btn px-5 py-2 rounded-xl border border-slate-200 text-xs font-black tracking-widest transition-all text-slate-500 hover:border-indigo-400 flex items-center gap-2" data-main="{main}">
                    {main} <i class="fas fa-chevron-down text-[8px] opacity-50 group-hover:rotate-180 transition-transform"></i>
                </button>
                <div class="absolute top-full left-0 mt-2 w-32 bg-white border border-slate-100 rounded-xl shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50 py-2 border-t-4 border-t-indigo-500">
                    <button onclick="filterBy('{main}', 'ALL')" class="block w-full text-left px-4 py-2 text-[10px] font-black text-indigo-600 border-b border-slate-50 mb-1 italic">VIEW ALL</button>
                    {sub_items}
                </div>
            </div>
            '''
        else:
            nav_html += f'''
            <button onclick="filterBy('{main}', 'ALL')" class="filter-btn px-5 py-2 rounded-xl border border-slate-200 text-xs font-black tracking-widest transition-all text-slate-500 hover:border-indigo-400" data-main="{main}">{main}</button>
            '''

    # 4. 生成完整網頁 (修正了 JS 模板字串轉義，並升級粒子網路)
    full_html = f'''
    <!DOCTYPE html>
    <html lang="zh-Hant">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Johnathan's Teaching Hub</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            #bg-canvas {{ position: fixed; top: 0; left: 0; z-index: -1; width: 100%; height: 100%; background: #f8fafc; pointer-events: none; }}
            .lesson-card {{ transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }}
            .filter-btn.active {{ background-color: #4f46e5; color: white; border-color: #4f46e5; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3); }}
            .glass-effect {{ background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.5); box-shadow: 0 10px 30px -10px rgba(0,0,0,0.05); }}
            .card-glow:hover {{ box-shadow: 0 20px 40px -15px rgba(79, 70, 229, 0.25); border-color: rgba(79, 70, 229, 0.2); }}
        </style>
    </head>
    <body class="min-h-screen text-slate-900 font-sans relative">
        <canvas id="bg-canvas"></canvas>

        <div class="max-w-7xl mx-auto px-4 py-12 relative z-10">
            <header class="mb-12 border-b border-slate-200/60 pb-8 flex flex-col lg:flex-row justify-between items-start lg:items-end gap-6">
                <div>
                    <h1 class="text-4xl font-black tracking-tighter text-slate-900 mb-2 italic">JOHNATHAN'S LAB</h1>
                    <p class="text-slate-500 font-medium border-l-4 border-indigo-500 pl-4 uppercase text-xs tracking-widest">Interactive Learning Resources Portfolio</p>
                </div>
                <div class="flex flex-col items-end">
                    <div class="text-[10px] text-slate-400 font-mono flex items-center bg-white/80 backdrop-blur-md px-4 py-2 rounded-full border border-slate-200/50 shadow-sm">
                        <span class="inline-block w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse shadow-[0_0_8px_rgba(34,197,94,0.6)]"></span>
                        SYNCED: {update_time} (HKT)
                    </div>
                </div>
            </header>

            <div class="sticky top-6 z-30 glass-effect p-4 rounded-2xl mb-10">
                <div class="flex flex-col md:flex-row gap-6 items-center justify-between">
                    <div id="filter-container" class="flex flex-wrap gap-3">
                        <button onclick="filterBy('ALL', 'ALL')" class="filter-btn active px-5 py-2 rounded-xl border border-slate-200 text-xs font-black tracking-widest transition-all" data-main="ALL">ALL</button>
                        {nav_html}
                    </div>
                    <div class="relative w-full md:w-64">
                        <i class="fas fa-search absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 text-xs"></i>
                        <input type="text" id="search-input" placeholder="Search lessons..." oninput="handleSearch()"
                               class="w-full pl-10 pr-4 py-2 bg-white/80 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-indigo-500/15 focus:border-indigo-400 transition-all text-xs font-bold shadow-sm">
                    </div>
                </div>
            </div>

            <div id="lessons-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"></div>
            
            <div id="empty-state" class="hidden text-center py-32">
                <div class="text-6xl mb-6 opacity-20">🛰️</div>
                <h3 class="text-xl font-bold text-slate-400 italic font-mono uppercase">Target Not Found</h3>
            </div>
            
            <footer class="mt-24 pt-8 border-t border-slate-200/60 text-center text-slate-400 text-[10px] font-bold uppercase tracking-[0.4em]">
                Johnathan-LH Lab • Automated Deployment System
            </footer>
        </div>

        <script>
            // --- 高級互動粒子網路系統 ---
            const canvas = document.getElementById('bg-canvas');
            const ctx = canvas.getContext('2d');
            let particles = [];
            
            // 滑鼠位置物件
            const mouse = {{ x: null, y: null, radius: 180 }};

            // 監聽滑鼠移動與離開
            window.addEventListener('mousemove', (e) => {{
                mouse.x = e.x;
                mouse.y = e.y;
            }});
            window.addEventListener('mouseout', () => {{
                mouse.x = null;
                mouse.y = null;
            }});

            class Particle {{
                constructor() {{
                    this.x = Math.random() * canvas.width;
                    this.y = Math.random() * canvas.height;
                    this.size = Math.random() * 2 + 1; // 粒子大小
                    this.speedX = (Math.random() - 0.5) * 1.2; // 緩慢漂浮
                    this.speedY = (Math.random() - 0.5) * 1.2;
                }}
                draw() {{
                    ctx.fillStyle = 'rgba(79, 70, 229, 0.5)'; // 靛藍色粒子
                    ctx.beginPath();
                    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                    ctx.closePath();
                    ctx.fill();
                }}
                update() {{
                    this.x += this.speedX;
                    this.y += this.speedY;
                    
                    // 邊界反彈
                    if (this.x > canvas.width || this.x < 0) this.speedX *= -1;
                    if (this.y > canvas.height || this.y < 0) this.speedY *= -1;
                }}
            }}

            function init() {{
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
                particles = [];
                // 根據螢幕寬度決定粒子數量，避免手機卡頓
                let numberOfParticles = Math.floor((canvas.width * canvas.height) / 15000);
                if(numberOfParticles > 100) numberOfParticles = 100; 

                for (let i = 0; i < numberOfParticles; i++) {{
                    particles.push(new Particle());
                }}
            }}

            function animate() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                
                for (let i = 0; i < particles.length; i++) {{
                    particles[i].update();
                    particles[i].draw();

                    // 1. 粒子與粒子之間的連線 (網路效果)
                    for (let j = i; j < particles.length; j++) {{
                        let dx = particles[i].x - particles[j].x;
                        let dy = particles[i].y - particles[j].y;
                        let distance = Math.sqrt(dx * dx + dy * dy);
                        
                        // 當粒子靠近時連線
                        if (distance < 120) {{
                            ctx.beginPath();
                            ctx.strokeStyle = `rgba(148, 163, 184, ${{0.2 - distance/600}})`; // 灰色淡線
                            ctx.lineWidth = 0.5;
                            ctx.moveTo(particles[i].x, particles[i].y);
                            ctx.lineTo(particles[j].x, particles[j].y);
                            ctx.stroke();
                        }}
                    }}

                    // 2. 粒子與鼠標之間的連線 (引力效果)
                    if (mouse.x != null && mouse.y != null) {{
                        let dxMouse = mouse.x - particles[i].x;
                        let dyMouse = mouse.y - particles[i].y;
                        let distMouse = Math.sqrt(dxMouse * dxMouse + dyMouse * dyMouse);
                        
                        if (distMouse < mouse.radius) {{
                            ctx.beginPath();
                            ctx.strokeStyle = `rgba(79, 70, 229, ${{0.6 - distMouse/mouse.radius}})`; // 靛藍色強化線
                            ctx.lineWidth = 1;
                            ctx.moveTo(particles[i].x, particles[i].y);
                            ctx.lineTo(mouse.x, mouse.y);
                            ctx.stroke();
                        }}
                    }}
                }}
                requestAnimationFrame(animate);
            }}

            window.addEventListener('resize', init);
            init();
            animate();

            // --- 課件資料與渲染邏輯 ---
            const lessons = {lessons_json};
            let currentMain = 'ALL';
            let currentSub = 'ALL';
            let searchQuery = '';

            function render() {{
                const grid = document.getElementById('lessons-grid');
                const empty = document.getElementById('empty-state');
                grid.innerHTML = '';
                
                const filtered = lessons.filter(l => {{
                    const matchMain = currentMain === 'ALL' || l.subject === currentMain;
                    const matchSub = currentSub === 'ALL' || l.sub === currentSub;
                    const matchSearch = l.title.toLowerCase().includes(searchQuery) || l.path.toLowerCase().includes(searchQuery);
                    return matchMain && matchSub && matchSearch;
                }});

                if (filtered.length === 0) {{
                    empty.classList.remove('hidden');
                }} else {{
                    empty.classList.add('hidden');
                    filtered.forEach(l => {{
                        // 注意：這裡已經修復了變數轉義問題！
                        grid.innerHTML += `
                            <div class="lesson-card glass-effect p-7 rounded-3xl card-glow transition-all flex flex-col justify-between group bg-white/60">
                                <div>
                                    <div class="flex justify-between items-start mb-6">
                                        <div class="flex gap-2">
                                            <span class="px-2 py-0.5 bg-slate-800 text-white text-[9px] font-black uppercase rounded tracking-widest group-hover:bg-indigo-600 transition-colors">${{l.subject}}</span>
                                            <span class="px-2 py-0.5 bg-white border border-slate-200 text-slate-500 text-[9px] font-black uppercase rounded tracking-widest">${{l.sub}}</span>
                                        </div>
                                        <i class="fas fa-external-link-alt text-slate-300 text-[10px] group-hover:text-indigo-400 transition-colors"></i>
                                    </div>
                                    <h3 class="text-xl font-black text-slate-800 mb-2 leading-tight tracking-tight">${{l.title}}</h3>
                                    <p class="text-[10px] text-slate-500 font-mono truncate mb-6 opacity-70">${{l.path}}</p>
                                </div>
                                <a href="${{l.url}}" target="_blank" rel="noopener noreferrer" class="w-full text-center py-4 bg-white hover:bg-indigo-600 hover:text-white text-indigo-600 font-black rounded-2xl transition-all text-[10px] tracking-[0.2em] shadow-sm border border-indigo-100 group-hover:border-transparent">
                                    LAUNCH LESSON
                                </a>
                            </div>
                        `;
                    }});
                }}
            }}

            function filterBy(main, sub) {{
                currentMain = main;
                currentSub = sub;
                document.querySelectorAll('.filter-btn').forEach(btn => {{
                    btn.classList.toggle('active', btn.dataset.main === main);
                }});
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