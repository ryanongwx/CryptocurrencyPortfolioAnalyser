from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    pass

class Transaction(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    coin = models.CharField(max_length=10, verbose_name='Name of Cryptocurrency')
    transactiontype = models.CharField(max_length=10, verbose_name='Type of Transaction')
    price = models.FloatField(verbose_name="Price Transacted")
    tokenqty = models.FloatField(verbose_name="Quantity Transacted")
    date = models.DateField(verbose_name="Date of Transaction")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    totalprice = models.FloatField()
    transactionfee = models.FloatField()

    def __str__(self):
        return f"{self.coin} Transaction {self.auto_increment_id} : {self.tokenqty}{self.coin} at {self.price} on {self.date}"