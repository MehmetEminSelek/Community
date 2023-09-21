import logging

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import datetime
from Models.models import *
from .serializers import *
from datetime import datetime
from GenericServices.gen001errormanagement import gen001errormanagement

logger = logging.getLogger(__name__)


@api_view(['POST'])
def cmty006getusercommunitydata(request):
    # data = []
    # seen_data = set()
    year = datetime.now().year
    month = datetime.now().month
    period = str(year) + "-" + str(month)
    print('period', period)
    print(request)
    UserCommunityDataSerializer = UserCommunityDataSerializer(
        data=request.data)
    err = gen001errormanagement(UserCommunityDataSerializer.initial_data)
    if UserCommunityDataSerializer.is_valid() == False:
        return Response({"errId": 2, "errMessage": err[30], "RC": 99}, status=status.HTTP_400_BAD_REQUEST)

    try:
        hrewpoints = RewardsModel.objects.get(
            hrew_userid=UserCommunityDataSerializer.data["ownerId"],
            hrew_country=UserCommunityDataSerializer.data["countryCode"],
            hrew_period=period)
    except:
        return Response({"errId": 10, "errMessage": "dbError: get hrewpoint", "RC": 99}, status=status.HTTP_400_BAD_REQUEST)

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
    # data.append(friends_info)
    # seen_data.add(tuple(friends_info.items()))
    return Response({"errId": 0, "errMessage": "Success", "RC": 00, "data": user_info}, status=status.HTTP_200_OK)
