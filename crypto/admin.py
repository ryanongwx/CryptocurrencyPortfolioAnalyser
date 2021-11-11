from django.contrib import admin
from .models import Transaction
from django.contrib.auth import get_user_model

User = get_user_model()
# Register your models here.
admin.site.register(Transaction)
admin.site.register(User)
