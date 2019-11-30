from django.contrib import admin
from gestion.models import Ouvrage, Emprunt, Tarif, Auteur, Profile, Genre



@admin.register(Emprunt)
class EmpruntAdmin(admin.ModelAdmin):
    list_display = ('id', 'ouvrage', 'borrower', 'date_emprunt', 'retard', 'pénalité')
    list_filter = ('retard', 'date_emprunt')
    
    fieldsets = (
        (None, {
            'fields': ('ouvrage', 'borrower')
        }),
        ('Retour', {
            'fields': ('date_emprunt','retard')
        }),
    )


@admin.register(Ouvrage)
class OuvrageAdmin(admin.ModelAdmin):
	list_display = ('id', 'type', 'titre', 'année', 'auteur', 'nb_copies', 'autorisé')
	list_filter = ('type', 'nb_copies','autorisé', 'année')

	fieldsets = (
        (None, {
            'fields': ('type', 'titre', 'genre', 'année', 'auteur')
        }),
   	    ('Qualités', {
            'fields': ('autorisé', 'nb_copies')
        }),
    )


@admin.register(Auteur)
class AuteurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prénom', 'naissance', 'mort')
    list_filter = ('nom', 'naissance','mort')

    fieldsets = (
        (None, {
            'fields': ('nom', 'prénom', 'lien', 'img')
        }),
        ('Dates importantes', {
            'fields': ('naissance', 'mort')
        }),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nb_livres', 'nb_autres', 'nb_retards', 'premier_retard', 'bad_user')
    list_filter = ('user', 'bad_user')


@admin.register(Tarif)
class TarifAdmin(admin.ModelAdmin):
    list_display = ('statut','prix')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass



# Register the admin class with the associated model
#admin.site.register(Ouvrage, OuvrageAdmin)


# class ClientAdmin(admin.ModelAdmin):
# 	list_display = ('id_client', 'nom', 'prénom', 'statut', 'nb_livres', 'nb_autres', 'nb_retards','bad_user')

# # Register the admin class with the associated model
# admin.site.register(Client, ClientAdmin)






