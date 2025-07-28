# views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import House, HouseCategory, AdditionalFeatures,Proximity
from .serializers import HouseSerializer, HouseCategorySerializer, AdditionalFeaturesSerializer,ProximitySerializer

class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer

class HouseCategoryViewSet(viewsets.ModelViewSet):
    queryset = HouseCategory.objects.all()
    serializer_class = HouseCategorySerializer

class AdditionalFeaturesViewSet(viewsets.ModelViewSet):
    queryset = AdditionalFeatures.objects.all()
    serializer_class = AdditionalFeaturesSerializer
class ProximityViewSet(viewsets.ModelViewSet):
    queryset=Proximity.objects.all()
    serializer_class=ProximitySerializer