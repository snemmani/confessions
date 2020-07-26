from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Confession

class ConfessionTests(APITestCase):
    def test_create_confession_valid(self):
        """
        Ensure we can create a new Confession object.
        """
        url = reverse('confessions_cr')
        data = {'heading': 'Test Heading', 'text': 'Some Valid Text'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Confession.objects.count(), 1)
        self.assertEqual(Confession.objects.get().heading, data['heading'])
        self.assertEqual(Confession.objects.get().text, data['text'])

    def test_create_confession_invalid(self):
        """
        Ensure we can create a new Confession object.
        """
        url = reverse('confessions_cr')
        data = {'heading': 'Test Heading', 'text': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Confession.objects.count(), 1)
        self.assertEqual(Confession.objects.get().heading, str(data['heading']))
        self.assertEqual(Confession.objects.get().text, str(data['text']))

    def test_get_confessions(self):
        """
        Ensure we can can get all confession objects.
        """
        url = reverse('confessions_cr')
        data = {'heading': 'Test Heading', 'text': 1}
        response = self.client.post(url, data, format='json')
        response2 = self.client.get(url)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_get_confessions(self):
        """
        Ensure we can create a Single confession object.
        """
        url_p = reverse('confessions_cr')
        url = reverse('confessions_rud', args=[1])
        url_404 = reverse('confessions_rud', args=[100])
        data = {'heading': 'Test Heading', 'text': 1}
        response = self.client.post(url_p, data, format='json')
        response2 = self.client.get(url)
        response3 = self.client.get(url_404)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response3  .status_code, status.HTTP_404_NOT_FOUND)
    
    def test_put_confessions(self):
        """
        Ensure we can edit a Single confession object.
        """
        url_p = reverse('confessions_cr')
        url = reverse('confessions_rud', args=[1])
        data = {'heading': 'Test Heading', 'text': 1}
        response = self.client.post(url_p, data, format='json')
        response2 = self.client.put(url)
        self.assertEqual(response2.status_code, status.HTTP_501_NOT_IMPLEMENTED)

    def test_delete_confessions(self):
        """
        Ensure we can delete a Single confession object.
        """
        url_p = reverse('confessions_cr')
        url = reverse('confessions_rud', args=[1])
        data = {'heading': 'Test Heading', 'text': 1}
        response = self.client.post(url_p, data, format='json')
        response2 = self.client.delete(url)
        response2 = self.client.get(url)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)
        