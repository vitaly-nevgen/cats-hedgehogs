from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from cats_hedgehogs.models import User, Pet


class PetsUnauthorizedTestCase(APITestCase):
    def test_unauthorized_pet_list(self):
        url = reverse('pet-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(url, data={'pet_type': 'ct'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_pet_detail(self):
        url = reverse('pet-detail', kwargs={'pet_pk': '1'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(url, data={'pet_type': 'ct'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PetsTestCase(APITestCase):
    user = None
    user_creds = {'username': 'vitaly', 'password': '12345'}

    def setUp(self):
        self.user = User.objects.create_user(**self.user_creds)
        self.client.login(**self.user_creds)

    def tearDown(self):
        self.user = None

        Pet.objects.all().delete()
        User.objects.all().delete()

    def test_empty_pet_list(self):
        url = reverse('pet-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

    def test_pet_create_and_read_own(self):
        url = reverse('pet-list')
        data = {
            'pet_type': 'ct',
            'breed': 'bbb',
            'callsign': 'ccc'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected_data = {**data, 'id': response.json()['id']}
        self.assertEqual(response.json(), expected_data)

    def test_pet_list_access_not_own(self):
        another_user = User.objects.create_user(username='vasya', password='root')

        Pet.objects.create(
            pet_type='ct',
            breed='vvvv',
            callsign='ssss',
            owner=another_user
        )

        url = reverse('pet-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

    def test_pet_detail_access_not_own(self):
        another_user = User.objects.create_user(username='vasya', password='root')

        pet = Pet.objects.create(
            pet_type='ct',
            breed='vvvv',
            callsign='ssss',
            owner=another_user
        )

        url = reverse('pet-detail', kwargs={'pet_pk': pet.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
