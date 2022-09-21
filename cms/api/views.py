from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from cms.api.serializers import StateSerializer,DistrictSerializer,DistrictDetailSerializer
from cms.models import State,District

class StateList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    queryset = State.objects.all()
    serializer_class = StateSerializer

class DistrictList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class DistrictDetail(generics.ListAPIView):
    lookup_field = "state_id"
    serializer_class =DistrictDetailSerializer

    def get_queryset(self):
        
        state_id = self.kwargs['state_id']
        print(f"state_id ******> {state_id}")
        print(f"Count : {District.objects.filter(state_id=state_id).count()}")
        return District.objects.filter(state_id=state_id)
    

    