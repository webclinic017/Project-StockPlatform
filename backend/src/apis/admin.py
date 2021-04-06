from django.contrib import admin

# Register your models here.

from .models import User, Strategy, Result

admin.site.register(User)
admin.site.register(Strategy)
admin.site.register(Result)