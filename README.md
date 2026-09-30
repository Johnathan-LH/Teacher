# 數學及 ICT 課件庫

> 使用 AI 助手維護本網站？請讓它先讀 [AGENTS.md](AGENTS.md)。所有改動記錄在 [CHANGELOG.md](CHANGELOG.md)。

網站：https://johnathan-lh.github.io/Teacher/

## 資料夾結構

```
Math/F1/  數學中一課件
ICT/F1/   ICT 中一課件
ICT/F4/   ICT 中四課件
index.html  課件目錄（Google Sites 嵌入這一頁）
```

新年級就新開資料夾，例如 `Math/F2/`。

## 加新課件

1. 把 HTML 上載到對應資料夾，例如 `Math/F2/畢氏定理.html`。
2. 在 Google 試算表「課件清單」加一行：科目、年級、課題、課件名稱，
   「連結」只需填檔案路徑，例如 `Math/F2/畢氏定理.html`。
3. 等幾分鐘，重新整理網站就會看到新課件。

## 試算表欄名（第一行不要改）

科目 | 年級 | 課題 | 課件名稱 | 連結 | 簡介 | 標籤

- 只填了課題、未填課件名稱的行，會顯示為「課件準備中」。
- 標籤可用逗號分隔，例如 `互動,練習`。
- 「連結」也可以填完整網址（https://…），用來放其他網站的課件。

## 改網站設定

打開 `index.html`，在 `CONFIG` 裡可以改學校名稱、標題、試算表連結和科目次序。
