# from .web_crawler import get_subjects, get_subject_html
# from .processor import process_courses, process_prerequisites
# from .models import Subject, Course, Prerequisite
# from time import sleep, time
from .web_crawler import fetch_urls, store_results
from .processor import process_catalog
from .constants import *
import os

def scrape_catalog():
    # Scrape Catalog Subjects
    os.makedirs(DATA_DIR, exist_ok=True)
    results = fetch_urls([('catalog', CATALOG_URL)])
    catalog_path = store_results(os.path.join(DATA_DIR), results)[0]
    process_catalog(catalog_path)



def scrape_data():
    scrape_catalog()


    # start, end = 0, 0
    # subjects = Subject.objects.all()

    # if len(subjects) < 215:
    #     start = time()
    #     print('Subjects not in database. Scraping...')
    #     get_subjects()
    #     print('Finished scraping subjects')
    #     end = time()
    #     print(f'TIME SCRAPING: {end - start}')
    # else:
    #     print('Subjects already in database')
        
    # subject_list = Subject.objects.all()

    # start = time()
    # for subject_obj in subject_list:
    #     courses = Course.objects.filter(subject=subject_obj)
        
    #     if len(courses) == 0:
    #         print(f'\r{subject_obj.code} courses not in database. Scraping...',end='')
    #         subject_html = get_subject_html(subject_obj)
    #         # print(f'Processing {subject_obj.code} courses...')
    #         process_courses(subject_html, subject_obj)
    #         # print(f'Completed {subject_obj.code} courses.')
    #         sleep(1)
    #     else:
    #         print(f'{subject_obj.code} courses already in database.')
    # end = time()
    # print(f'\nTIME GETTING COURSES: {end - start}')
    
    # start = time()
    # for subject_obj in subject_list:
    #     prerequisites_processed = Prerequisite.objects.filter(subject_id=subject_obj)
        
    #     if len(prerequisites_processed) == 0:
    #         print(f'\rProcessing {subject_obj.code} prerequisites...', end='')
    #         process_prerequisites(subject_obj)
    #         # print(f'Completed {subject_obj.code} prerequisites.')
    #     else:
    #         print(f'{subject_obj.code} prerequisites already in database.')
    # end = time()
    # print(f'\nTIME PROCESSING PREREQUISITES: {end - start}')

if __name__ == '__main__':
    scrape_data()