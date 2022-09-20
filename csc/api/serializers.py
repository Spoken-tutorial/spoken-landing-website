from django.contrib.auth.models import User, Group


from rest_framework import serializers

from csc.models import Student, Student_certificate_course,CertifiateCategories
from csc.api.utility import send_pwd_mail

class CertifiateCategoriesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CertifiateCategories
        fields = ["category_cert","code","title"]

class StudentCertificateCourseSerializer(serializers.ModelSerializer):
    cert_category = serializers.SlugRelatedField(
        slug_field='code',
        queryset=CertifiateCategories.objects.all()
     )
    class Meta:
        model = Student_certificate_course
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
        fields = ["certificate_course","user","gender","dob","phone","edu_qualification","vle_id","state","city","district","pincode","address","date_of_registration","category","occupation"]

    
    def create(self, validated_data):
        user = validated_data.pop('user')
        user['username'] = user['email']
        
        try:
            User.objects.create(**user)
        except (Exception):
            raise serializers.ValidationError(f"Request Failed : User with email {user['email']} already exists.")
        u = User.objects.get(email=user['email'])
        course_data = validated_data.pop('certificate_course')
        vle_ids = validated_data.pop('vle_id')
        validated_data['user_id'] = u.id # validated_data updated
        student = Student.objects.create(**validated_data)
        student.vle_id.add(*vle_ids)
        for data in course_data:
            Student_certificate_course.objects.create(student=student, **data)
        student_group = Group.objects.get(name='STUDENT') 
        student_group.user_set.add(u)
        send_pwd_mail(u)
        return student

    def update(self,instance,validated_data):
        student = instance
        user_obj = student.user
        has_user = 'user' in validated_data 
        has_courses = 'certificate_course' in validated_data 
        has_vle_ids = 'vle_id' in validated_data 
        user = []
        course_data = []
        vle_ids = []
        if has_user : user = validated_data.pop('user')
        if has_courses : course_data = validated_data.pop('certificate_course')
        if has_vle_ids : vle_ids = validated_data.pop('vle_id')
       
        instance = super(StudentSerializer,self).update(instance,validated_data)
        existing_courses = [x.cert_category for x in student.certificate_course.all()]
        
        for data in course_data:
            if data['cert_category'] in existing_courses:
                continue
            Student_certificate_course.objects.create(student=student, **data)

        if has_user:
            s = UserSerializer(user_obj,data=user)
            if s.is_valid():
                s.save()
        for item in vle_ids:
            student.vle_id.add(*vle_ids)

        return instance


    def validate_certificate_course(self, value):
        if not value:
            raise serializers.ValidationError("certificate_course field cannot be empty")
        courses = []
        for item in value:
            if item['cert_category'] in courses:
                raise serializers.ValidationError(f"Duplicate entry for {item['cert_category']}")
            else:
                courses.append(item['cert_category'])
        return value



