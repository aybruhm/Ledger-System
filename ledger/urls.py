# Django Imports
from django.urls import path

# App Imports
from ledger.views import Deposit, Withdraw, CreateUserAccount, CreateUser,\
    GetUserBalance, GetAccountBalance


app_name = "ledger"


urlpatterns = [
    path("deposit/", Deposit.as_view(), name="deposit"),
    path("withdraw/", Withdraw.as_view(), name="withdraw"),
    
    path("create-user-account/", CreateUserAccount.as_view(), name="create-account"),
    path("create-user/", CreateUser.as_view(), name="create-user"),
    path("user-balance/<int:user>/", GetUserBalance.as_view(), name="user-balance"),
    path("account-balance/<str:name>/<int:user>/", GetAccountBalance.as_view(), name="account-balance"),
]
