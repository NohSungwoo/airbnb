from unicodedata import category

from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import (
    NotAuthenticated,
    NotFound,
    ParseError,
    PermissionDenied,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from categories.models import Category
from reviews.serializers import ReviewSerializer
from rooms.models import Amenity, Room
from rooms.serializers import (
    AmenitySerializer,
    RoomDetailSerializer,
    RoomListSerializer,
)
from medias.serializers import PhotoSerializer


class Amenities(APIView):

    def get(self, request):
        all_amenity = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenity, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        amenity = serializer.save()
        return Response(AmenitySerializer(amenity), status=status.HTTP_201_CREATED)


class AmenityDetail(APIView):

    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors)

        updated_amenity = serializer.save()
        return Response(
            AmenitySerializer(updated_amenity).data, status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Rooms(APIView):

    def get(self, request):
        all_rooms = Room.objects.all()

        serializer = RoomListSerializer(
            all_rooms, many=True, context={"request": request}
        )

        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            raise NotAuthenticated

        serializer = RoomDetailSerializer(data=request.data)
        category_id = request.data.get("categories")
        amenity_ids = request.data.get("amenities")

        if not category_id:
            raise ParseError("Category is required")
        if not amenity_ids:
            raise ParseError("Amenities are required")

        try:
            category = Category.objects.get(pk=category_id)

            if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                raise ParseError("The category kind should be rooms")

        except Category.DoesNotExist:
            raise NotFound("Category Not Found")

        if not serializer.is_valid():
            return Response(serializer.errors)

        with transaction.atomic():
            room = serializer.save(owner=request.user, categories=category)

            # Amenities는 ManyToMany Field
            for amenity_id in amenity_ids:
                amenity = Amenity.objects.get(pk=amenity_id)
                room.amenities.add(amenity)

        return Response(status=status.HTTP_201_CREATED)


class RoomDetail(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)

        serializer = RoomDetailSerializer(room, context={"request": request})

        return Response(serializer.data)

    def put(self, request, pk):
        # 유저 인증
        if not request.user.is_authenticated:
            raise NotAuthenticated

        try:
            room = self.get_object(pk)

        except Room.DoesNotExist:
            raise NotFound("Room DoesNotExist")

        # 유저 권한 확인
        if request.user != room.owner:
            raise PermissionDenied

        try:
            category_id = request.data["categories"]
            amenity_ids = request.data["amenities"]
        except KeyError:
            raise ParseError(f"{KeyError.args[0]} is required")

        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            raise NotFound("Category Not Found")

        if Category.CategoryKindChoices.EXPERIENCES == category.kind:
            raise ParseError("The category kind should be rooms")

        serializer = RoomDetailSerializer(room, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors)

        if transaction.atomic():
            updated_room = serializer.save()

            try:
                for amenity_id in amenity_ids:
                    amenity = Amenity.objects.get(pk=amenity_id)
                    room.amenities.add(amenity)
            except Amenity.DoesNotExist:
                raise NotFound("Amenity NotFound")

            return Response(RoomDetailSerializer(updated_room).data)

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            raise NotAuthenticated

        room = self.get_object(pk)

        if request.user != room.owner:
            raise PermissionDenied

        room.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomReviews(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)

        except Room.DoesNotExist:
            raise NotFound("Room DoesNotExist")

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))

            if page < 1:
                page = 1

        except ValueError:
            page = 1

        page_size = 5
        start = (page - 1) * page_size
        end = start + page_size

        room = self.get_object(pk)
        reviews = room.reviews.all()[start:end]

        serializer = ReviewSerializer(reviews, many=True)

        return Response(serializer.data)


class RoomAmenities(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)

        except Room.DoesNotExist:
            raise NotFound("Room DoesNotExist")

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))

            if page < 1:
                page = 1

        except ValueError:
            page = 1

        page_size = 5
        start = (page - 1) * page_size
        end = page * page_size

        room = self.get_object(pk)
        amenities = room.amenities.all()[start:end]

        serializer = AmenitySerializer(amenities, many=True)

        return Response(serializer.data)


class RoomPhotos(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)

        except Room.DoesNotExist:
            raise NotFound("Room DoesNotExist")

    def post(self, request, pk):
        if not request.user.is_authenticated:
            raise NotAuthenticated

        room = self.get_object(pk)

        if request.user != room.owner:
            raise PermissionDenied

        serializer = PhotoSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        if room.categories == Category.CategoryKindChoices.EXPERIENCES:
            raise ParseError("Category is should be room")

        photo = serializer.save(room=room)

        serializer = PhotoSerializer(photo)

        return Response(serializer.data)
