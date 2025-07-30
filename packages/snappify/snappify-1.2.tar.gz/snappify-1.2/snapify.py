#!/usr/bin/env python3
import argparse
import asyncio
import aiohttp
import aiofiles
import json
import logging
import os
import re
import sys
import zipfile
from datetime import datetime
from bs4 import BeautifulSoup
from colorama import Fore, Style, init as colorama_init

# Initialize Colorama
colorama_init(autoreset=True)

AUTOPOSTS_FILE = "autoposts.json"
DEFAULT_INTERVAL = 300    # seconds

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

# —————— Persistence ——————————————————————————————
DEFAULT_DATA = {"usernames": {}, "interval": DEFAULT_INTERVAL}

def save_data(data):
    with open(AUTOPOSTS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_data():
    if not os.path.exists(AUTOPOSTS_FILE):
        print(Fore.YELLOW + "No state file found; creating new one.")
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA.copy()
    try:
        with open(AUTOPOSTS_FILE, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(Fore.RED + f"State file corrupt ({e}); resetting.")
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA.copy()

    changed = False
    if not isinstance(data.get("usernames"), dict):
        data["usernames"] = {}
        changed = True
    if not isinstance(data.get("interval"), int):
        data["interval"] = DEFAULT_INTERVAL
        changed = True
    if changed:
        print(Fore.YELLOW + "Fixing state file structure.")
        save_data(data)
    return data

# —————— Snapchat Fetching Helpers —————————————————————
async def get_json(session, username):
    url = f"https://story.snapchat.com/@{username}"
    headers = {"User-Agent": "Mozilla/5.0"}
    async with session.get(url, headers=headers) as resp:
        if resp.status == 404:
            print(Fore.YELLOW + f"{username}: no story page (404).")
            return None
        text = await resp.text()
        try:
            raw = json.loads(
                BeautifulSoup(text, "html.parser")
                         .find(id="__NEXT_DATA__").string
            )
            return raw
        except Exception as e:
            print(Fore.RED + f"{username}: JSON parse error: {e}")
            return None

async def download_media(session, url, username):
    dirpath = os.path.join("snap_media", username)
    os.makedirs(dirpath, exist_ok=True)

    name = re.sub(r'[<>:"/\\|?*]', "", url.split("/")[-1])
    async with session.get(url) as resp:
        if resp.status != 200:
            return None
        ct = resp.headers.get("Content-Type", "")
        ext = ".jpg" if "image" in ct else ".mp4" if "video" in ct else ""
        if not ext:
            return None

        path = os.path.join(dirpath, name + ext)
        async with aiofiles.open(path, "wb") as f:
            async for chunk in resp.content.iter_chunked(1024):
                await f.write(chunk)
        return path

async def create_zip(username, files):
    zdir = os.path.join("zips", username)
    os.makedirs(zdir, exist_ok=True)
    zname = f"{username}_{datetime.now():%Y-%m-%d_%H%M}.zip"
    zpath = os.path.join(zdir, zname)
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(f, os.path.basename(f))
    return zpath

# —————— Core Processing ———————————————————————————
async def process_username(username, session, data, force_zip=False):
    cfg = data["usernames"].setdefault(username, {"last": []})
    last = set(cfg["last"])

    raw = await get_json(session, username)
    if not raw:
        return

    snaps = (raw.get("props", {})
                .get("pageProps", {})
                .get("story", {})
                .get("snapList", []))
    urls = [s["snapUrls"]["mediaUrl"] for s in snaps]
    new = [u for u in urls if u not in last]
    if not new:
        print(Fore.CYAN + f"{username}: no new snaps.")
        return

    print(Fore.GREEN + f"{username}: found {len(new)} new item(s), downloading…")
    tasks = [download_media(session, u, username) for u in new]
    results = await asyncio.gather(*tasks)
    files = [p for p in results if p]

    if not files:
        print(Fore.RED + f"{username}: download failed.")
        return

    # Only zip if -z was passed
    if force_zip:
        z = await create_zip(username, files)
        for f in files:
            try: os.remove(f)
            except: pass
        print(Fore.MAGENTA + f"{username}: downloaded {len(files)} snaps (zipped → {z})")
    else:
        print(Fore.MAGENTA + f"{username}: downloaded {len(files)} snaps")

    # Update last-downloaded and persist
    cfg["last"] = list(last.union(new))
    save_data(data)

# —————— Monitoring Loop ———————————————————————————
async def check_loop(data, force_zip=False):
    interval = data["interval"]
    async with aiohttp.ClientSession() as session:
        while True:
            for user in list(data["usernames"].keys()):
                await process_username(user, session, data, force_zip=force_zip)
            print(Fore.YELLOW + f"Sleeping {interval}s…")
            await asyncio.sleep(interval)

# —————— CLI —————————————————————————————————————
def main():
    parser = argparse.ArgumentParser(prog="snapify",
        description="Download Snapchat story media or monitor for new snaps")
    parser.add_argument(
        "-u", "--user",
        help="comma-separated usernames to ADD (downloads now)"
    )
    parser.add_argument(
        "-r", "--remove",
        help="comma-separated usernames to REMOVE"
    )
    parser.add_argument(
        "-c", "--check-interval", type=int,
        help="set polling interval in seconds"
    )
    parser.add_argument(
        "-z", "--zip", action="store_true",
        help="bundle downloaded snaps into a ZIP"
    )
    parser.add_argument(
        "command", nargs="?", choices=("start",),
        help="‘start’ to begin monitoring loop"
    )
    args = parser.parse_args()

    data = load_data()
    changed = False
    added = []

    # Add users
    if args.user:
        for u in args.user.split(","):
            u = u.strip()
            if u and u not in data["usernames"]:
                data["usernames"][u] = {"last": []}
                added.append(u)
                print(Fore.GREEN + f"Added user: {u}")
        changed = True

    # Remove users
    if args.remove:
        for u in args.remove.split(","):
            u = u.strip()
            if u in data["usernames"]:
                del data["usernames"][u]
                print(Fore.RED + f"Removed user: {u}")
        changed = True

    # Set interval
    if args.check_interval is not None:
        data["interval"] = args.check_interval
        print(Fore.YELLOW + f"Set interval = {args.check_interval}s")
        changed = True

    # on config change without “start”: save & one-off
    if changed and args.command != "start":
        save_data(data)
        if added:
            async def oneoff():
                async with aiohttp.ClientSession() as session:
                    for u in added:
                        await process_username(u, session, data, force_zip=args.zip)
            asyncio.run(oneoff())
        print(Style.BRIGHT + "\nTo start monitoring for new snaps, run:")
        zip_flag = " -z" if args.zip else ""
        print(Fore.CYAN + f"  snapify start{zip_flag}\n")
        sys.exit(0)

    # Start monitoring loop
    if args.command == "start":
        print(Style.BRIGHT + "Entering watch mode—press Ctrl+C to exit.\n")
        try:
            asyncio.run(check_loop(data, force_zip=args.zip))
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nInterrupted; exiting.")
            save_data(data)
            sys.exit(0)

    parser.print_help()

if __name__ == "__main__":
    main()
