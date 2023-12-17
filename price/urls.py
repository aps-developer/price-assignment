from django.urls import path

from .views import PriceView, PriceCalculatorView

urlpatterns = [
    path('', PriceView.as_view()),
    path('calculate/', PriceCalculatorView.as_view()),
]