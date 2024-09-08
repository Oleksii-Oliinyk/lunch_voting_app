from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [

    path('login/', views.custom_login, name='login'),

    path("get_restaurants/", views.get_restaurants, name="Get Restaurants"),
    path("add_restaurant/", views.add_restaurant, name="Add Restaurants"),
    
    path("get_users/", views.get_users, name = "Get Users"),
    path("add_user/", views.add_user, name = "Add User"),
    
    path('menu/add/', views.add_menu, name="add_menu"),
    path('menu/<int:restaurant_id>/<str:day_of_week>/', views.get_menu, name="Get Menu"),

    path('vote/', views.vote, name="Vote for Menu"),
    path('get_daily_votes/', views.get_daily_votes, name="Vote for Menu"),
]