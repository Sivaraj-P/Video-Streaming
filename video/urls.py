from django.urls import path
from .views import VideoAPIView


urlpatterns=[
    path('videos',VideoAPIView.as_view(),name="video"),
    path('videos/<int:id>',VideoAPIView.as_view(),name="video_id"),
]

