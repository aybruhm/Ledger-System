# Django Imports
from django.urls import path

# App Imports
from ledger.views import LedgerAPI, Deposit, Withdraw, CreateUserAccount, \
    AccountToAccountTransfer, AccountToUserTransfer,\
    GetUserBalance, GetAccountBalance


app_name = "ledger"


urlpatterns = [
    path("", LedgerAPI.as_view(), name="ledger"),
    path("deposit/", Deposit.as_view(), name="deposit"),
    path("withdraw/", Withdraw.as_view(), name="withdraw"),
    path("account-to-user-transfer/<str:user_account>/", AccountToUserTransfer.as_view(), name="account-to-user-transfer"),
    path("account-to-account-transfer/", AccountToAccountTransfer.as_view(), name="account-to-user-transfer"),
    path("create-user-account/", CreateUserAccount.as_view(), name="create-account"),
    path("user-balance/", GetUserBalance.as_view(), name="user-balance"),
    path("account-balance/<str:name>/", GetAccountBalance.as_view(), name="account-balance"),
]
