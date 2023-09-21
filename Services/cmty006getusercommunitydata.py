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
    operation_id='Get User Community Data',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'countryCode': openapi.Schema(type=openapi.TYPE_STRING, maxLength=2, description='User community country code'),
            'userLanguage': openapi.Schema(type=openapi.TYPE_STRING, maxLength=2, description='User language choice, necessary information for Gen001errormanagement service'),
            'ownerId': openapi.Schema(type=openapi.TYPE_INTEGER, description='Owner ID of Community')
        },

        required=['userLanguage', 'userProg',
                  'userCountry', 'year', 'month']
    ),
    responses={200: "Post all community data related to a specific user", },
    operation_description="Retrieve all community data related to a specific user"
)
@api_view(['POST'])
def cmty006getusercommunitydata(request):
    year = datetime.now().year
    month = datetime.now().month
    period = str(year) + "-" + str(month)
    userCommunityDataSerializer = UserCommunityDataSerializer(
        data=request.data)
    request.data["err_Service"] = "cmty006"
    request.data["err_Language"] = request.data["userLanguage"]
    if userCommunityDataSerializer.is_valid() == False:
        return Response({"errId": 2, "errMessage": gen001errormanagement(2, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
    try:
        hrewpoints = RewardsModel.objects.get(
            hrew_userid=userCommunityDataSerializer.data["ownerId"],
            hrew_country=userCommunityDataSerializer.data["countryCode"],
            hrew_period=period)
    except:
        return Response({"errId": 73, "errMessage": gen001errormanagement(73, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)

    # user_info = {}
    user_info = {
        "user_userprog": hrewpoints.hrew_userid,
        "user_countrycode": hrewpoints.hrew_country,
        "user_period": hrewpoints.hrew_period,
        "user_friendscount:": hrewpoints.hrew_friendscount,
        "user_cmtycount": hrewpoints.hrew_cmtycount,
        "user_level": hrewpoints.hrew_userlevel,
        "user_levelperc": int(hrewpoints.hrew_levelperc),
        "user_rewpoints": hrewpoints.hrew_userrp,
        "user_cmtyrewpoints": hrewpoints.hrew_cmtyrp,
        "user_userearn": hrewpoints.hrew_userearn,
        "user_userwin": hrewpoints.hrew_userwin
    }

    return Response({"RC": 00, "errId": 0, "errMessage": "Success", "data": user_info}, status=status.HTTP_200_OK)
