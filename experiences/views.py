from django.db import transaction

from rest_framework import status
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from categories.models import Category
from .models import Perk, Experience
from .serializers import PerkSerializer, ExperienceSerializer


class Experiences(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):

        all_experiences = Experience.objects.filter(category__kind=Category.CategoryKindChoices.EXPERIENCES)

        serializer = ExperienceSerializer(all_experiences, many=True)

        return Response(serializer.data)

    def post(self, request):

        serializer = ExperienceSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        perks_pk = request.data.get("perks")
        category_pk = request.data.get("categories")
        host = request.user

        try:
            category = Category.objects.get(pk=category_pk)
        except Category.DoesNotExist:
            raise ParseError("Category NotFound")

        if category.kind != Category.CategoryKindChoices.EXPERIENCES:
            raise ParseError("Category must be an Experience")

        with transaction.atomic():
            experience = serializer.save(host=host, category=category)

            for perk_pk in perks_pk:
                try:
                    perk = Perk.objects.get(pk=perk_pk)
                    experience.perks.add(perk)

                except Perk.DoesNotExist:
                    raise NotFound("Perk is does not exist")

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ExperienceDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)

        except Experience.DoesNotExist:
            raise NotFound

    def put(self, request, pk):

        user = request.user
        experience = self.get_object(pk)
        perk_pks = request.data.get("perks", [])

        if user != experience.host:
            raise PermissionDenied

        serializer = ExperienceSerializer(experience, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors)

        with transaction.atomic():
            experience = serializer.save()
            experience.perks.clear()

            for perk_pk in perk_pks:
                try:
                    perk = Perk.objects.get(pk=perk_pk)
                    experience.perks.add(perk)

                except Perk.DoesNotExist:
                    return NotFound("Perk NotFound")

        serializer = ExperienceSerializer(experience)

        return Response(serializer.data)

    def delete(self, request, pk):
        experience = self.get_object(pk)

        experience.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)



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

    def get_object(self, pk):
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

        return Response(
            PerkSerializer(updated_perk).data, status=status.HTTP_201_CREATED
        )

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
