# Rest Framework Imports
from rest_framework import serializers

# App Imports
from ledger.models import Transaction, User, Account


class DepositWithdrawTransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transaction
        fields = ("account", "amount", "type")


class TransferUserTransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transaction
        fields = ("account", "amount", "type")
        

class TransferTransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transaction
        fields = ("account", "to_account", "amount", "type")


class AccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = ("id", "name",)
        

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", \
            "email", "username", "password")
        
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get("password"))
        user.save()
        return user