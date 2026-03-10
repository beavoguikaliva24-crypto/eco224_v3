from django.contrib import admin
from .models import FraisScolarite, Paiement, Versement

admin.site.register(FraisScolarite)
admin.site.register(Paiement)
admin.site.register(Versement)