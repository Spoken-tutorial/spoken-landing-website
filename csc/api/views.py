from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from csc.api.serializers import StudentSerializer,VLECSCSerializer
from csc.models import Student, VLE

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
    