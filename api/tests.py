import unittest

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from .models import Product


class SpecBackendTests(APITestCase):
    """
    Test the backend API
    """
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="anything")
        self.login_url = reverse('knox_login')
        self.user_data = {"username": "alice", "password": "anything"}
        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.token = response.data.get("token")
        self.assertIsNotNone(self.token)
        self.auth_header = {"HTTP_AUTHORIZATION": f"Token {self.token}"}

        self.product = Product.objects.create(
            name="Banana", description="Yellow", price=1.5, stock=50
        )
        Product.objects.create(
            name="Apple", description="Red", price=2.5, stock=100
        )
        Product.objects.create(
            name="Orange", description="Orange", price=1.0, stock=30
        )

    def test_user_login_and_info(self):
        """
        Test user login and info retrieval
        :return:
        """
        res = self.client.get(reverse("current-user"), **self.auth_header)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["username"], "alice")

    def test_product_search(self):
        """
        Test product search and ordering
        :return:
        """
        res = self.client.get(reverse("product-list"), {"search": "Banana"}, **self.auth_header)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data[0]["name"], "Banana")

        res = self.client.get(reverse("product-list"), {"ordering": "price"}, **self.auth_header)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data[0]["name"], "Orange")


    def test_product_selection(self):
        """
        Test selecting a product
        :return:
        """
        res = self.client.post(reverse("select-product", args=[self.product.pk]), **self.auth_header)
        self.assertEqual(res.status_code, 200)
        selected = self.client.get(reverse("selected-products"), **self.auth_header)
        self.assertEqual(len(selected.data), 1)
        self.assertEqual(selected.data[0]["id"], self.product.id)

    def test_logout(self):
        """
        Test clearing out session on logout.
        :return:
        """
        # Select a product to add it to the session
        self.client.post(reverse("select-product", args=[self.product.pk]), **self.auth_header)
        selected = self.client.get(reverse("selected-products"), **self.auth_header)
        self.assertEqual(len(selected.data), 1)
        self.assertEqual(selected.data[0]["id"], self.product.id)

        # Logout
        res = self.client.post(reverse("knox_logout"), **self.auth_header)
        self.assertEqual(res.status_code, 204)

        # Check if the session is cleared
        selected = self.client.get(reverse("selected-products"), **self.auth_header)
        self.assertEqual(selected.status_code, 401)
        self.assertEqual(selected.json()["detail"], "Invalid token.")


class ProductModelTestCase(unittest.TestCase):
    """
    Testing model specific units
    """
    def setUp(self):
        self.product = Product.objects.create(
            name="Banana", description="Yellow", price=1.5, stock=50
        )

    def test_str_method(self):
        """
        Test returning string on model object.
        :return:
        """
        self.assertEqual(str(self.product), "Banana")
