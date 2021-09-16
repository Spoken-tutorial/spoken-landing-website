from .serializers import TutorialProgressSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import TutorialProgress

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_tutorial_progress(request):
    if request.method == 'POST':
        serializer = TutorialProgressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def get_set_tutorial_progress(request):
    try:
        tp=TutorialProgress.objects.get(
            user=request.user, 
            tutorial=request.data['tutorial'],
            foss=request.data['foss'],
            language=request.data['language']
        )
    except TutorialProgress.DoesNotExist:
        return Response({'status': 'Tutorial Progress does not exist'}, status=status.HTTP_200_OK)
    if request.method == 'POST':
        if tp.status:
            tp.status=False
        else:
            tp.status=True
        tp.save()
        return Response({'status': tp.status}, status=status.HTTP_200_OK)
    if request.method == 'GET':
        if tp.status:
            time_completed=tp.total_duration
        else:
            time_completed=tp.time_completed
        return Response({'status': tp.status,'time_completed':time_completed}, status=status.HTTP_200_OK)