import requests
import logging
from bs4 import BeautifulSoup as bs
import os
import re

from constants import CATALOG_URL, SUBJECT_URL, IGNORE_SUBJECTS
from connector import connect_database

def get_subjects():
    page = requests.get(CATALOG_URL)
    
    if page.status_code != 200:
        print('Error: Could not connect to catalog.ucdavis.edu')
        return 1
    
    soup = bs(page.content, 'html.parser')
    subjects = soup.find_all('a', {'href': re.compile(r'^/courses-subject-code/[a-z]+')})
    
    database, cursor = connect_database()
    
    for subject in subjects:
        # Replace zero-width space
        subject.text.replace('\u200b', '')
        
        if subject in IGNORE_SUBJECTS:
            print('Ignoring subject', subject.text)
            continue
        
        # Extract name and code
        name, code = re.search(r'(.+) \(([A-Z]{3})\)', subject.text).groups()
        cursor.execute('INSERT INTO subjects (code, subject_name) VALUES (%s, %s)', (code, name))
        
    database.commit()
    cursor.close()
    database.close()
    
    return 0



def get_subject_html(subject_code):
    url = SUBJECT_URL.format(subject_code.lower())
    
    page = requests.get(url)
    
    if page.status_code != 200:
        print(f'Error: Could not connect to {url}')
        return None
    
    soup = bs(page.content, 'html.parser')
    courses = soup.find_all('div', {'class': 'courseblock'})
        
    return courses

if __name__ == '__main__':
    get_subject_html('EAE')