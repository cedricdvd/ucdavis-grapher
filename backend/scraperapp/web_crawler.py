import aiohttp
import asyncio
import os
import logging
from .constants import ASYNCIO_URL, CATALOG_URL, LOG_DIR

logger = logging.getLogger('webcrawler')
logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'scraperapp.log'),
    filemode='a',
    encoding='utf-8',
    level=logging.DEBUG,
)

async def async_fetch_url(session, name, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            html = await response.text()
            return name, html
    except aiohttp.ClientError as e:
        logger.error(f'Could not fetch {url}: {e}')
        return name, None

async def async_fetch_urls(urls, rate_limit=1.0):
    async with aiohttp.ClientSession(ASYNCIO_URL) as session:
        # tasks = [async_fetch_url(session, name, url) for name, url in urls]
        tasks = []
        length = len(urls)
        for i, (name, url) in enumerate(urls):
            tasks.append(async_fetch_url(session, name, url))
            await asyncio.sleep(rate_limit)
            logger.debug(f'Fetched {name} URL')
        results = await asyncio.gather(*tasks, return_exceptions=True)
        # print(f'\rFetched {length}/{length} urls')
    return results

def fetch_urls(urls, rate_limit=1.0):
    return asyncio.run(async_fetch_urls(urls, rate_limit))


def store_to_file(name, filepath, source_code):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(source_code)

    logger.debug(f'Stored {name} at {filepath}')

def store_results(dir_path, results):
    filepaths = []
    tasks = []

    # Parallelize
    for name, source_code in results:
        filepath = os.path.join(dir_path, f'{name}.html')
        filepaths.append((name, filepath))
        tasks.append((name, filepath, source_code))
        store_to_file(name, filepath, source_code)
        # logger.debug(f'Stored {name} at {filepath}')

    # NOTE: Parallelizing here isn't as useful because the bottleneck
    # comes from having to request for URLs
    # with ThreadPoolExecutor() as executor:
    #     futures = [executor.submit(store_to_file, *task) for task in tasks]

    return filepaths
