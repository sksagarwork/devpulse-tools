#!/usr/bin/env python3
"""
IndexNow Automated URL Submission Tool for CryptoCalc Pro.
Submits all site URLs to Bing, Yandex, Seznam, and Naver for rapid indexation.
Usage: python3 tools/indexnow_submit.py
"""

import urllib.request
import json
import xml.etree.ElementTree as ET
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITEMAP_FILE = os.path.join(BASE_DIR, "sitemap.xml")

def get_urls():
    tree = ET.parse(SITEMAP_FILE)
    root = tree.getroot()
    urls = []
    for elem in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
        loc = elem.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        if loc is not None and loc.text:
            urls.append(loc.text.strip())
    return urls

def main():
    urls = get_urls()
    print(f"Loaded {len(urls)} URLs from sitemap.")

    host = "sksagarwork.github.io"
    key = "7b82f6e910b9818b5cf60f172a3b"
    key_location = f"https://{host}/devpulse-tools/{key}.txt"

    payload = {
        "host": host,
        "key": key,
        "keyLocation": key_location,
        "urlList": urls
    }

    # Ensure key file exists
    key_path = os.path.join(BASE_DIR, f"{key}.txt")
    with open(key_path, "w") as f:
        f.write(key)

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"}
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow API Response: HTTP {resp.status}")
    except Exception as e:
        print(f"IndexNow submission notice: {e}")

if __name__ == "__main__":
    main()
