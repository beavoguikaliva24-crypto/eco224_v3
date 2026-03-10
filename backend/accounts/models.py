from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserManager(BaseUserManager):
    def create_user(self, contact, password=None, **extra_fields):
        if not contact:
            raise ValueError("Le numéro de téléphone est obligatoire")
        contact = str(contact).strip()

        role = extra_fields.get("role", "STUDENT")
        if role in ["DEV", "ADMIN", "STAFF"]:
            extra_fields.setdefault("is_staff", True)

        user = self.model(contact=contact, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, contact, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "DEV")
        return self.create_user(contact, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    contact = models.CharField(max_length=25, unique=True, verbose_name="N° de Téléphone")
    email = models.EmailField(verbose_name="Adresse email", blank=True, default="")
    first_name = models.CharField(max_length=150, verbose_name="Prénom(s)")
    last_name = models.CharField(max_length=150, verbose_name="Nom")
    adress = models.CharField(max_length=255, blank=True, verbose_name="Adresse")
    profession = models.CharField(max_length=100, blank=True, verbose_name="Profession")
    photo = models.ImageField(upload_to="users_photos/", null=True, blank=True, verbose_name="Photo de profil")

    ROLE_CHOICES = (
        ("DEV", "Développeur"),
        ("ADMIN", "Administrateur"),
        ("STAFF", "Direction/Bureau"),
        ("TEACHER", "Enseignant"),
        ("PARENT", "Parent"),
        ("STUDENT", "Élève"),
        ("OTHER", "Autre"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="STUDENT", verbose_name="Rôle")

    permission = models.CharField(max_length=255, blank=True, verbose_name="Niveau de Permission")

    is_active = models.BooleanField(default=True, verbose_name="Compte actif")
    is_staff = models.BooleanField(default=False, verbose_name="Accès admin Django")
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "contact"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ["-date_joined"]
        permissions = [
            ("can_view_financial_reports", "Peut voir les rapports financiers"),
            ("can_edit_all_grades", "Peut modifier toutes les notes"),
            ("can_manage_enrollments", "Peut gérer les inscriptions"),
            ("can_access_audit_log", "Peut consulter le journal d'audit"),
            ("can_validate_exams", "Peut valider les examens"),
        ]

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()}) - permissions: {self.permission}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def save(self, *args, **kwargs):
        logic = {
            "DEV": "CRUD (ajout mis a jour supression)",
            "ADMIN": "CRUD (ajout mis a jour supression)",
            "STAFF": "CRU (ajouter et modifier)",
            "TEACHER": "CR (ajouter simple)",
            "PARENT": "R (voir)",
            "STUDENT": "R (voir)",
            "OTHER": "R (voir)",
        }
        self.permission = logic.get(self.role, "R (voir)")

        if self.role in ["DEV", "ADMIN", "STAFF"]:
            self.is_staff = True

        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def map_role_to_group(sender, instance, created, **kwargs):
    role_mapping = {
        "DEV": "Développeurs",
        "ADMIN": "Administrateurs",
        "STAFF": "Direction",
        "TEACHER": "Enseignants",
        "PARENT": "Parents",
        "STUDENT": "Élèves",
        "OTHER": "Autres",
    }

    group_name = role_mapping.get(instance.role)
    if group_name:
        group, _ = Group.objects.get_or_create(name=group_name)
        all_role_groups = Group.objects.filter(name__in=role_mapping.values())
        instance.groups.remove(*all_role_groups)
        instance.groups.add(group)