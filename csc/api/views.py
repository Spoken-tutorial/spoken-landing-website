from rest_framework import generics,status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse,HttpResponse

from csc.api.serializers import StudentSerializer,VLECSCSerializer
from csc.models import Student, VLE, Student_Foss,CategoryCourses,CSCTestAtttendance
from csc.utils import TEST_COMPLETED_BY_STUDENT,PASS_GRADE
import json

class StudentListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class SutdentDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    lookup_field = "user__email"
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
class VLEListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = VLE.objects.all()
    serializer_class = VLECSCSerializer
    
class VLEDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    lookup_field = "user__email"
    queryset = VLE.objects.all()
    serializer_class = VLECSCSerializer
    
def studentTest(request,user__email):
    d = {}
    d['email'] = user__email
    try:
        student = Student.objects.get(user__email=user__email)
        courses = set()
        cert_categories = [courses.add(x.cert_category) for x in Student_Foss.objects.filter(student=student)]
        scores = {}
        ta = CSCTestAtttendance.objects.filter(student=student,status__gte=TEST_COMPLETED_BY_STUDENT)
        for item in ta:
            scores[item.test.foss.foss] = item.mdlgrade
        for course in courses:
            d[course.code] = {
                'title' : course.title
            }
            fosses = [x.foss for x in CategoryCourses.objects.filter(certificate_category=course)]
            temp = dict()
            for foss in fosses:
                temp[foss.foss] = scores.get(foss.foss,'NA')
                
            d[course.code]['foss'] = temp
            b = [ x == 'NA' or float(x) < PASS_GRADE for x in temp.values()]
            if True in b:
                d[course.code]['status'] = 0
            else:
                d[course.code]['status'] = 1
    except Student.DoesNotExist as e:
        return HttpResponse(status=404)
    return JsonResponse(d)
    
    