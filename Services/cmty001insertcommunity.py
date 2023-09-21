from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import datetime
from Models.models import *
from .serializers import *
from GenericServices.gen001errormanagement import gen001errormanagement
from django.db import transaction
from django.core.cache import cache

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method='post',
    operation_id='Insert Community',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'userLanguage': openapi.Schema(type=openapi.TYPE_STRING, maxLength=2, description='User language choice, necessary information for Gen001errormanagement service'),
            'ownerId': openapi.Schema(type=openapi.TYPE_INTEGER, min_value=1, description='Owner ID of Community'),
            'ownerCountryCode': openapi.Schema(type=openapi.TYPE_STRING, maxLength=2, description='Owner community country code'),
            'ownerPresenterID': openapi.Schema(type=openapi.TYPE_INTEGER, min_value=0, description='Owner presenter ID')
        },
        required=['userLanguage', 'ownerId',
                  'ownerCountryCode', 'ownerPresenterID']
    ),
    responses={200: "Status OK", },
    operation_description="Insert/creation of user community "
)
@api_view(['POST'])
def cmty001insertcommunity(request):
    cmty001Data = CMTY001Serializer(data=request.data)
    if cmty001Data.is_valid() == False:
        return Response({"errId": 1, "errMessage":  gen001errormanagement(1, request.data), "RC": 99}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    try:
        ownerData = UserModel.objects.using("user").get(
            user_Prog=cmty001Data.data["ownerId"])
    except:
        return Response({"errId": 2, "errMessage":  gen001errormanagement(2, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
    if cmty001Data.data["ownerPresenterID"] == cmty001Data.data["ownerId"]:
        return Response({"errId": 33, "errMessage":  gen001errormanagement(33, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
    if cmty001Data.data["ownerPresenterID"] == 0:
        presenter_country = ownerData.user_CountryCode
    else:
        try:
            presenterData = UserModel.objects.using("user").get(
                user_Prog=cmty001Data.data["ownerPresenterID"])
            presenter_country = presenterData.user_CountryCode
        except:
            return Response({"errId": 6, "errMessage": gen001errormanagement(6, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
    if cmty001Data.data["ownerCountryCode"] == presenter_country:
        result = PROCSAMECOUNTRY(cmty001Data.data)
        procsame = transaction.savepoint()
        if "RC" in result.data:
            if result.data["RC"] == 99:
                transaction.savepoint_rollback(procsame)
                return Response({"errId": result.data["errId"], "errMessage": result.data["errMessage"], "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
    else:
        result = PROCDIFFCOUNTRIES(cmty001Data.data, presenter_country)
        procdiff = transaction.savepoint()
        if "RC" in result.data:
            if result.data["RC"] == 99:
                transaction.savepoint_rollback(procdiff)
                return Response({"errId": result.data["errId"], "errMessage": result.data["errMessage"], "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
        result = PROCSAMECOUNTRY(cmty001Data.data)
        if "RC" in result.data:
            if result.data["RC"] == 99:
                return Response({"errId": result.data["errId"], "errMessage": result.data["errMessage"], "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"errId": 0, "status": "success", "RC": 0}, status=status.HTTP_200_OK)


def PROCSAMECOUNTRY(userData):
    country_data = userData
    level = 0
    try:
        CommunityModel.objects.create(
            cmty_ownerid=country_data["ownerId"],
            cmty_country=country_data["ownerCountryCode"],
            cmty_memberid=country_data["ownerId"],
            cmty_status="P",
            cmty_cmtylevel=level)
    except:
        return Response({"errId": 50, "errMessage":  gen001errormanagement(50, userData.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
    year = datetime.now().year
    month = datetime.now().month
    try:
        RewardsModel.objects.create(
            hrew_userid=country_data["ownerId"],
            hrew_period=str(year) + "-" + str(month),
            hrew_country=country_data["ownerCountryCode"],
            hrew_cmtycount=1,
            hrew_userrp=50,
            hrew_insertdate=datetime.now(),
            hrew_lastupdate=datetime.now())
    except:
        return Response({"errId": 51, "errMessage": gen001errormanagement(51, userData.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)

    try:
        for update_data in CommunityModel.objects.filter(cmty_memberid=country_data["ownerPresenterID"]).filter(
                cmty_country=country_data["ownerCountryCode"]).order_by("-cmty_cmtylevel"):
            try:
                CommunityModel.objects.create(
                    cmty_ownerid=update_data.cmty_ownerid,
                    cmty_country=country_data["ownerCountryCode"],
                    cmty_memberid=country_data["ownerId"],
                    cmty_status="P",
                    cmty_cmtylevel=update_data.cmty_cmtylevel+1)
            except:
                return Response({"errId": 55, "errMessage": gen001errormanagement(55, userData.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"errId": 56, "errMessage": gen001errormanagement(56, userData.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)

    # UPDATE REWARDS POINT

    try:
        if CommunityModel.objects.filter(cmty_cmtylevel=1,
                                         cmty_memberid=country_data["ownerId"],
                                         cmty_country=country_data["ownerCountryCode"]).exists():
            community = CommunityModel.objects.filter(cmty_cmtylevel=1,
                                                      cmty_memberid=country_data["ownerId"],
                                                      cmty_country=country_data["ownerCountryCode"])
            community = community[0]
            try:
                rewards_updated = RewardsModel.objects.get(
                    hrew_userid=community.cmty_ownerid,
                    hrew_country=country_data["ownerCountryCode"])
            except:
                return Response({"errId": 62, "errMessage": gen001errormanagement(62, userData.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
            try:
                rewards_updated.hrew_cmtycount = rewards_updated.hrew_cmtycount + 1
                rewards_updated.hrew_friendscount = rewards_updated.hrew_friendscount + 1
                rewards_updated.hrew_lastupdate = datetime.now()
                rewards_updated.save()
            except:
                return Response({"errId": 63, "errMessage": gen001errormanagement(63, userData.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"errId": 64, "errMessage": gen001errormanagement(64, userData.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)

    # CMTY_CMTYLEVEL__GT IS GREATER THAN FOR LESS THAN USE CMTY_CMTYLEVEL__LT FOR GREATER OR EQUAL USE CMTY_CMTYLEVEL__GTE
    if CommunityModel.objects.filter(cmty_cmtylevel__gt=1,
                                     cmty_memberid=country_data["ownerId"],
                                     cmty_country=country_data["ownerCountryCode"]).exists():
        try:
            community_1 = CommunityModel.objects.filter(cmty_cmtylevel=1,
                                                        cmty_memberid=country_data["ownerId"],
                                                        cmty_country=country_data["ownerCountryCode"])
            community_1 = CommunityModel.objects.filter(cmty_cmtylevel__gt=1,
                                                        cmty_memberid=country_data["ownerId"],
                                                        cmty_country=country_data["ownerCountryCode"])
            community_1 = community_1[0]
            try:
                rewards_updated = RewardsModel.objects.get(
                    hrew_userid=community_1.cmty_ownerid,
                    hrew_country=country_data["ownerCountryCode"])
                rewards_updated.hrew_cmtycount = rewards_updated.hrew_cmtycount + 1
                rewards_updated.hrew_lastupdate = datetime.now()
                rewards_updated.save()
            except:
                return Response({"errId": 65, "errMessage": gen001errormanagement(65, userData.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"errId": 66, "errMessage": gen001errormanagement(66, userData.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"errId": 0, "status": "success", "RC": 0}, status=status.HTTP_200_OK)


def PROCDIFFCOUNTRIES(userData, presenter_country):
    country_data = userData
    level = 0
    if CommunityModel.objects.filter(cmty_ownerid=country_data["ownerPresenterID"]).filter(cmty_country=country_data["ownerCountryCode"]).filter(cmty_cmtylevel=level).exists() == True:
        return Response({"errId": 0, "status": "success", "RC": 0}, status=status.HTTP_200_OK)
    # ISRTCOMMPRESS
    year = datetime.now().year
    month = datetime.now().month
    period = str(year) + "-" + str(month)
    try:
        for community in CommunityModel.objects.filter(cmty_memberid=country_data["ownerPresenterID"]).filter(
                cmty_country=presenter_country).order_by("-cmty_ownerid").order_by("cmty_cmtylevel"):
            try:
                for presentercommunity in CommunityModel.objects.filter(cmty_memberid=community.cmty_ownerid).filter(
                        cmty_country=presenter_country).order_by("-cmty_ownerid").order_by("cmty_cmtylevel"):
                    if CommunityModel.objects.filter(
                            cmty_ownerid=presentercommunity.cmty_ownerid).filter(
                            cmty_country=country_data["ownerCountryCode"]).filter(
                            cmty_memberid=presentercommunity.cmty_memberid).exists() == False:
                        try:
                            CommunityModel.objects.create(
                                cmty_ownerid=presentercommunity.cmty_ownerid,
                                cmty_memberid=presentercommunity.cmty_memberid,
                                cmty_country=country_data["ownerCountryCode"],
                                cmty_cmtylevel=presentercommunity.cmty_cmtylevel,
                                cmty_status="A")
                        except:
                            return Response({"errId": 67, "errMessage": gen001errormanagement(67, userData.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"errId": 68, "errMessage": gen001errormanagement(68, userData.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
            if RewardsModel.objects.filter(
                    hrew_userid=community.cmty_ownerid).filter(
                    hrew_country=country_data["ownerCountryCode"]).filter(
                    hrew_period=period).exists() == False:
                try:
                    ctr_friends = CommunityModel.objects.filter(
                        cmty_ownerid=community.cmty_ownerid).filter(
                        cmty_country=country_data["ownerCountryCode"]).filter(
                        cmty_cmtylevel=1).count()
                except:
                    return Response({"errId": 69, "errMessage": gen001errormanagement(69, userData.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    ctr_cmty = CommunityModel.objects.filter(
                        cmty_ownerid=community.cmty_ownerid).filter(
                        cmty_country=country_data["ownerCountryCode"]).count()
                except:
                    return Response({"errId": 70, "errMessage": gen001errormanagement(70, userData.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    RewardsModel.objects.create(
                        hrew_userid=community.cmty_ownerid,
                        hrew_period=period,
                        hrew_country=country_data["ownerCountryCode"],
                        hrew_cmtycount=ctr_cmty,
                        hrew_friendscount=ctr_friends,
                        hrew_lastupdate=datetime.now(),
                        hrew_insertdate=datetime.now())
                except:
                    return Response({"errId": 71, "errMessage": gen001errormanagement(71, userData.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"errId": 72, "errMessage": gen001errormanagement(72, userData.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"errId": 0, "status": "success", "RC": 00}, status=status.HTTP_200_OK)
