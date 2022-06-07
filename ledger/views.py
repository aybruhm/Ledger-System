# Django Imports
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
                account_name = serializer.validated_data.get("name")
                amount = serializer.validated_data.get("amount")
                
                # Save serialized data
                serializer.save()
                
                payload = success_response(
                    status="success",
                    message="₦{} has been deposited to {} account!".format(account_name, amount),
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
    serilizer_class = CreateTransactionSerializer
    
    def post(self, request:HttpRequest) -> response.Response:
        pass