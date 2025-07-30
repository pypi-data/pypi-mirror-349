#!/usr/bin/env python3
"""
fapelloify CLI: fetch all images & videos from a Fapello album URL
"""

import argparse
import asyncio
import re
import sys
import urllib.parse

import aiohttp
from bs4 import BeautifulSoup

def debug_log(message: str):
    print(message)  # Replace or extend this with your actual logging/discord debug method.

async def get_webpage_content(url: str, session: aiohttp.ClientSession):
    async with session.get(url, allow_redirects=True) as response:
        return await response.text(), str(response.url), response.status

async def fetch_fapello_page_media(page_url: str, session: aiohttp.ClientSession, username: str) -> dict:
    try:
        content, base_url, status = await get_webpage_content(page_url, session)
        if status != 200:
            debug_log(f"[DEBUG] Failed to fetch {page_url} with status {status}")
            return {}
        soup = BeautifulSoup(content, 'html.parser')

        # images under fapello.com/content/<username>/
        image_tags = soup.find_all('img', src=True)
        page_images = [
            img['src'] for img in image_tags
            if img['src'].startswith("https://fapello.com/content/") and f"/{username}/" in img['src']
        ]

        # videos via <source type="video/mp4">
        video_tags = soup.find_all('source', type="video/mp4", src=True)
        page_videos = [
            vid['src'] for vid in video_tags
            if vid['src'].startswith("https://") and f"/{username}/" in vid['src']
        ]

        debug_log(f"[DEBUG] {page_url}: Found {len(page_images)} images, {len(page_videos)} videos")
        return {"images": page_images, "videos": page_videos}

    except Exception as e:
        debug_log(f"[DEBUG] Exception fetching {page_url}: {e}")
        return {}

async def fetch_fapello_album_media(album_url: str) -> dict:
    media = {"images": [], "videos": []}
    parsed = urllib.parse.urlparse(album_url)
    path_parts = parsed.path.strip("/").split("/")
    username = path_parts[0] if path_parts else ""
    if not username:
        debug_log("[DEBUG] Could not extract username from album URL.")
        return media

    headers = {"User-Agent": "Mozilla/5.0"}
    async with aiohttp.ClientSession(headers=headers) as session:
        # 1) Scrape pagination links from main page
        content, base_url, status = await get_webpage_content(album_url, session)
        if status != 200:
            debug_log(f"[DEBUG] Failed to load main album page: {status}")
            return media

        soup = BeautifulSoup(content, 'html.parser')
        links = {
            a['href'] for a in soup.find_all('a', href=True)
            if a['href'].startswith(album_url) and re.search(r'/\d+/?$', a['href'])
        }
        if not links:
            links = {album_url}
        debug_log(f"[DEBUG] Found {len(links)} album pages")

        # 2) Fetch each page’s media
        tasks = [fetch_fapello_page_media(url, session, username) for url in links]
        results = await asyncio.gather(*tasks)
        for res in results:
            media["images"].extend(res.get("images", []))
            media["videos"].extend(res.get("videos", []))

        # 3) Handle infinite-scroll style “next page”
        visited = set()
        current = album_url
        while current and current not in visited:
            visited.add(current)
            page_content, page_base, status = await get_webpage_content(current, session)
            if status != 200:
                break
            page_soup = BeautifulSoup(page_content, 'html.parser')

            # collect media directly
            imgs = [
                img['src'] for img in page_soup.find_all('img', src=True)
                if img['src'].startswith("https://fapello.com/content/") and f"/{username}/" in img['src']
            ]
            vids = [
                vid.get('src') for vid in page_soup.find_all('video', src=True)
                if vid['src'].startswith("https://") and f"/{username}/" in vid['src']
            ]
            debug_log(f"[DEBUG] {current}: +{len(imgs)} images, +{len(vids)} videos")
            media["images"].extend(imgs)
            media["videos"].extend(vids)

            # find next page link
            next_div = page_soup.find("div", id="next_page")
            if next_div and (a := next_div.find("a", href=True)):
                current = urllib.parse.urljoin(page_base, a['href'])
            else:
                break

    # dedupe
    media["images"] = list(dict.fromkeys(media["images"]))
    media["videos"] = list(dict.fromkeys(media["videos"]))
    debug_log(f"[DEBUG] Total for {username}: {len(media['images'])} images, {len(media['videos'])} videos")
    return media

async def main():
    parser = argparse.ArgumentParser(prog="fapelloify", description="Fetch media from fapello.com albums")
    parser.add_argument("-u", "--url", required=True, help="Album URL (e.g. https://fapello.com/username)")
    args = parser.parse_args()

    debug_log(f"[INFO] Starting fetch for {args.url}")
    media = await fetch_fapello_album_media(args.url)

    print("\n=== Fetch Complete ===")
    print(f"Images: {len(media['images'])}")
    print(f"Videos: {len(media['videos'])}")
    # TODO: download or process media["images"] / media["videos"] as needed

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
