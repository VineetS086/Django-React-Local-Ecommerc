from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.core.mail import send_mail

import random
import string
from datetime import datetime, tzinfo

from .constants import (
    VerificationPassed,
    KeyValidityTime,
    VerificationFailed,

)

class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None): #pass all required fields
        if not email:
            raise ValueError('Email is required')
        
        if not username:
            raise ValueError('Name is required')


        user = self.model(
            email       = self.normalize_email(email),
            username    = username,
        )

        user.set_password(password)
        user.save(using=self._db)

        #Extra
        user.get_unique_key                     # REMOVE LATER
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)

        user.is_superuser   = True
        user.is_admin       = True
        user.is_staff       = True
        user.is_active      = True
        user.is_verified    = True
        user.is_trusted     = True

        user.save(using = self._db)
        return user
        

class Account(AbstractBaseUser):
    
    #Main Fields
    email   = models.EmailField(unique=True)
    username    = models.CharField('name', max_length=50)
    phone_no= models.CharField(max_length=10)
    # image   = models.ImageField()


    #Dates
    date_joined = models.DateField(auto_now_add=True)
    last_login  = models.DateTimeField(auto_now=True)
    student_discount_date   = models.DateField(null=True, blank=True)

    #User Permissions
    is_superuser= models.BooleanField(default=False)
    is_admin    = models.BooleanField(default=False)
    is_staff    = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)
    is_trusted  = models.BooleanField(default=False)
    is_student  = models.BooleanField(default=False)

    ##ExteaFields-
    #varification
    is_email_verified   = models.BooleanField(default=False)
    is_phone_verified   = models.BooleanField(default=False)
    unique_key          = models.CharField(max_length=20, default='')
    unique_key_time     = models.DateTimeField(auto_now_add=True)

    ##Extra Fields end^

    #change below
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = [
        'username',
        
    ]
    object = AccountManager()

    #Perms
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    #Methods and Properties
    def __str__(self):
        return f'{self.username}'


    ##EXTRA Functionc START

    
    #varification
    @property
    def get_unique_key(self):
        chars   = string.ascii_letters + string.digits
        rnd_str = ''.join((random.choice(chars) for _ in range(10)))

        self.unique_key = f'{rnd_str}{self.id}'
        self.save()

        self.unique_key_time = timezone.now()
        return self.unique_key
        
    def is_key_valid(self, key):
        time_flag = (self.unique_key_time-timezone.now()).total_seconds()<KeyValidityTime

        if time_flag and key!=self.unique_key:
            return False
        return True

    def verify(self, key):
        if self.is_key_valid():
            self.is_verified = True
            return VerificationPassed

        return VerificationFailed

    def email_user(self, subject, message, from_email=None, html_message=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], html_message=html_message, **kwargs)
    
        
    ##EXTRA Functionc end



