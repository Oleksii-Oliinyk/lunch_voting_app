from rest_framework import serializers
from .models import Restaurant, User, Menu, Vote

from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        
        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        data['user'] = user 
        return data

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'version', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True},
            'created_at': {'read_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class MenuSerializer(serializers.ModelSerializer):

    restaurant_name = serializers.ReadOnlyField(source='restaurant.name') 

    class Meta:
        model = Menu
        fields = ['id', 'restaurant','restaurant_name', 'day_of_week', 'items', 'create_at', 'updated_at']


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = [ 'menu_id', 'vote_time']

class VoteCountSerializer(serializers.ModelSerializer):
    vote_count = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'day_of_week', 'items', 'vote_count']

    def get_vote_count(self, obj):
        return obj.votes.filter(vote_time__date=timezone.now().date()).count()    