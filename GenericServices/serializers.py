from rest_framework import serializers
from django.core.exceptions import ValidationError


class GEN001Serializer(serializers.Serializer):
    err_Language = serializers.CharField(max_length=2, default="EN")


class GEN002Serializer(serializers.Serializer):
    countryCode = serializers.CharField(max_length=2, default="IT")
    queryType = serializers.IntegerField()
    countryName = serializers.CharField(max_length=50, default="Italy")
    counter = serializers.IntegerField(default=0)
