from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import (
    CountryViewSet, CityDetailAPIView,CityListAPIView, ServiceViewSet,HotelListAPIView,HotelDetailAPIView, RoomEditViewAPIView,ReviewCreateAPIView,HotelCreteViewAPIView,RoomCreteViewAPIView,
    RoomListAPIView,RoomDetailAPIView, ReviewUpdateAPIView,BookingViewSet, ReviewListAPIView,ReviewDetailAPIView, UserProfileDetailAPIView,UserProfileListAPIView,HotelEditViewAPIView,
RegisterView,LoginView,LogoutView
)

router = SimpleRouter()

router.register(r'booking', BookingViewSet)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='user_register'),
    path('login/', LoginView.as_view(), name='user_login'),
    path('logout/', LogoutView.as_view(), name='user_logout'),


    path('', include(router.urls)),
    path('city/', CityListAPIView.as_view(), name='city-list'),
    path('city/<int:pk>/', CityDetailAPIView.as_view(), name='city-detail'),
    path('hotel/', HotelListAPIView.as_view(), name='hotel-list'),
    path('hotel/<int:pk>/', HotelDetailAPIView.as_view(), name='hotel-detail'),
    path('room/', RoomListAPIView.as_view(), name='room-list'),
    path('room/<int:pk>/', RoomDetailAPIView.as_view(), name='room-detail'),
    path('review/', ReviewListAPIView.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail'),
    path('review/create/', ReviewCreateAPIView.as_view(), name='review-create'),
    path('review/<int:pk>/update/', ReviewUpdateAPIView.as_view(), name='review_update'),
    path('user/', UserProfileListAPIView.as_view(), name='userprofile-list'),
    path('user/<int:pk>/', UserProfileDetailAPIView.as_view(), name='userprofile-detail'),

    path('hotel/create/', HotelCreteViewAPIView.as_view(), name='hotel_create'),
    path('hotel/<int:pk>/edit/', HotelEditViewAPIView.as_view(), name='hotel_edit'),
    path('room/create/', RoomCreteViewAPIView.as_view(), name='room_create'),
    path('room/<int:pk>/edit/', RoomEditViewAPIView.as_view(), name='room_update'),

]