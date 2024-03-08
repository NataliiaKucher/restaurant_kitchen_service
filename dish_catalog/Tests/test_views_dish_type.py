from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from dish_catalog.models import DishType

DISH_TYPE_FORMAT_URL = reverse("dish_catalog:dish-type-list")


class PublicDishTypeTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DISH_TYPE_FORMAT_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDishTypeTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_user_manufacturer(self):
        DishType.objects.create(name="Pizza")
        DishType.objects.create(name="Pasta")
        response = self.client.get(DISH_TYPE_FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        dish_type = DishType.objects.all()
        self.assertEqual(
            list(response.context["dish_type_list"]),
            list(dish_type),
        )
        self.assertTemplateUsed(
            response,
            "dish_catalog/dish_type_list.html"
        )


class DishTypeCreateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_create_dish_type(self):
        dish_type_count_before = DishType.objects.count()
        response = self.client.post(reverse(
            "dish_catalog:dish-type-create"
        ),
            data={
                "name": "Pizza",
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            DishType.objects.count(),
            dish_type_count_before + 1
        )


class DishTypeUpdateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.dish_type = DishType.objects.create(
            name="Pizza",
        )

    def test_update_dish_type(self):
        response = self.client.post(
            reverse(
                "dish_catalog:dish-type-update",
                kwargs={"pk": self.dish_type.pk}
            ),
            data={
                "name": "Salad",
            }
        )
        self.assertEqual(
            response.status_code,
            302
        )
        self.dish_type.refresh_from_db()
        self.assertEqual(
            self.dish_type.name, "Salad"
        )


class DishTypeDeleteTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.dish_type = DishType.objects.create(
            name="Salad",
        )

    def test_delete_dish_type(self):
        dish_type_count_before = DishType.objects.count()
        response = self.client.post(
            reverse(
                "dish_catalog:dish-type-delete",
                kwargs={"pk": self.dish_type.pk}
            )
        )
        self.assertEqual(
            response.status_code, 302
        )
        self.assertEqual(
            DishType.objects.count(),
            dish_type_count_before - 1
        )
