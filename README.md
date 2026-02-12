# 📚 Restart  Society: Wikipedia Vital Articles Archiver 

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg) ![Articles](https://img.shields.io/badge/Articles-1000-orange.svg) ![Status](https://img.shields.io/badge/Status-Automated-green.svg)

An automated tool designed to monitor, download, and compress the **1,000 Level 3 Vital Articles** from Wikipedia. This collection represents the core foundation of human knowledge. Optimized for **PythonAnywhere**, this script balances archival depth with storage efficiency.

## Table of Contents

- [Technical Overview](technical-overview)

- [🚀 Deployment Guide](deployment-guide)

- [1️⃣ Setup Environment](setup-environment)

- [2️⃣ Configure Script](configure-script)

- [3️⃣ Schedule](schedule)

- [📂 File Structure](file-structure)

- [🧪 Running Tests](running-tests)

- [✨ Safety & Efficiency](safety-efficiency)

- [📄 License](license)


<p align="center">
  <img src="restart.png" alt="Restarting Society" width="600">
</p>

---

## 🛠️ Technical Overview

The script automates a 4-step workflow:

1.  **🔍 Scrape**: Parses the [Wikipedia Vital Level 3](https://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Level/3) index.
2.  **⚖️ Compare**: Uses **ETags** to check if any of the 1,000 articles have changed since the last snapshot.
3.  **📥 Fetch**: Retrieves the full HTML via the **Wikimedia REST API** only for modified content.
4.  **📦 Compress**: Bundles all updates into a timestamped `.zip` archive to save disk space.

---

## 🚀 Deployment Guide

### 1️⃣ Setup Environment
```bash
pip install requests beautifulsoup4
```

### 2️⃣ Configure Script
Update these variables inside `vital_download.py`:
* **BASE_DIR**: Your storage path (e.g., `/home/yourusername/vital_articles/`).
* **USER_AGENT**: Your email (required by Wikipedia's Bot Policy).
* **MAX_DISK_USAGE_MB**: Set to `450` to stay safely within PythonAnywhere's 512MB limit.

### 3️⃣ Schedule
Set this task to run **Weekly** or **Monthly** in the PythonAnywhere Tasks dashboard to manage CPU and storage quotas.

---

## 📂 File Structure

```text
/vital_articles/
├── download_log.json             # 🔑 ETag version history
├── vital_level3_2026-01-24.zip   # 📦 Compressed snapshot
└── vital_download.py             # 🐍 Automation script
```

## 🧪 Running Tests
This project includes a test suite to verify connectivity, scraping logic, and compression without exhausting your Wikipedia API limits or disk space.

To run the tests:
```bash
python3 test.py
```
*The test script uses `unittest` and `mock` to simulate Wikipedia responses, ensuring your logic is solid before you start a massive 1,000-article download.*

---

## ✨ Safety & Efficiency

* **💾 Disk Guard**: The script automatically checks disk usage and aborts if it exceeds 450MB to prevent account lockout.
* **📦 High Compression**: Uses `ZIP_DEFLATED` to shrink the 1,000-article library by ~80%.
* **🐢 Rate Limiting**: Employs a 0.1s sleep interval to respect Wikipedia's servers.

---

## 📄 License
Content is provided under the [Creative Commons Attribution-ShareAlike License](https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License).
