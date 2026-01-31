# NKNU-Soar

> 🚀 一個專為高師大學生設計的強大、模組化 LINE Bot 後端系統，旨在簡化校園服務。
>
> **由學生打造，為學生服務。**

NKNU-Soar 是驅動高師大學生 LINE Bot —— **高師小飛雁** 的後端引擎。

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)](#)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.117.1-009688?logo=fastapi&logoColor=white)](#)
[![LINE API](https://img.shields.io/badge/LINE_Messaging_API-SDK_v3-00B900?logo=line&logoColor=white)](#)

[![en readme](https://img.shields.io/badge/lang-en-red)](./README.md) [![zh-tw readme](https://img.shields.io/badge/lang-zh--tw-yellow)](./README_zhtw.md)

## 前置需求

在開始之前，請確保您具備以下條件：

- **Python 3.12** 或更高版本
- 一個 **LINE Developers Channel** (Messaging API)
    - 您將需要 `Channel Access Token` 和 `Channel Secret`。

## 環境設定

請按照以下步驟設置開發環境：

### 1. 安裝依賴套件

使用 `pip` 安裝所需的 Python 套件：

```bash
pip install -r requirements.txt
```

### 2. 生成核心綁定 (Core Bindings)

本專案依賴 **[NKNU-Core](https://github.com/GDG-on-Campus-NKNU/NKNU-Core)**，這是一個共享的 C 語言函式庫。您必須執行綁定生成器來下載最新的
DLL 並生成必要的 Python 綁定：

```bash
python bindings_generator.py
```

> **注意**：此腳本會下載 `core.dll` 並生成 `soar/nknu_core/bindings.py`。若未執行此步驟，應用程式將無法運作。

### 3. 設定配置

1. **複製設定檔**：
   專案附帶了一個範例設定檔。請將其重新命名為 `config.py` 以供實際使用。
   ```bash
   # 將 soar 目錄下的 example_config.py 重新命名為 config.py
   mv soar/example_config.py soar/config.py
   ```

2. **設定環境變數**：
   您需要將 LINE Bot 的憑證匯出為環境變數。
    * **Windows (PowerShell)**:
      ```powershell
      $env:CHANNEL_ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
      $env:CHANNEL_SECRET = "YOUR_CHANNEL_SECRET"
      ```
    * **Linux/Mac**:
      ```bash
      export CHANNEL_ACCESS_TOKEN="YOUR_ACCESS_TOKEN"
      export CHANNEL_SECRET="YOUR_CHANNEL_SECRET"
      ```

## 專案結構

```
NKNU-Soar/
├── soar/
│   ├── modules/            # 核心系統模組 (資料庫, 分析等)
│   ├── plugins/            # 功能插件 (您可以在此新增 Bot 功能)
│   ├── routes/             # FastAPI 路由 (Webhook 端點)
│   ├── nknu_core/          # 自動生成的 NKNU-Core CFFI 綁定
│   ├── config.py           # 應用程式設定 (Git 忽略 不要上傳到GitHub)
│   ├── example_config.py   # 範例設定檔 
│   └── main.py             # 應用程式進入點
├── bindings_generator.py   # 用於下載並綁定 NKNU-Core 的腳本
├── run.py                  # 啟動腳本
└── requirements.txt        # Python 依賴清單
```

## 啟動專案

使用 run 腳本啟動伺服器：

```bash
python run.py
```

伺服器將在 `http://0.0.0.0:8000` 上啟動。LINE Webhook URL 應設定為指向 `YOUR_DOMAIN/callback`。

## 開發指南

NKNU-Soar 使用 **插件式架構 (plugin-based architecture)**。每個功能都是 `soar/plugins/`
目錄下一個獨立的插件。

### 建立新插件

要新增功能，請在 `soar/plugins/` 中建立一個新資料夾並新增 `main.py`。使用提供的事件裝飾器 (decorators) 來處理使用者互動。

**範例結構：**

```
soar/plugins/my_feature/
└── main.py
```

**程式碼範例 (完整細節請參考 `soar/plugins/hello_world`)：**

```python
from soar.core.plugin_event_manager import on_message
from soar.models.event_wrapper.on_message_event import OnMessageEvent


# 處理開頭為 "hello" 的文字訊息
@on_message.add_handler(key="hello")
def say_hello(message_event: OnMessageEvent):
    # 取得使用者輸入
    user_msg = message_event.get_split_user_message()

    # 回覆使用者
    message_event.add_text_message("Hello there!")
    message_event.submit_reply()
```

### 數據追蹤 (Analytics Tracking)

我們提供內建的 **Analytics Decorator** 來自動追蹤功能使用情況。

* **目的**：記錄特定功能或處理程序被觸發的頻率。
* **用法**：使用 `@analytic("EVENT_NAME")` 裝飾您的處理函式。

**實作範例：**

```python
from soar.modules.analytics.analytics import analytic
from soar.core.plugin_event_manager import on_message
from soar.models.event_wrapper.on_message_event import OnMessageEvent


@on_message.add_handler(key="check_schedule")
@analytic("schedule_query")  # <--- 在資料庫中將此事件追蹤為 "schedule_query"
def check_schedule_handler(message_event: OnMessageEvent):
    # 您的邏輯程式碼
    message_event.add_text_message("This is the schedule...")
    message_event.submit_reply()
```

當 `check_schedule_handler` 被呼叫時，系統將自動在分析資料庫中記錄一筆 `schedule_query`。
