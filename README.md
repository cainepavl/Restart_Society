# 🕵️ Restart Society: Wikipedia Vital Articles Archiver

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg) ![Articles](https://img.shields.io/badge/Articles-1000-orange.svg) ![Status](https://img.shields.io/badge/Status-Automated-green.svg)

An automated tool designed to monitor, download, and compress the **1,000 Level 3 Vital Articles** from Wikipedia. This collection represents the core foundation of human knowledge. Optimized for **PythonAnywhere**, this script balances archival depth with storage efficiency.

<p align="center">
  <img src="restart.png" alt="Restarting Society" width="600">
</p>

---

## 📋 Table of Contents

- [How It Works](#how-it-works)
- [Installation](#installation)
- [WSL (Windows Subsystem for Linux)](#wsl-windows-subsystem-for-linux)
- [Configuration](#configuration)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Testing](#testing)
- [Safety & Efficiency](#safety--efficiency)
- [Disclaimer](#disclaimer)
- [License](#license)
- [Contact/Connect](#contactconnect)

---

## 🔍 How It Works

The script automates a 4-step workflow:

1. **🔍 Scrape**: Parses the [Wikipedia Vital Level 3](https://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Level/3) index to build a list of all 1,000 article titles.
2. **⚖️ Compare**: Uses **ETags** to check if any article has changed since the last snapshot — only modified content is re-downloaded.
3. **📥 Fetch**: Retrieves the full HTML via the **Wikimedia REST API** for each changed article.
4. **📦 Compress**: Bundles all updates into a timestamped `.zip` archive using `ZIP_DEFLATED` to save disk space.

---

## 🛠️ Installation

### 🐍 Verify Python

```bash
python3 --version
# Requires Python 3.x
```

### 📥 Clone the Repository

```bash
git clone https://github.com/cainepavl/Restart_Society.git
cd Restart_Society
```

### 📦 Virtual Environment

A virtual environment is optional but recommended for local runs. On **PythonAnywhere**, skip this step — install directly into your user environment instead.

```bash
python3 -m venv venv
source venv/bin/activate      # Linux / macOS / WSL
# venv\Scripts\activate       # Windows (native CMD)
```

### ⬇️ Install Dependencies

```bash
pip3 install requests beautifulsoup4
```

---

## 🐧 WSL (Windows Subsystem for Linux)

This script is pure CLI with no GUI, so there are **no display server requirements** — it runs in WSL without any extra setup.

**File paths**: Use Linux-style paths inside WSL (e.g. `/home/yourname/vital_articles/`). Avoid Windows-style paths (`C:\...`) — they will not resolve correctly inside the WSL environment.

**Scheduling locally in WSL**: If you are not using PythonAnywhere, you can schedule the script with cron inside WSL:

```bash
crontab -e
# Add a line like this to run every Sunday at 2am:
0 2 * * 0 /usr/bin/python3 /home/yourname/Restart_Society/vital_download.py >> /home/yourname/vital_articles/cron.log 2>&1
```

> **Note:** WSL 2 cron does not survive a Windows reboot by default. For persistent scheduling from Windows, use **Windows Task Scheduler** to launch `wsl python3 /path/to/vital_download.py` on a schedule, or simply use PythonAnywhere.

---

## ⚙️ Configuration

Open `vital_download.py` and update the three variables at the top of the file before your first run:

```python
# Where all output files are stored. Created automatically on first run.
# PythonAnywhere:  "/home/yourusername/vital_articles/"
# Local Linux/WSL: "/home/yourname/vital_articles/"
BASE_DIR = "/home/yourusername/vital_articles/"

# Required by Wikipedia's Bot Policy. Must be a real, working email address
# so Wikipedia can contact you if the script sends unexpected traffic.
# Format: "AppName/Version (contact@example.com)"
USER_AGENT = "VitalDownloader/1.0 (your_email@example.com)"

# Safety ceiling in megabytes. The script aborts if disk usage exceeds this.
# PythonAnywhere free tier: 512MB total — 450 leaves a safe buffer.
# Local use: raise this to match your available disk space.
MAX_DISK_USAGE_MB = 450
```

---

## 🚀 Usage

### Run Locally

```bash
python3 vital_download.py
```

On first run the script creates `BASE_DIR`, downloads all 1,000 articles (expect 10–20 minutes depending on your connection), and writes a `.zip` archive and a `download_log.json`. Subsequent runs only re-download articles whose ETags have changed.

### Schedule on PythonAnywhere

1. Log in to [PythonAnywhere](https://www.pythonanywhere.com/) and open the **Tasks** tab.
2. Click **Add a new scheduled task**.
3. Set the command to:
   ```
   python3 /home/yourusername/Restart_Society/vital_download.py
   ```
4. Set the interval to **Weekly** or **Monthly** — daily runs are unnecessary given Wikipedia's edit velocity and will eat into your CPU quota.

---

## 🗂️ File Structure

```text
Restart_Society/
├── vital_download.py             # 🐍 Main archiver script
├── test.py                       # 🧪 Unit test suite
└── restart.png                   # 🖼️  README image

/vital_articles/                  # Created by the script (BASE_DIR)
├── download_log.json             # 🔑 ETag version history — do not delete
├── vital_level3_2026-01-24.zip   # 📦 Compressed snapshot (date-stamped)
└── current_run/                  # 🗑️  Temp folder — auto-cleaned after zipping
```

---

## 🧪 Testing

The test suite mocks all network calls and filesystem I/O so no Wikipedia quota is consumed and no real files are written outside the test temp directory.

```bash
python3 test.py
# or
python3 -m unittest test -v
```

| Test | Coverage |
|---|---|
| `test_disk_space_pass` | Returns `True` when usage is within limit |
| `test_disk_space_fail` | Returns `False` when limit is exceeded |
| `test_get_article_list` | Parses titles correctly; filters out nav links and self-references |
| `test_download_article` | API response returns correct content and ETag |
| `test_zip_creation` | Files are bundled into `.zip` and deleted from temp dir after compression |

---

## ✨ Safety & Efficiency

- **💾 Disk Guard**: Checks disk usage before each run and aborts if `MAX_DISK_USAGE_MB` is exceeded — prevents account lockout on PythonAnywhere's free tier.
- **📦 High Compression**: Uses `ZIP_DEFLATED` to shrink the 1,000-article HTML library by ~80%.
- **⚖️ ETag Diffing**: Only re-downloads articles that have actually changed, keeping API load and bandwidth minimal.
- **🐢 Rate Limiting**: A 0.1s sleep between requests respects Wikipedia's servers and avoids triggering rate limits.

---

## 🔔 Disclaimer

This tool downloads article HTML from Wikipedia for **personal archival purposes only**. All Wikipedia content retrieved by this script is published under the [Creative Commons Attribution-ShareAlike 4.0 License (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/) — you must credit Wikipedia and share any derivatives under the same license. This project is not affiliated with or endorsed by the Wikimedia Foundation.

---

## 📄 License

This project's code is licensed under the MIT License. Wikipedia article content downloaded by the script is separately governed by CC BY-SA 4.0 — see the [Disclaimer](#disclaimer) above.

---

## 📩 Contact/Connect

**Caine Pavlosky**

* Email: [cainepavl@outlook.com](mailto:cainepavl@outlook.com)
* Portfolio: [fairdinkumstudios.com](https://fairdinkumstudios.com/)
* LinkedIn: [linkedin.com/in/cainepavlosky008](https://linkedin.com/in/cainepavlosky008)
