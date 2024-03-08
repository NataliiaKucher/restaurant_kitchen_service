from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from dish_catalog.models import DishType, Dish

DISH_FORMAT_URL = reverse("dish_catalog:dish-list")


class PublicDishTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DISH_FORMAT_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDishTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_user_dish(self):
        dish_type = DishType.objects.create(name="Pizza")
        Dish.objects.create(name="Rice", price=2.50, dish_type=dish_type)
        Dish.objects.create(name="Varenuky", price=4.50, dish_type=dish_type)
        response = self.client.get(DISH_FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        dishes = Dish.objects.all()
        self.assertEqual(
            list(response.context["dish_list"]),
            list(dishes),
        )
        self.assertTemplateUsed(
            response,
            "dish_catalog/dish_list.html"
        )
