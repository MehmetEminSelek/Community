from rest_framework import serializers
from .models import *


class CommunityModel(serializers.ModelSerializer):
    class Meta:
        model = CommunityModel
        fields = ("__all__")


class RewardsModel(serializers.ModelSerializer):
    class Meta:
        model = RewardsModel
        fields = ("__all__")


class Comlevel(serializers.ModelSerializer):
    class Meta:
        model = Comlevel
        fields = ("__all__")
