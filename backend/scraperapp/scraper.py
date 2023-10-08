from .models import Course, Prerequisite
from bs4 import BeautifulSoup as bs
import re

class Scraper:
    
    def __init__(self):
        self.COURSE_CODE_PATTERN = r'[A-Z]{3} [0-9]{3}[A-Z]{,2}'
        self.successor_map = dict()     # < course code > : < successor's prerequisite object >
        self.course_id = dict()         # < course code > : < course object >
        
    def process_course(self, course_html, subject_obj):
        soup = bs(course_html, 'html.parser')
        code = soup.find('span', {'class': 'detail-code'}).text.strip()
        
        # Skip object if already in database
        if code in self.course_id:
            return None
        
        title = soup.find('span', {'class': 'detail-title'}).text.strip()[2:]
        description = soup.find('p', {'class': 'courseblockextra noindent'}).text.strip()
        description = description.removeprefix('Course Description: ')
        
        prereq_str = soup.find('p', {'class': 'detail-prerequisite'})
        if prereq_str is not None:
            prereq_str = prereq_str.text.strip()
            prereq_str = prereq_str.removeprefix('Prerequisite(s): ')
            prereq_str = prereq_str.removesuffix('.')
            prereq_str = prereq_str.replace('\xa0', ' ')
            
        course_obj = Course(
            code=code,
            title=title,
            subject=subject_obj,
            description=description,
            prerequisites=prereq_str
        )
        
        self.course_id[code] = course_obj
        course_obj.save()
        return course_obj

        
    def update_successors(self, course_obj):
        if course_obj.code not in self.successor_map:
            return
        
        successor_arr = self.successor_map[course_obj.code]
        
        # Map course object to successor
        for successor in successor_arr:
            successor.prerequisite_id = course_obj
            successor.save()
            
        return
    
    def process_prerequisites(self, subject_obj, course_obj):
        if course_obj.prerequisites is None:
            return
        
        # Clean prerequisite str and split CNF into separate strings
        prereq_str = course_obj.prerequisites.replace(' C- or better', '') # NOTE: can probably remove this
        prereq_arr = prereq_str.split(';')
        
        # Organize strings into groups of course codes
        group_num = 0
        for group in prereq_arr:
            codes = re.findall(self.COURSE_CODE_PATTERN, group)
            
            # Skip if no courses to process
            if len(codes) == 0:
                continue
            
            # Process prerequisites into database
            for prereq_code in codes:
                prereq_obj = Prerequisite(
                    subject_id = subject_obj,
                    course_id = course_obj,
                    course_code = course_obj.code,
                    prerequisite_id = None,
                    prerequisite_code = prereq_code,
                    group_num = group_num
                )
                
                # Checks if prerequisite course already processed
                if prereq_code in self.course_id:
                    prereq_obj.prerequisite_id = self.course_id[prereq_code]
                elif prereq_code in self.successor_map:
                    self.successor_map[prereq_code].append(prereq_obj)
                else:
                    self.successor_map[prereq_code] = [prereq_obj]
                    
                prereq_obj.save()
