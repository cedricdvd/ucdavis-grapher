from django.core.management.base import BaseCommand
from scraperapp.scraper import scrape_data

class Command(BaseCommand):
    help = 'Scrapes the course catalog and stores the data in the database'
    
    def handle(self, *args, **kwargs):
        scrape_data()