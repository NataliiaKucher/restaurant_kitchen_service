from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator

from .models import Cook, Dish


class CooksExperienceYearCreateForm(UserCreationForm):
    years_of_experience = forms.IntegerField(
        required=True,
        validators=[MinValueValidator(1)],
        help_text="Enter your years of experience (at least 1 years required)."
    )

    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "years_of_experience",
        )


class DishForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Dish
        exclude = ("cookers",)


class CooksExperienceYearUpdateForm(forms.ModelForm):
    years_of_experience = forms.IntegerField(
        required=True,
        validators=[MinValueValidator(1)],
        help_text="Enter your years of experience (at least 1 years required)."
    )

    class Meta:
        model = Cook
        fields = (
            "first_name",
            "last_name",
            "years_of_experience",
        )

    def clean_years_of_experience(self):
        years_of_experience = self.cleaned_data["years_of_experience"]
        return years_of_experience


class DishSearchForm(forms.Form):
    dish_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name"
            }
        )
    )


class CookSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by username"
            }
        )
    )


class DishTypeSearchForm(forms.Form):
    name_dish_type = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by type"
            }
        )
    )
