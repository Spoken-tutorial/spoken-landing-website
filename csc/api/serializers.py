from django.contrib.auth.models import User, Group


from rest_framework import serializers

from csc.models import Student, Student_certificate_course,CertifiateCategories
from csc.api.utility import send_pwd_mail

class CertifiateCategoriesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CertifiateCategories
        fields = ["category_cert","code","title"]

class StudentCertificateCourseSerializer(serializers.ModelSerializer):
    # cert_category = serializers.StringRelatedField()
    cert_category = serializers.SlugRelatedField(
        slug_field='code',
        queryset=CertifiateCategories.objects.all()
     )
    class Meta:
        model = Student_certificate_course
        # fields = ["cert_category", "programme_starting_date"]
        fields = ["cert_category","programme_starting_date"]



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name","last_name","email"]


        
class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    certificate_course = StudentCertificateCourseSerializer(many=True)
    
    class Meta:
        model = Student
        fields = ["certificate_course","user","gender","dob","phone","edu_qualification","vle_id","state","city","district","pincode","address","date_of_registration"]
    
    def create(self, validated_data):
        user = validated_data.pop('user')
        user['username'] = user['email']
        
        try:
            User.objects.create(**user)
        except (Exception):
            raise serializers.ValidationError(f"Request Failed : User with email {user['email']} already exists.")
        u = User.objects.get(email=user['email'])
        print(f"user  : {u}")
        course_data = validated_data.pop('certificate_course')
        vle_ids = validated_data.pop('vle_id')
        print(f"vle_ids ---- {vle_ids}")
        validated_data['user_id'] = u.id # validated_data updated
        student = Student.objects.create(**validated_data)
        student.vle_id.add(*vle_ids)
        for data in course_data:
            Student_certificate_course.objects.create(student=student, **data)
        student_group = Group.objects.get(name='STUDENT') 
        student_group.user_set.add(u)
        send_pwd_mail(u)
        return student




