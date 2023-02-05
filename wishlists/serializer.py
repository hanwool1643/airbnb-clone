from rest_framework.serializers import ModelSerializer
from rooms.serializer import RoomListSerializer
from .models import Wishlist


class WishlistSerializer(ModelSerializer):

    rooms = RoomListSerializer(read_only=True, many=True)

    class Meta:
        model = Wishlist
        fields = (
            "name",
            "rooms",
        )