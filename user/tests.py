from rest_framework.test import APIClient,APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User

class UserAuthTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "first_name": "Raj",
            "last_name": "Siva",
            "email_id": "raj@gmail.com",
            "password": "Password@123"
        }
        self.user = User.objects.create_user(**self.user_data)
        self.user.set_password(self.user_data['password'])
        self.user.save()

    def test_login_with_correct_data(self):
        response = self.client.post(reverse('login'), {'email_id': self.user_data['email_id'], 'password': self.user_data['password']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_with_no_data(self):
        response = self.client.post(reverse('login'), {})
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_login_with_incorrect_data(self):
        response = self.client.post(reverse('login'), {'email_id': 'wrongemail@example.com', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_non_suitable_data(self):
        response = self.client.post(reverse('login'), {'email_id': '1234567890', 'password': 'wrongformat@example.com'})
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_create_user_with_valid_data(self):
        response = self.client.post(reverse('user'), {
            "first_name": "Vijay",
            "last_name": "Doe",
            "email_id": "vijay@gmail.com",
            "password": "Passwor@d123"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email_id'], "vijay@gmail.com")

    def test_create_user_with_invalid_data(self):
        response = self.client.post(reverse('user'), {
            "first_name": "Jane",
            "last_name": "Doe",
            "email_id": "not-an-email",
            "password": "password123"
        })
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_get_user_with_valid_token(self):
        response = self.client.post(reverse('login'), {'email_id': self.user_data['email_id'], 'password': self.user_data['password']})
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(reverse('user'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email_id'], self.user_data['email_id'])

    def test_get_user_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'wrongtoken')
        response = self.client.get(reverse('user'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
