# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HouseViewSet, HouseCategoryViewSet, AdditionalFeaturesViewSet,ProximityViewSet

router = DefaultRouter()
router.register('houses', HouseViewSet)
router.register('categories', HouseCategoryViewSet)
router.register('features', AdditionalFeaturesViewSet)
router.register('proximity',ProximityViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
