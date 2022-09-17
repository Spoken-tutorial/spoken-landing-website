from rest_framework import generics
from rest_framework.authentication import TokenAuthentication,BaseAuthentication
from rest_framework.permissions import IsAuthenticated

from csc.api.serializers import StudentSerializer,StudentCertificateCourseSerializer
from csc.models import Student

# from rest_framework_swagger.views import get_swagger_view
# schema_view = get_swagger_view(title='Pastebin API')

class StudentListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class SutdentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    lookup_field = "user__email"
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    

    