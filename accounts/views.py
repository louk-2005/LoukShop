#django files
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect

#rest_files
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny
#your files
from .serializers import UserRegisterSerializer,ResetPasswordRequestSerializer,ResetPasswordSerializer
from .models import User,ResetPassword
from django.utils.translation import activate
# from rest_framework_tracking.mixins import LoggingMixin


#python library
import os



class RegisterAPIView(APIView):
    """
    this view is for registering new user
    """
    def post(self, request):
        srz = UserRegisterSerializer(data=request.data)
        if srz.is_valid():
            srz.create(srz.validated_data)
            return Response(data={'message':'you register successfully','data':srz.data}, status=status.HTTP_201_CREATED)
        return Response(data={'message':'validation error','data':srz.errors}, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetAPIView(generics.GenericAPIView):
    """
    this view is for reset password request and send you an email
    """
    serializer_class = ResetPasswordRequestSerializer
    permission_classes = (AllowAny,)
    throttle_scope = 'requestPasswordReset'
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            cd = serializer.validated_data
            email = cd['email']
            user = User.objects.filter(email=email).first()

            if user:
                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(user)
                reset_password = ResetPassword.objects.create(email=email, token=token)
                reset_password.save()

                reset_url = f"http://127.0.0.1:8000/api/v1/accounts/reset/password/{token}/"
                send_mail(
                    'reset your password',
                    _(f'use this link to reset your password: {reset_url}'),
                    "Louk",
                    [f"{reset_password.email}"],
                    fail_silently=True,
                )
                return Response({'message': _('We have sent you a link to reset your password')},
                                status=status.HTTP_200_OK)

            return Response({"message": _("User whit this email is not exist")}, status=status.HTTP_404_NOT_FOUND)
        return Response(data={'message':_('validation error'),'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(generics.GenericAPIView):
    """
    this view is for reset password request and allow you to reset your password
    """
    serializer_class = ResetPasswordSerializer
    permission_classes = (AllowAny,)
    throttle_scope = 'passwordReset'

    def post(self,request,token):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            reset_password = ResetPassword.objects.filter(token=token).first()
            if not reset_password:
                return Response({"message": _("Invalid Token")}, status=status.HTTP_404_NOT_FOUND)

            user = User.objects.get(email=reset_password.email)
            if user:
                user.set_password(serializer.validated_data['password'])
                user.save()
                return Response({"message": _("Your password has been reset")}, status=status.HTTP_200_OK)
            return Response({"message": _("User with this email not found")}, status=status.HTTP_404_NOT_FOUND)
        return Response(data={'message':_('validation error'),'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ChangeLanguageView(APIView):
    def post(self, request):
        lang = request.data.get('language', 'fa')
        activate(lang)
        request.session['django_language'] = lang
        return Response({"message": "Language changed successfully."})


# abolfazl password 123123Ali@
#
# {
#                 "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjE5ODk4NywiaWF0IjoxNzQwMTUwOTg3LCJqdGkiOiJlYjY0NmRkMjc3NjM0MWQyYWRiYTNlYmI5ZmFkYWNlMiIsInVzZXJfaWQiOjF9.S7NigQIknbBsClfN6uUrfHsoI49S5EDM7NV5br7XTzc",
#         "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxMDE0OTg3LCJpYXQiOjE3NDAxNTA5ODcsImp0aSI6IjI3YzY1YjgxYTczNTQzYmI4MTQxOGJjYzlhZTM1MjYyIiwidXNlcl9pZCI6MX0.JYR9gKMwWo1Y7wnSTdhJ1phJUFtzc094tbB6WR9bJgw"
#     }
#     "data": {  it is for amir@gmail.com
#         "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NTQyMTg3NCwiaWF0IjoxNzM5MzczODc0LCJqdGkiOiI3ZTBlNTExZmQxYjI0YTNiOTY5YmQzZjY4ZDk5MTQwMiIsInVzZXJfaWQiOjJ9.hg8ngvdvvfFK1BRLW2H-36oGLMGz9dWgBDso_44YV-k",
#         "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQwMjM3ODc0LCJpYXQiOjE3MzkzNzM4NzQsImp0aSI6IjBkZDU3Yzg4NDU5ZTQyNTFiZTQxZmY5YzhiZjg2MThlIiwidXNlcl9pZCI6Mn0.2e0raWiZBqCshHaWDVIeisVi53XI_bbTMc1Iy_p-tgk"



