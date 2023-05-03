from django.urls import path

from .views import *
from django.urls import path

urlpatterns = [
    path('', home, name='home'),
    path('manage-add/', add_elements, name='manage_ontology_add'),
    path('manage-random/', return_random_element, name='manage_return_random'),
    path('manage-del_all/', delete_elements, name='manage_ontology_del_all'),
    path('manage-del_one/', delete_one_element, name='manage_ontology_del_one'),
    path('ontology_visualization/', visual, name='ontology_visualization'),
    path('my_view/', my_view, name='my_view'),
]
