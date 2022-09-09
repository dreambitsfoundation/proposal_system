from rest_framework.test import APIRequestFactory, force_authenticate
from django.test import TestCase
from authentication.models import User
from rest_framework import status

from authentication.views import LoginView, UserView

class UserLogin(TestCase):
    """
    This test is only meant to test login API
    """

    def setUp(self) -> None:
        u = User.objects.create(phone_number="1234567890", name="Test Name", email="EmailID")
        u.set_password("pass1234")
        u.save()
    
    def test_create_login(self):
        factory = APIRequestFactory()
        request = factory.post('/auth/login/', {'phone_number': '1234567890', 'password': 'pass1234'}, format='json')
        view = LoginView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self) -> None:
        User.objects.all().delete()

class TestUserAccountAPIs(TestCase):
    
    def setUp(self) -> None:
        u = User.objects.create(phone_number="1234567891", name="Test Name", email="EmailID")
        u.set_password("pass1234")
        u.save()

    def test_create_user(self):
        factory = APIRequestFactory()
        request = factory.post('/auth/user_account/', {'phone_number': '1234567890', 'password': 'pass1234', 'name': 'Test User'}, format='json')
        view = UserView.as_view()
        response = view(request)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_get_user(self):
        u = User.objects.get(phone_number='1234567891')
        factory = APIRequestFactory()
        request = factory.get('/auth/user_account/')
        force_authenticate(request, u)
        view = UserView.as_view()
        response = view(request)
        self.assertEquals(response.data['id'], u.pk)

    def test_update_user(self):
        u = User.objects.get(phone_number='1234567891')
        factory = APIRequestFactory()
        request = factory.put('/auth/user_account/', {'name': 'New Test User'}, format='json')
        force_authenticate(request, u)
        view = UserView.as_view()
        response = view(request)
        # Check the ID if that is same.
        self.assertEquals(response.data['name'], 'New Test User')

    def tearDown(self) -> None:
        User.objects.all().delete()

