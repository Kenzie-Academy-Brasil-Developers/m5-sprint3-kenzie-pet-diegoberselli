from email import message

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from animals.serializers import AnimalSerializer

from .models import Animal

# Create your views here.


class AnimalView(APIView):
    def get(self, request):

        animal = Animal.objects.all()
        serializer = AnimalSerializer(animal, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AnimalSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AnimalViewDetail(APIView):
    def get(self, request, animal_id):
        try:
            animal = Animal.objects.get(id=animal_id)
        except Animal.DoesNotExist:
            return Response(
                {"message": "Animal not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = AnimalSerializer(animal)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, animal_id):
        try:
            animal = Animal.objects.get(id=animal_id)
            animal.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Animal.DoesNotExist:
            return Response(
                {"message": "Animal not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, animal_id):
        try:
            animal = Animal.objects.get(id=animal_id)
        except Animal.DoesNotExist:
            return Response(
                {"message": "Animal not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = AnimalSerializer(animal, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        try:
            serializer.save()
        except KeyError as error:
            return Response({"message": error.args[0]}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
            
        return Response(serializer.data, status=status.HTTP_200_OK)
