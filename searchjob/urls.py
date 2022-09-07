from django.conf.urls.static import static
from django.urls import path

from .views import *


handler404 = custom_handler404
handler500 = custom_handler500


urlpatterns = [
    #main_view
    path('', MainView.as_view(), name='main'),
    path('vacancies/', VacanciesView.as_view(), name='vacancies'),
    path('vacancies/<int:pk>/', VacancyDetailView.as_view(), name='vacancy'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company'),
    path('vacancies/category/<str:code>/', CategoryView.as_view(), name='category'),
    path('vacancies/<int:id>/send/', send_view, name='send'),
    path('search/', SearchView.as_view(), name='search'),
    #account_view
    path('account/start/', CompanyStartView.as_view(), name='start'),
    path('account/create/', CompanyCreateView.as_view(), name='create_company'),
    path('account/edit/', CompanyEditView.as_view(), name='edit_company'),
    path('account/myvacancies/', VacanciesListView.as_view(), name='my_vacancies'),
    path('account/myvacancy/', VacancyCreateView.as_view(), name='create_vacancy'),
    path('account/editvacancy/<int:pk>/', VacancyEditView.as_view(), name='edit_vacancy'),
    path('account/delete/<int:pk>/', VacancyDeleteView.as_view(), name='delete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)