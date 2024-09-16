from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from wishlists.models import Wishlist
from wishlists.serializers import WishlistSerializer


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

    def get(self, request, pk):
        pass
