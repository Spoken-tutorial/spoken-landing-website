from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from csc.api.serializers import StudentSerializer
from csc.models import Student

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
    

    