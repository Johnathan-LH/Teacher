import os
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

def generate():
    categories = {}
    
    # 遍歷整個倉庫
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.html') and file != 'index.html':
                file_path = os.path.join(root, file)
                display_path = file_path.replace('./', '').replace('\\', '/')
                category = os.path.dirname(display_path) or "根目錄"
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        soup = BeautifulSoup(f, 'html.parser')
                        title = soup.title.string if soup.title else file
                except:
                    title = file

                if category not in categories:
                    categories[category] = []
                categories[category].append({"title": title, "url": display_path})

    # 獲取香港時間用於除錯
    hk_tz = pytz.timezone('Asia/Hong_Kong')
    update_time = datetime.now(hk_tz).strftime('%Y-%m-%d %H:%M:%S')

    sections_html = ""
    for cat, items in sorted(categories.items()):
        # 確保 target="_blank" 寫在 href 旁邊
        items_html = "".join([
            f'''
            <a href="{item['url']}" target="_blank" rel="noopener noreferrer" class="group p-5 bg-white border border-gray-200 rounded-xl shadow-sm hover:border-blue-500 hover:shadow-md transition-all flex flex-col justify-between">
                <div>
                    <div class="text-blue-600 font-bold group-hover:text-blue-700 flex justify-between items-center mb-2">
                        <span class="text-lg">{item['title']}</span>
                        <i class="fas fa-external-link-alt text-xs opacity-30 group-hover:opacity-100"></i>
                    </div>
                    <p class="text-xs text-gray-400 font-mono break-all">{item['url']}</p>
                </div>
                <div class="mt-4 text-[10px] text-blue-400 font-semibold uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-opacity">
                    Open in new tab →
                </div>
            </a>
            ''' for item in items
        ])
        
        sections_html += f'''
        <section class="mb-12">
            <h2 class="text-xl font-black text-gray-800 mb-5 flex items-center">
                <span class="bg-blue-600 w-1.5 h-6 rounded-full mr-3"></span>
                {cat.replace('/', ' / ').upper()}
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {items_html}
            </div>
        </section>
        '''

    full_html = f'''
    <!DOCTYPE html>
    <html lang="zh-Hant">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Johnathan's Teaching Hub</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    </head>
    <body class="bg-slate-50 min-h-screen p-6 md:p-12 text-slate-900">
        <div class="max-w-6xl mx-auto">
            <header class="mb-16 border-b border-slate-200 pb-8 flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
                <div>
                    <h1 class="text-4xl font-black tracking-tight text-slate-900">Johnathan's Resources</h1>
                    <p class="text-slate-500 mt-2 font-medium">ICT & Mathematics Interactive Courseware</p>
                </div>
                <div class="text-right">
                    <div class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">系統狀態</div>
                    <div class="text-xs text-green-600 font-mono mt-1 flex items-center justify-end">
                        <span class="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></span>
                        最後自動更新: {update_time} (HKT)
                    </div>
                </div>
            </header>
            
            <div class="space-y-4">
                {sections_html if sections_html else "<div class='text-center py-20 text-slate-400 italic'>偵測中... 請確認倉庫內已有 HTML 檔案。</div>"}
            </div>

            <footer class="mt-20 pt-8 border-t border-slate-200 text-center text-slate-400 text-xs">
                <p>© 2026 Johnathan-LH. 所有的教學資源連結均預設在新分頁開啟。</p>
            </div>
        </div>
    </body>
    </html>
    '''
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(full_html)

if __name__ == "__main__":
    generate()
