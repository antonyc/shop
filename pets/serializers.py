# coding: utf-8

from django.conf import settings
from rest_framework import serializers
from django.core import urlresolvers

class CoordinatesSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lon = serializers.FloatField()


class PetCreationSerializer(serializers.Serializer):
    images = serializers.Serializer(many=True, required=False)
    # geo point (latitude, longitude)
    position = CoordinatesSerializer()
    phone_number = serializers.CharField()
    user_description = serializers.CharField(required=False)
    breed_by_user = serializers.CharField()

    def validate_images(self, attrs, field_name):
        if not field_name in attrs:
            return attrs
        for filename in attrs[field_name]:
            full_path = os.path.join(settings.MEDIA_ROOT, filename)
            if not os.path.exists(full_path):
                raise serializers.ValidationError(
                    'File "{0}" does not exist'.format(filename)
                )
        return attrs


class ImagePath(serializers.Serializer):
    path = serializers.CharField()


class PetSerializer(serializers.Serializer):
    self = serializers.SerializerMethodField('create_self')
    id = serializers.CharField()
    images = serializers.Serializer(many=True)
    user_description = serializers.CharField()
    breed_by_user = serializers.CharField()
    created_at = serializers.DateTimeField()

    def create_self(self, pet):
        return urlresolvers.reverse('pets_view', kwargs=dict(id=str(pet.id)))
