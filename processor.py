# <div class="courseblock">
#   <h3 class="cols noindent">
#       <span class="text courseblockdetail detail-code margin--span text--semibold text--big"> -- course code
#           <b>EAE 140</b>
#       </span>
#       <span class="text courseblockdetail detail-title margin--span text--semibold text--big"> -- course title
#           <b>— Rocket Propulsion</b>
#       </span>
#       <span class="text courseblockdetail detail-hours_html margin--span text--semibold text--big"> -- units
#           <b>(4 units)</b>
#       </span>
#   </h3>
# <div class="noindent"></div>
# <div class="noindent">
#   <p class="courseblockextra noindent"> -- description
#       <em>Course Description:</em> Fluid and thermodynamics of rocket engines, liquid and solid rocket propulsion. Space propulsion concepts and space mission requirements.
#   </p></div><div class="noindent">
#   <p class="text courseblockdetail detail-prerequisite"> -- prerequisites
#       <i>Prerequisite(s): </i><a class="bubblelink code" href="/search/?P=EME%20106" onclick="return showCourse(this, 'EME 106');" title="EME 106">EME 106</a> C- or better.
#   </p></div><div class="noindent notinpdf">
# <div class="courseblockextra noindent">
# <h4 class="toggle bubble-hide"></h4>
# <ul>
# <li><span class="label"><em>Learning Activities:</em></span> Lecture 4 hour(s).</li>
# <li><span class="label"><em>Enrollment Restriction(s):</em></span> Restricted to upper division standing.</li>
# <li><span class="label"><em>Credit Limitation(s):</em></span> Not open for credit to students who have taken identical EAE 189A prior to Fall Quarter 2013.</li>
# <li><span class="label"><em>Grade Mode:</em></span> Letter.</li>
# <li><span class="label"><em>General Education:</em></span> Science &amp; Engineering (SE).</li></ul>

from connector import connect_database
from bs4 import BeautifulSoup as bs
import re

def process_courses(subject_html, subject_id):
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
    database, cursor = connect_database()
    
    cursor.execute('SELECT id, prerequisites FROM courses WHERE subject_id = (SELECT id FROM subjects WHERE code = %s) AND prerequisites IS NOT NULL', (subject_code,))
    courses = cursor.fetchall()
    
    # Loop through course
    for course_id, prerequisites in courses:
        # Ignore C- or better
        prerequisites = prerequisites.replace(' C- or better', '')
        
        # Parse "and"
        prerequisites = prerequisites.split(';')
        
        # Parse each disjunction
        for prerequisite in prerequisites:
            
            # Extract courses
            prereq_course = re.findall(r'[A-Z]{3} [0-9]{3}[A-Z]{,2}', prerequisite)
            for course in prereq_course:
                
                # Get course_id if exists and insert into database
                cursor.execute('SELECT id FROM courses WHERE course_code = %s', (course,))
                prerequisite_id = cursor.fetchone()
                if prerequisite_id is None:
                    continue
                prerequisite_id = prerequisite_id[0]
                cursor.execute('INSERT INTO prerequisites (course_id, prerequisite_id) VALUES (%s, %s)', (course_id, prerequisite_id))
    
    database.commit()
    cursor.close()
    database.close()
    
    return 0

if __name__ == '__main__':
    process_prerequisites('EAE')
