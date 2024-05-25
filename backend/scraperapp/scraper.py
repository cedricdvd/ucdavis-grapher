from time import sleep, time
from .models import Subject, Course, Prerequisite
from .web_crawler import fetch_urls, store_results
from .processor import process_catalog, process_subjects, process_prerequisites
from .constants import *
import os
import logging

logger = logging.getLogger('scraper')
logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'scraperapp.log'),
    filemode='w',
    encoding='utf-8',
    level=logging.DEBUG,
)

def scrape_catalog():
    # Scrape Catalog Subjects
    os.makedirs(DATA_DIR, exist_ok=True)
    logger.debug('Fetching Catalog URL HTML')
    results = fetch_urls([('catalog', CATALOG_URL)])
    logger.debug('Storing Catalog HTML')
    catalog_path = store_results(os.path.join(DATA_DIR), results)[0][1]
    logger.debug('Processing catalog subjects')
    process_catalog(catalog_path)

def scrape_courses():
    os.makedirs(os.path.join(DATA_DIR, SUBJECT_DIR), exist_ok=True)

    logger.debug('Formatting subject urls')
    subjects = Subject.objects.all()
    urls = []
    for subject in subjects:
        url = SUBJECT_URL.format(subject.code.lower())
        urls.append((subject.code, url))

    logger.debug('Fetching subject pages')
    results = fetch_urls(urls, 1)

    logger.debug('Storing subject html')
    # subject_paths = store_results(os.path.join(DATA_DIR, SUBJECT_DIR), results)

    logger.debug('Processing subject courses')
    # process_subjects(subject_paths)
    # paths = os.listdir(os.path.join(DATA_DIR, SUBJECT_DIR))
    # subs = [(file[:3], os.path.join(DATA_DIR, SUBJECT_DIR, file)) for file in paths]

def scrape_prerequisites():
    logger.debug('Getting subejcts from db')
    subjects = Subject.objects.all()

    logger.debug('Processing prerequisites')
    process_prerequisites(subjects)

def scrape_data():
    os.makedirs(LOG_DIR, exist_ok=True)
    start, end = 0, 0

    start = time()
    # scrape_catalog()
    end = time()
    logger.info(f'TIME SCRAPING SUBJECTS: {end - start}')

    start = time()
    scrape_courses()
    end = time()
    logger.info(f'TIME SCRAPING COURSES: {end - start}')

    start = time()
    # scrape_prerequisites()
    end = time()
    logger.info(f'TIME SCRAPING PREREQUISITES: {end - start}')

if __name__ == '__main__':
    scrape_data()