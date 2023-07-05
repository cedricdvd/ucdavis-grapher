from connector import connect_database
from scraper import get_subjects, get_subject_html
from processor import process_courses, process_prerequisites

import os
import time

def main():
    database, cursor = connect_database()
    
    with open('sql/create_subjects.sql', 'r') as file:
        create_table = file.read()
        
    cursor.execute(create_table)
    
    cursor.execute('SELECT COUNT(*) FROM subjects')
    if cursor.fetchone()[0] < 217:
        print('Subjects not in database. Scraping...')
        get_subjects()
    else:
        print('Subjects already in database.')
    
    
    with open('sql/create_courses.sql', 'r') as file:
        create_table = file.read()
        
    cursor.execute(create_table)
    
    cursor.execute('SELECT code FROM subjects')
    subject_codes = [code[0] for code in  cursor.fetchall()]
    
    for subject_code in subject_codes:
        
        cursor.execute('SELECT id FROM subjects WHERE code = %s', (subject_code,))
        subject_id = cursor.fetchone()[0]
        
        cursor.execute('SELECT Count(*) FROM courses WHERE subject_id = %s', (subject_id,))
        course_count = cursor.fetchone()
        
        if course_count[0] != 0:
            print(f'{subject_code} courses already in database.')
            continue
            
        print(f'{subject_code} courses not in database. Scraping...')
        subject_html = get_subject_html(subject_code)
        print(f'Processing {subject_code} couses...')
        
        process_courses(subject_html, subject_id)
        print(f'Completed {subject_code} courses.')
        # time.sleep(1)
    
    with open('sql/create_prerequisites.sql', 'r') as file:
        create_table = file.read()
        
    cursor.execute(create_table)
    
    for subject in subject_codes:
        print(f'Processing {subject} prerequisites...')
        process_prerequisites(subject)
    
    database.commit()
    cursor.close()
    database.close()
    
    
if __name__ == '__main__':
    main()