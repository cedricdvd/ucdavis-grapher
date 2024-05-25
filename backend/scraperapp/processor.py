from .models import Subject, Course, Prerequisite
from .web_crawler import fetch_urls, store_to_file
from .constants import IGNORE_SUBJECTS
from bs4 import BeautifulSoup as bs
import re

def create_soup(html_file_path):
    # Open HTML and read contents
    with open(html_file_path, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

    soup = bs(html_content, 'html.parser')
    return soup

def process_catalog(catalog_file):
    soup = create_soup(catalog_file)

    subjects = soup.find_all('a', {'href': re.compile(r'^/courses-subject-code/[a-z]+')})

    for subject in subjects:
        subject.text.replace('\u200b', '')
        subject_name, subject_code = re.search(r'(.+) \(([A-Z]{3})\)', subject.text).groups()

        if subject_code in IGNORE_SUBJECTS:
            print(f'Ignoring {subject_code}')
            continue

        try:
            obj = Subject.objects.get(code=subject_code)

            setattr(obj, 'code', subject_code)
            setattr(obj, 'name', subject_name)
            obj.save()
            print(f'Entry {subject_code} Updated')
        except Subject.DoesNotExist:
            obj = Subject(code=subject_code, name=subject_name)
            obj.save()
            print(f'Entry {subject_code} Saved')

# def process_courses(subject_html, subject_obj):
    
#     for course in subject_html:
#         soup = bs(str(course), 'html.parser')
#         course_code = soup.find('span', {'class': 'detail-code'}).text.strip()
        
#         # Skip objects already in database
#         if Course.objects.filter(code=course_code).exists():
#             continue
        
#         title = soup.find('span', {'class': 'detail-title'}).text.strip()[2:]
#         description = soup.find('p', {'class': 'courseblockextra noindent'}).text.strip()
#         description = description.removeprefix('Course Description: ')
        
#         prerequisites = soup.find('p', {'class': 'detail-prerequisite'})
#         if prerequisites is not None:
#             prerequisites = prerequisites.text.strip()
#             prerequisites = prerequisites.removeprefix('Prerequisite(s): ')
#             prerequisites = prerequisites.removesuffix('.')
#             prerequisites = prerequisites.replace('\xa0', ' ')
            
#         course_object = Course(
#             code=course_code,
#             title=title,
#             subject=subject_obj,
#             description=description,
#             prerequisites=prerequisites
#         )
        
#         course_object.save()


# def process_prerequisites(subject_obj):
#     courses = Course.objects.filter(subject=subject_obj, prerequisites__isnull=False)
    
#     for course in courses:
#         # Get course id and prerequisites
#         prerequisite_string = course.prerequisites.replace(' C- or better', '')
        
#         # Clean description, split CNF into separate disjunctions
#         prerequisite_list = prerequisite_string.split(';')
        
#         # Splits prerequisite list into course groups
#         groups = parse_groups(prerequisite_list)
        
#         # Processes each group into table
#         for group_num, group in enumerate(groups):
#             process_group(group_num, group, course, subject_obj)
        
        
        
# def parse_groups(prerequisite_list):
#     groups = []
#     for group in prerequisite_list:
        
#         # Extract courses
#         prereqs = re.findall(r'[A-Z]{3} [0-9]{3}[A-Z]{,2}', group)
        
#         # Skip if no courses to process
#         if len(prereqs) == 0:
#             continue
        
#         groups.append(prereqs)
        
#     return groups


# def process_group(group_num, group, course_obj, subject_obj):
#     for prerequisite_code in group:
#         try:
#             prerequisite_obj = Course.objects.get(code=prerequisite_code)
#         except Course.DoesNotExist:
#             prerequisite_obj = None
            
#         prerequisite_object = Prerequisite(
#             subject_id  = subject_obj,
#             course_id = course_obj,
#             course_code = course_obj.code,
#             prerequisite_id = prerequisite_obj,
#             prerequisite_code = prerequisite_code,
#             group_num = group_num
#         )
#         prerequisite_object.save()
