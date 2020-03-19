from django.contrib import admin
from . import models

admin.site.register(models.OnsiteModel)
admin.site.register(models.OrgInsertion)
admin.site.register(models.SystemUpdateModel)

# Register your models here.
