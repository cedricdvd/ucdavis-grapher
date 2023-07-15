from django.db import models

# Create your models here.
class Subject(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=60)

class Course(models.Model):
    code = models.CharField(max_length=20)
    title = models.TextField()
    description = models.TextField(null=True)
    prerequisites = models.TextField(null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    
class Prerequisite(models.Model):
    subject_id = models.ForeignKey(Subject, default=-1, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    prerequisite_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='prerequisite_id', null=True)
    prerequisite_code = models.CharField(max_length=20)
    group_num = models.IntegerField()
