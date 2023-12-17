from django.forms import ModelForm, ValidationError

from .models import (
    DistanceAdditionalPrice,
    DistanceBasePrice,
    TimeMultiplierFactor,
    WaitingCharges
)


class DistanceBasePriceForm(ModelForm):
    """
    Form for handling 'Distance Base Price' inputs
    """

    class Meta:
        model = DistanceBasePrice
        fields = ["price", "kms", "day"]

    def clean_price(self):
        if self.cleaned_data['price'] <= 0:
            raise ValidationError("Price must be greater than 0.")
        return self.cleaned_data['price']
    
    def clean_kms(self):
        if self.cleaned_data['kms'] <= 0:
            raise ValidationError("Distance must be greater than 0.")
        return self.cleaned_data['kms']
    

class DistanceAdditionalPriceForm(ModelForm):
    """
    Form for handling 'Distance Additional Price' inputs
    """

    class Meta:
        model = DistanceAdditionalPrice
        fields = ['price_before_threshold', "threshold_kms", "price_after_threshold"]

    
    def clean_price(self):
        if self.cleaned_data['price'] <= 0:
            raise ValidationError("Price must be greater than 0.")
        return self.cleaned_data['price']
    
    def clean_kms(self):
        if self.cleaned_data['kms'] <= 0:
            raise ValidationError("Distance must be greater than 0.")
        return self.cleaned_data['kms']


class TimeMultiplierFactorForm(ModelForm):
    """
    Form for handling 'Time Multiplier Factor' inputs
    """

    class Meta:
        model = TimeMultiplierFactor
        fields = ["factor", "hours"]
    
    def clean_factor(self):
        if self.cleaned_data['factor'] <= 0:
            raise ValidationError("Multiplication factor must be greater than 0.")
        return self.cleaned_data['factor']
    
    def clean_hours(self):
        if self.cleaned_data['hours'] <= 0:
            raise ValidationError("Number of hours must be greater than 0.")
        return self.cleaned_data['hours']


class WaitingChargesForm(ModelForm):
    """
    Form for handling 'Waiting Charges' inputs
    """

    class Meta:
        model = WaitingCharges
        fields = ['wait_time', "wait_time_price"]

    
    def clean_price(self):
        if self.cleaned_data['wait_time_price'] <= 0:
            raise ValidationError("Price must be greater than 0.")
        return self.cleaned_data['wait_time_price']
    
    def clean_kms(self):
        if self.cleaned_data['wait_time'] <= 0:
            raise ValidationError("Wait time must be greater than 0.")
        return self.cleaned_data['wait_time']