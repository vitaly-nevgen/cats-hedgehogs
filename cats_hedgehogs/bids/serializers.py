from rest_framework import serializers

from cats_hedgehogs.models import Bid


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ('id', 'value', 'owner', 'lot', )
        read_only_fields = ('owner', 'lot', )
