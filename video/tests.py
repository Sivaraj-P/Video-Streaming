from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Video
from user.models import User
import tempfile

class VideoAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(first_name="Siva", last_name="Raj", email_id="siva@gmail.com", password="Password@123")
        self.user2 = User.objects.create_user(first_name="Ram", last_name="Raju", email_id="raju@gmail.com", password="Password@123")


        self.video_file = SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")
        self.video = Video.objects.create(
            video_name="Python Programming",
            category="Educational",
            description="Zero to Hero course",
            file=self.video_file,
            created_by=self.user1
        )

        self.valid_video_file = SimpleUploadedFile("new_video.mp4", b"file_content", content_type="video/mp4")
        self.invalid_video_file = SimpleUploadedFile("new_video.txt", b"file_content", content_type="text/plain")

        self.video_data = {
            "video_name": "Django Programming",
            "category": "Educational",
            "description": "Zero to Hero course",
            "file": self.valid_video_file
        }

        self.invalid_video_data = {
            "video_name": "",
            "category": "New Category",
            "description": "New Description",
            "file": self.invalid_video_file
        }

    def test_get_video_with_correct_id(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('video_id', args=[self.video.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['video_name'], self.video.video_name)

    def test_get_video_with_incorrect_id(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('video_id', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_create_video_with_correct_data(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(reverse('video'), self.video_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['video_name'], self.video_data['video_name'])

    def test_create_video_with_unwanted_data(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(reverse('video'), self.invalid_video_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_update_video_with_correct_data(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(reverse('video_id', args=[self.video.id]), self.video_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['video_name'], self.video_data['video_name'])

    def test_update_video_with_incorrect_id(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(reverse('video_id', args=[999]), self.video_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_update_video_with_unwanted_data(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(reverse('video_id', args=[self.video.id]), self.invalid_video_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_update_video_created_by_another_user(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(reverse('video_id', args=[self.video.id]), self.video_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_delete_video_with_correct_id(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(reverse('video_id', args=[self.video.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_video_with_incorrect_id(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(reverse('video_id', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_delete_video_created_by_another_user(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(reverse('video_id', args=[self.video.id]))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
