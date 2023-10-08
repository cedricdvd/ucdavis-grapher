from bs4 import BeautifulSoup as bs
from .models import Subject
from .constants import CATALOG_URL, SUBJECT_URL_FORMAT, IGNORED_SUBJECTS
import requests
import re

class WebCrawler:
    
    def __init__(self):
        self.subjects = []
        self.SUBJECT_URL_PATTERN = re.compile(r'^/courses-subject-code/[a-z]+')
        self.SUBJECT_LISTING_PATTERN = re.compile(r'(.+) \(([A-Z]{3})\)')
        
    def request_subjects(self):
        content = self.request_page_content(CATALOG_URL)
        
        if content is None:
            return None
        
        # Grab url pattern
        soup = bs(content, 'html.parser')
        subject_arr = soup.find_all('a', {'href': self.SUBJECT_URL_PATTERN})
        
        for subject in subject_arr:
            # Replace zero-width space
            subject_str = subject.text.replace('\u200b', '')

            # Extract name and code
            title, code = re.search(self.SUBJECT_LISTING_PATTERN, subject_str).groups()
            
            if code in IGNORED_SUBJECTS:
                print(f'Ignoring {code}')
                continue
            
            # Saves subject to database and adds to list
            subject_object = Subject(code=code, name=title)
            subject_object.save()
            self.subjects.append(subject_object)
            
        return self.subjects
        
    def request_subject_html(self, code):
        url = SUBJECT_URL_FORMAT.format(code.lower())
        return self.request_page_content(url)
    
    def request_page_content(self, url):
        page = requests.get(url)
        
        if page.status_code != 200:
            print(f'Error: Could not connect to {url}')
            return None
        
        return page.content
