from django.db import models


# Create your models here.
class Subject(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.name} ({self.code})'


class Course(models.Model):
    code = models.CharField(max_length=20)
    title = models.TextField()
    description = models.TextField(null=True)
    prerequisites = models.TextField(null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject')

    def __str__(self):
        return f'{self.code} - {self.title}'


class Prerequisite(models.Model):
    subject_id = models.ForeignKey(Subject, default=-1, on_delete=models.CASCADE, related_name='subject_id')
    course_code = models.CharField(max_length=20)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_id')
    prerequisite_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='prerequisite_id', null=True)
    prerequisite_code = models.CharField(max_length=20)
    group_num = models.IntegerField()

    def __str__(self):
        return f'{self.prerequisite_code} ({self.course_id}, {self.group_num})'
