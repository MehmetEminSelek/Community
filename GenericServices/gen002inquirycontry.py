from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import datetime
from Models.models import *
from .serializers import *
from .gen001errormanagement import gen001errormanagement

# TODO: what does Check counter_input filled in


def gen002inquirycontry(request):
    gen002data = GEN002Serializer(data=request)
    if gen002data.is_valid():
        if gen002data["queryType"] == 1:
            if gen002data["counter"] != CountryModel.objects.all().count():
                try:
                    countryTable = CountryModel.objects.all()
                except:
                    return Response({"errId": 31, "errMessage": gen001errormanagement(31, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
            if gen002data["countryName"] == "":
                try:
                    countryTable = CountryModel.objects.filter(
                        countryCode=gen002data["countryCode"])
                except:
                    return Response({"errId": 31, "errMessage": gen001errormanagement(31, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
            try:
                CountryModel.objects.filter(countryCode=gen002data["countryCode"])[
                    :gen002data["counter"]]
            except:
                return Response({"errId": 31, "errMessage": gen001errormanagement(31, request.data), "errDate": datetime.now()}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"errId": 0, "errMessage": "Success", "RC": 00}, status=status.HTTP_200_OK)
        elif gen002data["queryType"] == 2:
            try:
                countryTable = CountryModel.objects.filter(
                    countryCode=gen002data["countryCode"])
            except:
                return Response({"errId": 5, "errMessage": gen001errormanagement(5, request.data), "RC": 99}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"errId": 0, "errMessage": "Success", "Ouput Data": countryTable, "RC": 00}, status=status.HTTP_200_OK)
