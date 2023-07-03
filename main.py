from connector import connect_database
from scraper import get_subjects, get_subject_html

import os
import time

def main():
    database, cursor = connect_database()
    
    with open('sql/create_subjects.sql', 'r') as file:
        create_subjects_sql = file.read()
        
    cursor.execute(create_subjects_sql)
    
    cursor.execute('SELECT COUNT(*) FROM subjects')
    if cursor.fetchone()[0] < 217:
        print('Subjects not in database. Scraping...')
        get_subjects()
    else:
        print('Subjects already in database.')
    
    cursor.execute('SELECT code FROM subjects')
    subject_codes = cursor.fetchall()
    
    # os.makedirs('html', exist_ok=True)
    for subject_code in subject_codes:
        code = subject_code[0]
        if not os.path.exists(f'html/{code}.html'):
            print(f'{code} not in directory. Scraping...')
            print(get_subject_html(code))
            time.sleep(0.5)
        else:
            print(f'{code} already in directory.')
    
    cursor.close()
    database.close()
    
    
if __name__ == '__main__':
    main()