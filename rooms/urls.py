from django.urls import path
from . import views

urlpatterns = [
    path("", views.Rooms.as_view()),
    path("<int:pk>", views.RoomDetail.as_view()),
    path("amenity/", views.Amenities.as_view()),
    path("amenity/<int:pk>", views.AmenityDetail.as_view()),
]
