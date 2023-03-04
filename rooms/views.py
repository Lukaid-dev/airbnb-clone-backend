# django import convention

# from django
from django.db import transaction
from django.conf import settings
from django.utils import timezone

# from third party like rest_framework

from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, PermissionDenied, ParseError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

# from same app

from .models import Amenity, Room
from .serializers import AmenitySerializer, RoomDetailSerializer, RoomListSerializer

# from other apps

from categories.models import Category
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateBookingSerializer


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
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
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


class RoomDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(
            room,
            context={
                "request": request,
            },
        )
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)

        # # authentication check
        # if not request.user.is_authenticated:
        #     raise NotAuthenticated

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

        # # check if user is owner of the room
        # if not request.user.is_authenticated:
        #     raise NotAuthenticated

        if room.owner != request.user:
            raise PermissionDenied

        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    # pagination
    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = page_size * (page - 1)
        end = start + page_size
        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    # lazy loading
    # room.reviews.all()[start:end],

    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                room=room,
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class RoomAmenities(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1
        page_size = 3
        start = page_size * (page - 1)
        end = start + page_size
        room = self.get_object(pk)
        serializer = AmenitySerializer(
            room.amenities.all()[start:end],
            many=True,
        )
        return Response(serializer.data)


class RoomPhotos(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk)

        # # authentication check
        # if not request.user.is_authenticated:
        #     raise NotAuthenticated

        if room.owner != request.user:
            raise PermissionDenied

        serializer = PhotoSerializer(data=request.data)

        if serializer.is_valid():
            photo = serializer.save(
                room=room,
            )
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)


class RoomBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # IsAuthenticatedOrReadOnly means that all user can read (get) but only authenticated user can write (post, put, delete)

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        now = timezone.now().astimezone().date()
        # now = timezone.localtime(timezone.now()).date()
        print(now)
        Bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            check_in__gt=now,
        )
        serializer = PublicBookingSerializer(Bookings, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)
        # model에선 guest만 required이기 떄문에 client에서 guest만 보내도 valid하다고 나옴
        # 근데 상황에 따라 valid조건이 달라지기 때문에 serializer에서 validate를 통해 조건을 추가해줘야함
        serializer = CreateBookingSerializer(data=request.data, context={"room": room})

        if serializer.is_valid():
            booking = serializer.save(
                user=request.user,
                room=room,
                kind=Booking.BookingKindChoices.ROOM,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
