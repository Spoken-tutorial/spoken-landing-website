from rest_framework import serializers
from django_ers.models import *


class JobFairSerializer(serializers.ModelSerializer):

	class Meta:
		model = Event
		fields = '__all__'
		depth = 1