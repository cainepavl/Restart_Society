# 📚 Restart  Society: Wikipedia Vital Articles Archiver 

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg) ![Articles](https://img.shields.io/badge/Articles-1000-orange.svg) ![Status](https://img.shields.io/badge/Status-Automated-green.svg)![Security](https://img.shields.io/badge/Security-DKIM-blue.svg)

An automated tool designed to monitor, download, and compress the **1,000 Level 3 Vital Articles** from Wikipedia. This collection represents the core foundation of human knowledge. Optimized for **PythonAnywhere**, this script balances archival depth with storage efficiency.

<p align="center">
  <img src="restart.png" alt="Restarting Society" width="600">
</p>

---


## 🛠️ Module 1: Wikipedia Vital Archiver (Level 3)

Automated system to monitor, download, and compress the 1,000 most essential articles from Wikipedia. Optimized for **PythonAnywhere** to balance archival depth with storage efficiency.

### 🔄 The Workflow
1.  **🔍 Scrape**: Parses the [Wikipedia Vital Level 3](https://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Level/3) index.
2.  **⚖️ Compare**: Uses **ETags** to download only articles that have changed since the last run.
3.  **📦 Compress**: Bundles updates into timestamped `.zip` archives.
4.  **💾 Disk Guard**: Automatically aborts if disk usage exceeds 450MB (safe for Free Tier accounts).



---

## 🔒 Module 2: DKIM Body Hash Verifier

A surgical tool for verifying the `bh=` tag in email signatures. It implements **Relaxed Body Canonicalization** per **RFC 6376**.

<!--### ✨ RFC 6376 Compliance Features 
* **Horizontal WSP Reduction**: Uses hex-encoded regex (`[\x20\x09]+`) to target only standard space and tab characters within lines.
* **Line Stripping**: Removes all horizontal WSP from the end of each line before hashing.
* **CRLF Standardization**: Normalizes all line endings to `\r\n`.
* **Trailing Truncation**: Correctly removes empty trailing lines while preserving the mandatory final CRLF. -->



---

## 🚀 Deployment & Usage

### 1️⃣ Setup
```bash
pip install requests beautifulsoup4
```

### 2️⃣ Running the Archiver
Update `BASE_DIR` and `USER_AGENT` in `vital_download.py`, then run:
```bash
python3 vital_download.py
```

### 3️⃣ Verifying DKIM Hashes
Save the raw email body to `raw_body.bin`, update the `expected_bh` in `verify_dkim.py`, and run:
```bash
python3 verify_dkim.py
```

---

## 📂 File Structure
```text
/project_root/
├── vital_download.py     # Wikipedia automation script
├── verify_dkim.py        # RFC-compliant security script
├── test.py               # Test suite for canonicalization logic
├── download_log.json     # Archiver version history
└── ancient_laptop.png    # Project header image
```

---

## 📄 License
* **Code**: MIT License.
* **Content**: Wikipedia content is available under the [CC BY-SA License](https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License).
