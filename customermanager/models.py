from django.db import models
from django.conf import settings


class Customer(models.Model):
    salutation = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=100)
    street = models.CharField(max_length=150, blank=True, default="")
    house_number = models.CharField(max_length=20, blank=True, default="")
    zip_code = models.CharField(max_length=10, blank=True, default="")
    city = models.CharField(max_length=120, blank=True, default="")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_profile",
        null=True,
        blank=True,
    )

    # ✅ Frontend-Kompatibilität: Form sendet nur "name"
    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    @name.setter
    def name(self, value: str) -> None:
        value = (value or "").strip()
        if not value:
            self.first_name = ""
            self.last_name = ""
            return

        parts = value.split()
        self.first_name = parts[0]
        self.last_name = " ".join(parts[1:]) if len(parts) > 1 else ""

    def __str__(self):
        address = ""
        if self.street or self.house_number or self.zip_code or self.city:
            address = f", {self.street} {self.house_number}, {self.zip_code} {self.city}".strip()

        return f"{self.name} ({self.email}){address}"