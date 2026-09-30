# 更新記錄

最新的記錄放在最上方。格式及規則見 [AGENTS.md](AGENTS.md) 第 4 節。

## 2026-09-30
- 修改：`index.html` 加入 `<!DOCTYPE html>`、`lang`、`charset` 及 `viewport`，改善手機顯示（之前手機會顯示縮細的桌面版）。
- 修改：`index.html` 讀取試算表失敗時，改用瀏覽器內上次成功讀到的清單，並顯示「未能連線」提示。
- 修改：ICT 中一「避障車」（ICT/F1/避障車.html）預先把 JSX 轉成普通 JavaScript，移除 Babel，改用 React production 版本，加快開啟速度；內容不變。
- 修改：ICT 中四「電腦系統」（ICT/F4/cpu_trail_web.html）頁內對象由「中三」改為「中四」，與試算表一致。
- 修改：固定課件 CDN 版本（React 18.3.1、Vue 3.5.43 production 版、Tailwind 3.4.17），避免外部新版本令課件失效。
- 下架並刪除：數學 中一「坐標」— 坐標特工：幾何變換模擬器（Math/F1/坐標.html）；原因：教師認為效果不理想。
- 下架並刪除：數學 中三「三角學」— 三角學秘笈：恆等式與特殊角（Math/F3/SinCosTan.html）；原因：教師認為效果不理想。
- 修改：改用新的課件目錄頁 `index.html`，由 Google 試算表「課件清單」提供資料，按科目 → 年級 → 課題分類，明亮圓潤風格。
- 修改：Google Sites 改為「按網址嵌入」`https://johnathan-lh.github.io/Teacher/`。
- 刪除：舊的自動目錄產生器 `generate_index.py` 及 `.github/workflows/auto-update.yml`。
- 移動：`ICT/cpu_trail_web.html` → `ICT/F4/cpu_trail_web.html`。
- 新增：`README.md`、`AGENTS.md`、`CLAUDE.md`、`CHANGELOG.md`。
- 上架（整理現有課件到試算表）：
  - 數學 中一「坐標」— 坐標特工：幾何變換模擬器（Math/F1/坐標.html）
  - 數學 中一「百分數」— 百分數變化 統一視覺化演示（Math/F1/百分數.html）
  - 數學 中三「三角學」— 三角學秘笈：恆等式與特殊角（Math/F3/SinCosTan.html）
  - ICT 中一「避障車」— ICT 實作：避障小車任務控制中心（ICT/F1/避障車.html）
  - ICT 中四「電腦系統」— ICT 基礎測試：CPU 指令週期（ICT/F4/cpu_trail_web.html）
  - 數學 中二「直線」— 三角形的外角（未有連結，顯示「未上載」）
