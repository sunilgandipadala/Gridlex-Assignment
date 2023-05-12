from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin


from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
    
        user.set_password(password)  #Create hashed password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Generate a username based on the email
        username = email.split('@')[0]

        return self.create_user(email, password, username=username, **extra_fields)

class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30,unique=False)
    last_name = models.CharField(max_length=30,unique=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email
    


User = get_user_model()
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    body = models.TextField()
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(User, on_delete=models.CASCADE) #this needs to be fixed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #version = models.IntegerField(default=1)

    def __str__(self): 
        return self.title

class Comment(models.Model):
    user_name = models.CharField(max_length=255)
    email = models.EmailField()
    comment_text = models.TextField()
    blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE)
    #parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_text[:50]
    
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    firstname = models.TextField()
    lastname=models.TextField()
    
    # Add any other fields you need for the user profile

    def __str__(self):
        return self.user.username

    
