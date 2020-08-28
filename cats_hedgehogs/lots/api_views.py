from rest_framework import generics

from cats_hedgehogs.models import Lot
from cats_hedgehogs.permissions import IsOwnerOrReadOnly
from cats_hedgehogs.lots.serializers import LotSerializer, LotCreateSerializer
from rest_framework.permissions import IsAuthenticated

class LotListApi(generics.ListCreateAPIView):
    def get_queryset(self):
        return (
            Lot.objects.all()
            .prefetch_related('pet')
            .prefetch_related('owner')
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LotCreateSerializer
        else:
            return LotSerializer


class LotDetailApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lot.objects.all()
    serializer_class = LotSerializer
    lookup_url_kwarg = 'lot_pk'
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated, )
