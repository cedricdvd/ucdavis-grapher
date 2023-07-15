from connector import connect_database
from bs4 import BeautifulSoup as bs
import re


def process_courses(subject_html, subject_id):
    '''Processes courses from a subject and adds them to the database
    
    Courses are in the form:
    
    <div class="courseblock">
        <h3 class="cols noindent">
            <span class="text courseblockdetail detail-code margin--span text--semibold text--big">
                <b>{course_code}</b>
            </span>
            <span class="text courseblockdetail detail-title margin--span text--semibold text--big">
                <b>- {course_title}</b>
            </span>
            ...
        </h3>
        ...
        <p class="courseblockextra noindent">
            <em>Course Description:</em> {description}
        </p></div><div class="noindent">
        <p class="text courseblockdetail detail-prerequisite">
            <i>Prerequisite(s): </i> {prerequistes}
        </p></div><div class="noindent notinpdf">
    <div class="courseblockextra noindent">
    '''

    database, cursor = connect_database()
    
    for course in subject_html:
        
        soup = bs(str(course), 'html.parser')
        course_code = soup.find('span', {'class': 'detail-code'}).text.strip()
        title = soup.find('span', {'class': 'detail-title'}).text.strip()[2:]
        description = soup.find('p', {'class': 'courseblockextra noindent'}).text.strip()
        description = description.removeprefix('Course Description: ')
        
        cursor.execute('INSERT INTO courses (course_code, title, subject_id, course_description) VALUES (%s, %s, %s, %s)', (course_code, title, subject_id, description))
        
        prerequisites = soup.find('p', {'class': 'detail-prerequisite'})
        
        if prerequisites is not None:
            prerequisites = prerequisites.text.strip()
            prerequisites = prerequisites.removeprefix('Prerequisite(s): ')
            prerequisites = prerequisites.removesuffix('.')
            prerequisites = prerequisites.replace('\xa0', ' ')
            
            cursor.execute('UPDATE courses SET prerequisites = %s WHERE course_code = %s', (prerequisites, course_code))
            
    database.commit()
    cursor.close()
    database.close()


def process_prerequisites(subject_code):
    '''Processes prerequisites for a subject and adds them to the database
    
    Prerequisites are in Conjunctive Normal Form (CNF) and look as follows:
        (A or B or C); (D or E or F); (G); (H or I)
    '''
    database, cursor = connect_database()
    
    # Get courses with prerequisites
    cursor.execute('SELECT id, prerequisites FROM courses WHERE subject_id = (SELECT id FROM subjects WHERE code = %s) AND prerequisites IS NOT NULL', (subject_code,))
    courses = cursor.fetchall()
    
    # Loop through courses
    for course_id, prerequisite_list in courses:
        # Keep track of gropus in CNF
        group_id = 1
        
        # Clean description, split CNF into separate disjunctions
        prerequisite_list = prerequisite_list.replace(' C- or better', '')
        prerequisite_list = prerequisite_list.split(';')
        
        # Parse each disjunction
        for group in prerequisite_list:
            
            # Extract courses
            prereq_courses = re.findall(r'[A-Z]{3} [0-9]{3}[A-Z]{,2}', group)
            
            # Skip is no courses to process
            if len(prereq_courses) == 0:
                continue
            
            # Extract prereq_id and insert into database
            for prereq_code in prereq_courses:
                cursor.execute('SELECT id FROM courses WHERE course_code = %s', (prereq_code,))
                prereq_id = cursor.fetchone()
                if prereq_id is not None:
                    prereq_id = prereq_id[0]
                
                # Insert prerequisite into table
                cursor.execute('INSERT INTO prerequisites (group_num, course_id, prerequisite_code, prerequisite_id) VALUES (%s, %s, %s, %s)', (group_id, course_id, prereq_code, prereq_id))
                
            group_id += 1
    
    database.commit()
    cursor.close()
    database.close()
    
    return 0

if __name__ == '__main__':
    process_prerequisites('EAE')
