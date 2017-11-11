from django.contrib import admin
from account.models import Site, ImportUser, Log

admin.site.register(Site)
admin.site.register(ImportUser)
admin.site.register(Log)
