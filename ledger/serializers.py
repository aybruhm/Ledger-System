# Rest Framework Imports
from rest_framework import serializers

# App Imports
from ledger.models import Account, User


class AccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = ("id", "name", "user", "available_amount", "type",)
        

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ("id", "firstname", "lastname", "username")