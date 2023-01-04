from functools import partial
from django.contrib.auth.models import User, Group


from rest_framework import serializers

from csc.models import Student, Student_certificate_course,CertifiateCategories, VLE, CSC, Transaction,CategoryCourses,Student_Foss
from csc.api.utility import send_pwd_mail,map_foss_to_student

from csc.utils import getFirstName,getLastName

from django.contrib.auth.hashers import make_password
import random
import string
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

class UserForVLESerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]

class VLESerializer(serializers.ModelSerializer):
    user = UserForVLESerializer()
    class Meta:
        model = VLE
        fields = ["user"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name","last_name","email"]


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    certificate_course = StudentCertificateCourseSerializer(many=True)
    vle_id = VLESerializer(many=True)
    
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
        vle_email = vle_ids[0]['user']['email']
        validated_data['user_id'] = u.id # validated_data updated
        student = Student.objects.create(**validated_data)
        try:
            vle_spk = VLE.objects.get(user__email=vle_email)
            student.vle_id.add(vle_spk.id)
        except User.DoesNotExist:
            raise serializers.ValidationError(f"User with email {vle_email} does not exists.")
        for data in course_data:
            Student_certificate_course.objects.create(student=student, **data)
        student_group = Group.objects.get(name='STUDENT') 
        student_group.user_set.add(u)
        send_pwd_mail(u)
        #map courses
        map_foss_to_student(student)
        
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
            map_foss_to_student(instance,fdate=data['programme_starting_date'])

        if has_user:
            s = UserSerializer(user_obj,data=user)
            if s.is_valid():
                s.save()
            # if 'email' in user:
            #     send_pwd_mail(user_obj)
            if "email" in user:
                user_obj.username = user['email']
                user_obj.email = user['email']
                user_obj.save()
                send_pwd_mail(user_obj)
                student.mdl_mail_sent = 1
                student.save()
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
    
    def validate_vle_id(self, value):
        vle_email = value[0]['user']['email']
        if not User.objects.filter(email=vle_email).exists():
            raise serializers.ValidationError(f"VLE with email {vle_email} does not exist.")
        
        return value


class VLEUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')
    name = serializers.CharField(write_only = True)
    
    def get_full_name(self, user):
        return f"{user.first_name} {user.last_name}"
        
    class Meta:
        model = User
        fields = ['email','full_name','name']

class CSCSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSC
        fields = ['csc_id','institute','state','city','district','block','address','pincode','plan']
        
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['transcdate']
        
class VLECSCSerializer(serializers.ModelSerializer):
    csc = CSCSerializer()
    user = VLEUserSerializer()
    transaction_date = TransactionSerializer(many=True)
    class Meta:
        model = VLE
        fields = ['csc','user','phone','transaction_date']
        
    def create(self, validated_data):
        user = {}
        userdata = validated_data.pop('user')
        user['username'] = userdata['email']
        user['email'] = userdata['email']
        user['first_name'] = getFirstName(userdata['name'])
        user['last_name'] = getLastName(userdata['name'])
        try:
            User.objects.create(**user)
        except Exception as e:
            raise serializers.ValidationError(f"Request Failed : User with email {user['email']} already exists.")
        u = User.objects.get(email=user['email'])
        csc_data = validated_data.pop('csc')
        s = CSCSerializer(data=csc_data)
        s.is_valid(raise_exception=True)
        obj = s.save()
        transaction_data = validated_data.pop('transaction_date')
        validated_data['user_id'] = u.id # validated_data updated
        validated_data['csc_id'] = obj.id # validated_data updated
        vle = VLE.objects.create(**validated_data)
        vle_group = Group.objects.get(name='VLE') 
        vle_group.user_set.add(u)
        t = Transaction.objects.create(vle=vle,csc=obj,transcdate=transaction_data[0]['transcdate'])
        send_pwd_mail(u)
        return vle
    
    def validate_user(self, value):
        try:
            vle_email = value['email']
            if User.objects.filter(email=vle_email).exists():
                raise serializers.ValidationError(f"VLE with email {vle_email} already exist.")
        except Exception as e:
            print(e)
        
        return value
    
    def update(self,instance,validated_data):
        vle = instance
        has_user = 'user' in validated_data 
        has_transaction = 'transaction_date' in validated_data 
        has_csc = 'csc' in validated_data 
        
        if has_csc : csc_data = validated_data.pop('csc')
        if has_transaction : transaction_data = validated_data.pop('transaction_date')[0]
        if has_user : user_data = validated_data.pop('user')
        instance = super(VLECSCSerializer,self).update(instance,validated_data)
        if has_csc:
            c = CSCSerializer(instance.csc,csc_data,partial=True)
            c.is_valid(raise_exception=True)
            c.save()
        if has_transaction : 
            t = Transaction.objects.create(vle=instance,csc=instance.csc,transcdate=transaction_data['transcdate'])
        if has_user:
            user_obj = instance.user
            if "email" in user_data:
                user_obj.username = user_data['email']
                user_obj.email = user_data['email']
                user_obj.save()
                send_pwd_mail(user_obj)
                
            if "name" in user_data:
                user_obj.first_name = getFirstName(user_data['name'])
                user_obj.last_name = getLastName(user_data['name'])

            user_obj.save()
            # u = VLEUserSerializer(instance.user,user_data,partial=True)
            # u.is_valid(raise_exception=True)
            # u.save()

        return instance