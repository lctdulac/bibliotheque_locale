####### Ce fichier définit les modèles de données (différentes tables) utilisées par notre projet

from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

from datetime import datetime, timezone, timedelta

import uuid



class Profile(models.Model):
    nb_livres = models.IntegerField(default=0)
    nb_autres = models.IntegerField(default=0)

    nb_retards = models.IntegerField(default=0)
    premier_retard = models.DateTimeField(null=True, blank=True, default=None)
    deuxième_retard = models.DateTimeField(null=True, blank=True, default=None)
    troisième_retard = models.DateTimeField(null=True, blank=True, default=None)


    BOOL_CHOICE = (
        (0, 0),
        (1, 1)
    )
    bad_user = models.IntegerField(default=0, choices=BOOL_CHOICE)
    
    
    date_bad_user = models.DateTimeField(null=True, blank=True, default=None)

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, unique=True)

    STATUT_TYPE = (
        ('e', 'Étudiant'),
        ('c', 'En recherche d\'emploi'),
        ('r', 'Retraité'),
        ('f', 'Moins de 18 ans'),
        ('a', 'Adulte sans réduction')
    )

    statut = models.CharField(
        max_length=1,
        choices=STATUT_TYPE,
        blank=True,
        help_text='Statut de l\'abonné',
    )

    def __str__(self):
        """Fonction requise par Django pour manipuler les objets Ouvrages dans la base de données."""
        return self.user.username

    @property # property?
    def check_bad_user(self):
        durée_premier_retard = (datetime.now(timezone.utc).date() - self.premier_retard)
        if (durée_premier_retard < timedelta(days=365)) and (self.nb_retards > 3):
            return True
        return False

    # def reset_retards(self):
    #     durée_premier_retard = (date.today() - self.premier_retard)
    #     if (durée_premier_retard > timedelta(days=365)) and user.is_overdue == True:
    #         self.premier_retard = date.today()


class Auteur(models.Model):
    nom = models.CharField(max_length=100)
    prénom = models.CharField(max_length=100)
    lien = models.CharField(max_length=100, default=None, blank=True, null=True)
    img = models.ImageField(upload_to='img/', verbose_name='Photo de l\'auteur', blank=True, null=True)

    YEAR_CHOICES = [(r,r) for r in range(1800, datetime.now(timezone.utc).date().year+1)]

    naissance = models.IntegerField(('Naissance:'), choices=YEAR_CHOICES, default=datetime.now(timezone.utc).date().year)
    mort = models.IntegerField(('Mort:'), choices=YEAR_CHOICES, default=None, null=True, blank=True)

    def __str__(self):
        """Fonction requise par Django pour manipuler les objets Ouvrages dans la base de données."""
        return f'{self.nom}, {self.prénom}'

    def get_absolute_url(self):
        """Cette fonction est requise pas Django, lorsque vous souhaitez détailler le contenu d'un objet."""
        return reverse('auteur-detail', args=[str(self.id)])


class Genre(models.Model):
    titre = models.CharField(max_length=100, help_text='Entrer le genre de l\'ouvrage (e.g. Science Fiction)')

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return reverse('genre-detail', args=[str(self.id)])


