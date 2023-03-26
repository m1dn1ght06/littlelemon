from django.test import TestCase, Client
from django.urls import reverse
import json
from .models import *
from .views import *

# Create your tests here.
class MenuTest(TestCase):
    def test_menu_creation(self):
        item = Menu.objects.create(Title='steak', Price=12, Inventory='3')
        self.assertEqual(item.Title, 'steak')
        self.assertEqual(item.Price, 12)
        self.assertEqual(item.Inventory, '3')

class MenuViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.menu_item1 = Menu.objects.create(Title='steak', Price=12.00, Inventory=3)
        self.menu_item2 = Menu.objects.create(Title='salad', Price=8.00, Inventory=5)

    def test_getall(self):
        response = self.client.get(reverse('MenuItemsView'))
        self.assertEqual(response.status_code, 200)

        # Deserialize the response content
        data = json.loads(response.content)
        for item in data:
            item['Price'] = float(item['Price'])
            item['Inventory'] = float(item['Inventory'])

        # Check that the serialized data matches the expected data
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['Title'], self.menu_item1.Title)
        self.assertEqual(data[0]['Price'], self.menu_item1.Price)
        self.assertEqual(data[0]['Inventory'], self.menu_item1.Inventory)
        self.assertEqual(data[1]['Title'], self.menu_item2.Title)
        self.assertEqual(data[1]['Price'], self.menu_item2.Price)
        self.assertEqual(data[1]['Inventory'], self.menu_item2.Inventory)
