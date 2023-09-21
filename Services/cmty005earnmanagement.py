from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from Models.models import *
from .serializers import *
from datetime import datetime
from GenericServices.gen001errormanagement import gen001errormanagement
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method='post',
    operation_id='Earn Management',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'userLanguage': openapi.Schema(type=openapi.TYPE_STRING, maxLength=2, description='User language choice, necessary information for Gen001errormanagement service'),
            'userProg': openapi.Schema(type=openapi.TYPE_INTEGER, description='Prog ID of user, automatically assigned in registraion service'),
            'userCountry': openapi.Schema(type=openapi.TYPE_STRING, maxLength=2, description='User community country code'),
            'year': openapi.Schema(type=openapi.TYPE_INTEGER, min_value=2023, max_value=2200, description='Reward points of user'),
            'month': openapi.Schema(type=openapi.TYPE_INTEGER, min_value=1, max_value=12, description='Points win by the user')
        },

        required=['userLanguage', 'userProg',
                  'userCountry', 'year', 'month']
    ),
    responses={200: "Post calculate the community owner earning", },
    operation_description="Calculate the community owner earning; it must be called after cmty004rewardpointsassignment"
)
@api_view(['POST'])
def cmty005earnmanagement(request):
    earnManagementSerializer = EarnManagementSerializer(data=request.data)
    if earnManagementSerializer.is_valid() == False:
        return Response({"errId": 2, "errMessage": gen001errormanagement(2, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)

    try:
        input_user = UserModel.objects.using("user").get(
            user_Prog=earnManagementSerializer.data["userProg"])
        user_CountryCode = input_user.user_CountryCode
    except:
        return Response({"errId": 30, "errMessage": gen001errormanagement(30, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)

# -------------------------------------END OF VALIDATION-------------------------------------
    period = str(earnManagementSerializer.data["year"]) + \
        "-" + str(earnManagementSerializer.data["month"])
    # print('period-->', period)
    output_data = []
    seen_data = set()
    for cmty_upper in CommunityModel.objects.filter(
            cmty_cmtylevel__gte=0).filter(
            cmty_memberid=earnManagementSerializer.data["userProg"]).filter(
            cmty_country=earnManagementSerializer.data["userCountry"]).order_by("cmty_cmtylevel"):
        # -----CHECK HREW-----
        print('user-->', cmty_upper.cmty_ownerid)
        request.data["userProg"] = cmty_upper.cmty_ownerid
        result = checkhrew(request.data, period)
        if "RC" in result.data:
            if result.data["RC"] == 99:
                return Response({"errId": result.data["errId"], "errMessage": result.data["errMessage"], "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
        try:
            get_hisrew = RewardsModel.objects.get(
                hrew_userid=cmty_upper.cmty_ownerid,
                hrew_period=period,
                hrew_country=earnManagementSerializer.data["userCountry"])
        except:
            return Response({"errId": 10, "errMessage": gen001errormanagement(10, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)

        print('hrew owner -->', get_hisrew.hrew_userid,
              get_hisrew.hrew_userlevel,
              get_hisrew.hrew_levelperc,
              get_hisrew.hrew_cmtyrp,
              get_hisrew.hrew_userrp)

        userearn = get_hisrew.hrew_userrp * get_hisrew.hrew_levelperc / 100
        userperc = get_hisrew.hrew_levelperc
        totalearn = userearn
        cmtyearn = 0
        # print ('user earn-->', userearn)

        # i = 0
        for community in CommunityModel.objects.filter(
                cmty_cmtylevel=1).filter(
                cmty_ownerid=cmty_upper.cmty_ownerid).filter(
                cmty_country=earnManagementSerializer.data["userCountry"]):
            # print('cmtyuser-->', community.cmty_memberid, community.cmty_country)

            request.data["userProg"] = community.cmty_memberid
            result = checkhrew(request.data, period)
            if "RC" in result.data:
                if result.data["RC"] == 99:
                    return Response({"errId": result.data["errId"], "errMessage": result.data["errMessage"], "RC": 99}, status=status.HTTP_400_BAD_REQUEST)

            try:
                get_cmtyhrew = RewardsModel.objects.get(
                    hrew_userid=community.cmty_memberid,
                    hrew_period=period,
                    hrew_country=community.cmty_country)
            except:
                return Response({"errId": 77, "errMessage": gen001errormanagement(77, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
            deltaperc = userperc - get_cmtyhrew.hrew_levelperc
            earning = get_cmtyhrew.hrew_cmtyrp * deltaperc / 100
            cmtyearn = cmtyearn + earning
            totalearn = totalearn + earning
            # print('cmty earning-->', deltaperc, get_cmtyhrew.hrew_cmtyrp, earning )
            # print('cmtyearnings-->', cmtyearn)
            # print('totalearnings -->', totalearn)

        try:
            get_hisrew.hrew_userearn = userearn
            get_hisrew.hrew_cmtyearn = cmtyearn
            get_hisrew.hrew_lastupdate = datetime.now()
            get_hisrew.save()
        except:
            return Response({"errId": 10, "errMessage": "dbError:update hrew user earnings", "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
        cmty_info = {}
        cmty_info = {
            "userprog": cmty_upper.cmty_ownerid,
            "userEarning": userearn,
            "cmtyEarning": cmtyearn,
            "totalEarning": totalearn
        }
        output_data.append(cmty_info)
        seen_data.add(tuple(cmty_info.items()))
    return Response({"errId": 0, "errMessage": "Success", "RC": 0,
                     "data": output_data}, status=status.HTTP_200_OK)


def checkhrew(request, period):
    try:
        reward_query = RewardsModel.objects.filter(hrew_userid=request["userProg"]).filter(
            hrew_period=period).filter(hrew_country=request["userCountry"])
    except:
        return Response({"errId": 10, "errMessage": gen001errormanagement(10, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
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


def getoldhrew(request):
    year = request["year"]
    month = request["month"]
    if month == 1:
        month = 12
        year -= year
    else:
        month = month - 1
    period = str(year) + "-" + str(month)
    print('old period-->', period)

    try:
        getOld_hisrew = RewardsModel.objects.filter(hrew_userid=request["userProg"]).filter(
            hrew_period=period).filter(hrew_country=request["userCountry"])
    except:
        return Response({"errId": 73, "errMessage": gen001errormanagement(73, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
    if not getOld_hisrew.exists():
        return Response({"errId": 78, "errMessage": gen001errormanagement(78, request.data), "RC": 99}, status=status.HTTP_404_NOT_FOUND)
    getOld_hisrew = getOld_hisrew[0]
    request["friendsCount"] = getOld_hisrew.hrew_friendscount
    request["communityCount"] = getOld_hisrew.hrew_cmtycount
    return Response({"errId": 0, "errMessage": "Success", "RC": 0, "data": request}, status=status.HTTP_200_OK)
