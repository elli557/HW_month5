from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, ProductReviewSerializer, CategoryWithCountSerializer, CategoryValidateSerializer, ProductValidateSerializer, ReviewValidateSerializer

@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CategoryValidateSerializer(data=request.data)
        if serializer.is_valid():
            category = Category.objects.create(name=serializer.validated_data['name'])
            return Response(CategorySerializer(category).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CategoryValidateSerializer(data=request.data)
        if serializer.is_valid():
            category.name = serializer.validated_data['name']
            category.save()
            return Response(CategorySerializer(category).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductValidateSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                product = Product.objects.create(title=serializer.validated_data['title'], description=serializer.validated_data.get('description', ''), price=serializer.validated_data['price'], category_id=serializer.validated_data['category_id'])
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        if serializer.is_valid():
            product.title = serializer.validated_data['title']
            product.description = serializer.validated_data.get('description', '')
            product.price = serializer.validated_data['price']
            product.category_id = serializer.validated_data['category_id']
            product.save()
            return Response(ProductSerializer(product).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def review_list(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                review = Review.objects.create(text=serializer.validated_data['text'], product_id=serializer.validated_data['product_id'], stars=serializer.validated_data['stars'])
            return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        if serializer.is_valid():
            review.text = serializer.validated_data['text']
            review.product_id = serializer.validated_data['product_id']
            review.stars = serializer.validated_data['stars']
            review.save()
            return Response(ReviewSerializer(review).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def category_list_with_count(request):
    categories = Category.objects.all()
    serializer = CategoryWithCountSerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_list_with_reviews_and_rating(request):
    products = Product.objects.all()
    serializer = ProductReviewSerializer(products, many=True)
    return Response(serializer.data)