from django.urls import path , include
from .views import *

urlpatterns=[

    # path('users/',list_users),
    # path('users/<int:pk>/',retrieve_user)
    path("users/",UserViewset.as_view({"get":"get","post":"post"})),
    path("users/<int:id>/",UserViewset.as_view({"put":"update","delete":"remove"})),
    path("users/<str:email>/",UserViewset.as_view({"get":"search_user"}))
]