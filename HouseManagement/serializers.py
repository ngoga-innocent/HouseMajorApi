from rest_framework import serializers
from .models import (
    House, HouseCategory, AdditionalFeatures, HouseFeatureAssignment,
    HouseFeatureImage, HouseImages, Proximity, Agent
)


# --- Agent Serializer for creation ---
class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'


# --- Feature Images ---
class HouseFeatureImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseFeatureImage
        fields = ['id', 'image']


# --- Feature Assignment Serializer ---
class HouseFeatureAssignmentSerializer(serializers.ModelSerializer):
    feature = serializers.PrimaryKeyRelatedField(queryset=AdditionalFeatures.objects.all())
    images = HouseFeatureImageSerializer(many=True, required=False)

    class Meta:
        model = HouseFeatureAssignment
        fields = ['id', 'feature', 'available_number', 'images']

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        assignment = HouseFeatureAssignment.objects.create(**validated_data)
        for image_data in images_data:
            HouseFeatureImage.objects.create(assignment=assignment, **image_data)
        return assignment


# --- House Images Serializer ---
class HouseImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseImages
        fields = ['id', 'images']

class HouseCategorySerializer(serializers.ModelSerializer):
    class Meta: 
        model = HouseCategory
        fields = '__all__'

class AdditionalFeaturesSerializer(serializers.ModelSerializer):
    class Meta: 
        model = AdditionalFeatures
        fields = '__all__'
class ProximitySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Proximity
        fields = '__all__'
# --- Main House Serializer ---
class HouseSerializer(serializers.ModelSerializer):
    agent = AgentSerializer()  # nested agent creation
    house_category = serializers.PrimaryKeyRelatedField(queryset=HouseCategory.objects.all())
    feature_assignments = HouseFeatureAssignmentSerializer(many=True, required=False)
    house_images = HouseImagesSerializer(many=True, required=False)

    class Meta:
        model = House
        fields = [
            'id', 'thumbnail', 'house_category', 'payment_category',
            'address', 'latitude', 'longitude', 'price', 'description',
            'agent', 'feature_assignments', 'house_images', 'is_booked'
        ]

    def create(self, validated_data):
        # 1️⃣ Extract and create agent
        agent_data = validated_data.pop('agent', None)
        agent_instance = None
        if agent_data:
            agent_instance = Agent.objects.create(**agent_data)

        # 2️⃣ Extract nested features and house images
        features_data = validated_data.pop('feature_assignments', [])
        house_images_data = validated_data.pop('house_images', [])

        # 3️⃣ Create house with new agent
        house = House.objects.create(agent=agent_instance, **validated_data)

        # 4️⃣ Create feature assignments with optional images
        for feature_data in features_data:
            images_data = feature_data.pop('images', [])
            assignment = HouseFeatureAssignment.objects.create(house=house, **feature_data)
            for img in images_data:
                HouseFeatureImage.objects.create(assignment=assignment, **img)

        # 5️⃣ Create house images
        for img_data in house_images_data:
            HouseImages.objects.create(house=house, **img_data)

        return house