class Ouvrage(models.Model):
    titre = models.CharField(max_length=100)
    nb_copies = models.IntegerField(default=1)

    BOOL_CHOICE = (
        (0, 0),
        (1, 1)
    )

    autorisé = models.IntegerField(default=1, choices=BOOL_CHOICE)

    OUVRAGES_TYPE = (
        ('r', 'Revue'),
        ('d', 'DVD'),
        ('v', 'Vinyl'),
        ('l', 'Livre'),
        ('c', 'CD')
    )


    type =  models.CharField(
        max_length=1,
        choices=OUVRAGES_TYPE,
        blank=True,
        help_text='Type d\'ouvrage',
    )


    YEAR_CHOICES = [(r,r) for r in range(1800, datetime.now(timezone.utc).date().year+1)]

    année = models.IntegerField(('année'), choices=YEAR_CHOICES, default=datetime.now(timezone.utc).date().year)


    auteur = models.ForeignKey(Auteur, on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(Genre, help_text='Selectionner un genre pour cet ouvrage')

    def __str__(self):
        """Fonction requise par Django pour manipuler les objets Ouvrages dans la base de données."""
        return self.titre

    def get_absolute_url(self):
        """Cette fonction est requise pas Django, lorsque vous souhaitez détailler le contenu d'un objet."""
        return reverse('ouvrage-detail', args=[str(self.id)])

    def update_copies(self):
        self.nb_copies -= 1

    # def save(self, *args, **kwargs):
    #     self.update_copies()
    #     super(Ouvrage, self).save(*args, **kwargs) 



class EmpruntQuerySet(models.QuerySet):
    """ permet de gérer les multiples delete """

    def delete(self, *args, **kwargs):
        for obj in self:
            obj.delete()
        super(EmpruntQuerySet, self).delete(*args, **kwargs)

class Emprunt(models.Model):
    objects = EmpruntQuerySet.as_manager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID pour cet emprunt')
    date_emprunt = models.DateTimeField()

    BOOL_CHOICE = (
        (0, 0),
        (1, 1)
    )

    retard = models.IntegerField(default=0, choices=BOOL_CHOICE)
    pénalité = models.IntegerField(default=0)

    ouvrage = models.ForeignKey(Ouvrage, on_delete=models.SET_NULL, null=True)
    borrower = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)

    class Meta:
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """Fonction requise par Django pour manipuler les objets Ouvrages dans la base de données."""
        return f'{self.id} ({self.ouvrage.titre})'


    ## Triggers:
    def save(self, *args, **kwargs):
        
        def diminue_copie():
            ## Descend le nombre de copies de 1
            if self.ouvrage.nb_copies > 0:
                new_nb_copies = self.ouvrage.nb_copies - 1
                Ouvrage.objects.filter(id=self.ouvrage.id).update(nb_copies = new_nb_copies)
                print(self.ouvrage.titre, "emprunté avec succès.")
                super(Emprunt, self).save(*args, **kwargs)
            else:
                print("Impossible à emprunter. Il n'y a plus de copies disponibles.")
                pass

        ## Incrémente le nombre de livres de Profile, et diminue le nombre de copie

        if (self.ouvrage.autorisé == 1) and (self.borrower.bad_user == 0):
            if self.ouvrage.type == 'l':
                if self.borrower.nb_livres < 3:
                    new_nb_livres = self.borrower.nb_livres + 1
                    Profile.objects.filter(id=self.borrower.id).update(nb_livres = new_nb_livres)
                    diminue_copie()
                else:
                    print("Impossible à emprunter. Trop de livres déjà empruntés.")
            else:
                if self.borrower.nb_autres < 2:
                    new_nb_autres = self.borrower.nb_autres + 1
                    Profile.objects.filter(id=self.borrower.id).update(nb_autres = new_nb_autres)
                    diminue_copie()
                else:
                    print("Impossible à emprunter. Trop d'oeuvres de type DVD/CD/Vinyl déjà empruntées.")
        elif (self.borrower.bad_user == 1):
            print("Impossible à emprunter. Vous êtes blacklisté.")
        else:
            print("Impossible à emprunter. Cette oeuvre n'est pas autorisé au prêt.")


    def delete(self, *args, **kwargs):

        def augmente_copie():
            ## Augmente le nombre de copies de 1
            new_nb_copies = self.ouvrage.nb_copies + 1
            Ouvrage.objects.filter(id=self.ouvrage.id).update(nb_copies = new_nb_copies)
            print(self.ouvrage.titre, "rendu avec succès.")
            super(Emprunt, self).delete(*args, **kwargs)

        ## Décrémente le nombre de livres de Profile, et augmente le nombre de copie

        if self.ouvrage.type == 'l':
            new_nb_livres = self.borrower.nb_livres - 1
            Profile.objects.filter(id=self.borrower.id).update(nb_livres = new_nb_livres)
            augmente_copie()
           
        else:
            new_nb_autres = self.borrower.nb_autres - 1
            Profile.objects.filter(id=self.borrower.id).update(nb_autres = new_nb_autres)
            augmente_copie()



    ## Methods:
    def compute_date_retour(self):
        date_retour = self.date_emprunt + timedelta(weeks=+4)
        return date_retour

    def compute_pénalité(self):
        pénalité = (datetime.now(timezone.utc) - self.date_retour).days - 3
        if pénalité<0:
            pénalité = 0
        return pénalité

    ## Properties:

    @property
    def date_retour(self):
        return self.compute_date_retour()

    @property
    def pénalité_property(self):
        return self.compute_pénalité()
    
    @property
    def is_overdue(self):
        if self.date_retour and datetime.now(timezone.utc).date() > self.date_retour.date():
            return True
        return False


class Tarif(models.Model):

    STATUT_TYPE = (
        ('e', 'Étudiant'),
        ('c', 'En recherche d\'emploi'),
        ('r', 'Retraité'),
        ('f', 'Moins de 18 ans'),
        ('a', 'Adulte sans réduction')
    )

    statut = models.CharField(
        max_length=1,
        choices=STATUT_TYPE,
        blank=True,
        help_text='Statut de l\'abonné',
    )

    prix = models.IntegerField()

    def __str__(self):
        """Fonction requise par Django pour manipuler les objets Ouvrages dans la base de données."""
        return f'{self.statut} ({self.prix})'






