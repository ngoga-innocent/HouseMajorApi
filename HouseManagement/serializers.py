# serializers.py

from rest_framework import serializers
from .models import HouseCategory, AdditionalFeatures, House, HouseFeatureAssignment, HouseFeatureImage,Proximity,HouseImages

class HouseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseCategory
        fields = '__all__'

class AdditionalFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalFeatures
        fields = '__all__'

class HouseFeatureImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseFeatureImage
        fields = ['id', 'image']

class HouseFeatureAssignmentSerializer(serializers.ModelSerializer):
    feature = AdditionalFeaturesSerializer()
    images = HouseFeatureImageSerializer(many=True, read_only=True)

    class Meta:
        model = HouseFeatureAssignment
        fields = ['id', 'feature', 'available_number', 'images']
class HouseImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model=HouseImages
        fields='__all__'
class HouseSerializer(serializers.ModelSerializer):
    house_category = HouseCategorySerializer()
    feature_assignments = HouseFeatureAssignmentSerializer(many=True, read_only=True)
    house_images = HouseImagesSerializer(many=True, read_only=True)

    class Meta:
        model = House
        fields = [
            'id', 'thumbnail', 'house_category', 'payment_category',
            'address', 'latitude', 'longitude', 'price', 'description',
            'feature_assignments','is_booked','house_images'
        ]
class ProximitySerializer(serializers.ModelSerializer):
    class Meta:
        model=Proximity
        fields='__all__'