from django.core.management.base import BaseCommand
from scraperapp.models import Subject, Course
from scraperapp.web_crawler import WebCrawler
from scraperapp.scraper import Scraper
from bs4 import BeautifulSoup as bs
import time


class Command(BaseCommand):
    help = 'Scrapes the course catalog and stores the data in the database'

    def handle(self, *args, **kwargs):
        start = time.perf_counter()
        self.scrape_data()
        end = time.perf_counter()
        print(f'Finished parsing in {end - start:0.4f} seconds')
        
    def scrape_data(self):
        subjects = Subject.objects.all()
        web_crawler = WebCrawler()
        
        if len(subjects) < 215:
            print('Subjects not in database. Scraping...')
            subjects = web_crawler.request_subjects()
            print('Finished scraping subjects')
        else:
            print('Subjects already in database')
        
        scraper = Scraper()
        
        for subject_obj in subjects:
            courses = Course.objects.filter(subject=subject_obj)
            
            if len(courses) != 0:
                print(f'{subject_obj.code} courses already in database.')
                continue
            
            print(f'{subject_obj.code} courses not in database. Requesting HTML...')
            subject_html = web_crawler.request_subject_html(subject_obj.code)
            soup = bs(subject_html, 'html.parser')
            html_arr= soup.find_all('div', {'class': 'courseblock'})
            print(f'Processing {subject_obj.code} courses and prerequisites...')
            for course_html in html_arr:
                course_obj = scraper.process_course(str(course_html), subject_obj)
                if course_obj is not None:
                    scraper.update_successors(course_obj)
                    scraper.process_prerequisites(subject_obj, course_obj)
            print(f'Finished processing {subject_obj.code} courses and prerequisites.')
            time.sleep(0.25)
