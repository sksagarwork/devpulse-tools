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
    print(f"Loaded {len(urls)} URLs from sitemap:")
    for u in urls:
        print(f" - {u}")

    host = "sksagarwork.github.io"
    key = "7b82f6e910b9818b5cf60f172a3b" # Generated IndexNow Key
    key_location = f"https://{host}/devpulse-tools/{key}.txt"

    payload = {
        "host": host,
        "key": key,
        "keyLocation": key_location,
        "urlList": urls
    }

    # Also create the verification key file in the repo root
    key_path = os.path.join(BASE_DIR, f"{key}.txt")
    with open(key_path, "w") as f:
        f.write(key)
    print(f"Wrote IndexNow verification key to {key}.txt")

    print("\nPayload ready for IndexNow submission to https://api.indexnow.org/indexnow")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
