# Django Imports
from django.db.models import Sum
from django.http import HttpRequest

# Rest Framework Imports
from rest_framework import views, response, status

# App Imports
from ledger.serializers import AccountSerializer, UserSerializer, CreateTransactionSerializer
from ledger.models import Account

# Third Part Imports
from rest_api_payload import success_response, error_response


class Deposit(views.APIView):
    serializer_class = CreateTransactionSerializer
    
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
                account_user = serializer.validated_data.get("user")
                
                # Get user account and update available amount
                user_account = Account.objects.get(name=account_name, user=account_user)
                user_account.available_amount += amount
                user_account.save()
                
                # Save serialized data
                serializer.save()
                
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
    serializer_class = CreateTransactionSerializer
    
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
                account_user = serializer.validated_data.get("user")
                
                # Get user account and subtract amount from available amount
                user_account = Account.objects.get(name=account_name, user=account_user)
                user_account.available_amount -= amount
                user_account.save()
                
                # Save serialized data
                serializer.save()
                
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
    
    
class AccountToAccountTransfer(views.APIView):
    serializer_class = CreateTransactionSerializer
    
    def post(self, request:HttpRequest) -> response.Response:
        pass
    

class AccountToUserTransfer(views.APIView):
    serializer_class = CreateTransactionSerializer
    
    def post(self, request:HttpRequest) -> response.Response:
        pass
    
    
class GetUserBalance(views.APIView):
    
    def get(self, request:HttpRequest, user:int) -> response.Response:
        """
        It returns the total balance of all accounts belonging to a user
        
        :param request: This is the request object that is passed to the view
        :type request: HttpRequest
        :param user: The user id of the user whose balance is being requested
        :type user: int
        :return: A response object
        """
        
        user_accounts = Account.objects.filter(user=user).aggregate(Sum("available_amount"))
        
        payload = success_response(
            status="success",
            message="Your total balance is ₦{}"\
                .format(user_accounts["available_amount__sum"]),
            data={}
        )
        return response.Response(data=payload, status=status.HTTP_202_ACCEPTED)
    

class GetAccountBalance(views.APIView):
    serializer_class = AccountSerializer
    
    def get(self, request:HttpRequest, name:str, user:int) -> response.Response:
        account = Account.objects.get(name=name, user=user)
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
            serializer.save()
            
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