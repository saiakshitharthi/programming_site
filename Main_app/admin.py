from django.contrib import admin
from . import models
# Register your models here.
print('Registered models')
admin.site.register(models.Problems)
admin.site.register(models.Submissions)
admin.site.register(models.User_info)
admin.site.register(models.Friends) 