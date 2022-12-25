from django.urls import path
from . import views

urlpatterns = [
    path("amenity/", views.Amenities.as_view()),
    path("amenity/<int:pk>", views.AmenityDetail.as_view()),
]
