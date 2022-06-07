# Django Imports
from django.urls import path

# App Imports
from ledger.views import Deposit


app_name = "ledger"


urlpatterns = [
    path("deposit/", Deposit.as_view(), name="deposit"),
]
