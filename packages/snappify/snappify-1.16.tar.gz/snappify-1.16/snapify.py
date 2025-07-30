#!/usr/bin/env python3
import argparse
import asyncio
import aiohttp
import aiofiles
import json
from yarl import URL
import logging
import os
import re
import sys
import zipfile
from datetime import datetime
from urllib.parse import urlparse, unquote
from bs4 import BeautifulSoup
from colorama import Fore, Style, init as colorama_init
import getpass
from snapchat import Snapchat

# Initialize Colorama
colorama_init(autoreset=True)

AUTOPOSTS_FILE = "autoposts.json"
DEFAULT_INTERVAL = 300    # seconds

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# —————— Global flags for private auth ——————————————————————————————
PRIVATE_AUTH = False
COOKIE_FILE = None

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

# —————— Utility for slugifying titles ——————————————————
def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text

# —————— Download friend stories via SnapWrap ——————————————————
async def download_friend_stories_via_snapwrap():
    """
    Uses SnapWrap to log in and download ALL of your friends' current 24h Stories.
    """
    user = input("Snapchat username: ").strip()
    pwd = getpass.getpass("Snapchat password: ")
    print("Logging in via SnapWrap…")
    snap = Snapchat(user, pwd)
    snap.begin()  # perform login
    print("Fetching friend stories…")
    friend_stories = snap.get_friend_stories()  # dict {username: [storyObj,...]}
    for friend, stories in friend_stories.items():
        dest = os.path.join("snap_media", "friends", friend)
        os.makedirs(dest, exist_ok=True)
        for story in stories:
            snap.save_snap(story, dest)
    print(Fore.GREEN + "All friend stories downloaded via SnapWrap.")

# —————— Build an aiohttp session, with optional private cookies or SnapWrap —————————
async def make_session():
    headers = {"User-Agent": "Mozilla/5.0"}

    if PRIVATE_AUTH:
        # ignore cookies.json method, use SnapWrap instead
        await download_friend_stories_via_snapwrap()
        # We still return a normal aiohttp session for the rest of the code (highlights, spotlights, per-user stories)
        return aiohttp.ClientSession(headers=headers)
    else:
        # public mode: no auth cookies needed
        return aiohttp.ClientSession(headers=headers)

# —————— Extracting media URLs ——————————————————
def extract_media_urls(data):
    media = {}
    page_props = data.get("props", {}).get("pageProps", {})

    def recurse(obj, path):
        if isinstance(obj, dict):
            for key, val in obj.items():
                if key == "snapList" and isinstance(val, list):
                    title = (
                        (obj.get("storyTitle") or {}).get("value")
                        or obj.get("title")
                        or obj.get("displayName")
                        or (path[-1] if path else "unknown")
                    )
                    urls = [
                        snap.get("snapUrls", {}).get("mediaUrl")
                        for snap in val
                        if snap.get("snapUrls", {}).get("mediaUrl")
                    ]
                    media.setdefault(title, []).extend(urls)
                else:
                    recurse(val, path + [key])
        elif isinstance(obj, list):
            for item in obj:
                recurse(item, path)

    recurse(page_props, [])
    logging.debug(f"extract_media_urls found albums: {list(media.keys())}")
    return media

# —————— Snapchat Fetching Helpers ————————————————————
async def get_json(session, username):
    url = f"https://story.snapchat.com/@{username}"
    async with session.get(url) as resp:
        if resp.status == 404:
            logging.warning(f"{username}: no story page (404).")
            return None
        if resp.status in (401, 403):
            logging.error(f"{username}: access denied (private?).")
            sys.exit(1)
        text = await resp.text()
        tag = BeautifulSoup(text, "html.parser").find(id="__NEXT_DATA__")
        if not tag:
            logging.error(f"{username}: no __NEXT_DATA__ found.")
            return None
        try:
            return json.loads(tag.string.strip())
        except Exception as e:
            logging.error(f"{username}: JSON parse error: {e}")
            return None

