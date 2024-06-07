from django.urls import path
from .views import UserApiView,LoginAPIView


urlpatterns=[
    path('login',LoginAPIView.as_view(),name='login'),
    path('user',UserApiView.as_view(),name='user')
]