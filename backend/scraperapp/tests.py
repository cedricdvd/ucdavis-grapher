from django.test import TestCase
from scraperapp.models import Subject
from django.db import IntegrityError

# Create your tests here.
class SubjectTestCase(TestCase):
    def test_subject_creation(self):
        subject = Subject(code='ABC', name='Test Subject')
        
        self.assertEqual(subject.code, 'ABC')
        self.assertEqual(subject.name, 'Test Subject')
    