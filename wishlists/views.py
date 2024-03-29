from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist
from .serializers import WishlistSerializer
from rest_framework.response import Response


class Wishlists(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(
            wishlists,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            wishlist = serializer.save(user=request.user)
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
