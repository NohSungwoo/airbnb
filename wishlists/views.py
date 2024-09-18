from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rooms.models import Room
from wishlists.models import Wishlist
from wishlists.serializers import WishlistSerializer
from rest_framework import status

class Wishlists(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        all_wishlists = Wishlist.objects.filter(user=user)

        serializer = WishlistSerializer(
            all_wishlists, many=True, context={"request": request}
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        wishlists = serializer.save(user=request.user)

        serializer = WishlistSerializer(wishlists)

        return Response(serializer.data)


class WishlistDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)

        except Wishlist.DoesNotExist:
            raise NotFound("Wishlist DoesNotExist")

    def get(self, request, pk):
        user = request.user
        wishlist = self.get_object(pk, user)

        serializer = WishlistSerializer(wishlist, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        user = request.user
        wishlist = self.get_object(pk, user)

        serializer = WishlistSerializer(wishlist, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors)

        wishlist = serializer.save()

        serializer = WishlistSerializer(wishlist, context={"request": request})

        return Response(serializer.data)


    def delete(self, request, pk):
        user = request.user
        wishlist = self.get_object(pk, user)

        wishlist.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class WishlistToggle(APIView):

    def get_wishlist(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)

        except Wishlist.DoesNotExist:
            raise NotFound

    def get_room(self, room_pk):
        try:
            return Room.objects.get(pk=room_pk)

        except Room.DoesNotExist:
            raise NotFound

    def put(self, request, pk, room_pk):
        user = request.user
        wishlist = self.get_wishlist(pk, user)
        room = self.get_room(room_pk)

        if wishlist.rooms.filter(pk=room.pk).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)

        return Response(status=status.HTTP_200_OK)
