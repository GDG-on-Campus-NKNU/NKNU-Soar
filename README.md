# NKNU-Soar

> 🚀 A powerful, modular LINE Bot backend designed to streamline campus services for NKNU students.
>
> **By Students, For Students.**

NKNU-Soar is the backend engine powering the Line bot for NKNU students — 高師校園小飛燕.

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)](#)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.117.1-009688?logo=fastapi&logoColor=white)](#)
[![LINE API](https://img.shields.io/badge/LINE_Messaging_API-SDK_v3-00B900?logo=line&logoColor=white)](#)

[![en readme](https://img.shields.io/badge/lang-en-red)](./README.md) [![zh-tw readme](https://img.shields.io/badge/lang-zh--tw-yellow)](./README_zhtw.md)

## Prerequisites

Before you begin, ensure you have the following:

- **Python 3.12** or higher
- A **LINE Developers Channel** (Messaging API)
    - You will need the `Channel Access Token` and `Channel Secret`.

## Environment Setup

Follow these steps to set up the development environment:

### 1. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 2. Generate Core Bindings

This project relies on **[NKNU-Core](https://github.com/GDG-on-Campus-NKNU/NKNU-Core)**, a shared C library. You must
run the bindings generator to download the latest
DLLs and generate the necessary Python bindings:

```bash
python bindings_generator.py
```

> **Note**: This script downloads `core.dll` and generates `soar/nknu_core/bindings.py`. The application will not run
> without this step.

### 3. Configuration

1. **Duplicate the config file**:
   The project comes with an example config. Rename it to `config.py` for actual use.
   ```bash
   # Rename example_config.py to config.py in the soar directory
   mv soar/example_config.py soar/config.py
   ```

2. **Set Environment Variables**:
   You need to export your LINE Bot credentials as environment variables.
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

## Project Structure

```
NKNU-Soar/
├── soar/
│   ├── modules/            # Core system modules (Database, Analytics, etc.)
│   ├── plugins/            # Feature plugins (Where you add new bot features)
│   ├── routes/             # FastAPI routes (Webhook endpoints)
│   ├── nknu_core/          # Auto-generated CFFI bindings for NKNU-Core
│   ├── config.py           # Application configuration (Git-ignored. DO NOT COMMIT THIS FILE)
│   ├── example_config.py   # Example configuration 
│   └── main.py             # Application entry point
├── bindings_generator.py   # Script to download and bind NKNU-Core
├── run.py                  # Startup script
└── requirements.txt        # Python dependencies
```

## Running the Project

Start the server using the run script:

```bash
python run.py
```

The server will start on `http://0.0.0.0:8000`. The LINE Webhook URL should be configured to point to
`YOUR_DOMAIN/callback`.

## Development Guidelines

NKNU-Soar uses a **plugin-based architecture**. Each feature is a self-contained
plugin in the `soar/plugins/` directory.

### Creating a New Plugin

To add a new feature, create a new folder in `soar/plugins/` and add a `main.py`. Use the provided event decorators to
handle user interactions.

**Example Structure:**

```
soar/plugins/my_feature/
└── main.py
```

**Code Example (Refer to `soar/plugins/hello_world` for full details):**

```python
from soar.core.plugin_event_manager import on_message, on_postback
from soar.models.event_wrapper.on_message_event import OnMessageEvent


# Handle text messages starting with "hello"
@on_message.add_handler(key="hello")
def say_hello(message_event: OnMessageEvent):
    # Get user input
    user_msg = message_event.get_split_user_message()

    # Reply to user
    message_event.add_text_message("Hello there!")
    message_event.submit_reply()
```

### Analytics Tracking

We provide a built-in **Analytics Decorator** to track feature usage automatically.

* **Usage**: Decorate your handler function with `@analytic("EVENT_NAME")`.

**Implementation Example:**

```python
from soar.modules.analytics.analytics import analytic
from soar.core.plugin_event_manager import on_message
from soar.models.event_wrapper.on_message_event import OnMessageEvent


@on_message.add_handler(key="check_schedule")
@analytic("schedule_query")  # <--- Tracks this event as "schedule_query" in the DB
def check_schedule_handler(message_event: OnMessageEvent):
    # Your logic here
    message_event.add_text_message("This is the schedule...")
    message_event.submit_reply()
```

When `check_schedule_handler` is called, the system will automatically log an entry for `schedule_query` in the
analytics database.
