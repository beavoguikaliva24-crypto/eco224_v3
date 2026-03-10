from django.db import transaction
from django.contrib.auth import get_user_model
from .models import Student, Parent

User = get_user_model()

def create_full_enrollment(user_data, student_data, parent_link_data=None):
    """
    Crée un User, un profil Parent et un Student en une seule transaction.
    """
    try:
        with transaction.atomic():
            # 1. Création de l'utilisateur (Compte du Parent)
            # On utilise le contact comme USERNAME_FIELD selon votre modèle User
            parent_user = User.objects.create_user(
                contact=user_data['contact'],
                password=user_data['password'],
                email=user_data.get('email', ''),
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                adress=user_data.get('adress', ''),
                profession=user_data.get('profession', ''),
                role='PARENT'
            )

            # 2. Création du profil Parent lié au User
            parent_profile = Parent.objects.create(user=parent_user)

            # 3. Création de l'élève lié au parent
            # On injecte le parent_profile dans les données de l'élève
            student = Student.objects.create(
                parents=parent_profile,
                nom=student_data['nom'],
                prenom1=student_data['prenom1'],
                prenom2=student_data.get('prenom2'),
                prenom3=student_data.get('prenom3'),
                genre=student_data['genre'],
                jour_naissance=student_data['jour_naissance'],
                mois_naissance=student_data['mois_naissance'],
                annee_naissance=student_data['annee_naissance'],
                lieu_naissance=student_data.get('lieu_naissance'),
                pere=student_data.get('pere'),
                mere=student_data.get('mere'),
            )

            return student, "Inscription réussie"

    except Exception as e:
        # En cas d'erreur, la transaction.atomic annule tout (rollback)
        return None, f"Erreur lors de l'inscription : {str(e)}"