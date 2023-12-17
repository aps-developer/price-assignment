import logging
from django.contrib import admin

from .forms import (
    DistanceBasePriceForm,
    DistanceAdditionalPriceForm,
    TimeMultiplierFactorForm,
    WaitingChargesForm
)
from .models import (
    DistanceAdditionalPrice,
    DistanceBasePrice,
    TimeMultiplierFactor,
    PriceConfiguration,
    WaitingCharges
)

logger = logging.getLogger()


class DistanceBasePriceInline(admin.TabularInline):
    model = DistanceBasePrice
    extra = 0
    form = DistanceBasePriceForm


class DistanceAdditionalPriceInline(admin.TabularInline):
    model = DistanceAdditionalPrice
    extra = 0
    form = DistanceAdditionalPriceForm


class TimeMultiplierFactorInline(admin.TabularInline):
    model = TimeMultiplierFactor
    extra = 0
    form = TimeMultiplierFactorForm


class WaitingChargesInline(admin.TabularInline):
    model = WaitingCharges
    extra = 0
    form = WaitingChargesForm


class PriceConfigurationAdmin(admin.ModelAdmin):
    inlines = [
        DistanceBasePriceInline,
        DistanceAdditionalPriceInline,
        TimeMultiplierFactorInline,
        WaitingChargesInline
    ]
    model = PriceConfiguration
    verbose_name = "Price Configuration"
    verbose_name_plural = "Price Configuration"
    readonly_fields = ["updated_by", "created_by", "created_at", "updated_at"]
    list_display =['name', 'is_active']

    def get_fields(self, request, obj):
        if not obj:
            return ["name"]
        return ["name", "updated_by", "created_by", "created_at", "updated_at", "is_active"]
    
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.updated_by = request.user
        logger.info(f' ***** UPDATED BY - {request.user.username} *****')
        obj.save()


admin.site.register(PriceConfiguration, PriceConfigurationAdmin)