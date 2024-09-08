from rest_framework.decorators import api_view
from .models import Category
from .serializers import CategorySerializer
from rest_framework.response import Response


@api_view(["GET", "POST"])
def categories(request):

    if request.method == "GET":
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data)

    else:
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save()

            return Response(CategorySerializer(new_category).data)

        else:
            return Response(serializer.errors)


@api_view()
def category(request, pk):
    category = Category.objects.get(pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)
