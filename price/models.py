from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class PriceConfiguration(models.Model):
    name = models.CharField(_("Price Config Name"), max_length=50)
    is_active = models.BooleanField(_("is active"), default=False)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="created_by",
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Price Configuration"


class DistanceBasePrice(models.Model):
    DAYS_OF_WEEK = (
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
        (7, "Sunday"),
    )

    price = models.FloatField(_("base price"))
    kms = models.FloatField(_("kms upto"))
    day = models.PositiveSmallIntegerField(_("day"), choices=DAYS_OF_WEEK)
    price_configuration = models.ForeignKey(
        PriceConfiguration, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "Distance Base Price"
        unique_together = ("day", "price_configuration")

    def __str__(self) -> str:
        day_of_week = "none"
        for number, day in self.DAYS_OF_WEEK:
            if number == self.day:
                day_of_week = day
                break
        return f"{self.price_configuration.name} - {day_of_week}"


class DistanceAdditionalPrice(models.Model):
    threshold_kms = models.FloatField(_("threshold kms"))
    price_after_threshold = models.FloatField(_("price/km after threshold"))
    price_before_threshold = models.FloatField(_("price/km before threshold"))
    price_configuration = models.OneToOneField(
        PriceConfiguration, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.price_configuration} - Rs. {self.price_after_threshold}/km"

    class Meta:
        verbose_name_plural = "Distance Additional Price"


class TimeMultiplierFactor(models.Model):
    class Meta:
        verbose_name_plural = "Time Multiplier Factor"

    factor = models.FloatField(_("time factor"))
    hours = models.FloatField(_("under hours"))
    price_configuration = models.ForeignKey(
        PriceConfiguration, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.price_configuration} - TMF under {self.hours} hour{ 's' if self.hours > 1 else ''}"
    

class WaitingCharges(models.Model):
    class Meta:
        verbose_name_plural = "Waiting Charges"

    wait_time = models.FloatField(_("Wait time (in mins)"))
    wait_time_price = models.FloatField(_("price"))
    price_configuration = models.OneToOneField(
        PriceConfiguration, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.price_configuration} - Rs. {self.wait_time_price} / {self.wait_time} min"
