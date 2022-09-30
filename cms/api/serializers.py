from rest_framework import serializers

from cms.models import State,District

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ["id","name"]
        readonly = ["id", "name"]

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ["id","name","state"]
        readonly = ["id","name","state"]

class DistrictDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ["id","name"]
        readonly = ["id","name"]