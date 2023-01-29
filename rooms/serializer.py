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


class RoomDetailSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    owner = TinyUserSerializer(
        read_only=True
    )  # read_only=True: RoomDetailSerializer 사용시 owner 요구하지 않음
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

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user


class RoomListSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
        )

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return request.user == room.owner
