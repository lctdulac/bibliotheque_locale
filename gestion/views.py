from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from gestion.models import Ouvrage, Emprunt, Tarif, Auteur, Profile, Genre
from django.db.models import Avg, Count, Min, Sum

from django.shortcuts import get_object_or_404
from datetime import datetime, timezone, timedelta, date


## Fonction annexe

def update_and_populate_db(date_today):

    ''' Fonction qui, à chaque arrivée sur la page, met à jour le statut des retards et des pénalités'''


    # Met à jour les retards sur les emprunts
    for emp in Emprunt.objects.all():
        if emp.is_overdue:
            if emp.retard == 0:
                print("Un nouveau retard a été trouvé.")
                emp.retard = 1
                print("Augmentation du nombre de retard de l'utilisateur concerné.")
                if emp.borrower.nb_retards == 0:
                    emp.borrower.premier_retard = date_today
                if emp.borrower.nb_retards == 1:
                    emp.borrower.deuxième_retard = date_today
                if emp.borrower.nb_retards == 2:
                    emp.borrower.troisième_retard = date_today
                    emp.borrower.bad_user = 1
                    emp.borrower.date_bad_user = date_today
                emp.borrower.nb_retards = emp.borrower.nb_retards + 1
                emp.borrower.save()
            emp.pénalité = emp.pénalité_property
            super(Emprunt, emp).save()


    # Met à jour le nombre de retards sur les utiliateurs
    for brw in Profile.objects.all():

        ## Réinitialisation du statut de blacklisté

        if brw.bad_user == 1:
            date_fin_bad_user = brw.date_bad_user + timedelta(days=730)
            if date_today - date_fin_bad_user > timedelta(days=0):
                print("Fin de période de blacklist.")
                brw.bad_user = 0

        ## Réinitialisation des dates de retard

        if brw.premier_retard != None:
            if date_today - (brw.premier_retard + timedelta(days=365)) > timedelta(days=0):
                brw.premier_retard = brw.deuxième_retard
                brw.deuxième_retard = brw.troisième_retard
                brw.troisième_retard = None
                brw.nb_retards -= 1

        brw.save()


## Vues du site


def index(request):
    """Vue de la page d'accueil"""

    # Etat de la base de donnée
    date_today = datetime.now(timezone.utc)
    num_ouvrages = Ouvrage.objects.all().count()
    num_emprunts = Emprunt.objects.all().count()
    num_ouvrages_dispo = Ouvrage.objects.aggregate(Sum('nb_copies'))['nb_copies__sum']
    num_retard = Emprunt.objects.filter(retard = 1).all().count()
    num_en_regle = num_emprunts - num_retard


    # met à jour le statut des emprunts et des utilisateurs
    update_and_populate_db(date_today)

    # Nombre de visites de cette page
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1


    # met à jour le contexte
    context = {
        'date_today': date_today,
        'num_ouvrages': num_ouvrages,
        'num_emprunts': num_emprunts,
        'num_ouvrages_dispo': num_ouvrages_dispo,
        'num_visits': num_visits,
        'num_retard': num_retard,
        'num_en_regle': num_en_regle
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)



class OuvrageListView(generic.ListView):
    model = Ouvrage
    ordering = ["titre"]
    paginate_by = 10

class OuvrageDetailView(generic.DetailView):
    model = Ouvrage

class GenreListView(generic.ListView):
    ordering = ["titre"]
    model = Genre
    paginate_by = 10

class GenreDetailView(generic.DetailView):
    model = Genre

class AuteurListView(generic.ListView):
    ordering = ["nom"]
    model = Auteur
    paginate_by = 10

class TarifListView(generic.ListView):
    ordering = ["prix"]
    model = Tarif
    paginate_by = 10

class AuteurDetailView(generic.DetailView):
    model = Auteur

class MonCompteListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view """

    model = Emprunt
    template_name ='gestion/mon_compte.html'
    paginate_by = 10

    # méthodes de classes

    def get_queryset(self):

        connected_user = self.request.user
        connected_profile = Profile.objects.get(user=connected_user) ## NB : use get with user=xxx or filter with user__in=xxx selon si xxx est une queryset ou un object

        return Emprunt.objects.filter(borrower = connected_profile).order_by('date_emprunt')

    def get_context_data(self,**kwargs):

        # met à jour le statut des emprunts et des utilisateurs 
        date_today = datetime.now(timezone.utc)
        update_and_populate_db(date_today)

        connected_user = self.request.user
        connected_profile = Profile.objects.get(user=connected_user)

        context = super(MonCompteListView, self).get_context_data(**kwargs)
        context['bad_user'] = connected_profile.bad_user
        context['nb_livres'] = connected_profile.nb_livres
        context['nb_autres'] = connected_profile.nb_autres
        context['date'] = datetime.now(timezone.utc)
        context['nb_retards'] = connected_profile.nb_retards
        context['statut'] = connected_profile.get_statut_display
        if connected_profile.date_bad_user != None:
            context['date_fin_bad_user'] = connected_profile.date_bad_user + timedelta(days=730)
        return context
