from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cats_hedgehogs.models import User, Pet, Lot, Bid

from cats_hedgehogs.tests.test_lots import create_pet


class BidsUnauthorizedTestCase(APITestCase):
    def test_bid_list_no_auth(self):
        url = reverse('bid-list', kwargs={'lot_pk': '1'})

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(url, data={'value': '111'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_bid_detail_no_auth(self):
        url = reverse('bid-detail', kwargs={'lot_pk': '1', 'bid_pk': '2'})

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(url, data={'value': '333'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_bid_accept_no_auth(self):
        url = reverse('bid-accept', kwargs={'lot_pk': '1', 'bid_pk': '2'})

        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BidsTestCase(APITestCase):
    user_creds = {'username': 'vitaly', 'password': '12345'}
    another_creds = {'username': 'vasya', 'password': 'abcdef'}

    def setUp(self):
        self.user = User.objects.create_user(**self.user_creds)
        self.another_user = User.objects.create_user(**self.another_creds)
        self.client.login(**self.user_creds)

    def tearDown(cls):
        Lot.objects.all().delete()
        Pet.objects.all().delete()
        User.objects.all().delete()

    def test_bid_create(self):
        pet = create_pet(self.user)
        lot = Lot.objects.create(pet=pet, owner=self.another_user, start_price=3333)

        url = reverse('bid-list', kwargs={'lot_pk': lot.id})

        data = {'value': 111}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        got_bid_id = response.json()['id']
        expected_data = {
            'id': got_bid_id,
            'lot': lot.id,
            'owner': self.user.id,
            **data
        }
        self.assertEqual(response.json(), expected_data)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [expected_data])

        url = reverse('bid-detail', kwargs={'lot_pk': lot.id, 'bid_pk': got_bid_id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_data)

    def test_bid_accept(self):
        pet = create_pet(self.user)
        lot = Lot.objects.create(pet=pet, owner=self.user, start_price=3333)
        bid = Bid.objects.create(
            value=111,
            owner=self.another_user,
            lot=lot
        )

        url = reverse('bid-accept', kwargs={'lot_pk': lot.id, 'bid_pk': bid.id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            'detail': 'Unable to accept bid. This lot already has an accepted bid'
        }
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_data)


    def test_bid_accept_non_owner(self):
        pet = create_pet(self.another_user)
        lot = Lot.objects.create(pet=pet, owner=self.another_user, start_price=3333)
        bid = Bid.objects.create(
            value=111,
            owner=self.user,
            lot=lot
        )

        url = reverse('bid-accept', kwargs={'lot_pk': lot.id, 'bid_pk': bid.id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