# —————— Download a single media URL to a specific directory ——————————————————
async def download_media_to_dir(session, url, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    parsed = urlparse(url)
    name = unquote(os.path.basename(parsed.path))
    name = re.sub(r'[<>:"/\\|?*]', "", name)

    async with session.get(url) as resp:
        if resp.status != 200:
            logging.error(f"Failed to download {url}: HTTP {resp.status}")
            return None
        ct = resp.headers.get("Content-Type", "")
        ext = ".jpg" if "image" in ct else ".mp4" if "video" in ct else ""
        if not ext:
            return None

        path = os.path.join(dest_dir, f"{name}{ext}")
        async with aiofiles.open(path, "wb") as f:
            async for chunk in resp.content.iter_chunked(1024):
                await f.write(chunk)
        return path

# —————— ZIP creation ———————————————————————————
async def create_zip(username, files):
    zdir = os.path.join("zips", username)
    os.makedirs(zdir, exist_ok=True)
    zname = f"{username}_{datetime.now():%Y-%m-%d_%H%M}.zip"
    zpath = os.path.join(zdir, zname)
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(f, os.path.basename(f))
    return zpath

# —————— Core Processing (stories + highlights + spotlights) —————————————————
async def process_username(username, session, data, force_zip=False):
    cfg = data["usernames"].setdefault(username, {"last": []})
    last = set(cfg["last"])

    raw = await get_json(session, username)
    if not raw:
        return

    # — Stories —
    page_props = raw.get("props", {}).get("pageProps", {})
    story = page_props.get("story") or {}
    snaps = story.get("snapList", [])
    story_urls = [
        s["snapUrls"]["mediaUrl"]
        for s in snaps
        if s.get("snapUrls", {}).get("mediaUrl")
    ]
    new_story = [u for u in story_urls if u not in last]

    if new_story:
        logging.info(f"{username}: found {len(new_story)} new story item(s), downloading…")
        tasks = [
            download_media_to_dir(session, u, os.path.join("snap_media", username, "stories"))
            for u in new_story
        ]
        results = await asyncio.gather(*tasks)
        story_files = [p for p in results if p]
        if story_files:
            if force_zip:
                z = await create_zip(username, story_files)
                for f in story_files: os.remove(f)
                logging.info(f"{username}: story snaps zipped → {z}")
            else:
                logging.info(f"{username}: downloaded {len(story_files)} story snaps")
        else:
            logging.error(f"{username}: story downloads failed.")
        last.update(new_story)
    else:
        logging.debug(f"{username}: no new story snaps")

    # — Spotlights —
    media_map = extract_media_urls(raw)
    spotlight_urls = [
        url for key, lst in media_map.items()
        if "spotlight" in key.lower()
        for url in lst
    ]
    new_spot = [u for u in spotlight_urls if u not in last]
    if new_spot:
        logging.info(f"{username}: found {len(new_spot)} new spotlight item(s), downloading…")
        dest = os.path.join("snap_media", username, "spotlights")
        tasks = [
            download_media_to_dir(session, u, dest)
            for u in new_spot
        ]
        results = await asyncio.gather(*tasks)
        spot_files = [p for p in results if p]
        if spot_files:
            if force_zip:
                z = await create_zip(username, spot_files)
                for f in spot_files: os.remove(f)
                logging.info(f"{username}: spotlight snaps zipped → {z}")
            else:
                logging.info(f"{username}: downloaded {len(spot_files)} spotlight snaps")
        else:
            logging.error(f"{username}: spotlight downloads failed.")
        last.update(new_spot)
    else:
        logging.debug(f"{username}: no new spotlight snaps")

    # — Highlights —
    highlight_keys = sorted(
        [k for k in media_map.keys() if "spotlight" not in k.lower()],
        key=lambda s: s.lower()
    )
    highlight_pairs = [(title, u) for title in highlight_keys for u in media_map.get(title, [])]
    new_high = [(t, u) for (t, u) in highlight_pairs if u not in last]
    if new_high:
        logging.info(f"{username}: found {len(new_high)} new highlight item(s), downloading…")
        tasks = []
        for title, u in new_high:
            slug = slugify(title)
            dest = os.path.join("snap_media", username, "highlights", slug)
            tasks.append(download_media_to_dir(session, u, dest))
        results = await asyncio.gather(*tasks)
        high_files = [p for p in results if p]
        if high_files:
            if force_zip:
                z = await create_zip(username, high_files)
                for f in high_files: os.remove(f)
                logging.info(f"{username}: highlight snaps zipped → {z}")
            else:
                logging.info(f"{username}: downloaded {len(high_files)} highlight snaps")
        else:
            logging.error(f"{username}: highlight downloads failed.")
        last.update([u for (_, u) in new_high])
    else:
        logging.debug(f"{username}: no new highlight snaps")

    cfg["last"] = list(last)
    save_data(data)

# —————— Highlights-Only Download Helper ———————————————————————————
async def download_highlights_only(username, session, data, force_zip=False):
    cfg = data["usernames"].setdefault(username, {"last": []})
    last = set(cfg["last"])

    raw = await get_json(session, username)
    if not raw:
        return

    media_map = extract_media_urls(raw)
    highlight_keys = sorted(
        [k for k in media_map.keys() if "spotlight" not in k.lower()],
        key=lambda s: s.lower()
    )
    highlight_pairs = [(title, u) for title in highlight_keys for u in media_map.get(title, [])]
    new_high = [(t, u) for (t, u) in highlight_pairs if u not in last]
    if not new_high:
        logging.debug(f"{username}: no new highlight snaps.")
        return

    logging.info(f"{username}: found {len(new_high)} new highlight item(s), downloading…")
    tasks = []
    for title, u in new_high:
        slug = slugify(title)
        dest = os.path.join("snap_media", username, "highlights", slug)
        tasks.append(download_media_to_dir(session, u, dest))
    results = await asyncio.gather(*tasks)
    high_files = [p for p in results if p]

    if not high_files:
        logging.error(f"{username}: highlight downloads failed.")
        return

    if force_zip:
        z = await create_zip(username, high_files)
        for f in high_files: os.remove(f)
        logging.info(f"{username}: highlight snaps zipped → {z}")
    else:
        logging.info(f"{username}: downloaded {len(high_files)} highlight snaps")

    last.update([u for (_, u) in new_high])
    cfg["last"] = list(last)
    save_data(data)

# —————— Monitoring Loop ————————————————————————————
async def check_loop(data, force_zip=False):
    interval = data["interval"]
    session = await make_session()
    async with session:
        while True:
            for user in list(data["usernames"].keys()):
                await process_username(user, session, data, force_zip=force_zip)
            logging.info(f"Sleeping {interval}s…")
            await asyncio.sleep(interval)

# —————— CLI —————————————————————————————————————
def main():
    global PRIVATE_AUTH, COOKIE_FILE

    parser = argparse.ArgumentParser(prog="snapify",
        description="Download Snapchat story media, highlights, and spotlights, or monitor for new snaps")
    parser.add_argument("-u", "--user",
        help="comma-separated usernames to ADD (downloads now)")
    parser.add_argument("-r", "--remove",
        help="comma-separated usernames to REMOVE")
    parser.add_argument("-c", "--check-interval", type=int,
        help="set polling interval in seconds")
    parser.add_argument("-z", "--zip", action="store_true",
        help="bundle downloaded snaps into a ZIP")
    parser.add_argument("--highlights", action="store_true",
        help="download only highlights for added users")
    parser.add_argument("-p", "--private", action="store_true",
        help="enable private story download (requires SnapWrap login)")
    parser.add_argument("--cookie-file",
        help="(ignored in private mode)")
    parser.add_argument("command", nargs="?", choices=("start",),
        help="‘start’ to begin monitoring loop")
    args = parser.parse_args()

    PRIVATE_AUTH = args.private
    COOKIE_FILE = args.cookie_file

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
                session = await make_session()
                async with session:
                    if args.highlights:
                        for u in added:
                            await download_highlights_only(u, session, data, force_zip=args.zip)
                    else:
                        for u in added:
                            await process_username(u, session, data, force_zip=args.zip)
            asyncio.run(oneoff())
        print(Style.BRIGHT + "\nTo start monitoring for new snaps, run:")
        zip_flag = " -z" if args.zip else ""
        private_flag = " -p" if args.private else ""
        print(Fore.CYAN + f"  snapify start{zip_flag}{private_flag}\n")
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
