from django.core.management.base import BaseCommand
from scraperapp.scraper import scrape_data
import time


class Command(BaseCommand):
    help = 'Scrapes the course catalog and stores the data in the database'

    def handle(self, *args, **kwargs):
        start = time.perf_counter()
        scrape_data()
        end = time.perf_counter()
        print(f'Finished parsing in {end - start:0.4f} seconds')
