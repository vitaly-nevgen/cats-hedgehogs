from django.contrib import admin
from django.urls import path, include

from rest_framework.authtoken import views


from cats_hedgehogs.pets.api_views import PetListApi, PetDetailApi
from cats_hedgehogs.lots.api_views import LotListApi, LotDetailApi
from cats_hedgehogs.bids.api_views import BidListApi, BidDetailApi, BidAcceptView

"""
/pet/ (show only user's)
/pet/<pet_pk>


/lot/ (POST, GET) (all lots) ?only_mine=True
/lot/<lot_pk> GET, PUT, DELETE 

/lot/<lot_pk>/bid (POST, GET)
/lot/<lot_pk>/bid/<bid_pk> (GET, PUT, DELETE)


/lot/<lot_pk>/bid/<bid_pk>/accept (POST) (if author?)
"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('session/', include('rest_framework.urls')),

    path('api/token/', views.obtain_auth_token),
    path('api/pet/', PetListApi.as_view(), name='pet-list'),
    path('api/pet/<pet_pk>', PetDetailApi.as_view(), name='pet-detail'),

    path('api/lot/', LotListApi.as_view(), name='lot-list'),
    path('api/lot/<lot_pk>/', LotDetailApi.as_view(), name='lot-detail'),
    path('api/lot/<lot_pk>/bid/', BidListApi.as_view(), name='bid-list'),
    path('api/lot/<lot_pk>/bid/<bid_pk>/', BidDetailApi.as_view(), name='bid-detail'),
    path('api/lot/<lot_pk>/bid/<bid_pk>/accept', BidAcceptView.as_view(), name='bid-accept'),
]
