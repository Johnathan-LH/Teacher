import os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json

def generate():
    all_lessons = []
    subjects = set()
    
    # 1. 遞歸掃描倉庫內所有目錄
    for root, dirs, files in os.walk('.'):
        # 排除隱藏資料夾 (如 .git, .github)
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            # 只處理 HTML 檔案，且排除首頁本身
            if file.endswith('.html') and file != 'index.html':
                file_path = os.path.join(root, file)
                # 將路徑轉換為網頁可用的格式 (統一使用正斜線)
                display_path = file_path.replace('./', '').replace('\\', '/')
                
                # --- 核心邏輯：獲取完整的層級路徑作為分類 ---
                path_parts = display_path.split('/')
                if len(path_parts) > 1:
                    # 合併除了檔名以外的所有父文件夾名稱，例如 Math/F1/test.html -> "MATH / F1"
                    subject = " / ".join(path_parts[:-1]).upper()
                else:
                    subject = "根目錄"
                
                subjects.add(subject)
                
                # 嘗試提取 HTML 內的 <title> 標籤作為課件名稱
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        soup = BeautifulSoup(f, 'html.parser')
                        title = soup.title.string if soup.title else file
                except Exception:
                    title = file

                all_lessons.append({
                    "title": str(title).strip(),
                    "url": display_path,
                    "subject": subject,
                    "path": display_path
                })

    # 2. 手動計算香港時間 (HKT: UTC+8) 用於顯示系統狀態
    now_utc = datetime.utcnow()
    now_hkt = now_utc + timedelta(hours=8)
    update_time = now_hkt.strftime('%Y-%m-%d %H:%M:%S')

    # 3. 準備數據並生成 HTML
    subjects_sorted = sorted(list(subjects))
    lessons_json = json.dumps(all_lessons)

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
            .lesson-card {{ transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }}
            .filter-btn.active {{ background-color: #2563eb; color: white; border-color: #2563eb; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3); }}
            .glass-effect {{ background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); }}
            ::-webkit-scrollbar {{ width: 6px; }}
            ::-webkit-scrollbar-thumb {{ background: #cbd5e1; border-radius: 10px; }}
        </style>
    </head>
    <body class="bg-[#f8fafc] min-h-screen text-slate-900 font-sans">
        <div class="max-w-7xl mx-auto px-4 py-12">
            
            <!-- 頁頭部分 -->
            <header class="mb-12 border-b border-slate-200 pb-8 flex flex-col lg:flex-row justify-between items-start lg:items-end gap-6">
                <div>
                    <h1 class="text-4xl font-black tracking-tighter text-slate-900 mb-2 italic">JOHNATHAN'S LAB</h1>
                    <p class="text-slate-500 font-medium border-l-4 border-blue-500 pl-4">ICT & Mathematics Interactive Learning Hub</p>
                </div>
                <div class="flex flex-col items-end">
                    <div class="flex gap-4 mb-2">
                        <div class="text-center px-4 py-2 bg-white rounded-xl border border-slate-200 shadow-sm">
                            <div class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Total Lessons</div>
                            <div class="text-xl font-black text-blue-600">{len(all_lessons)}</div>
                        </div>
                    </div>
                    <div class="text-[10px] text-slate-400 font-mono flex items-center bg-white px-3 py-1.5 rounded-full border border-slate-200 shadow-sm">
                        <span class="inline-block w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></span>
                        LAST SYNC: {update_time} (HKT)
                    </div>
                </div>
            </header>

            <!-- 控制面板 (過濾器與搜尋) -->
            <div class="sticky top-6 z-30 glass-effect p-4 rounded-2xl shadow-xl border border-white/50 mb-10 flex flex-col gap-4">
                <div class="flex flex-col md:flex-row gap-4 items-center justify-between">
                    <div id="filter-container" class="flex flex-wrap gap-2">
                        <button onclick="filterBy('ALL')" class="filter-btn active px-4 py-1.5 rounded-lg border border-slate-200 text-[10px] font-black tracking-widest transition-all" data-subject="ALL">ALL</button>
                        {"".join([f'<button onclick="filterBy(\'{s}\')" class="filter-btn px-4 py-1.5 rounded-lg border border-slate-200 text-[10px] font-black tracking-widest transition-all text-slate-500 hover:border-blue-400" data-subject="{s}">{s}</button>' for s in subjects_sorted])}
                    </div>
                    
                    <div class="relative w-full md:w-72">
                        <i class="fas fa-search absolute left-4 top-1/2 -translate-y-1/2 text-slate-300 text-xs"></i>
                        <input type="text" id="search-input" placeholder="Search keywords..." oninput="handleSearch()"
                               class="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500 transition-all text-xs">
                    </div>
                </div>
            </div>

            <!-- 課件列表 -->
            <div id="lessons-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <!-- 由 JavaScript 動態生成 -->
            </div>

            <!-- 無內容提示 -->
            <div id="empty-state" class="hidden text-center py-32">
                <div class="text-6xl mb-6 opacity-20">🛰️</div>
                <h3 class="text-xl font-bold text-slate-800 italic">No courseware found matching your criteria.</h3>
            </div>

            <footer class="mt-24 pt-8 border-t border-slate-200 text-center text-slate-300 text-[10px] font-bold uppercase tracking-[0.4em]">
                Johnathan-LH Learning Hub • Automated CI/CD System
            </footer>
        </div>

        <script>
            const lessons = {lessons_json};
            let currentFilter = 'ALL';
            let searchQuery = '';

            function render() {{
                const grid = document.getElementById('lessons-grid');
                const empty = document.getElementById('empty-state');
                grid.innerHTML = '';
                
                const filtered = lessons.filter(l => {{
                    const matchFilter = currentFilter === 'ALL' || l.subject === currentFilter;
                    const matchSearch = l.title.toLowerCase().includes(searchQuery) || l.path.toLowerCase().includes(searchQuery);
                    return matchFilter && matchSearch;
                }});

                if (filtered.length === 0) {{
                    empty.classList.remove('hidden');
                }} else {{
                    empty.classList.add('hidden');
                    filtered.forEach(l => {{
                        grid.innerHTML += `
                            <div class="lesson-card bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-2xl hover:-translate-y-1.5 transition-all flex flex-col justify-between group">
                                <div>
                                    <div class="flex justify-between items-start mb-6">
                                        <span class="px-2 py-0.5 bg-slate-900 text-white text-[9px] font-black uppercase rounded tracking-widest italic group-hover:bg-blue-600 transition-colors">${{l.subject}}</span>
                                        <i class="fas fa-external-link-alt text-slate-200 text-[10px]"></i>
                                    </div>
                                    <h3 class="text-lg font-black text-slate-800 mb-2 leading-tight tracking-tight">${{l.title}}</h3>
                                    <p class="text-[10px] text-slate-400 font-mono truncate mb-6">${{l.path}}</p>
                                </div>
                                <a href="${{l.url}}" target="_blank" rel="noopener noreferrer" class="w-full text-center py-3 bg-slate-50 hover:bg-blue-600 hover:text-white text-blue-600 font-black rounded-xl transition-all text-[10px] tracking-[0.2em] shadow-inner hover:shadow-lg">
                                    LAUNCH LESSON
                                </a>
                            </div>
                        `;
                    }});
                }}
            }}

            function filterBy(subject) {{
                currentFilter = subject;
                document.querySelectorAll('.filter-btn').forEach(btn => {{
                    btn.classList.toggle('active', btn.dataset.subject === subject);
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
