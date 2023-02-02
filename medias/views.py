from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import Photo
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class PhotoDetail(APIView):
    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):

        permission_classes = [IsAuthenticated]

        photo = self.get_object(pk)
        if (photo.room and request.user != photo.room.owner) or (
            photo.experience and photo.experience.host != request.user
        ):
            return PermissionDenied

        photo.delete()
        return Response(status=HTTP_200_OK)
