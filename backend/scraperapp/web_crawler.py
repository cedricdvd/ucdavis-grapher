# from models import Subject

from .constants import CATALOG_URL, SUBJECT_URL, IGNORE_SUBJECTS
from bs4 import BeautifulSoup as bs
import requests
import re

import aiohttp
import asyncio
import os

async def async_fetch_url(session, name, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            html = await response.text()
            return name, html
    except aiohttp.ClientError as e:
        print(f'Error fetching {url}: e')
        return name, None

async def async_fetch_urls(urls, rate_limit=1.0):
    async with aiohttp.ClientSession() as session:
        # tasks = [async_fetch_url(session, name, url) for name, url in urls]
        tasks = []
        length = len(urls)
        for i, (name, url) in enumerate(urls):
            print(f'\rFetched {i}/{length} urls',end='')

            tasks.append(async_fetch_url(session, name, url))
            await asyncio.sleep(rate_limit)
        results = await asyncio.gather(*tasks, return_exceptions=True)
        print(f'\rFetched {length}/{length} urls')
    return results

def fetch_urls(urls, rate_limit=1.0):
    return asyncio.run(async_fetch_urls(urls, rate_limit))

def store_to_file(filepath, source_code):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(source_code)

def store_results(dir_path, results):
    filepaths = []
    for name, source_code in results:
        filepath = os.path.join(dir_path, f'{name}.html')
        filepaths.append((name, filepath))
        store_to_file(filepath, source_code)

    return filepaths
