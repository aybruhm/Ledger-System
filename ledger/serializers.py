# Rest Framework Imports
from rest_framework import serializers

# App Imports
from ledger.models import Account, User


class TransactAccount(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = ("name", "user", "amount", "type")
        
    def create(self, validated_data):
        """
        It gets the validated data, gets the account name and user, 
        and then increases the available amount with the deposited amount
        
        :param validated_data: The validated data from the serializer
        :return: The account object is being returned.
        """
        
        account_name = validated_data.get("name")
        account_user = validated_data.get("user")
        amount = validated_data.get("amount")
        
        # Get user and account name, 
        # and then increase available amount with deposited amount
        account = Account.objects.get(name=account_name, user=account_user)
        account.available_amount += amount
        
        return account


class AccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = ("id", "name", "user", "available_amount", "type",)
        

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ("id", "firstname", "lastname", "username")