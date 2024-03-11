from django.contrib.auth import get_user_model
from django.test import TestCase

from dish_catalog.models import DishType, Dish


class ModelsTests(TestCase):
    def test_dish_type_str(self):
        dish_type = DishType.objects.create(
            name="test",
        )
        expected_str = f"{dish_type.name}"
        self.assertEqual(
            str(dish_type),
            expected_str
        )

    def test_dish_str(self):
        dish_type = DishType.objects.create(
            name="test",
        )
        dish = Dish.objects.create(
            name="test",
            price=2.50,
            description="test description",
            dish_type=dish_type
        )
        self.assertEqual(
            str(dish),
            f"{dish.name} ({dish.price} {dish.description})")

    def test_cook_str(self):
        cook = get_user_model().objects.create(
            username="test",
            email="<EMAIL>",
            password="test123",
            first_name="test_first_name",
            last_name="test_last_name",
        )

        self.assertEqual(
            str(cook),
            f"{cook.username} ({cook.first_name} {cook.last_name})"
        )

    def test_years_of_experience(self):
        username = "test"
        years_of_experience = "test_years_of_experience"
        password = "test123"
        cook = get_user_model().objects.create_user(
            username=username,
            years_of_experience=years_of_experience,
            password=password,
        )
        self.assertEqual(cook.username, username)
        self.assertEqual(cook.license_number, years_of_experience)
        self.assertTrue(cook.check_password(password))
