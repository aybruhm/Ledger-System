# Django Imports
import json
from typing import final
from django.db.models import Sum
from django.contrib.auth.models import User
from django.http import HttpRequest

# Rest Framework Imports
from rest_framework import views, response, status

# App Imports
from ledger.serializers import AccountSerializer, TransferUserTransactionSerializer, UserSerializer, \
    TransferTransactionSerializer, \
        DepositWithdrawTransactionSerializer
from ledger.models import Account

# Third Part Imports
from rest_api_payload import success_response, error_response


class LedgerAPI(views.APIView):
    
    PROTOCOL = "http://"
    
    def get(self, request:HttpRequest) -> response.Response:
        
        HOST_NAME = request.get_host() + "/"
        BASE_URL = self.PROTOCOL + HOST_NAME

        welcome_data = {
            "routes": {
                "register": BASE_URL + "api-auth/create-user/",
                "login": BASE_URL + "api-auth/login/",
                "logout": BASE_URL + "api-auth/logout/",
                "deposit": BASE_URL + "api/deposit/",
                "withdraw": BASE_URL + "api/withdraw/",
                "account-user": BASE_URL + "api/account-to-user-transfer/<str:user_account/<int:to_user>/",
                "account-account": BASE_URL + "api/account-to-account-transfer/",
                "create-user-account": BASE_URL +"api/create-user-account/",
                "user-balance": BASE_URL + "api/user-balance/",
                "account-balance": BASE_URL + "api/account-balance/<str:name>/",
            },
        }
        return response.Response(data=welcome_data, status=status.HTTP_200_OK)


class Deposit(views.APIView):
    serializer_class = DepositWithdrawTransactionSerializer
    
    def post(self, request:HttpRequest) -> response.Response:
        """
        > The function checks if the transaction type is deposit, 
        if it is, it saves the serialized data
        and returns a success response, otherwise, it returns an error response
        
        :param request: This is the request object that is passed to the view
        :type request: HttpRequest
        :return: A response object
        """
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            
            if serializer.validated_data.get("type") == "deposit":
            
                # Get validated data
                account_name = serializer.validated_data.get("account")
                amount = serializer.validated_data.get("amount")
                
                # Get user account and update available amount
                user_account = Account.objects.get(name=account_name, user=request.user)
                user_account.available_amount += amount
                user_account.save()
                
                # Save serialized data
                serializer.save(user=request.user)
                
                payload = success_response(
                    status="success",
                    message="₦{} has been deposited to {} account!".format(amount, account_name),
                    data=serializer.data
                )
                return response.Response(data=payload, status=status.HTTP_201_CREATED)

            else:
                
                payload = error_response(
                    status="error",
                    message="Wrong transaction type!"
                )
                return response.Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            
            payload = error_response(
                status="error",
                message=serializer.errors
            )
            return response.Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
        
        
class Withdraw(views.APIView):
    serializer_class = DepositWithdrawTransactionSerializer
    
    def post(self, request:HttpRequest) -> response.Response:
        """
        > It validates the data sent in the request, checks if the transaction type is `withdraw`, 
        gets the user's account, subtracts the amount from the available amount, 
        saves the serialized data and returns a success response
        
        :param request: This is the request object that is sent to the view
        :type request: HttpRequest
        :return: A response object
        """
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            
            if serializer.validated_data.get("type") == "withdraw":
            
                # Get validated data
                account_name = serializer.validated_data.get("account")
                amount = serializer.validated_data.get("amount")
                
                # Get user account and subtract amount from available amount
                user_account = Account.objects.get(name=account_name, user=request.user)
                user_account.available_amount -= amount
                user_account.save()
                
                # Save serialized data
                serializer.save(user=request.user)
                
                payload = success_response(
                    status="success",
                    message="₦{} has been deducted from {} account!".format(amount, account_name),
                    data=serializer.data
                )
                return response.Response(data=payload, status=status.HTTP_201_CREATED)

            else:
                
                payload = error_response(
                    status="error",
                    message="Wrong transaction type!"
                )
                return response.Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            
            payload = error_response(
                status="error",
                message=serializer.errors
            )
            return response.Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    
    
