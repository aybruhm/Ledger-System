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
      

class TransactionTypes(models.TextChoices):
    DEPOSIT = "deposit", "desposit" 
    WITHDRAW = "withdraw", "withdraw"
    TRANSFER = "transfer", "transfer"
    
    class Meta:
        db_table = "transaction_types"
     
        
class Account(TimeStampModel):
    name = models.CharField(max_length=255, unqiue=True)
    slug = models.SlugField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    available_amount = models.FloatField(default=0.0)
    type = models.CharField(choices=TransactionTypes, max_length=10)
    
    def __str__(self) -> str:
        return "Account for {}".format(self.name)
    
    def save(self, *args, **kwargs):
        
        if not self.slug:
            self.slug = slugify(self.name)
        
        super(Account, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = "Accounts"
        db_table = "accounts"