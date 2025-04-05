from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from habit.models import Habit
from users.models import User


class JWTAuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.habit = Habit.objects.create(
            user_owner=self.user,
            time="09:00:00",
            action="Test habit",
            execution_time=60,
            is_public=False
        )

    def test_jwt_token_obtain(self):

        url = reverse('users:token_obtain_pair')
        data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_protected_endpoint_access(self):

        url = reverse('habit:habits-detail', args=[self.habit.id])

        # Without authentication
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # With valid token
        token = self.client.post(reverse('users:token_obtain_pair'), {
            "email": "test@example.com",
            "password": "testpass123"
        }).data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserRegistrationTests(APITestCase):
    def test_user_registration(self):
        url = reverse('users:user-register')
        data = {
            "email": "newuser@example.com",
            "password": "strongpassword123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()
        self.assertTrue(user.check_password('strongpassword123'))

    def test_password_hashing(self):
        data = {
            "email": "test@example.com",
            "password": "plaintext"
        }
        response = self.client.post(reverse('users:user-register'), data)
        user = User.objects.get(email=data['email'])
        self.assertNotEqual(user.password, 'plaintext')
