# from rest_framework.decorators import api_view
# from rest_framework.exceptions import NotFound
# from rest_framework.status import HTTP_204_NO_CONTENT
# from rest_framework.response import Response

from .models import Category
from .serializers import CategorySerializer

# from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# class Categories(APIView):
#     def get(self, request):
#         all_category = Category.objects.all()
#         serializer = CategorySerializer(all_category, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             new_category = serializer.save()
#             return Response(CategorySerializer(new_category).data)
#         else:
#             return Response(serializer.errors, status=400)


# class CategoryDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Category.objects.get(pk=pk)
#         except Category.DoesNotExist:
#             raise NotFound

#     def get(self, request, pk):
#         category = self.get_object(pk)
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         category = self.get_object(pk)
#         serializer = CategorySerializer(
#             category,
#             data=request.data,
#             partial=True,
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=400)

#     def delete(self, request, pk):
#         category = self.get_object(pk)
#         category.delete()
#         return Response(status=HTTP_204_NO_CONTENT)


# @api_view(["GET", "POST"])
# def categories(request):
#     if request.method == "GET":
#         all_category = Category.objects.all()
#         serializer = CategorySerializer(all_category, many=True)

#         return Response(serializer.data)

#     elif request.method == "POST":
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             # serializer의 create method를 찾음
#             new_category = serializer.save()
#             return Response(CategorySerializer(new_category).data)
#         else:
#             return Response(serializer.errors, status=400)


# @api_view(["GET", "PUT", "DELETE"])
# def category(request, pk):
#     try:
#         category = Category.objects.get(pk=pk)
#     except Category.DoesNotExist:
#         raise NotFound

#     if request.method == "GET":
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)

#     elif request.method == "PUT":
#         serializer = CategorySerializer(
#             category,
#             data=request.data,
#             partial=True,
#         )
#         if serializer.is_valid():
#             # serializer에 instance를 같이 넘겨주면 update method를 찾음
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=400)

#     elif request.method == "DELETE":
#         category.delete()
#         return Response(status=HTTP_204_NO_CONTENT)
