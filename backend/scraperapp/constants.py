# URLs
CATALOG_URL = 'https://catalog.ucdavis.edu/courses-subject-code/'
SUBJECT_URL = 'https://catalog.ucdavis.edu/courses-subject-code/{}/'

# Database handling
IGNORE_SUBJECTS = [
    'MMG', # Courses coming soon
    'DVM', # Courses are not displayed
    'PDF',
]

# HTML Path
DATA_DIR = './scraperapp/html_data'
SUBJECT_DIR = 'subjects'
LOG_DIR = './scraperapp/logs'

MAX_THREADS = 32
MAX_PROCESSES = 1