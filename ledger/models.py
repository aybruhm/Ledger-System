# Django Imports
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.utils.text import slugify

# App Imports
from ledger.timestamps import TimeStampModel
           
            
class Account(TimeStampModel):
    name = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    available_amount = models.FloatField(default=0.0)
    
    def __str__(self) -> str:
        return self.name
          
    def save(self, *args, **kwargs):
        
        if self.name:
            self.name = slugify(self.name)
        
         
        user_accounts = Account.objects.filter(user=self.user)
        
        if user_accounts.count() > 10:
            raise ValidationError("You can only have 10 accounts!")
        
        super(Account, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = "User Accounts"
        db_table = "accounts"
        
        
class Transaction(TimeStampModel):
    
    TRANSACTION_TYPES = (
        ("deposit", "desposit"),
        ("withdraw", "withdraw"),
        ("transfer", "transfer")
    )
    account = models.ForeignKey(Account, on_delete=models.CASCADE, help_text="sender", null=True)
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, help_text="receiver", null=True, related_name="transfer_to")
    slug = models.SlugField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="sender", null=True)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="receiver", null=True, related_name="to_user")
    amount = models.FloatField(default=0.0)
    type = models.CharField(choices=TRANSACTION_TYPES, max_length=10)
    
    def __str__(self) -> str:
        return "{}'s transaction".format(self.account)
        
    class Meta:
        verbose_name_plural = "User Transactions"
        db_table = "transactions"
    
