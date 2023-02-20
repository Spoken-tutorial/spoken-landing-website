from datetime import date

from csc.api.views import StudentListCreate,SutdentDetail
from csc.models import CSC, VLE, Student, Transaction
from csc.api.serializers import StudentSerializer

from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.urls import reverse

import pytest


class BaseCreationTests(APITestCase):
    databases = '__all__'

    @pytest.mark.django_db()
    def setUp(self):
        check_admin = User.objects.filter(username="test_admin")
        if not check_admin:
            self.user = User.objects.create_superuser('test_admin', 'testadmin@admin.com', 'testadminpass')
        else:
            self.user = User.objects.get(username='testadmin')
        self.token = Token.objects.create(user=self.user)

        # Create CSC
        self.test_csc = CSC.objects.create(
            csc_id="test_csc",
            institute="1",
            state="Tamil Nadu",
            district="Dindigul",
            plan="Testing",
        )
        # Create VLE
        self.test_vle = VLE.objects.create(
            csc=self.test_csc,
            user=self.user,
            phone="9990001111",
        )
        # Create student user
        self.test_student_user = User.objects.create_user(
            username='Test Student Name',
            email='test@teststudent.com',
            password='testpassword',
            first_name="First", last_name="Last"
        )
        # Create student
        self.test_student = Student.objects.create(
            student_id="Test Student ID",
            user=self.test_student_user,
            phone="9990002222",
        )
        # Create transaction
        self.test_transaction = Transaction.objects.create(
            vle=self.test_vle,
            csc=self.test_csc,
            tenure="quarterly",
            transcdate=date.fromisoformat('2030-12-01')
        )

    def test_successful_response_status(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(reverse('detail_student', kwargs={'user__email': 'JP.KASBA@GMAIL.COM'}), format='json')
        # response = self.client.get(reverse('create_list_student'), format='json') # HTTP_AUTHORIZATION=self.token 

        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_response(self):
        response = self.client.get(reverse('detail_student', kwargs={'user__email': 'JP.KASBA@GMAIL.COM'}), format='json')

        self.assertEqual(response.status_code, 401)

    def test_not_found_response(self):
        self.client.force_authenticate(self.user)
        unidentified_email = "unidentified@email.com"
        response = self.client.get(reverse('detail_student', kwargs={'user__email': unidentified_email}), format='json')

        self.assertEqual(response.status_code, 404)

    def test_successful_response_data(self):
        self.client.force_authenticate(self.user)

        # Testing student from existing fixtures
        response = self.client.get(reverse('detail_student', kwargs={'user__email': 'JP.KASBA@GMAIL.COM'}), format='json')
        self.assertEqual(
            response.json(),
            {'csc': {
                'csc_id': '445868460014',
                'institute': 'JAI PRAKASH KUMAR THAKUR',
                'state': 'Jharkhand',
                'city': 'Godda',
                'district': 'Godda',
                'block': 'Meherma',
                'address':'AT-CSC MEHARMA NEAR BLOCK OFFICE@GODDA,MEHARMA,JHARKHAND,PIN-814160',
                'pincode': '814160',
                'plan': 'All India Hackathon'
                }, 
                'user': {'email': 'JP.KASBA@GMAIL.COM', 'full_name': 'JAI PRAKASH KUMAR THAKUR'},
                'phone': '9931161472',
                'transaction_date': [{'transcdate': '2022-10-01'}]}
        )

        response = self.client.get(reverse('detail_student', kwargs={'user__email': 'test@teststudent.com'}), format='json')
        self.assertEqual(
            response.json(),
            {'csc': {
                'csc_id': 'test_csc',
                'institute': '1',
                'state': 'Tamil Nadu',
                'city': None,
                'district': 'Dindigul',
                'block': None,
                'address': None,
                'pincode': None,
                'plan': 'Testing'
                }, 
                'user': {'email': 'test@teststudent.com', 'full_name': 'JAI PRAKASH KUMAR THAKUR'},
                'phone': '9931161472',
                'transaction_date': [{'transcdate': '2022-10-01'}]}
        )  