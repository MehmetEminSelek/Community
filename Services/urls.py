from django.urls import path
from . import cmty001insertcommunity, cmty002usercommunitycountries, cmty003usercommuntyfriends, cmty004rewardpointassignment
from . import cmty005earnmanagement, cmty006getusercommunitydata
# from . import datacmty999test


urlpatterns = [
    path('cmty001', cmty001insertcommunity.cmty001insertcommunity),
    path('cmty002', cmty002usercommunitycountries.cmty002usercommunitycountries),
    path('cmty003', cmty003usercommuntyfriends.cmty003usercommuntyfriends),
    path('cmty004', cmty004rewardpointassignment.cmty004rewardpointassignment),
    path('cmty005', cmty005earnmanagement.cmty005earnmanagement),
    path('cmty006', cmty006getusercommunitydata.cmty006getusercommunitydata),
    # path('cmty999', cmty002usercommunitycountries.cmty002usercommunitycountries),
]
