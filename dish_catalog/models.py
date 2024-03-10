from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from restaurant_kitchen_service import settings


class DishType(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Cook(AbstractUser):
    years_of_experience = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        verbose_name = "cook"
        verbose_name_plural = "cooks"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("dish_catalog:cook-detail", kwargs={"pk": self.pk})


class Dish(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    description = models.TextField(max_length=50, blank=True)
    dish_type = models.ForeignKey(
        DishType,
        on_delete=models.CASCADE)

    cookers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="dishes"
    )

    def __str__(self):
        return f"{self.name}: {self.price} ({self.description})"
