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
        tasks = [async_fetch_url(session, name, url) for name, url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
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
        filepaths.append(filepath)
        store_to_file(filepath, source_code)

    return filepaths

# def get_subjects():
#     page = requests.get(CATALOG_URL)
    
#     if page.status_code != 200:
#         print('Error: Could not connect to catalog.ucdavis.edu')
#         return 1
    
#     soup = bs(page.content, 'html.parser')
#     subjects = soup.find_all('a', {'href': re.compile(r'^/courses-subject-code/[a-z]+')})
    
#     for subject in subjects:
#         # Replace zero-width space
#         subject.text.replace('\u200b', '')

#         # Extract name and code
#         subject_name, subject_code = re.search(r'(.+) \(([A-Z]{3})\)', subject.text).groups()
        
#         if subject_code in IGNORE_SUBJECTS:
#             print(f'Ignoring {subject_code}')
#             continue
        
#         subject_object = Subject(code=subject_code, name=subject_name)
#         subject_object.save()
    
#     return 0

# def get_subject_html(subject_obj):
#     subject_code = subject_obj.code
#     url = SUBJECT_URL.format(subject_code.lower())
    
#     page = requests.get(url)
    
#     if page.status_code != 200:
#         print(f'Error: Could not connect to {url}')
#         return None
    
#     soup = bs(page.content, 'html.parser')
#     return soup.find_all('div', {'class': 'courseblock'})

# if __name__ == '__main__':
#     print(asyncio.run(fetch_urls([CATALOG_URL])))