from django.contrib.auth import get_user_model
from django.test import TestCase

from dish_catalog.forms import (CooksExperienceYearCreateForm,
                                CooksExperienceYearUpdateForm,
                                DishSearchForm,
                                DishTypeSearchForm,
                                CookSearchForm,
                                DishForm,
                                )
from dish_catalog.models import DishType, Cook


class FormTests(TestCase):
    def test_form_validity(self):
        form_data = {
            "username": "new_user",
            "password1": "testing123new",
            "password2": "testing123new",
            "years_of_experience": 5,
            "first_name": "new_first_name",
            "last_name": "new_last_name",
        }
        form = CooksExperienceYearCreateForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data, form_data)

    def test_update_year_of_experience(self):
        new_year_of_exp = {
            "years_of_experience": 5,
        }
        form = CooksExperienceYearUpdateForm(data=new_year_of_exp)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data, new_year_of_exp)


class DishSearchFormTest(TestCase):
    def test_form_rendering(self):
        form = DishSearchForm()
        expected_html = (
            "<input type='text' name='dish_name' "
            "placeholder='Search by name' maxlength='255' "
            "id='id_dish_name'>"
        )
        self.assertHTMLEqual(str(form["dish_name"]), expected_html)

    def test_form_validation(self):
        form = DishSearchForm(data={"dish_name": "Varenuky"})
        self.assertTrue(form.is_valid())
        form = DishSearchForm(data={})
        self.assertTrue(form.is_valid())


class DishTypeSearchFormTest(TestCase):
    def test_form_rendering(self):
        form = DishTypeSearchForm()
        expected_html = (
            "<input type='text' name='name_dish_type' "
            "placeholder='Search by type' maxlength='255' "
            "id='id_name_dish_type'>"
        )
        self.assertHTMLEqual(str(form["name_dish_type"]), expected_html)

    def test_form_validation(self):
        form = DishSearchForm(data={"name_dish_type": "Pizza"})
        self.assertTrue(form.is_valid())
        form = DishSearchForm(data={})
        self.assertTrue(form.is_valid())


class CookSearchFormTest(TestCase):
    def test_form_rendering(self):
        form = CookSearchForm()
        expected_html = (
            "<input type='text' name='username' "
            "placeholder='Search by username' maxlength='255' "
            "id='id_username'>"
        )
        self.assertHTMLEqual(str(form["username"]), expected_html)

    def test_form_validation(self):
        form = CookSearchForm(data={"username": "admin1"})
        self.assertTrue(form.is_valid())
        form = CookSearchForm(data={})
        self.assertTrue(form.is_valid())


class DishFormTest(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(name="Pasta")
        self.cook1 = Cook.objects.create(username="John", years_of_experience=5)
        self.cook2 = Cook.objects.create(username="Alice", years_of_experience=2)

    def test_dish_form_valid(self):
        form_data = {
            "name": "Holubtsi",
            "price": 10.99,
            "description": "test description",
            "dish_type": self.dish_type.id,
        }
        form = DishForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_dish_form_invalid(self):
        form_data = {
            "name": "Rice",
            "dish_type": self.dish_type.id,
            "cooks": [],
        }
        form = DishForm(data=form_data)
        self.assertFalse(form.is_valid())
