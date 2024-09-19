from django.shortcuts import render
from .models import User,EmailVerificationToken
from .serializer import UserSerializer,EmailVerificationTokenSerializer
from rest_framework.views import APIView
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response 
from rest_framework import status,generics
from rest_framework.exceptions import AuthenticationFailed

class RegisterView(APIView):

    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            token=EmailVerificationToken.objects.create(user=user)
            site = get_current_site(request)
            mail_subject = "Email Verification"
            message=render_to_string('mail_verification.html',{'user':user.email,'domain':site.domain,
                                                               'token':token.token})
            send_mail(mail_subject,message,settings.EMAIL_HOST_USER,[user.email],fail_silently=False )
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    serializer_class=UserSerializer
    def post(self,request):
        email_or_phone=request.data.get('email_or_phone')
        password=request.data.get('password')
        try:
            user=User.objects.get(email=email_or_phone)
        except User.DoesNotExist:
            try:
                user=User.objects.get(phone=email_or_phone)
            except User.DoesNotExist:
                raise AuthenticationFailed('Invalid email or phone number')
            
        



