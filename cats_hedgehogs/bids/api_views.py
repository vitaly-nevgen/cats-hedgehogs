from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from cats_hedgehogs.helpers import require_lock
from cats_hedgehogs.models import Lot, Bid
from cats_hedgehogs.permissions import IsOwnerOrReadOnly, RelatedLotOwnerOnly
from cats_hedgehogs.bids.serializers import BidSerializer


class BidListApi(generics.ListCreateAPIView):
    serializer_class = BidSerializer

    @staticmethod
    def get_nested_lot(kwargs):
        return get_object_or_404(Lot, pk=kwargs['lot_pk'])

    @staticmethod
    def get_bids_queryset(kwargs):
        lot = BidListApi.get_nested_lot(kwargs)
        return Bid.objects.filter(lot=lot)

    def perform_create(self, serializer):
        lot = self.get_nested_lot(self.kwargs)

        @transaction.atomic
        @require_lock(Bid, 'ACCESS EXCLUSIVE')
        def inner_func():
            if lot.finished:
                raise ValidationError('Lot already finished')
            serializer.save(
                owner=self.request.user,
                lot=lot
            )

        inner_func()

    def get_queryset(self):
        return BidListApi.get_bids_queryset(self.kwargs)


class BidDetailApi(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BidSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated, )
    lookup_url_kwarg = 'bid_pk'

    def get_queryset(self):
        return BidListApi.get_bids_queryset(self.kwargs)


class BidAcceptView(generics.GenericAPIView):
    # adding empty serializer to avoid any data be sent
    serializer_class = serializers.Serializer
    permission_classes = (IsAuthenticated, RelatedLotOwnerOnly, )
    lookup_url_kwarg = 'bid_pk'

    def get_queryset(self):
        return BidListApi.get_bids_queryset(self.kwargs)

    @transaction.atomic
    @require_lock(Bid, 'ACCESS EXCLUSIVE')
    def perform_accept(self, bid):
        if bid.lot.finished:
            return False

        bid.accepted = True
        bid.save()

        return True

    def post(self, request, *args, **kwargs):
        bid = self.get_object()

        if not self.perform_accept(bid):
            return Response({
                "detail": "Unable to accept bid. This lot already has an accepted bid"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
