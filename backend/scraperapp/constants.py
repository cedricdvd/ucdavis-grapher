# URLs
CATALOG_URL = 'https://catalog.ucdavis.edu/courses-subject-code/'
SUBJECT_URL_FORMAT = 'https://catalog.ucdavis.edu/courses-subject-code/{}/'
ASYNCIO_URL = 'https://catalog.ucdavis.edu'
ASYNCIO_FORMAT = '/courses-subject-code/{}/'

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