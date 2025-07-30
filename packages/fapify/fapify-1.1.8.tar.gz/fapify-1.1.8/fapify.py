#!/usr/bin/env python3
"""
fapify CLI: fetch & download images & videos from leakedzone.com (via fapello endpoints)
"""

import argparse
import asyncio
import os
import re
import sys
import uuid
import shutil
import urllib.parse

import aiohttp
from bs4 import BeautifulSoup
from tabulate import tabulate
from colorama import Fore, Style, init as colorama_init

# Initialize colorama
colorama_init(autoreset=True)

async def get_webpage_content(url: str, session: aiohttp.ClientSession):
    async with session.get(url, allow_redirects=True) as response:
        return await response.text(), str(response.url), response.status

async def fetch_fapello_page_media(page_url: str, session: aiohttp.ClientSession, username: str) -> dict:
    content, _, status = await get_webpage_content(page_url, session)
    if status != 200:
        print(f"[ERROR] Failed to fetch {page_url} (status {status})", file=sys.stderr)
        return {}
    soup = BeautifulSoup(content, 'html.parser')
    images = [
        img['src'] for img in soup.find_all('img', src=True)
        if img['src'].startswith("https://fapello.com/content/") and f"/{username}/" in img['src']
    ]
    videos = [
        vid['src'] for vid in soup.find_all('source', type="video/mp4", src=True)
        if vid['src'].startswith("https://") and f"/{username}/" in vid['src']
    ]
    return {"images": images, "videos": videos}

async def fetch_fapello_album_media(album_url: str) -> dict:
    media = {"images": [], "videos": []}
    parsed = urllib.parse.urlparse(album_url)
    username = parsed.path.strip("/").split("/")[0] if parsed.path else ""
    if not username:
        print("[ERROR] Could not extract username from album URL.", file=sys.stderr)
        return media

    headers = {"User-Agent": "Mozilla/5.0"}
    async with aiohttp.ClientSession(headers=headers) as session:
        # Grab the paginated album pages
        content, base, status = await get_webpage_content(album_url, session)
        if status != 200:
            print(f"[ERROR] Failed to load main album page: {status}", file=sys.stderr)
            return media
        soup = BeautifulSoup(content, 'html.parser')
        links = {
            a['href'] for a in soup.find_all('a', href=True)
            if a['href'].startswith(album_url) and re.search(r'/\d+/?$', a['href'])
        } or {album_url}

        tasks = [fetch_fapello_page_media(u, session, username) for u in links]
        for res in await asyncio.gather(*tasks):
            if res:
                media["images"].extend(res["images"])
                media["videos"].extend(res["videos"])

        # follow “next” links
        visited = set()
        current = album_url
        while current and current not in visited:
            visited.add(current)
            page_content, page_base, status = await get_webpage_content(current, session)
            if status != 200:
                break
            ps = BeautifulSoup(page_content, 'html.parser')
            imgs = [
                img['src'] for img in ps.find_all('img', src=True)
                if img['src'].startswith("https://fapello.com/content/") and f"/{username}/" in img['src']
            ]
            vids = [
                vid.get('src') for vid in ps.find_all('video', src=True)
                if vid['src'].startswith("https://") and f"/{username}/" in vid['src']
            ]
            media["images"].extend(imgs)
            media["videos"].extend(vids)
            nxt = ps.find("div", id="next_page")
            if nxt and (a := nxt.find("a", href=True)):
                current = urllib.parse.urljoin(page_base, a['href'])
            else:
                break

    # dedupe
    media["images"] = list(dict.fromkeys(media["images"]))
    media["videos"] = list(dict.fromkeys(media["videos"]))
    return media

def ensure_ffmpeg():
    if shutil.which("ffmpeg") is None:
        print(f"{Fore.RED}Error: ffmpeg not found. Please install and add to your PATH.{Style.RESET_ALL}")
        sys.exit(1)

def update_table(user: str, mode: str, status: str):
    os.system("cls" if os.name == "nt" else "clear")
    title = f"{Fore.GREEN}{Style.BRIGHT}{'Fapify'.center(70)}{Style.RESET_ALL}"
    table = tabulate(
        [[user, mode, status]],
        headers=[Style.BRIGHT + h + Style.RESET_ALL for h in ("User", "Mode", "Status")],
        tablefmt="fancy_grid",
        stralign="center",
    )
    print(f"{title}\n{Fore.CYAN}{table}{Style.RESET_ALL}")

async def download_worker(user: str, url: str, idx: int, total: int, folder: str, ext: str):
    fname = f"fapify_{user}_{uuid.uuid4().hex}.{ext}"
    update_table(user, folder, f"Downloading {idx}/{total}: {fname}")
    cmd = ["ffmpeg", "-y", "-i", url, "-c", "copy", f"{user}/{folder}/{fname}"]
    from asyncio import subprocess as sp
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=sp.DEVNULL,
        stderr=sp.DEVNULL
    )
    await proc.wait()

async def download_bulk(user: str, urls: list, folder: str, ext: str, batch: int):
    os.makedirs(f"./{user}/{folder}", exist_ok=True)
    sem = asyncio.Semaphore(batch)
    total = len(urls)
    async def sem_task(i, u):
        async with sem:
            await download_worker(user, u, i, total, folder, ext)
    await asyncio.gather(*(sem_task(i, u) for i, u in enumerate(urls, 1)))

async def main():
    parser = argparse.ArgumentParser(
        prog="fapify",
        description="Fetch & download media from fapello.com albums"
    )
    parser.add_argument(
        "-u", "--user",
        required=True,
        help="Username or full album URL"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-p", "--photos", action="store_true", help="Only download images")
    group.add_argument("-v", "--videos", action="store_true", help="Only download videos")
    parser.add_argument(
        "-b", "--batch", type=int, default=5,
        help="Concurrent downloads (default: 5)"
    )
    args = parser.parse_args()

    # Derive username & album_url
    if args.user.startswith("http"):
        album_url = args.user
        username = urllib.parse.urlparse(album_url).path.strip("/").split("/")[0]
    else:
        username = args.user
        album_url = f"https://fapello.com/{username}"

    ensure_ffmpeg()
    mode = "images only" if args.photos else "videos only" if args.videos else "images + videos"
    update_table(username, mode, "Starting…")

    media = await fetch_fapello_album_media(album_url)
    imgs, vids = media["images"], media["videos"]

    if args.photos or not args.videos:
        update_table(username, "images", f"Found {len(imgs)} images")
        if imgs:
            await download_bulk(username, imgs, "images", "jpg", args.batch)

    if args.videos or not args.photos:
        update_table(username, "videos", f"Found {len(vids)} videos")
        if vids:
            await download_bulk(username, vids, "videos", "mp4", args.batch)

    update_table(username, mode, "Complete ✅")
    print(f"\nDone: images={len(imgs)}, videos={len(vids)}")


def cli():
    """Console-script entry point."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    cli()