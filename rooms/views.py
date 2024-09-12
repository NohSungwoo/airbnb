from rest_framework.exceptions import NotFound
from rest_framework.views import APIView

from rooms.models import Amenity
from rooms.serializers import AmenitySerializer
from rest_framework.response import Response
from rest_framework import status


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
        return Response(AmenitySerializer(updated_amenity).data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
