from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "eleve", "matiere", "periode", "note1", "note2", "moyenne", "appreciation")
    list_filter = ("eleve", "matiere", "periode")
    search_fields = ("eleve__full_name", "matiere__nom")