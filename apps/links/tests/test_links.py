import mock
from datetime import timedelta

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from django.utils import timezone

from ..models import VisitedLink


class VisitedLinkTestCase(APITestCase):
    def setUp(self) -> None:
        self.user, _ = get_user_model().objects.get_or_create(
            username='testuser', password='12345'
        )
        self.url_to_create_links = reverse('apps.links:visitedlink-visited-links')
        self.url_to_get_domains = reverse('apps.links:visitedlink-visited-domains')

    def test_links_creation(self):
        self.client.force_login(self.user)
        data = {
           'links': [
              'https://ya.ru/',
              'https://ya.ru/search/?text=мемы+с+котиками',
              'https://sber.ru',
              'https://stackoverflow.com/questions/65724760/how-it-is'
            ]	
        }
        visited_links = VisitedLink.objects.all()
        self.assertEqual(visited_links.count(), 0)
        response = self.client.post(self.url_to_create_links, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        visited_links = VisitedLink.objects.all()
        self.assertEqual(visited_links.count(), 4)

    def test_links_creation_with_incorrect_urls(self):
        self.client.force_login(self.user)
        data = {
           'links': [
              'https://ya.ru/',
              'https:/@ya.ru/search/?text=мемы+с+котиками',
            ]	
        }
        response = self.client.post(self.url_to_create_links, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_domains_getting(self):
        self.client.force_login(self.user)
        initial_data = {
           'links': [
              'https://ya.ru/',
              'https://ya.ru/search/?text=мемы+с+котиками',
              'https://ya.ru/ya.ru',
              'https://sber.ru',
              'https://sber.ru',
              'https://sber.ru/2',
           ]
        }
        expected_data = {
           'domains': [
              'ya.ru',
              'sber.ru',
            ]
        }
        response = self.client.post(self.url_to_create_links, data=initial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(self.url_to_get_domains)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(sorted(response.data['domains']), sorted(expected_data['domains']))

    def test_domains_getting_with_date_ranges(self):
        self.client.force_login(self.user)
        dates = [
            timezone.now() - timedelta(days=5),
            timezone.now() - timedelta(days=3),
            timezone.now(),
        ]

        data = [
            {
               'links': [
                    'https://ya.ru/search/?text=мемы+с+котиками',
                ]
            },
            {
                'links': [
                    'https://sber.ru',
                ]
            },
            {
                'links': [
                    'https://stackoverflow.com/questions/65724760/how-it-is'
                ]
            },
        ]

        for date, link in zip(dates, data):
            with mock.patch('django.utils.timezone.now', return_value=date):
                response = self.client.post(self.url_to_create_links, data=link, format='json')
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(self.url_to_get_domains)
        self.assertEqual(sorted(response.data['domains']), ['sber.ru', 'stackoverflow.com', 'ya.ru'])

        response = self.client.get(
            self.url_to_get_domains,
            {'from': int((timezone.now() - timedelta(days=4)).timestamp())},
        )
        self.assertEqual(sorted(response.data['domains']), ['sber.ru', 'stackoverflow.com'])

        response = self.client.get(
            self.url_to_get_domains,
            {
                'from': int((timezone.now() - timedelta(days=4)).timestamp()),
                'to': int((timezone.now() - timedelta(days=1)).timestamp()),
            },
        )
        self.assertEqual(sorted(response.data['domains']), ['sber.ru'])
