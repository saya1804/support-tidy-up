from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    first_name = None
    last_name = None
    date_joined = None
    groups = None
    user_permissions = None

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        db_table = "users"


class Category(models.Model):
    name = models.CharField(max_length=150)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name="subcategories", on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Belonging(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image_url = models.ImageField(upload_to='belongings_images/', null=True, blank=True)
    purchase_date = models.DateField()
    item_area = models.CharField(max_length=150)
    DAMAGE_LEVEL_CHOISES = [
        (1, '軽い損傷'),
        (2, 'やや軽い損傷'),
        (3, '中程度の損傷'),
        (4, 'やや重い損傷'),
        (5, '重い損傷'),
    ]
    damage_level = models.IntegerField(choices=DAMAGE_LEVEL_CHOISES)
    favorite_level = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
    is_in_decluttering = models.BooleanField(default=False)

    def __str__(self):
        return self.name