# Narrative Pipeline

[English README](README.md)

Narrative Pipeline 是一個給人類與 AI 協作長篇敘事寫作用的輕量 repo。它把流程拆得很清楚：先整理故事素材，再撰寫 `Narrative Spec`，接著逐場生成內容，最後做 critique 與 revision。

它不是一鍵生文玩具，而是一套可控、可追蹤、適合長篇創作的工作流程。

## 四層流程
1. Development：整理 premise、角色、世界觀與大綱。
2. Generation：一次只寫一場。
3. Critique：檢查結構、節奏、邏輯、角色一致性與語氣漂移。
4. Human Decision Layer：由人決定採用、退回、重寫與整體品味。

## 最簡單的開始方式
如果你是 Windows 使用者，直接在 repo 根目錄執行：

```bat
start.bat
```

它會自動幫你建立 `.venv` 並安裝本地 CLI。

建立第一個專案：

```bat
start.bat init my_story
start.bat status projects\my_story
```

## 手動安裝
如果你想自己控制環境，可以手動建立虛擬環境並安裝：

### Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## 新手建議流程
1. 執行 `narrative-pipeline init <名稱>` 建立 `projects/<名稱>/`。
2. 執行 `narrative-pipeline status <專案路徑>`，先看哪些檔案還是 placeholder。
3. 先填完這三個檔案：
   `00_brief/premise.md`
   `01_development/characters.yaml`
   `03_outline/outline.md`
4. 執行 `narrative-pipeline build-spec <專案路徑>`，確認已經可撰寫 spec。
5. 用 `prompts/spec/spec_generator.md` 完成 `02_spec/narrative_spec.md`。
6. 執行 `narrative-pipeline scene <專案路徑> --episode N --scene M` 建立場景檔。
7. 執行 `narrative-pipeline critique <專案路徑>` 建立整合 critique 報告。

## 常用指令
- `init`：建立新專案骨架與起始檔。
- `status`：顯示哪些檔案還缺、仍是 placeholder、或已完成。
- `build-spec`：確認 premise、角色與 outline 是否已經可供 spec 撰寫。
- `scene`：建立指定集數與場次的場景檔。
- `critique`：建立 critique 報告 placeholder。

## 專案結構
```text
projects/my_story/
|-- 00_brief/
|-- 01_development/
|-- 02_spec/
|-- 03_outline/
|-- 04_scenes/
|-- 05_critiques/
|-- 06_revisions/
`-- 07_exports/
```

## 命名決策
這個 repo 不使用 `Canon` 當系統名稱。規則文件統一稱為 `Narrative Spec`，主檔名是 `narrative_spec.md`。
