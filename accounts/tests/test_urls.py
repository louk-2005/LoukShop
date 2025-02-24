from django.test import SimpleTestCase
from django.urls import reverse,resolve
from accounts.views import *

class Test_Urls(SimpleTestCase):
    def test_register_view(self):
        url = reverse('accounts:register')
        self.assertEqual(resolve(url).func.view_class, RegisterAPIView)
    def test_request_password_view(self):
        url = reverse('accounts:request_password')
        self.assertEqual(resolve(url).func.view_class, RequestPasswordResetAPIView)
    def test_reset_password_view(self):
        url = reverse('accounts:RESET_PASSWORD_URL', args=['token'])
        self.assertEqual(resolve(url).func.view_class, ResetPasswordAPIView)
