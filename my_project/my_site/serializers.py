from rest_framework import serializers
from .models import (
    Country, City, Service, Hotel, HotelImage,
    Room, RoomImage, Booking, Review, UserProfile
)


from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']


class CountryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name','country_image']


class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city_name', 'city_image']

class CityNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name']



class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name','last_name','role','country']



class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name']

class UserProfileReviewSerializer(serializers.ModelSerializer):
    country = CountryNameSerializer()

    class Meta:
        model = UserProfile
        fields = ['first_name', 'user_image','country']




class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['service_name', 'service_image']

class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['hotel_image']

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'




class HotelListSerializer(serializers.ModelSerializer):
    hotel_image = HotelImageSerializer(read_only=True,many=True)
    avg_rating = serializers.SerializerMethodField()
    count_review = serializers.SerializerMethodField()
    class Meta:
        model = Hotel
        fields = ['id', 'hotel_name','hotel_image','avg_rating','count_review']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_review(self, obj):
        return obj.get_count_review()

class CityDetailSerializer(serializers.ModelSerializer):
    hotel = HotelListSerializer(many=True, read_only=True)
    class Meta:
        model = City
        fields = ['id', 'city_name', 'city_image', 'hotel']


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ['id', 'room_image']

class RoomSerializers(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_type', 'hotel_number', 'room_status', 'price', 'max_guest', 'room_description']


class RoomDetailSerializer(serializers.ModelSerializer):
    room = RoomImageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'room_type', 'hotel_number', 'room_status', 'price',
                  'max_guest', 'room_description', 'room']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'



class ReviewListSerializer(serializers.ModelSerializer):
    user = UserProfileReviewSerializer()
    class Meta:
        model = Review
        fields = ['id','user','text',]

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','user','text',]



class ReviewDetailSerializer(serializers.ModelSerializer):
    user = UserProfileReviewSerializer()
    created_date = serializers.DateTimeField(format='%Y-%m-%d')
    class Meta:
        model = Review
        fields = ['user','text','rating', 'created_date']




class HotelDetailSerializer(serializers.ModelSerializer):
    city = CityNameSerializer()
    country = CountrySerializer()
    hotel_image = HotelImageSerializer(read_only=True, many=True)
    service = ServiceSerializer(many=True)
    owner = UserProfileNameSerializer()
    room_hotels = RoomListSerializer(many=True, read_only=True,)
    review_hotel = ReviewListSerializer(read_only=True, many=True)
    avg_rating = serializers.SerializerMethodField()
    count_review = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ['hotel_image', 'hotel_star', 'hotel_name', 'city', 'country', 'postal_index', 'street',
                  'service', 'description', 'owner', 'room_hotels', 'review_hotel', 'avg_rating','count_review' ]

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_review(self, obj):
        return obj.get_count_review()
