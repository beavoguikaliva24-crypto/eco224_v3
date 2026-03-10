from django.db import models, transaction
from django.conf import settings
from datetime import date
import unicodedata
import re
from datetime import date, datetime

class sexe(models.TextChoices):
    MASCULIN = 'M', 'Masculin'
    FEMININ = 'F', 'Féminin'
    AUTRE = 'A', 'Autre'
class mois(models.TextChoices):
    JANVIER = '01', 'Janvier'
    FEVRIER = '02', 'Février'
    MARS = '03', 'Mars'
    AVRIL = '04', 'Avril'
    MAI = '05', 'Mai'
    JUIN = '06', 'Juin'
    JUILLET = '07', 'Juillet'
    AOUT = '08', 'Août'
    SEPTEMBRE = '09', 'Septembre'
    OCTOBRE = '10', 'Octobre'
    NOVEMBRE = '11', 'Novembre'
    DECEMBRE = '12', 'Décembre'
    INCONNU = '00', 'Inconnu'
    


# On suppose que sexe et mois sont importés depuis tes constantes
# from .constants import sexe, mois 

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile', verbose_name="Compte utilisateur", null=True, blank=True)
    parents = models.ForeignKey('Parent', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', verbose_name="Parents")
    
    matricule = models.CharField(max_length=50, unique=True, verbose_name="Matricule", blank=True)
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom1 = models.CharField(max_length=100, verbose_name="Prénom 1")
    prenom2 = models.CharField(max_length=100, null=True, blank=True, verbose_name="Prénom 2")
    prenom3 = models.CharField(max_length=100, null=True, blank=True, verbose_name="Prénom 3")
    full_name = models.CharField(max_length=300, null=True, blank=True, verbose_name="Nom complet")
    
    genre = models.CharField(max_length=1, choices=sexe.choices, verbose_name="Genre")
    photo = models.ImageField(upload_to='students_photos/', null=True, blank=True, verbose_name="Photo de l'élève")

    # Gestion de la naissance
    jour_choix = [(str(i).zfill(2), str(i).zfill(2)) for i in range(1, 32)]
    jour_naissance = models.CharField(max_length=2, choices=jour_choix, verbose_name="Jour de naissance")
    mois_naissance = models.CharField(max_length=2, default=mois.INCONNU, choices=mois.choices, verbose_name="Mois de naissance")
    annee_choix = [('0000', '0000')] + [(str(i), str(i)) for i in range(date.today().year, 1980, -1)]
    annee_naissance = models.CharField(max_length=4, choices=annee_choix, verbose_name="Année de naissance")
    
    date_naissance = models.CharField(max_length=10, null=True, blank=True, verbose_name="Date de naissance")
    lieu_naissance = models.CharField(max_length=100, null=True, blank=True, verbose_name="Lieu de naissance")
    
    # Informations filiation texte (en plus de la relation Parent)
    pere = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nom du père")
    mere = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nom de la mère")

    is_active = models.BooleanField(default=True, verbose_name="Élève actif")

    @property
    def affectation_actuelle(self):
        """Récupère la dernière affectation de l'élève"""
        # On importe ici pour éviter les imports circulaires
        from .models import Affectation 
        return Affectation.objects.filter(eleve=self).select_related('classe', 'annee_scolaire').last()

    def nettoyer_textes(self, text):
        if not text: return ""
        # Normalisation pour enlever les accents (ex: É -> E)
        texte_normalise = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
        return re.sub(r'[^a-zA-Z0-9\s]', '', texte_normalise).upper().strip()

    def generer_date_naissance_str(self):
        j, m, a = self.jour_naissance, self.mois_naissance, self.annee_naissance
        return f"{j}/{m}/{a}"

    def save(self, *args, **kwargs):
        # 1. Pré-traitement
        self.nom = self.nettoyer_textes(self.nom)
        self.prenom1 = self.nettoyer_textes(self.prenom1)
        self.prenom2 = self.nettoyer_textes(self.prenom2)
        self.prenom3 = self.nettoyer_textes(self.prenom3)
        
        prenoms = [p for p in [self.prenom1, self.prenom2, self.prenom3] if p]
        self.full_name = f"{' '.join(prenoms)} {self.nom}"
        self.date_naissance = f"{self.jour_naissance}/{self.mois_naissance}/{self.annee_naissance}"

        # 2. Sauvegarde avec gestion du matricule
        if not self.pk:
            # On utilise une transaction pour garantir l'intégrité
            with transaction.atomic():
                super().save(*args, **kwargs) # Premier save pour générer l'ID
                
                # Génération du matricule
                comp = [self.nom[:2], self.prenom1[:2], self.prenom2[:1], self.prenom3[:1]]
                lettres = ''.join([c for c in comp if c]).upper()
                date_code = f"{self.annee_naissance[-2:]}{self.mois_naissance}{self.jour_naissance}"
                annee_actuelle = str(date.today().year)[-2:]
                
                self.matricule = f"{lettres}[{date_code}{self.genre}{self.id}{annee_actuelle}]"
                
                # Deuxième save uniquement pour le matricule
                super().save(update_fields=['matricule'])
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.matricule}) - Genre: {self.get_genre_display()} - Né(e) le {self.date_naissance} à {self.lieu_naissance}"

class Teacher(models.Model):
    """Informations spécifiques aux enseignants"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_profile', verbose_name="Compte utilisateur")
    specialty = models.CharField(max_length=100, verbose_name="Spécialité") # ex: Mathématiques, Informatique
    hire_date = models.DateField(verbose_name="Date d'embauche")
    bio = models.TextField(blank=True, verbose_name="Biographie")
    cv = models.FileField(upload_to='cv_teachers/', null=True, blank=True, verbose_name="CV")

    def __str__(self):
        return f"M./Mme {self.user.get_full_name()} - Spécialité: {self.specialty}"

class Parent(models.Model):
    """Informations pour le suivi parental"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='parent_profile', verbose_name="Compte utilisateur")

    def __str__(self):
        return f"Parent: {self.user.get_full_name()}"