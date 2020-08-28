from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cats_hedgehogs.models import User, Pet, Lot

example_pet_dict = {
    'pet_type': 'ct',
    'breed': 'bbb',
    'callsign': 'ccc'
}


def create_pet(owner):
    data = {
        'owner': owner,
        **example_pet_dict
    }

    return Pet.objects.create(**data)


class LotsUnauthorizedTestCase(APITestCase):
    def test_lot_list_no_auth(self):
        url = reverse('lot-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(url, data={'start_price': '555'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lot_detail_no_auth(self):
        url = reverse('lot-detail', kwargs={'lot_pk': '1'})

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(url, data={'start_price': '555'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LotsTestCase(APITestCase):
    user_creds = {'username': 'vitaly', 'password': '12345'}
    another_creds = {'username': 'vasya', 'password': 'abcdef'}

    def setUp(self):
        self.user = User.objects.create_user(**self.user_creds)
        self.client.login(**self.user_creds)

    def tearDown(cls):
        Lot.objects.all().delete()
        Pet.objects.all().delete()
        User.objects.all().delete()

    def test_lot_create_and_read(self):
        pet = create_pet(self.user)

        data = {
            'start_price': 555,
            'pet': pet.id
        }

        url = reverse('lot-list')
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        lot_id = response.json()['id']

        expected_lot = {
            'id': lot_id,
            'owner': {'username': 'vitaly'},
            'pet': {'id': pet.id, **example_pet_dict},
            'start_price': 555
        }

        url = reverse('lot-list')
        response = self.client.get(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [expected_lot])

        url = reverse('lot-detail', kwargs={'lot_pk': lot_id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_lot)

    def test_lot_create_with_not_own_pet(self):
        another_user = User.objects.create_user(**self.another_creds)
        pet = create_pet(another_user)

        data = {
            'start_price': 555,
            'pet': pet.id
        }

        url = reverse('lot-list')
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_not_own_lot(self):
        another_user = User.objects.create_user(**self.another_creds)
        pet = create_pet(another_user)
        lot = Lot.objects.create(owner=another_user, pet=pet, start_price=777)

        url = reverse('lot-detail', kwargs={'lot_pk': lot.pk})
        response = self.client.put(url, data={'start_price': 888}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
