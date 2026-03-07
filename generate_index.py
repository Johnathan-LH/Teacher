import os
from bs4 import BeautifulSoup

def generate():
    lessons = []
    # 掃描根目錄下所有的 html 檔案
    for file in os.listdir('.'):
        if file.endswith('.html') and file != 'index.html':
            with open(file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                # 取得檔案的 <title>，若無則使用檔名
                title = soup.title.string if soup.title else file
                lessons.append({"title": title, "url": file})

    # 生成 HTML 內容（這裡使用你之前的網頁模板）
    html_template = f"""
    <!DOCTYPE html>
    <html lang="zh-Hant">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Johnathan 的課件庫</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50 p-10">
        <h1 class="text-3xl font-bold mb-8">📚 自動更新的課件目錄</h1>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            {''.join([f'<a href="{l["url"]}" class="p-6 bg-white shadow rounded-xl hover:bg-blue-50 transition">{l["title"]}</a>' for l in lessons])}
        </div>
    </body>
    </html>
    """
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)

if __name__ == "__main__":
    generate()
