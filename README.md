# 📚 Wikipedia Vital Articles Archiver

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg) ![License](https://img.shields.io/badge/License-CC%20BY--SA%203.0-lightgrey.svg) ![Status](https://img.shields.io/badge/Status-Automated-green.svg)

<p align="center">
  <img src="restart.png" alt="Restart Society">
</p>
An automated tool designed to monitor, download, and compress the 100 **Level 2 Vital Articles** from Wikipedia. Optimized for **PythonAnywhere**, this script ensures you always have the latest version of humanity's most essential knowledge while respecting storage limits and API etiquette.

---

## 🛠️ Technical Overview

The script automates a 4-step workflow to maintain a local archive:

1.  **🔍 Scrape**: Parses the [Wikipedia Vital Level 2](https://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Level/2) page to identify the 100 essential articles.
2.  **⚖️ Compare**: Checks the **ETag** (unique version identifier) of each article against a local log to see if it has been edited since the last run.
3.  **📥 Fetch**: Retrieves the full HTML content via the **Wikimedia REST API** only for the articles that have changed.
4.  **📦 Compress**: Bundles all newly updated articles into a timestamped `.zip` archive and wipes the temporary `.html` files to reclaim disk space.



---

## 🚀 Deployment Guide

### 1️⃣ Setup Environment
Ensure you have the necessary libraries installed on your PythonAnywhere account:
```bash
pip install requests beautifulsoup4
```

### 2️⃣ Configure Script
Before running, update these variables inside `vital_download.py`:
* **BASE_DIR**: Set this to your PythonAnywhere path (e.g., `/home/yourusername/vital_articles/`).
* **USER_AGENT**: Update with your contact email (a Wikipedia API requirement).

### 3️⃣ Schedule Daily Tasks
To automate this on **PythonAnywhere**:
1.  Navigate to the **Tasks** tab in your dashboard.
2.  Under **Scheduled Tasks**, set the frequency to **Weekly** and choose a time (e.g., `03:00`).
3.  Input the following command:
    `python3 /home/yourusername/vital_download.py`
4.  Click **Create**.

---

## 📂 File Structure

Once the script begins its daily cycles, your directory will be organized as follows:

```text
/vital_articles/
├── download_log.json             # 🔑 The 'memory' file (stores ETags)
├── vital_articles_2026-01-24.zip # 📦 Compressed snapshot of today's updates
├── vital_articles_2026-01-25.zip # 📦 Subsequent daily snapshots
└── vital_download.py             # 🐍 The main automation script
```

---

## ✨ Features & Optimizations

* **💾 Storage Savings**: HTML files are compressed using `ZIP_DEFLATED`, typically reducing total file size by **75–80%**.
* **📡 Bandwidth Efficient**: Uses conditional headers to ensure content is only downloaded if an update is detected.
* **🐢 Polite Scraping**: Includes a 0.1-second delay between requests to remain compliant with Wikipedia's bot policy.
* **🧹 Auto-Cleanup**: The script cleans its own workspace, ensuring no raw `.html` files linger outside of the ZIP archives.

---

## ⚠️ Important Notes

* **Log Integrity**: Do not delete `download_log.json`. If this file is lost, the script will re-download all 100 articles on its next run.
* **API Etiquette**: Keeping a valid email in the `USER_AGENT` is crucial for "Good Bot" status on Wikipedia.
* **Quota Management**: Periodically download old ZIPs to your local machine to stay under your PythonAnywhere storage quota.

---

## 📄 License
Content downloaded from Wikipedia is available under the [Creative Commons Attribution-ShareAlike License](https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License).
