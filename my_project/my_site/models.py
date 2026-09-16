from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Country(models.Model):
    country_name = models.CharField(max_length=64, unique=True)
    country_image = models.ImageField(upload_to='photo_country/')

    def __str__(self):
        return self.country_name

class UserProfile(AbstractUser):
    Role_Choices = (
    ('client', 'client'),
    ('owner','owner')
    )

    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(16),MaxValueValidator(80)], null=True, blank=True)
    user_image = models.ImageField(upload_to='user_image',null=True,blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    role = models.CharField(max_length=30, choices=Role_Choices, default='client')
    data_register = models.DateTimeField(auto_now_add=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

class City(models.Model):
    city_name = models.CharField(max_length=64, unique=True)
    city_image = models.ImageField(upload_to='photo_city/' ,null=True,blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, related_name='city_nam')

    def __str__(self):
        return self.city_name

class Service(models.Model):
    service_name = models.CharField(max_length=100, unique=True)
    service_image = models.ImageField(upload_to='photo_service/')

    def __str__(self):
        return self.service_name

class Hotel(models.Model):
    hotel_name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='hotel')
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    hotel_star = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    street = models.CharField(max_length=100)
    link_map = models.URLField()
    postal_index = models.PositiveSmallIntegerField()
    service = models.ManyToManyField(Service)
    description = models.TextField()
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='hotel_user')

    def __str__(self):
        return f'{self.hotel_name}-{self.hotel_star}'

    def get_avg_rating(self):
        ratings = self.review_hotel.all()
        if ratings.exists():
            return round(sum(i.rating for i in ratings) / ratings.count(), 2)
        return 0

    def get_count_review(self):
        return self.review_hotel.count()

class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE,related_name='hotel_image')
    hotel_image = models.ImageField(upload_to='photo_hotel/')


class Room(models.Model):
    Type_Choices = (
        ('люкс', 'люкс'),
        ('полулюкс', 'полулюкс'),
        ('стандарт', 'стандарт'),
        ('эконом', 'эконом'),
        ('семейный', 'семейный'),
        ('одноместный', 'одноместный'),
        ('двухместный', 'двухместный'),
    )
    Status_Room = (
        ('свободен', 'свободен'),
        ('забронирован ', 'забронирован '),
        ('занят', 'занят'),
    )
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    hotel_number = models.PositiveSmallIntegerField(unique=True)
    room_type = models.CharField(max_length=32, choices=Type_Choices)
    room_status = models.CharField(max_length=32, choices=Status_Room)
    price = models.PositiveSmallIntegerField()
    room_description = models.TextField()
    max_guest = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.hotel_number}-{self.hotel.hotel_name}'

class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room')
    room_image = models.ImageField(upload_to='photo_room/')

class Booking(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.hotel.hotel_name}-{self.room.hotel_number}'

class Review(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='review_hotel')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 11)],
                                               null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name}-{self.hotel.hotel_name}'

