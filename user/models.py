from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,email,  password=None,**extra_fields):
        """Creates and saves User with a given email, date of birth
        and password
        """
        
        if not email:
            raise ValueError("User must have an email addres")
        
       
        user = self.model(email = self.normalize_email(email),
                        **extra_fields
                          )
        
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    
    def create_superuser(self, email,  password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser has  to have is_staff')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser has  to have is_staff')
        
        user = self.create_user(
            email,
            password=password,
            **extra_fields
        )
        return user
    
    
        
        
class  User(AbstractUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=45)
    date_of_birth = models.DateField(null=True,blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=[]
    objects = UserManager()
    
    def __str__(self):
        return self.username
    
    
    

    
    