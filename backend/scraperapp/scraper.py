from .web_crawler import get_subjects, get_subject_html
from .processor import process_courses, process_prerequisites
from .models import Subject, Course, Prerequisite
from time import sleep

def scrape_data():
    subjects = Subject.objects.all()
    
    if len(subjects) < 215:
        print('Subjects not in database. Scraping...')
        get_subjects()
        print('Finished scraping subjects')
    else:
        print('Subjects already in database')
        
    subject_list = Subject.objects.all()
    
    for subject_obj in subject_list:
        courses = Course.objects.filter(subject=subject_obj)
        
        if len(courses) == 0:
            print(f'{subject_obj.code} courses not in database. Scraping...')
            subject_html = get_subject_html(subject_obj)
            print(f'Processing {subject_obj.code} courses...')
            process_courses(subject_html, subject_obj)
            print(f'Completed {subject_obj.code} courses.')
            sleep(1)
        else:
            print(f'{subject_obj.code} courses already in database.')
            
    for subject_obj in subject_list:
        prerequisites_processed = Prerequisite.objects.filter(subject_id=subject_obj)
        
        if len(prerequisites_processed) == 0:
            print(f'Processing {subject_obj.code} prerequisites...')
            process_prerequisites(subject_obj)
            print(f'Completed {subject_obj.code} prerequisites.')
        else:
            print(f'{subject_obj.code} prerequisites already in database.')
