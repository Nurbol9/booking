from django_filters.rest_framework import FilterSet
from .models import Hotel, Room


class HotelFilter(FilterSet):
    class Meta:
        model = Hotel
        fields = {
            'hotel_star': ['exact', 'gt', 'lt'],
            'country': ['exact'],
            'city': ['exact'],
            'service': ['exact'],
        }


class RoomFilter(FilterSet):
    class Meta:
        model = Room
        fields = {
            'price': ['exact', 'gt', 'lt'],
            'room_type': ['exact'],
            'room_status': ['exact'],
        }