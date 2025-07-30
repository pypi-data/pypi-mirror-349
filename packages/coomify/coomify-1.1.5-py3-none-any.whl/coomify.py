#!/usr/bin/env python3
"""
coomify CLI: download photos/videos from coomer.su
"""

import argparse
import asyncio
import os
import sys
import uuid
import shutil

import aiohttp  # async HTTP client :contentReference[oaicite:2]{index=2}
from bs4 import BeautifulSoup  # HTML parsing :contentReference[oaicite:3]{index=3}
from tabulate import tabulate
from colorama import Fore, Style, init as colorama_init

# Init colors
colorama_init(autoreset=True)

def ensure_ffmpeg():
    if shutil.which('ffmpeg') is None:
        print(f"{Fore.RED}Error: 'ffmpeg' not found. Install and add to PATH.{Style.RESET_ALL}")
        sys.exit(1)

API_BASE = "https://coomer.su"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def update_table(user: str, mode: str, status: str):
    os.system('cls' if os.name=='nt' else 'clear')
    title = f"{Fore.GREEN}{Style.BRIGHT}{'Coomify V1.0'.center(70)}{Style.RESET_ALL}"
    print(title, "\n")
    headers = [f"{Style.BRIGHT}User{Style.RESET_ALL}",
               f"{Style.BRIGHT}Mode{Style.RESET_ALL}",
               f"{Style.BRIGHT}Status{Style.RESET_ALL}"]
    print(f"{Fore.CYAN}{tabulate([[user, mode, status]],
          headers=headers, tablefmt='fancy_grid',
          stralign='center')}{Style.RESET_ALL}")

async def fetch_photo_urls(user: str):
    urls, page = [], 1
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        while True:
            url = f"{API_BASE}/{user}/photos?page={page}"
            update_table(user, "photos", f"GET {url}")
            resp = await session.get(url)
            if resp.status != 200:
                break
            html = await resp.text()
            soup = BeautifulSoup(html, 'html.parser')
            imgs = soup.select('div.gallery img[src]')
            if not imgs:
                break
            for img in imgs:
                src = img['src']
                if src.startswith('//'):
                    src = 'https:' + src
                urls.append(src)
            page += 1
    return list(dict.fromkeys(urls))

async def fetch_video_urls(user: str):
    urls, page = [], 1
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        while True:
            url = f"{API_BASE}/{user}/videos?page={page}"
            update_table(user, "videos", f"GET {url}")
            resp = await session.get(url)
            if resp.status != 200:
                break
            html = await resp.text()
            soup = BeautifulSoup(html, 'html.parser')
            vids = soup.select('div.gallery video source[src]')
            if not vids:
                break
            for source in vids:
                src = source['src']
                if src.startswith('//'):
                    src = 'https:' + src
                urls.append(src)
            page += 1
    return list(dict.fromkeys(urls))

async def download_worker(user: str, url: str, idx: int, total: int, folder: str, ext: str):
    fname = f"coomify_{user}_{uuid.uuid4().hex}.{ext}"
    update_table(user, folder, f"Downloading {idx}/{total}: {fname}")
    cmd = ["ffmpeg", "-y", "-i", url, "-c", "copy", f"{user}/{folder}/{fname}"]
    proc = await asyncio.create_subprocess_exec(*cmd)
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
    parser = argparse.ArgumentParser(prog="coomify",
        description="Download media from coomer.su")
    parser.add_argument("-u","--user", required=True, help="Username")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-p","--photos", action="store_true")
    group.add_argument("-v","--videos", action="store_true")
    parser.add_argument("-b","--batch", type=int, default=5,
                        help="Concurrent downloads (default:5)")
    args = parser.parse_args()

    ensure_ffmpeg()
    mode = ("photos only" if args.photos else
            "videos only" if args.videos else
            "photos + videos")
    update_table(args.user, mode, "Starting…")

    if args.photos or not args.videos:
        photos = await fetch_photo_urls(args.user)
        update_table(args.user, "photos", f"Found {len(photos)} photos")
        if photos:
            await download_bulk(args.user, photos, "photos", "jpg", args.batch)
    if args.videos or not args.photos:
        vids = await fetch_video_urls(args.user)
        update_table(args.user, "videos", f"Found {len(vids)} videos")
        if vids:
            await download_bulk(args.user, vids, "videos", "mp4", args.batch)

    update_table(args.user, mode, "Complete ✅")
    print(f"\nDone: photos={len(photos) if 'photos' in locals() else 0}, videos={len(vids) if 'vids' in locals() else 0}")

if __name__ == "__main__":
    asyncio.run(main())
