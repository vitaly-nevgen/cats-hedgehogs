from rest_framework import serializers

from cats_hedgehogs.models import User


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )
