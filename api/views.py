from rest_framework.response import Response
from rest_framework.decorators import api_view
from scraperapp.models import Subject, Course, Prerequisite
from .serializers import SubjectSerializer, CourseSerializer, PrerequisiteSerializer


@api_view(['GET'])
def getSubjects(request):
    subjects = Subject.objects.all()
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getSubjectCourses(request, subject_code):
    subject = Subject.objects.get(code=subject_code)
    courses = Course.objects.filter(subject=subject.id)
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def searchCourses(request, keyword):
    keyword = keyword.upper()
    courses = Course.objects.filter(code__startswith=keyword)
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getCourse(request, keyword):
    keyword = keyword.upper()
    course = Course.objects.get(code=keyword)
    serializer = CourseSerializer(course, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getPrerequisites(request, course_code):
    course = Course.objects.get(code=course_code)
    prerequisites = Prerequisite.objects.filter(course_id=course.id)
    serializer = PrerequisiteSerializer(prerequisites, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getSuccessors(request, course_code):
    course = Course.objects.get(code=course_code)
    prerequisites = Prerequisite.objects.filter(prerequisite_id=course.id)
    serializer = PrerequisiteSerializer(prerequisites, many=True)
    return Response(serializer.data)
