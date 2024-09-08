from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import login
from .models import Restaurant, User, Menu, Vote
from .serializers import  RestaurantSerializer, UserSerializer, MenuSerializer, LoginSerializer, VoteSerializer
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken



@api_view(['POST'])
@permission_classes([AllowAny])
def custom_login(request):
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        return Response({
            'message': 'Login successful',
            'access': access_token,
            'refresh': refresh_token
        }, status=200)
    
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_restaurants(request):

    restaurants = Restaurant.objects.all()
    serializer = RestaurantSerializer(restaurants, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_restaurant(request):
    serializer = RestaurantSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_menu(request, restaurant_id, day_of_week):
    try:
        menu = Menu.objects.get(restaurant__id=restaurant_id, day_of_week=day_of_week)
        restaurant_name = menu.restaurant.name
        serializer = MenuSerializer(menu).data
        serializer['restaurant_name'] = restaurant_name  
        return Response(serializer, status=200)
    except Menu.DoesNotExist:
        return Response({"error": "Menu not found for this day"}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_menu(request):
    serializer = MenuSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vote(request):
    user = request.user  # Get the user from the session
    serializer = VoteSerializer(data=request.data)

    if serializer.is_valid():
        today = timezone.now().date()
        if Vote.objects.filter(user_id=user, vote_time__date=today).exists():
            return Response({"error": "You have already voted today"}, status=status.HTTP_400_BAD_REQUEST)

        vote = serializer.save(user_id=user, vote_time=timezone.now())
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_daily_votes(request):
    today = timezone.now().date()
    current_weekday = today.strftime('%A').lower()

    menus = Menu.objects.filter(day_of_week=current_weekday)

    if not menus.exists():
        return Response({"message": "No menus available for today."}, status=status.HTTP_404_NOT_FOUND)

    vote_results = []
    for menu in menus:
        vote_count = Vote.objects.filter(menu_id=menu.id, vote_time__date=today).count()
        vote_results.append({
            'menu_id': menu.id,
            'restaurant': menu.restaurant.name,
            'day_of_week': menu.day_of_week,
            'items': menu.items,
            'vote_count': vote_count
        })
    
    return Response(vote_results, status=status.HTTP_200_OK)