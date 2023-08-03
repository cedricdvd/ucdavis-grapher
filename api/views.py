from rest_framework.response import Response
from rest_framework.decorators import api_view
from scraperapp.models import Subject, Course, Prerequisite
from .serializers import SubjectSerializer, CourseSerializer, PrerequisiteSerializer


@api_view(['GET'])
def getData(request):
    subjects = Subject.objects.all()
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def subjectDetail(request, subj):
    subjects = Subject.objects.get(code=subj)
    serializer = SubjectSerializer(subjects, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def subjectCourses(request, subj):
    subject = Subject.objects.get(code=subj)
    courses = Course.objects.filter(subject=subject.id)
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def courseDetails(request, course_code):
    course = Course.objects.get(code=course_code)
    prerequisites = Prerequisite.objects.filter(course_id=course.id)
    course_serializer = CourseSerializer(course, many=False)
    prerequisite_serializer = PrerequisiteSerializer(prerequisites, many=True)
    return Response(course_serializer.data)


@api_view(['GET'])
def prerequisiteDetails(request, course_code):
    course = Course.objects.get(code=course_code)
    prerequisites = Prerequisite.objects.filter(course_id=course.id)
    serializer = PrerequisiteSerializer(prerequisites, many=True)
    return Response(serializer.data)