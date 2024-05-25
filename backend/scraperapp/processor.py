from .models import Subject, Course, Prerequisite
from .web_crawler import fetch_urls, store_to_file
from .constants import IGNORE_SUBJECTS, LOG_DIR, MAX_WORKERS
from bs4 import BeautifulSoup as bs
import re
import logging
import os

logger = logging.getLogger('processor')
logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'scraperapp.log'),
    filemode='a',
    encoding='utf-8',
    level=logging.DEBUG,
)

def create_soup(html_file_path):
    # Open HTML and read contents
    with open(html_file_path, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

    soup = bs(html_content, 'html.parser')
    return soup

def process_catalog(catalog_file):
    soup = create_soup(catalog_file)

    subjects = soup.find_all('a', {'href': re.compile(r'^/courses-subject-code/[a-z]+')})
    length = len(subjects)
    ignore_count = 0

    for i, subject in enumerate(subjects):
        subject.text.replace('\u200b', '')
        subject_name, subject_code = re.search(r'(.+) \(([A-Z]{3})\)', subject.text).groups()

        if subject_code in IGNORE_SUBJECTS:
            logger.debug(f'Ignoring {subject_code}')
            ignore_count += 1
            continue

        try:
            obj = Subject.objects.get(code=subject_code)

            setattr(obj, 'code', subject_code)
            setattr(obj, 'name', subject_name)
            obj.save()
            logger.debug(f'Entry {subject_code} Updated')
        except Subject.DoesNotExist:
            obj = Subject(code=subject_code, name=subject_name)
            obj.save()
            logger.debug(f'Entry {subject_code} Saved')

def process_subjects(subject_paths):
    length = len(subject_paths)
    course_count = 0

    for i, (code, filepath) in enumerate(subject_paths):
        course_count += process_subject(code, filepath)
        logger.debug(f'Processed {code} courses')

    logger.info(f'Processed {course_count} total courses')

def process_subject(subject_code, filepath):

    soup = create_soup(filepath)
    courses = soup.find_all('div', {'class': 'courseblock'})
    obj = Subject.objects.get(code=subject_code)

    for course in courses:
        process_course(course, obj)

    return len(courses)

def process_course(course_html, subject_obj):

    soup = bs(str(course_html), 'html.parser')
    course = dict()
    course['code'] = soup.find('span', {'class': 'detail-code'}).text.strip()
    
    course['title'] = soup.find('span', {'class': 'detail-title'}).text.strip()[2:]
    description = soup.find('p', {'class': 'courseblockextra noindent'}).text.strip()
    course['description'] = description.removeprefix('Course Description: ')
    
    prerequisites = soup.find('p', {'class': 'detail-prerequisite'})
    if prerequisites is not None:
        prerequisites = prerequisites.text.strip()
        prerequisites = prerequisites.removeprefix('Prerequisite(s): ')
        prerequisites = prerequisites.removesuffix('.')
        prerequisites = prerequisites.replace('\xa0', ' ')

    course['prerequisites'] = prerequisites
    course['subject'] = subject_obj

    try:
        obj = Course.objects.get(code=course['code'])

        for key, val in course.items():
            setattr(obj, key, val)

        obj.save()

    except Course.DoesNotExist:
        obj = Course(
            code=course['code'],
            title=course['title'],
            subject=course['subject'],
            description=course['description'],
            prerequisites=course['prerequisites']
        )
    
        obj.save()

def process_prerequisites(subjects):

    prereq_count = 0
    length = len(subjects)

    for i, obj in enumerate(subjects):
        courses = Course.objects.filter(subject=obj, prerequisites__isnull=False)

        for course in courses:
            prereq_count += process_prerequisite(course, obj)

        logger.debug(f'Finished processing {obj.code} prerequisites')

    logger.info(f'Processed {prereq_count} total prerequisites')


def process_prerequisite(course_obj, subject_obj):
    prereq_count = 0

    prerequisite_string = course_obj.prerequisites.replace(' C- or better', '')
    
    # Clean description, split CNF into separate disjunctions
    prerequisite_list = prerequisite_string.split(';')
    
    # Splits prerequisite list into course groups
    groups = parse_groups(prerequisite_list)
    
    # Processes each group into table
    for group_num, group in enumerate(groups):
        prereq_count += process_group(group_num, group, course_obj, subject_obj)

    return prereq_count


def parse_groups(prerequisite_list):
    groups = []
    for group in prerequisite_list:
        
        # Extract courses
        prereqs = re.findall(r'[A-Z]{3} [0-9]{3}[A-Z]{,2}', group)
        
        # Skip if no courses to process
        if len(prereqs) == 0:
            continue
        
        groups.append(prereqs)
        
    return groups


def process_group(group_num, group, course_obj, subject_obj):

    for prerequisite_code in group:
        # Check if course exists
        try:
            prerequisite_obj = Course.objects.get(code=prerequisite_code)
        except Course.DoesNotExist:
            prerequisite_obj = None

        try:
            obj = Prerequisite.objects.get(
                subject_id = subject_obj,
                course_id = course_obj,
                prerequisite_id = prerequisite_obj,
            )

            setattr(obj, 'subject_id', subject_obj)
            setattr(obj, 'course_id', course_obj)
            setattr(obj, 'course_code', course_obj.code)
            setattr(obj, 'prerequisite_id', prerequisite_obj)
            setattr(obj, 'prerequisite_code', prerequisite_code)
            setattr(obj, 'group_num', group_num)

            obj.save()
        except Prerequisite.DoesNotExist:
            obj = Prerequisite(
                subject_id  = subject_obj,
                course_id = course_obj,
                course_code = course_obj.code,
                prerequisite_id = prerequisite_obj,
                prerequisite_code = prerequisite_code,
                group_num = group_num
            )

            obj.save()

    return len(group)