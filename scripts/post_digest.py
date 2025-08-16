#!/usr/bin/env python3
import os, json, sys, pathlib, requests  # pip install requests
REPORTS_DIR = pathlib.Path("runtime/overnight")
def find_latest():
    dirs = sorted([p for p in REPORTS_DIR.glob("overnight_*") if p.is_dir()], reverse=True)
    return dirs[0] if dirs else None

def main():
    dest = os.getenv("DISCORD_WEBHOOK_URL") or os.getenv("SLACK_WEBHOOK_URL")
    if not dest: 
        print("No webhook set; skip post."); return
    latest = find_latest()
    if not latest: 
        print("No reports."); return
    md = (latest/"digest.md").read_text()
    if "discord" in dest:
        requests.post(dest, json={"content": md[:1900]})
    else:  # slack
        requests.post(dest, json={"text": md[:3000]})
    print("Posted digest.")

if __name__ == "__main__": main()
