from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Amenity, Room
from .serializer import (
    AmenitySerializer,
    RoomListSerializer,
    RoomDetailSerializer,
    ReviewSerializer,
)
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT
from categories.models import Category
from django.db import transaction
from django.conf import settings
from medias.serializer import PhotoSerializer


class Amenities(APIView):
    def get(self, request):
        all_Amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_Amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)

        if serializer.is_valid():
            amenity = serializer.save()
            return Response(
                AmenitySerializer(amenity).data,
            )
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        return Response(AmenitySerializer(amenity).data)

    def put(self, request, pk):
        serializer = AmenitySerializer(
            self.get_object(pk),
            request.data,
            partial=True,
        )

        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    def get(self, request):
        all_Rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_Rooms,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError("Category is required")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("Category kind should be 'rooms'")
                except Category.DoesNotExist:
                    raise ParseError("Category not found")

                try:
                    with transaction.atomic():
                        room = serializer.save(
                            owner=request.user,
                            category=category,
                        )
                        amentities = request.data.get("amenities")
                        for amenity_pk in amentities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                        serializer = RoomDetailSerializer(room)
                        return Response(serializer.data)
                except Exception:
                    raise ParseError("Amenity not found")
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(
            room,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            if request.user == room.owner:
                category_pk = request.data.get("category")
                if category_pk:  # category_pk가 있을 떄
                    try:
                        category = Category.objects.get(pk=category_pk)
                        if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                            raise ParseError("Category kind should be 'rooms'")
                    except Category.DoesNotExist:
                        raise ParseError("Category not found")
                    try:
                        with transaction.atomic():
                            room = serializer.save(
                                owner=request.user,
                                category=category,
                            )
                            amenities = request.data.get("amenities")
                            if not amenities:  # amenities가 없을 때
                                return Response(RoomDetailSerializer(room).data)
                            room.amenities.clear()
                            for amenity_pk in amenities:  # amenities가 있을 때
                                amenity = Amenity.objects.get(pk=amenity_pk)
                                room.amenities.add(amenity)
                            serializer = RoomDetailSerializer(room)
                            return Response(serializer.data)
                    except Amenity.DoesNotExist:
                        raise ParseError("Amenity not found")
                else:  # category_pk 없을떄
                    try:
                        with transaction.atomic():
                            room = serializer.save()
                            amenities = request.data.get("amenities")
                            if not amenities:  # amenities가 없을 때
                                return Response(RoomDetailSerializer(room).data)
                            room.amenities.clear()
                            for amenity_pk in amenities:  # amenities가 있을 때
                                amenity = Amenity.objects.get(pk=amenity_pk)
                                room.amenities.add(amenity)
                            serializer = RoomDetailSerializer(room)
                            return Response(serializer.data)
                    except Amenity.DoesNotExist:
                        raise ParseError("Amenity not found")
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReview(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):

        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except:  # request.query_params가 {'page': 'string'} 일 경우 대비
            page = 1

        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)


class RoomAmenity(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except:
            raise ParseError("Room not found")

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except:
            page = 1
        room = self.get_object(pk)
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        serializer = AmenitySerializer(room.amenities.all()[start:end], many=True)
        return Response(serializer.data)


class RoomPhotos(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk)

        if not request.user.is_authenticated:
            raise NotAuthenticated
        if request.user != room.owner:
            raise PermissionDenied

        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)

        
