from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from dish_catalog.models import Cook

COOK_FORMAT_URL = reverse("dish_catalog:cook-list")


class PublicCookTest(TestCase):
    def test_login_required(self):
        res = self.client.get(COOK_FORMAT_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCookTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_user_cooks(self):
        Cook.objects.create(
            username="cook1",
            years_of_experience=4
        )
        Cook.objects.create(
            username="cook2",
            years_of_experience=7
        )
        response = self.client.get(COOK_FORMAT_URL)
        self.assertEqual(
            response.status_code, 200
        )
        cooks = Cook.objects.all()
        self.assertEqual(
            list(response.context["cook_list"]),
            list(cooks),
        )
        self.assertTemplateUsed(
            response,
            "dish_catalog/cook_list.html"
        )
