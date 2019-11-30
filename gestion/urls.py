from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ouvrage/', views.OuvrageListView.as_view(), name='ouvrage'),
    path('ouvrage/<int:pk>', views.OuvrageDetailView.as_view(), name='ouvrage-detail'),
    path('auteur/', views.AuteurListView.as_view(), name='auteur'),
    path('auteur/<int:pk>', views.AuteurDetailView.as_view(), name='auteur-detail'),
    path('genre/', views.GenreListView.as_view(), name='genre'),
    path('genre/<int:pk>', views.GenreDetailView.as_view(), name='genre-detail'),
    path('tarifs/', views.TarifListView.as_view(), name='tarif')
]

urlpatterns += [   
    path('mon_compte/', views.MonCompteListView.as_view(), name='mon_compte'),
]