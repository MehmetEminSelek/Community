import logging
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from Models.models import *
from .serializers import *
from datetime import datetime
from GenericServices.gen001errormanagement import gen001errormanagement

logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method='post',
    operation_id='Reward Point Assignment',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'userLanguage': openapi.Schema(type=openapi.TYPE_STRING, maxLength=2, description='User language choice, necessary information for Gen001errormanagement service'),
            'userProg': openapi.Schema(type=openapi.TYPE_INTEGER, description='Prog ID of user, automatically assigned in registraion service'),
            'userCountry': openapi.Schema(type=openapi.TYPE_STRING, maxLength=2, description='User community country code'),
            'rewardPoints': openapi.Schema(type=openapi.TYPE_INTEGER, max_digits=9, decimal_places=2, description='Reward points of user'),
            'userWin': openapi.Schema(type=openapi.TYPE_INTEGER, max_digits=9, decimal_places=2, description='Points win by the user')
        },

        required=['userLanguage', 'userProg',
                  'userCountry', 'rewardPoints', 'userWin']
    ),
    responses={200: "Post reward points assignment", },
    operation_description="Reward points assignment to user and his community"
)
@api_view(['POST'])
def cmty004rewardpointassignment(request):
    rewardPointsManagementSerializer = RewardPointsManagementSerializer(
        data=request.data)
    if rewardPointsManagementSerializer.is_valid() == False:
        return Response({"errId": 1, "errMessage": gen001errormanagement(1, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
    if rewardPointsManagementSerializer.data["userCountry"] != "":
        if UserModel.objects.using("user").filter(user_CountryCode=rewardPointsManagementSerializer.data["userCountry"]).exists() == False:
            return Response({"errId": 33, "errMessage": gen001errormanagement(33, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
    try:
        input_user = UserModel.objects.using("user").get(
            user_Prog=rewardPointsManagementSerializer.data["userProg"])
        user_CountryCode = input_user.user_CountryCode
    except:
        return Response({"errId": 33, "errMessage": gen001errormanagement(33, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
    if user_CountryCode != rewardPointsManagementSerializer.data["userCountry"]:
        return Response({"errId": 33, "errMessage": gen001errormanagement(33, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
# -------------------------------------END OF VALIDATION-------------------------------------

    year = datetime.now().year
    month = datetime.now().month
    period = str(year) + "-" + str(month)


# -----CHECK HREW-----
    result = checkhrew(rewardPointsManagementSerializer)
    if "RC" in result.data:
        if result.data["RC"] == 99:
            return Response({"errId": result.data["errId"], "errMessage": result.data["errMessage"], "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
    try:
        get_hisrew = RewardsModel.objects.get(
            hrew_userid=rewardPointsManagementSerializer.data["userProg"],
            hrew_period=period,
            hrew_country=rewardPointsManagementSerializer.data["userCountry"])
    except:
        return Response({"errId": 34, "errMessage": gen001errormanagement(34, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
# -----GET LEVEL-----
    request.data["userRp"] = get_hisrew.hrew_cmtyrp + \
        \
        rewardPointsManagementSerializer.data["rewardPoints"]
    result = getlevel(request.data)
    if "RC" in result.data:
        if result.data["RC"] == 99:
            return Response({"errId": result.data["errId"], "errMessage": result.data["errMessage"], "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result_level = result.data["data"]

    try:
        get_hisrew.hrew_userlevel = result_level["userLevel"]
        get_hisrew.hrew_levelperc = result_level["userLevelPerc"]
        get_hisrew.hrew_cmtyrp += rewardPointsManagementSerializer.data["rewardPoints"]
        get_hisrew.hrew_userrp += rewardPointsManagementSerializer.data["rewardPoints"]
        get_hisrew.hrew_userwin += rewardPointsManagementSerializer.data["userWin"]
        get_hisrew.hrew_lastupdate = datetime.now()
        get_hisrew.save()
    except:
        return Response({"errId": 39, "errMessage": gen001errormanagement(39, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
    output_data = []
    i = 0
    for community in CommunityModel.objects.filter(
            cmty_cmtylevel__gt=0).filter(
            cmty_memberid=rewardPointsManagementSerializer.data["userProg"]):
        community_status = community.cmty_status
        request.data["userProg"] = community.cmty_ownerid
        request.data["cmty_status"] = community_status
        request.data["period"] = period
        request.data["rewardsPoints"] = rewardPointsManagementSerializer.data["rewardPoints"]
        result = updatecmty(request.data)
        if "RC" in result.data:
            if result.data["RC"] == 99:
                return Response({"errId": result.data["errId"], "errMessage": result.data["errMessage"], "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
            output_data.append(result.data)
    return Response({"errId": 0, "errMessage": "Success", "RC": 0, "data": output_data}, status=status.HTTP_200_OK)


def getoldhrew(request):
    year = datetime.now().year
    month = datetime.now().month - 1
    if month == 1:
        month = 12
        year -= year
    else:
        month = month - 1
    period = str(year) + "-" + str(month)

    try:
        getOld_hisrew = RewardsModel.objects.filter(hrew_userid=request.data["userProg"]).filter(
            hrew_period=period).filter(hrew_country=request["userCountry"])
    except:
        return Response({"errId": 34, "errMessage": gen001errormanagement(34, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
    if not getOld_hisrew.exists():
        return Response({"errId": 34, "errMessage": gen001errormanagement(34, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
    getOld_hisrew = getOld_hisrew[0]
    request["friendsCount"] = getOld_hisrew.hrew_friendscount
    request["communityCount"] = getOld_hisrew.hrew_cmtycount
    return Response({"errId": 0, "errMessage": "Success", "RC": 0, "data": request}, status=status.HTTP_200_OK)


def checkhrew(request):
    year = datetime.now().year
    month = datetime.now().month
    period = str(year) + "-" + str(month)

    try:
        reward_query = RewardsModel.objects.filter(hrew_userid=request.data["userProg"]).filter(
            hrew_period=period).filter(hrew_country=request["userCountry"])
    except:
        return Response({"errId": 34, "errMessage": gen001errormanagement(34, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
    if reward_query.count() >= 1:
        reward_query = reward_query[0]
        request["userRp"] = reward_query.hrew_userrp
        request["cmtyRp"] = reward_query.hrew_cmtyrp
        return Response({"errId": 0, "errMessage": "Success", "RC": 0, "data": request}, status=status.HTTP_200_OK)
    result = getoldhrew(request)

    if "RC" in result.data:
        if result.data["RC"] == 99:
            return Response({"errId": result.data["errId"], "errMessage": result.data["errMessage"], "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = result.data["data"]

    request["userRp"] = request["rewardPoints"]
    result = getlevel(request)
    if "RC" in result.data:
        if result.data["RC"] == 99:
            return Response({"errId": result.data["errId"], "errMessage": result.data["errMessage"], "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = result.data["data"]

    try:
        RewardsModel.objects.create(
            hrew_userid=request["userProg"],
            hrew_period=period,
            hrew_country=request["userCountry"],
            hrew_friendscount=request["friendsCount"],
            hrew_cmtycount=request["communityCount"],
            hrew_insertdate=datetime.now(),
            hrew_lastupdate=datetime.now())
    except:
        return Response({"errId": 51, "errMessage": gen001errormanagement(51, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"errId": 0, "errMessage": "Success", "RC": 0, "data": result}, status=status.HTTP_200_OK)


def updatecmty(request):
    result = checkhrew(request)
    if "RC" in result.data:
        if result.data["RC"] == 99:
            return Response({"errId": result.data["errId"], "errMessage": result.data["errMessage"], "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
        else:
            request = result.data["data"]
    try:
        getOld_hisrew = RewardsModel.objects.get(hrew_userid=request["userProg"],
                                                 hrew_period=request["period"],
                                                 hrew_country=request["userCountry"])
    except:
        return Response({"errId": 34, "errMessage": gen001errormanagement(34, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)

    request["userRp"] = getOld_hisrew.hrew_cmtyrp + request["rewardsPoints"]
    result = getlevel(request)
    if "RC" in result.data:
        if result.data["RC"] == 99:
            return Response({"errId": result.data["errId"], "errMessage": result.data["errMessage"], "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result_level = result.data["data"]

    try:
        getOld_hisrew.hrew_userlevel = result_level["userLevel"]
        getOld_hisrew.hrew_levelperc = result_level["userLevelPerc"]
        getOld_hisrew.hrew_cmtyrp += request["rewardsPoints"]
        getOld_hisrew.hrew_lastupdate = datetime.now()
        getOld_hisrew.save()
        request["oldHisRew"] = getOld_hisrew.hrew_cmtyrp
    except:
        return Response({"errId": 75, "errMessage": gen001errormanagement(75, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"errId": 0, "errMessage": "Success", "RC": 0, "data": request}, status=status.HTTP_200_OK)


def getlevel(request):
    try:
        get_level = Comlevel.objects.get(
            com_countryid=request["userCountry"],
            Comlevel_from__lte=request["userRp"],
            Comlevel_to__gte=request["userRp"])
    except:
        return Response({"errId": 34, "errMessage": gen001errormanagement(34, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)

    request["userLevel"] = get_level.com_level
    request["userLevelPerc"] = get_level.Comlevel_perc
    return Response({"errId": 0, "errMessage": "Success", "RC": 0, "data": request}, status=status.HTTP_200_OK)
