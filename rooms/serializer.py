from rest_framework import serializers
from .models import Amenity, Room
from users.serializer import TinyUserSerializer
from categories.serializers import CategorySerializer


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
        )
        depth = 1

    rating = serializers.SerializerMethodField

    def get_rating(self, room):
        return room.rating()


class RoomDetailSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField()

    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(
        read_only=True,
    )

    class Meta:
        model = Room
        fields = "__all__"
        depth = 1

    def get_rating(self, room):
        return room.rating()
