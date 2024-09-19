from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
import uuid
from date import timedelta
from django.utils import timezone
from .manager import UserManager


# Create your models here.
class User(AbstractUser):
    email=models.EmailField(_(""), max_length=254)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    is_vefied=models.models.BooleanField(_(""),default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=[]
    objects=UserManager()
    def __str__(self):
        return self.email
    

class EmailVerificationToken(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    token=models.UUIDField(default=uuid.uuid4,editable=False)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def is_valid(self):
        return timezone.now()-self.created_at > timedelta(minutes=15)

class OtpGenerate(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    otp=models.CharField(max_length=6,null='True',blank='True')
    otp_created_at=models.DateTimeField(auto_now_add=True)

    def is_otp_expired(self):
        if self.otp_created_at:
            return timezone.now()-self.otp_created_at > timedelta(minutes=5)