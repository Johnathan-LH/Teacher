import os
from bs4 import BeautifulSoup

def generate():
    # 存放分類後的課件數據
    categories = {}
    
    # 遍歷整個倉庫
    for root, dirs, files in os.walk('.'):
        # 排除隱藏文件夾
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            # 只處理子文件夾中的 html，且排除 index.html 本身
            if file.endswith('.html') and file != 'index.html':
                file_path = os.path.join(root, file)
                # 移除路徑開頭的 './'
                display_path = file_path.replace('./', '').replace('\\', '/')
                
                # 獲取分類名稱
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

    # 生成 HTML
    sections_html = ""
    for cat, items in sorted(categories.items()):
        # 關鍵修改：加入 target="_blank" 和 rel="noopener noreferrer"
        items_html = "".join([
            f'''
            <a href="{item['url']}" target="_blank" rel="noopener noreferrer" class="group p-4 bg-white border border-gray-200 rounded-lg shadow-sm hover:border-blue-500 hover:shadow-md transition-all text-left">
                <div class="text-blue-600 font-medium group-hover:text-blue-700 flex justify-between items-center">
                    <span>{item['title']}</span>
                    <i class="fas fa-external-link-alt text-xs text-gray-300 group-hover:text-blue-400"></i>
                </div>
                <div class="text-xs text-gray-400 mt-1">{item['url']}</div>
            </a>
            ''' for item in items
        ])
        
        sections_html += f'''
        <section class="mb-10">
            <h2 class="text-xl font-bold text-gray-700 mb-4 flex items-center">
                <span class="bg-blue-600 w-2 h-6 rounded mr-3"></span>
                {cat.replace('/', ' / ')}
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
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
        <title>Johnathan 的課件門戶</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    </head>
    <body class="bg-gray-50 min-h-screen p-8">
        <div class="max-w-6xl mx-auto">
            <header class="mb-12 border-b pb-6 flex justify-between items-end">
                <div>
                    <h1 class="text-3xl font-bold text-gray-900">Johnathan's Teaching Resources</h1>
                    <p class="text-gray-500 mt-2">自動識別目錄結構：科目 / 單元 / 課件</p>
                </div>
                <div class="text-xs text-gray-400">所有鏈接將在新分頁開啟</div>
            </header>
            {sections_html if sections_html else "<p class='text-gray-400 italic'>尚未偵測到任何 HTML 課件...</p>"}
        </div>
    </body>
    </html>
    '''
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(full_html)

if __name__ == "__main__":
    generate()
