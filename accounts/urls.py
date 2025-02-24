#django files
from django.urls import path



#rest_frame files


#your files
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('request/reset/password/', views.RequestPasswordResetAPIView.as_view(), name='request_password'),
    path('reset/password/<str:token>/', views.ResetPasswordAPIView.as_view(), name='RESET_PASSWORD_URL'),

]








