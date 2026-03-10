from django.contrib import admin
from .models import AnneeScolaire, Periode, Classe, Matiere, MatiereClasse

admin.site.register(AnneeScolaire)
admin.site.register(Periode)
admin.site.register(Classe)
admin.site.register(Matiere)
admin.site.register(MatiereClasse)