import logging

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from Models.models import *
from .serializers import *
from GenericServices.gen001errormanagement import gen001errormanagement

logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method='post',
    operation_id='User Community Countries',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'userLanguage': openapi.Schema(type=openapi.TYPE_STRING, maxLength=2, description='User language choice, necessary information for Gen001errormanagement service'),
            'ownerId': openapi.Schema(type=openapi.TYPE_INTEGER, min_value=1, description='Owner ID of Community')
        },

        required=['userLanguage', 'ownerId']
    ),
    responses={200: "Post list of country", },
    operation_description="List of country in which user has an active community"
)
@api_view(['POST'])
def cmty002usercommunitycountries(request):
    data = []
    seen_data = set()
    listCountrySerializer = ListCountrySerializer(data=request.data)
    if listCountrySerializer.is_valid() == False:
        return Response({"errId": 2, "errMessage": gen001errormanagement(2, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
    try:
        community = CommunityModel.objects.filter(
            cmty_ownerid=listCountrySerializer.data["ownerId"])

        for i in community:
            countryCode = i.cmty_country
            ownerId = i.cmty_ownerid
            country_info = {}
            country_info = {
                "country_countrycode": countryCode, "ownerId": ownerId}
            if tuple(country_info.items()) not in seen_data:
                data.append(country_info)
                seen_data.add(tuple(country_info.items()))

        # # THIS ONE IS NOT WORKING THE QUERY IS RIGHT BUT I SUPPOSE THE WAY I AM TRYING TO GET THE DATA IS WRONG
        # countries1 = CountryModel.objects.using("db999").filter(
        #     country_countrycode__in=community
        # ).values_list(
        #     'country_name', flat=True
        # ).distinct().order_by('country_name').values('country_countrycode', 'country_name')

        # countries3 = CountryModel.objects.using("db999").filter(country_countrycode__in=CommunityModel.objects.using("default").filter(cmty_ownerid=listCountrySerializer.data["ownerId"]).values_list(
        #     'cmty_country', flat=True).distinct()).order_by('country_name').values('country_countrycode', 'country_name')

        # countries = CountryModel.objects.using("db999").filter(
        #     country_countrycode=community.cmty_country).order_by('country_name')
        # for country in countries:
        #     data = [{'country_countrycode': country.country_countrycode,
        #              'country_name': country.country_name}]
    except:
        return Response({"errId": 32, "errMessage": gen001errormanagement(32, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"errId": 0, "errMessage": "Success", "RC": 00, "data": data}, status=status.HTTP_200_OK)
