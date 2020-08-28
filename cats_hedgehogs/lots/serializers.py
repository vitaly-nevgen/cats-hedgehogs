from rest_framework import serializers

from cats_hedgehogs.models import Pet, Lot
from cats_hedgehogs.serializers import PublicUserSerializer
from cats_hedgehogs.pets.serializers import PetSerializer


class LotSerializer(serializers.ModelSerializer):
    pet = PetSerializer(read_only=True)
    owner = PublicUserSerializer(read_only=True)

    class Meta:
        model = Lot
        fields = ('id', 'owner', 'start_price', 'pet', )


class PetPKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        queryset = Pet.objects.filter(owner=user)
        return queryset


class LotCreateSerializer(serializers.ModelSerializer):
    pet = PetPKField()

    class Meta:
        model = Lot
        fields = ('id', 'start_price', 'pet', )
