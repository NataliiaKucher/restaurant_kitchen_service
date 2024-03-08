from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="test_admin"
        )
        self.client.force_login(self.admin_user)
        self.cook = get_user_model().objects.create_user(
            username="cook",
            password="test_cook",
            years_of_experience=5,
        )

    def test_cook_year_of_experience(self):
        """
        Test that years_of_experience is in list
        :return:
        """
        url = reverse("admin:dish_catalog_cook_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.cook.years_of_experience)

    def test_cook_detail_year_of_experience(self):
        """
        Test driver License number is on driver detail admin page
        :return:
        """
        url = reverse("admin:dish_catalog_cook_change", args=[self.cook.id])
        res = self.client.get(url)
        self.assertContains(res, self.cook.years_of_experience)
