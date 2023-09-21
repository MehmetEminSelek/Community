from rest_framework import serializers
from django.core.exceptions import ValidationError


class BaseRequestSerializer(serializers.Serializer):
    callType = serializers.IntegerField(min_value=1, max_value=6)


class CMTY001Serializer(serializers.Serializer):
    userLanguage = serializers.CharField(max_length=2)
    ownerId = serializers.IntegerField(min_value=1)
    ownerCountryCode = serializers.CharField(max_length=2)
    ownerPresenterID = serializers.IntegerField(min_value=0)


class REG008(serializers.Serializer):
    callType = serializers.IntegerField(min_value=1, max_value=6)
    userProg = serializers.IntegerField()
    userMail = serializers.CharField(max_length=50)
    userPhone = serializers.CharField(max_length=20)
    userFunctionType = serializers.CharField(max_length=1)
    verificationCode = serializers.CharField(max_length=16)


class LoginSerializer(serializers.Serializer):
    userProg = serializers.IntegerField()
    password = serializers.CharField(max_length=16)
    functionType = serializers.CharField(max_length=1)


class SendVerCodeSerializer(serializers.Serializer):
    userFunctionType = serializers.CharField(max_length=1)
    userProg = serializers.IntegerField()
    userMail = serializers.CharField(max_length=50)
    userPhone = serializers.CharField(max_length=20)


class PhoneSerializerVerify(serializers.Serializer):
    phone_userProg = serializers.IntegerField()
    phone_userPhone = serializers.CharField(max_length=20)
    phone_verificationCode = serializers.CharField(max_length=16)
    phone_callType = serializers.CharField(max_length=1)


class PhoneSerializer(serializers.Serializer):
    phone_userProg = serializers.IntegerField()
    phone_userPhone = serializers.CharField(max_length=20)
    phone_callType = serializers.CharField(max_length=1)


class RegCustomerSerializer(serializers.Serializer):
    userProg = serializers.IntegerField()


class RegCustomerSurnameSerializer(serializers.Serializer):
    userProg = serializers.IntegerField()
    surname = serializers.CharField(max_length=30)


class RegCustomerNameSerializer(serializers.Serializer):
    userProg = serializers.IntegerField()
    name = serializers.CharField(max_length=30)


class RegCustomerBdateSerializer(serializers.Serializer):
    userProg = serializers.IntegerField()
    bdate = serializers.DateField()


class ListCountrySerializer(serializers.Serializer):
    userLanguage = serializers.CharField(max_length=2)
    ownerId = serializers.IntegerField()


class ListFriendsSerializer(serializers.Serializer):
    countryCode = serializers.CharField(max_length=2)
    userLanguage = serializers.CharField(max_length=2)
    ownerId = serializers.IntegerField()


class RewardPointsManagementSerializer(serializers.Serializer):
    userLanguage = serializers.CharField(max_length=2)
    userProg = serializers.IntegerField()
    userCountry = serializers.CharField(max_length=2)
    rewardPoints = serializers.DecimalField(
        max_digits=9, decimal_places=2, coerce_to_string=False)
    userWin = serializers.DecimalField(
        max_digits=9, decimal_places=2, coerce_to_string=False)


class EarnManagementSerializer(serializers.Serializer):
    userLanguage = serializers.CharField(max_length=2)
    userProg = serializers.IntegerField()
    userCountry = serializers.CharField(max_length=2)
    year = serializers.IntegerField(min_value=2023, max_value=2200)
    month = serializers.IntegerField(min_value=1, max_value=12)


class UserCommunityDataSerializer(serializers.Serializer):
    countryCode = serializers.CharField(max_length=2)
    userLanguage = serializers.CharField(max_length=2)
    ownerId = serializers.IntegerField()
