from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator

from .models import Cook, Dish


class CooksExperienceYearForm(UserCreationForm):
    years_of_experience = forms.IntegerField(
        required=True,
        validators=[MinValueValidator(2)],
        help_text="Enter your years of experience (at least 2 years required)."
    )

    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "years_of_experience",
        )


class CookForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Dish
        fields = "__all__"


class CooksExperienceYearUpdateForm(forms.ModelForm):
    years_of_experience = forms.IntegerField(
        required=True,
        validators=[MinValueValidator(2)],
        help_text="Enter your years of experience (at least 2 years required)."
    )

    class Meta:
        model = Cook
        fields = ("years_of_experience",)

    def clean_license_number(self):
        years_of_experience = self.cleaned_data["years_of_experience"]
        return years_of_experience
