import os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json

def generate():
    all_lessons = []
    # 結構化分類：{ "ICT": {"F1": [], "F3": []}, "MATH": {...} }
    hierarchy = {}
    
    # 1. 掃描所有目錄
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.html') and file != 'index.html':
                file_path = os.path.join(root, file)
                display_path = file_path.replace('./', '').replace('\\', '/')
                
                # 獲取路徑層級
                path_parts = display_path.split('/')
                
                # 預設分類
                main_subject = "其他"
                sub_category = "全部"
                
                if len(path_parts) > 2:
                    # 例如 Math/F1/test.html -> Math, F1
                    main_subject = path_parts[0].upper()
                    sub_category = path_parts[1].upper()
                elif len(path_parts) == 2:
                    # 例如 Math/test.html -> Math, 全部
                    main_subject = path_parts[0].upper()
                
                # 提取標題
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
                
                # 建立層級索引
                if main_subject not in hierarchy:
                    hierarchy[main_subject] = set()
                hierarchy[main_subject].add(sub_category)

    # 2. 計算時間
    now_utc = datetime.utcnow()
    now_hkt = now_utc + timedelta(hours=8)
    update_time = now_hkt.strftime('%Y-%m-%d %H:%M:%S')

    # 3. 準備 JSON 與選單 HTML
    lessons_json = json.dumps(all_lessons)
    
    # 生成下拉選單的 HTML 結構
    nav_html = ""
    sorted_main = sorted(hierarchy.keys())
    for main in sorted_main:
        subs = sorted(list(hierarchy[main]))
        
        # 如果該科目有子目錄，則生成下拉選單
        if len(subs) > 1 or (len(subs) == 1 and subs[0] != "全部"):
            sub_items = "".join([
                f'<button onclick="filterBy(\'{main}\', \'{s}\')" class="block w-full text-left px-4 py-2 text-[10px] font-bold text-slate-600 hover:bg-blue-50 hover:text-blue-600 transition-colors uppercase tracking-widest">{s}</button>'
                for s in subs
            ])
            
            nav_html += f'''
            <div class="relative group">
                <button onclick="filterBy('{main}', 'ALL')" class="filter-btn px-5 py-2 rounded-xl border border-slate-200 text-xs font-black tracking-widest transition-all text-slate-500 hover:border-blue-400 flex items-center gap-2" data-main="{main}">
                    {main} <i class="fas fa-chevron-down text-[8px] opacity-50 group-hover:rotate-180 transition-transform"></i>
                </button>
                <div class="absolute top-full left-0 mt-2 w-32 bg-white border border-slate-100 rounded-xl shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50 py-2 border-t-4 border-t-blue-500">
                    <button onclick="filterBy('{main}', 'ALL')" class="block w-full text-left px-4 py-2 text-[10px] font-black text-blue-600 border-b border-slate-50 mb-1 italic">VIEW ALL</button>
                    {sub_items}
                </div>
            </div>
            '''
        else:
            # 沒有子目錄，則顯示普通按鈕
            nav_html += f'''
            <button onclick="filterBy('{main}', 'ALL')" class="filter-btn px-5 py-2 rounded-xl border border-slate-200 text-xs font-black tracking-widest transition-all text-slate-500 hover:border-blue-400" data-main="{main}">{main}</button>
            '''

    # 4. 生成完整網頁
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
            .lesson-card {{ transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }}
            .filter-btn.active {{ background-color: #2563eb; color: white; border-color: #2563eb; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2); }}
            .glass-effect {{ background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(12px); }}
        </style>
    </head>
    <body class="bg-[#f8fafc] min-h-screen text-slate-900 font-sans">
        <div class="max-w-7xl mx-auto px-4 py-12">
            
            <header class="mb-12 border-b border-slate-200 pb-8 flex flex-col lg:flex-row justify-between items-start lg:items-end gap-6">
                <div>
                    <h1 class="text-4xl font-black tracking-tighter text-slate-900 mb-2 italic">JOHNATHAN'S LAB</h1>
                    <p class="text-slate-500 font-medium border-l-4 border-blue-500 pl-4 uppercase text-xs tracking-widest">Interactive Learning Resources Portfolio</p>
                </div>
                <div class="flex flex-col items-end">
                    <div class="text-[10px] text-slate-400 font-mono flex items-center bg-white px-3 py-1.5 rounded-full border border-slate-200 shadow-sm">
                        <span class="inline-block w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></span>
                        SYNCED: {update_time} (HKT)
                    </div>
                </div>
            </header>

            <!-- 導航列：下拉選單 -->
            <div class="sticky top-6 z-30 glass-effect p-4 rounded-2xl shadow-xl border border-white/50 mb-10">
                <div class="flex flex-col md:flex-row gap-6 items-center justify-between">
                    <div id="filter-container" class="flex flex-wrap gap-3">
                        <button onclick="filterBy('ALL', 'ALL')" class="filter-btn active px-5 py-2 rounded-xl border border-slate-200 text-xs font-black tracking-widest transition-all" data-main="ALL">ALL</button>
                        {nav_html}
                    </div>
                    
                    <div class="relative w-full md:w-64">
                        <i class="fas fa-search absolute left-4 top-1/2 -translate-y-1/2 text-slate-300 text-xs"></i>
                        <input type="text" id="search-input" placeholder="Search lessons..." oninput="handleSearch()"
                               class="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500 transition-all text-xs font-bold">
                    </div>
                </div>
            </div>

            <div id="lessons-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"></div>

            <div id="empty-state" class="hidden text-center py-32">
                <div class="text-6xl mb-6 opacity-20">🛰️</div>
                <h3 class="text-xl font-bold text-slate-400 italic font-mono uppercase">Target Not Found</h3>
            </div>

            <footer class="mt-24 pt-8 border-t border-slate-200 text-center text-slate-300 text-[10px] font-bold uppercase tracking-[0.4em]">
                Johnathan-LH Lab • Automated Deployment System
            </footer>
        </div>

        <script>
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
                        grid.innerHTML += `
                            <div class="lesson-card bg-white p-7 rounded-3xl border border-slate-100 shadow-sm hover:shadow-2xl hover:-translate-y-2 transition-all flex flex-col justify-between group">
                                <div>
                                    <div class="flex justify-between items-start mb-6">
                                        <div class="flex gap-2">
                                            <span class="px-2 py-0.5 bg-slate-900 text-white text-[8px] font-black uppercase rounded tracking-widest group-hover:bg-blue-600 transition-colors">${{l.subject}}</span>
                                            <span class="px-2 py-0.5 bg-slate-100 text-slate-500 text-[8px] font-black uppercase rounded tracking-widest">${{l.sub}}</span>
                                        </div>
                                        <i class="fas fa-external-link-alt text-slate-200 text-[10px]"></i>
                                    </div>
                                    <h3 class="text-xl font-black text-slate-800 mb-2 leading-tight tracking-tight">${{l.title}}</h3>
                                    <p class="text-[10px] text-slate-400 font-mono truncate mb-6 opacity-60">${{l.path}}</p>
                                </div>
                                <a href="${{l.url}}" target="_blank" rel="noopener noreferrer" class="w-full text-center py-4 bg-slate-50 hover:bg-blue-600 hover:text-white text-blue-600 font-black rounded-2xl transition-all text-[10px] tracking-[0.2em] shadow-inner hover:shadow-blue-500/30">
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
                
                // 更新按鈕樣式
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