class AccountToUserTransfer(views.APIView):
    serializer_class = TransferUserTransactionSerializer
    
    def get_user_account(self, user_account:str):
        
        try:
            user_account = Account.objects.get(name=user_account)   
            return user_account
        except Exception:
            payload = error_response(
                status="error",
                message="Opps. Account does not exist!"
            )
            return response.Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, to_user:int, user_account:str):
        user_account =  self.get_user_account(user_account=user_account)
        serializer = AccountSerializer(user_account)
        
        payload = success_response(
            status="success", message="This account belongs to {}!"\
                .format(User.objects.get(id=to_user)),
            data=serializer.data
        )
        return response.Response(data=payload)
    
    def post(self, request:HttpRequest, to_user:int, user_account:str) -> response.Response:
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
                
            if serializer.validated_data.get("type") == "transfer":
            
                # Get receiver data
                from_account_name = serializer.validated_data.get("account")
                from_account_user = request.user
                
                # Get send (logged in) data 
                to_account_name = user_account
                to_account_user = User.objects.get(id=to_user)
                
                # Get amount
                amount = serializer.validated_data.get("amount")
                
                # Get send account, deduct amount from available amomut and save to database
                sender_account = Account.objects.get(name=from_account_name, user=from_account_user)
                sender_account.available_amount -= amount
                sender_account.save()
                
                # Get receiver account, add amount to available amount and save to database
                receiver_account = Account.objects.get(name=to_account_name, user=to_account_user)
                receiver_account.available_amount += amount
                receiver_account.save()
                
                # Save serialized data
                serializer.save(
                    user=request.user,
                    to_user=to_account_user,
                    to_account=Account.objects.get(name=user_account)
                )
                
                payload = success_response(
                    status="success",
                    message="₦{} has been transferred from {}'s {} account to {}'s {} account!"\
                        .format(amount, from_account_user, from_account_name, to_account_user, to_account_name),
                    data=serializer.data
                )
                return response.Response(data=payload, status=status.HTTP_201_CREATED)

            else:
                
                payload = error_response(
                    status="error",
                    message="Wrong transaction type!"
                )
                return response.Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            
            payload = error_response(
                status="error",
                message=serializer.errors
            )
            return response.Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    

class AccountToAccountTransfer(views.APIView):
    serializer_class = TransferTransactionSerializer
    
    def post(self, request:HttpRequest) -> response.Response:
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
                
            if serializer.validated_data.get("type") == "transfer":
            
                # Get validated data
                from_account_name = serializer.validated_data.get("account")
                to_account_name = serializer.validated_data.get("to_account")
                amount = serializer.validated_data.get("amount")
                
                # Get account to send money from
                sender_account = Account.objects.get(name=from_account_name, user=request.user)
                sender_account.available_amount -= amount
                sender_account.save()
                
                # Get account to receive money 
                receiver_account = Account.objects.get(name=to_account_name, user=request.user)
                receiver_account.available_amount += amount
                receiver_account.save()
                
                # Save serialized data
                serializer.save(user=request.user, to_user=request.user)
                
                payload = success_response(
                    status="success",
                    message="₦{} has been transferred from {} account to {} account!"\
                        .format(amount, from_account_name, to_account_name),
                    data=serializer.data
                )
                return response.Response(data=payload, status=status.HTTP_201_CREATED)

            else:
                
                payload = error_response(
                    status="error",
                    message="Wrong transaction type!"
                )
                return response.Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            
            payload = error_response(
                status="error",
                message=serializer.errors
            )
            return response.Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    
    
class GetUserBalance(views.APIView):
    
    def get(self, request:HttpRequest) -> response.Response:
        """
        It gets the sum of all the available amounts of all the accounts of the user making the request
        
        :param request: This is the request object that is passed to the view
        :type request: HttpRequest
        :return: A response object
        """
        
        user_accounts = Account.objects.filter(user=request.user).aggregate(Sum("available_amount"))
        
        payload = success_response(
            status="success",
            message="Your total balance is ₦{}"\
                .format(user_accounts["available_amount__sum"]),
            data={}
        )
        return response.Response(data=payload, status=status.HTTP_202_ACCEPTED)
    

class GetAccountBalance(views.APIView):
    serializer_class = AccountSerializer
    
    def get(self, request:HttpRequest, name:str) -> response.Response:
        """
        > It gets the account of the user with the name `name` and returns a response with the
        serialized account data
        
        :param request: This is the request object that is passed to the view
        :type request: HttpRequest
        :param name: The name of the account to be retrieved
        :type name: str
        :return: A response object.
        """
        account = Account.objects.get(name=name, user=request.user)
        serializer = self.serializer_class(account)
        
        payload = success_response(
            status="success",
            message="You have ₦{} in your wallet."\
                .format(account.available_amount),
            data=serializer.data
        )
        return response.Response(data=payload, status=status.HTTP_202_ACCEPTED)
    
    
class CreateUser(views.APIView):
    serializer_class = UserSerializer
    
    def post(self, request:HttpRequest) -> response.Response:
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            payload = success_response(
                status="success",
                message="User creation was a successful!",
                data=serializer.data
            )
            return response.Response(data=payload, status=status.HTTP_201_CREATED)
        
        payload = error_response(
            status="error", message=serializer.errors
        )
        return response.Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    
    
class CreateUserAccount(views.APIView):
    serializer_class = AccountSerializer
    
    def post(self, request:HttpRequest) -> response.Response:
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            
            payload = success_response(
                status="success",
                message="Account creation was a success!",
                data=serializer.data
            )
            return response.Response(data=payload, status=status.HTTP_202_ACCEPTED)
        
        payload = error_response(
            status="error", message=serializer.errors
        )
        return response.Response(data=payload, status=status.HTTP_400_BAD_REQUEST)