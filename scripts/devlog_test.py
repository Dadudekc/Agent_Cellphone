#!/usr/bin/env python3
from __future__ import annotations

import os
import json
import pathlib
import sys
import time
import traceback
from urllib import request, error, parse


def load_env(dotenv_path: str | None = None) -> None:
    path = pathlib.Path(dotenv_path or ".env")
    if not path.exists():
        return
    try:
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and val:
                os.environ.setdefault(key, val)
    except Exception:
        print("ENV_LOAD_ERROR:\n" + traceback.format_exc())


def main() -> int:
    load_env()
    url = os.environ.get("DISCORD_WEBHOOK_URL")
    user = os.environ.get("DEVLOG_USERNAME", "Agent Devlog")
    print(f"WEBHOOK_PRESENT={bool(url)} LENGTH={len(url) if url else 0}")
    if url:
        print(f"WEBHOOK_PREFIX={url[:32]}…")
    else:
        print("MISSING DISCORD_WEBHOOK_URL in environment/.env")
        return 2

    # Normalize webhook domain to avoid legacy discordapp.com issues
    if url:
        try:
            parts = parse.urlparse(url)
            netloc = parts.netloc.replace("discordapp.com", "discord.com")
            scheme = "https"
            url = parse.urlunparse((scheme, netloc, parts.path, parts.params, parts.query, parts.fragment))
        except Exception:
            pass

    payload = {
        "username": user,
        "embeds": [
            {
                "title": "Devlog test",
                "description": "This is a test from Agent Cellphone.",
                "color": 5814783,
            }
        ],
    }

    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "AgentCellphoneDevlog/1.0 (+local)",
    }

    attempts = 3
    last_exc: Exception | None = None
    for i in range(attempts):
        req = request.Request(url, data=data, headers=headers)
        try:
            with request.urlopen(req, timeout=12) as resp:
                body = resp.read()
                print(f"HTTP_STATUS={resp.status}")
                print(f"RESP_LEN={len(body)}")
                return 0
        except error.HTTPError as e:
            try:
                body = e.read()
            except Exception:
                body = b""
            print(f"HTTP_ERROR code={e.code} reason={e.reason}")
            print(f"RESP_BODY_PREVIEW={body[:256]!r}")
            last_exc = e
            # Retry on common transient or WAF codes
            if e.code in {403, 429, 500, 502, 503, 504} and i < attempts - 1:
                time.sleep(0.5 * (2 ** i))
                continue
            return 3
        except error.URLError as e:
            print(f"URL_ERROR reason={getattr(e, 'reason', repr(e))}")
            last_exc = e
            if i < attempts - 1:
                time.sleep(0.5 * (2 ** i))
                continue
            return 4
        except Exception as e:
            print("UNEXPECTED_ERROR:\n" + traceback.format_exc())
            last_exc = e
            if i < attempts - 1:
                time.sleep(0.5 * (2 ** i))
                continue
            return 5

    # If we exited loop without return, bubble up as generic failure
    if last_exc:
        print(f"FINAL_ERROR: {type(last_exc).__name__}: {last_exc}")
    return 6


if __name__ == "__main__":
    raise SystemExit(main())



