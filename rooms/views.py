from django.db import transaction

from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, PermissionDenied, ParseError

from .models import Amenity, Room
from categories.models import Category

from .serializers import AmenitySerializer, RoomDetailSerializer, RoomListSerializer


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            new_amenity = serializer.save()
            return Response(AmenitySerializer(new_amenity).data)
        else:
            return Response(serializer.errors, status=400)


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
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=204)


class Rooms(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True)
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
                        raise ParseError("Category should be a rooms")
            
                except Category.DoesNotExist:
                    raise ParseError("Category not found")
                
                try:
                    # 이 아래 query들은 하나의 transaction으로 묶어줘야 함
                    with transaction.atomic():
                        # request.user를 serializer의 validated_data에 넣어줌
                        # serializer returns model instance
                        new_room = serializer.save(owner=request.user, category=category)
                
                        # amenities 는 required field가 아니기 때문에 instance를 먼저 만들고 추가해줘야 함
                        amenities = request.data.get("amenities")
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            # for many to many relationship
                            new_room.amenities.add(amenity)
                            # new_room.amenities.remove(amenity)
                        serializer = RoomDetailSerializer(new_room)
                        return Response(serializer.data)
                except:
                    raise ParseError("Amenity not found")
            else:
                return Response(serializer.errors, status=400)
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
        serializer = RoomDetailSerializer(room)
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
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required")
            try:
                category = Category.objects.get(pk=category_pk)

                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("Category should be a rooms")
        
            except Category.DoesNotExist:
                raise ParseError("Category not found")
            
            try:
                with transaction.atomic():
                    new_room = serializer.save(category=category)
            
                    amenities = request.data.get("amenities")
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        new_room.amenities.add(amenity)
                    serializer = RoomDetailSerializer(new_room)
                    return Response(serializer.data)
            except:
                raise ParseError("Amenity not found")
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        room = self.get_object(pk)

        # check if user is owner of the room
        if not request.user.is_authenticated:
            raise NotAuthenticated
    
        if room.owner != request.user:
            raise PermissionDenied

        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)
