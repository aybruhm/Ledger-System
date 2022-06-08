# Rest Framework Imports
from rest_framework import serializers

# App Imports
from ledger.models import Transaction, User, Account


class CreateTransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transaction
        fields = ("account", "to_account", "user", "to_user", "amount", "type")
        

class TransferTransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transaction
        fields = ("to_account", "to_user", "amount", "type")
        
    def validate_from_user_accounts(self, value):
        pass
    
    def validate_to_user_account(self, value):
        pass


class AccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = ("id", "name", "user")
        

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ("id", "firstname", "lastname", \
            "email", "username", "password")
        
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.save()
        return user