from gc import get_objects

from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Perk
from .serializers import PerkSerializer


class Perks(APIView):

    def get(self, request):

        all_perks = Perk.objects.all()

        serializer = PerkSerializer(all_perks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        perk = serializer.save()

        return Response(PerkSerializer(perk).data, status=status.HTTP_201_CREATED)


class PerkDetail(APIView):

    def get_object(self, request, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)

        serializer = PerkSerializer(perk)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        perk = self.get_object(pk)

        serializer = PerkSerializer(perk, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors)

        updated_perk = serializer.save()

        return Response(PerkSerializer(updated_perk).data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

