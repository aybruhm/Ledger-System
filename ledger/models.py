# Django Imports
from django.db import models
from django.utils.text import slugify

# App Imports
from ledger.timestamps import TimeStampModel


class User(TimeStampModel):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    username = models.CharField(max_length=100, unique=True)
    
    def __str__(self) -> str:
        return "{} {}".format(self.firstname, self.lastname)

    class Meta:
        verbose_name_plural = "Users"
        db_table = "users"
           
            
class Account(TimeStampModel):
    name = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    available_amount = models.FloatField(default=0.0)
    
    def __str__(self) -> str:
        return self.name
          
    def save(self, *args, **kwargs):
        
        if not self.slug:
            self.name = slugify(self.name)
        
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
    type = models.CharField(choices=TRANSACTION_TYPES, max_length=10)
    
    def __str__(self) -> str:
        return "Transaction for {}".format(self.account.name)
    
    def save(self, *args, **kwargs):
        
        if not self.slug:
            self.slug = slugify(self.account.name)
        
        super(Transaction, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = "User Transactions"
        db_table = "transactions"
        
