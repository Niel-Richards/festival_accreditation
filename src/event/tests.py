from django.test import TestCase, SimpleTestCase
from django.urls import reverse

# Create your tests here.
class EventCreateViewTests(SimpleTestCase):
    
    def test_eventcreateview_status_code(self):
        response = self.client.get('/event/create/')
        self.assertEqual(response.status_code, 200)

    def test_eventcreateview_url_name(self):
        response = self.client.get(reverse('event:create_event'))
        self.assertEqual(response.status_code, 200)

        return reverse('account:user_detail', kwargs={'id': self.id})

