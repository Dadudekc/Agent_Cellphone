#!/usr/bin/env python3
"""
GitHub Clone Tool
=================
Clone a user's repositories using a Personal Access Token (classic PAT or fine-grained) into a target folder.

Usage (from D:\Agent_Cellphone):
  python overnight_runner/tools/github_clone_tool.py --user your-gh-username --token %GITHUB_TOKEN% --dest D:/repositories

Notes:
  - Requires git installed and on PATH
  - Token should have repo read access
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List

import json
import urllib.request


def fetch_repos(user: str, token: str) -> List[str]:
    repos: List[str] = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{user}/repos?type=owner&per_page=100&page={page}"
        req = urllib.request.Request(url, headers={"Authorization": f"token {token}", "User-Agent": "overnight-cloner"})
        with urllib.request.urlopen(req) as resp:  # nosec B310
            data = json.loads(resp.read().decode("utf-8"))
        if not data:
            break
        for r in data:
            if r.get("archived"):
                continue
            clone_url = r.get("clone_url")
            if clone_url:
                repos.append(clone_url)
        page += 1
    return repos


def clone_repo(clone_url: str, dest_dir: Path, token: str) -> None:
    # Inject token into URL: https://<token>@github.com/user/repo.git
    if clone_url.startswith("https://"):
        parts = clone_url.split("https://", 1)[1]
        auth_url = f"https://{token}@{parts}"
    else:
        auth_url = clone_url
    subprocess.run(["git", "clone", "--depth", "1", auth_url], cwd=str(dest_dir), check=False)


def main() -> int:
    p = argparse.ArgumentParser("github_clone_tool")
    p.add_argument("--user", required=True, help="GitHub username / owner")
    p.add_argument("--token", default=os.getenv("GITHUB_TOKEN", ""), help="GitHub token (or set GITHUB_TOKEN)")
    p.add_argument("--dest", default="D:/repositories", help="Destination root directory")
    args = p.parse_args()

    if not args.token:
        print("❌ Missing token. Pass --token or set GITHUB_TOKEN")
        return 2

    dest = Path(args.dest)
    dest.mkdir(parents=True, exist_ok=True)

    try:
        repos = fetch_repos(args.user, args.token)
    except Exception as e:
        print(f"❌ Failed to fetch repos: {e}")
        return 1

    if not repos:
        print("⚠️ No repositories found to clone.")
        return 0

    print(f"Found {len(repos)} repositories. Cloning into {dest}...")
    for url in repos:
        try:
            clone_repo(url, dest, args.token)
        except Exception as e:
            print(f"  ⚠️ Clone failed for {url}: {e}")
    print("✅ Done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())







