from rest_framework import generics

from cats_hedgehogs.models import Pet
from cats_hedgehogs.pets.serializers import PetSerializer


class PetListApi(generics.ListCreateAPIView):
    serializer_class = PetSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Pet.objects.filter(
            owner=self.request.user
        )


class PetDetailApi(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PetSerializer
    lookup_url_kwarg = 'pet_pk'

    def get_queryset(self):
        return Pet.objects.filter(
            owner=self.request.user
        )
