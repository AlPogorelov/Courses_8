from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from habit.models import Habit


class HabitModelTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.pleasant_habit = Habit.objects.create(
            user_owner=self.user,
            time="09:00:00",
            action="Test pleasant habit",
            is_useful=False,
            execution_time=30
        )

    def test_habit_creation(self):
        url = reverse('habit:habits-list')
        self.client.force_authenticate(user=self.user)

        data = {
            "user_owner": self.user.id,
            "action": "New habit",
            "time": "09:00:00",
            "execution_time": 60,
            "is_useful": True
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class HabitViewSetTests(APITestCase):
    def setUp(self):
        Habit.objects.all().delete()

        self.user = User.objects.create_user(
            email='user@example.com',
            password='testpass123'
        )
        self.habit = Habit.objects.create(
            user_owner=self.user,
            time="09:00:00",
            action="Test habit",
            execution_time=60,
            is_public=False
        )

        self.other_user = User.objects.create_user(
            email='user1@example.com',
            password='testpass456'
        )

    def test_habit_list_owner_access(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('habit:habits-list'))
        self.assertEqual(len(response.data['results']), 1)

    def test_public_habits_list(self):

        Habit.objects.create(
            user_owner=self.user,
            time="09:00:00",
            action="Public habit",
            execution_time=60,
            is_public=True
        )

        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse('habit:habits-public'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_habit_update_owner_permission(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse('habit:habits-detail', args=[self.habit.id])
        data = {"action": "Updated action"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class HabitValidationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        Habit.objects.all().delete()

        self.pleasant_habit = Habit.objects.create(
            user_owner=self.user,
            action="Pleasant habit",
            time="10:00:00",
            execution_time=30,
            is_useful=False,
        )

    def test_execution_time_validation(self):
        url = reverse('habit:habits-list')
        data = {
            "action": "Invalid habit",
            "execution_time": 150
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('execution_time', response.data)

    def test_related_habit_validation(self):
        pleasant_habit = Habit.objects.create(
            user_owner=self.user,
            action="Pleasant habit",
            time="10:00:00",
            execution_time=30,
            is_useful=False
        )

        data = {
            "action": "Test habit",
            "time": "12:00:00",
            "execution_time": 60,
            "is_useful": True,
            "related_habit": pleasant_habit.id,
            "reward": "Test reward",
            "user_owner": self.user.id
        }

        response = self.client.post(reverse('habit:habits-list'), data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('non_field_errors', response.data)
