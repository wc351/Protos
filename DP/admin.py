from django.contrib import admin
from DP import models

admin.site.register(models.BoolField)
admin.site.register(models.BoolMeasurement)
admin.site.register(models.IntField)
admin.site.register(models.IntMeasurement)
admin.site.register(models.DeciField)
admin.site.register(models.DeciMeasurement)
admin.site.register(models.FloatField)
admin.site.register(models.FloatMeasurement)
admin.site.register(models.CharField)
admin.site.register(models.CharMeasurement)
admin.site.register(models.Project)
admin.site.register(models.Site)
admin.site.register(models.Location)
admin.site.register(models.ObjectOfStudy)
admin.site.register(models.CurrentProject)




