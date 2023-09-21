import logging
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import datetime
from Models.models import *
from .serializers import *
from datetime import datetime
from GenericServices.gen001errormanagement import gen001errormanagement

logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method='post',
    operation_id='User Community Friends',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'userLanguage': openapi.Schema(type=openapi.TYPE_STRING, maxLength=2, description='User language choice, necessary information for Gen001errormanagement service'),
            'countryCode': openapi.Schema(type=openapi.TYPE_STRING, maxLength=2, description='User community country code'),
            'ownerId': openapi.Schema(type=openapi.TYPE_INTEGER, min_value=1, description='Owner ID of Community')
        },

        required=['userLanguage', 'countryCode', 'ownerId']
    ),
    responses={200: "Post list of friends", },
    operation_description="List of friends (fisrt level) for a specific country in user's community"
)
@api_view(['POST'])
def cmty003usercommuntyfriends(request):
    data = []
    seen_data = set()
    year = datetime.now().year
    month = datetime.now().month
    period = str(year) + "-" + str(month)
    listFriendsSerializer = ListFriendsSerializer(data=request.data)
    if listFriendsSerializer.is_valid() == False:
        return Response({"errId": 2, "errMessage": gen001errormanagement(2, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)

    try:
        community = CommunityModel.objects.filter(
            cmty_ownerid=listFriendsSerializer.data["ownerId"],
            cmty_country=listFriendsSerializer.data["countryCode"],
            cmty_cmtylevel=1)

        for i in community:

            try:
                hrewpoints = RewardsModel.objects.get(
                    hrew_userid=i.cmty_memberid,
                    hrew_country=i.cmty_country,
                    hrew_period=period)
            except:
                return Response({"errId": 73, "errMessage": gen001errormanagement(73, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = UserModel.objects.using(
                    "user").get(user_Prog=i.cmty_memberid)
            except:
                return Response({"errId": 74, "errMessage": gen001errormanagement(74, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)

            friends_info = {}
            friends_info = {
                "friends_userprog": hrewpoints.hrew_userid,
                "friends_usermail": user.user_Mail,
                "friends_countrycode": hrewpoints.hrew_country,
                "friends_period": hrewpoints.hrew_period,
                "friends_status": i.cmty_status,
                "friends_friendscount:": hrewpoints.hrew_friendscount,
                "friends_cmtycount": hrewpoints.hrew_cmtycount,
                "friends_level": hrewpoints.hrew_userlevel,
                "friends_levelperc": int(hrewpoints.hrew_levelperc),
                "friends_rewpoints": hrewpoints.hrew_userrp,
                "friends_cmtyrewpoints": hrewpoints.hrew_cmtyrp
            }
            data.append(friends_info)
            seen_data.add(tuple(friends_info.items()))

    except:
        return Response({"errId": 32, "errMessage": gen001errormanagement(32, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"errId": 0, "errMessage": "Success", "RC": 00, "data": data}, status=status.HTTP_200_OK)
