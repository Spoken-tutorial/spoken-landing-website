from rest_framework import serializers
from .models import Jobfair


class JobFairSerializer(serializers.ModelSerializer):

	class Meta:
		model = Jobfair
		#fields = ('name','event_date')
		fields = '__all__'
		depth = 1