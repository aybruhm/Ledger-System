# Rest Framework Imports
from rest_framework import serializers

# App Imports
from ledger.models import Transaction, User, Account


class CreateTransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transaction
        fields = ("account", "user", "amount", "type")
        

class AccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = ("id", "name", "user")
        

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ("id", "firstname", "lastname", "username")