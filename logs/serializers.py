from rest_framework import serializers
from .models import TutorialProgress

class TutorialProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorialProgress
        fields = ['tutorial', 'foss', 'language', 'time_completed', 'total_duration', 'status']
    
    def create(self, validated_data):
        try:
            tut_prog = TutorialProgress.objects.get(
                user=validated_data['user'],
                tutorial=validated_data['tutorial'],
                foss=validated_data['foss'],
                language=validated_data['language']
                )
            if not tut_prog.status:
                if tut_prog.time_completed < validated_data['time_completed']:
                    tut_prog.time_completed = validated_data['time_completed']
                    if tut_prog.time_completed >= tut_prog.total_duration:
                        tut_prog.status =True
                    tut_prog.save()
            return tut_prog
        except TutorialProgress.DoesNotExist:
            return TutorialProgress.objects.create(**validated_data)