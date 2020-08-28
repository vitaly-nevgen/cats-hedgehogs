from rest_framework import serializers

from cats_hedgehogs.models import Pet


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ('id', 'pet_type', 'breed', 'callsign', )
