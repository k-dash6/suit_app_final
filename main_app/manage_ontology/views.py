import os
import random

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *

from rdflib import URIRef, BNode, Literal, Namespace, Graph, RDF
from rdflib.namespace import FOAF, DCTERMS, XSD
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


def home(request):
    return render(request, 'manage_ontology/home.html')

def info(request):
    return render(request, 'manage_ontology/info.html')

def my_profile(request):
    return render(request, 'manage_ontology/my_profile.html', {'name': 'Dasha', 'user': request.user})

def manage_ontology(request):
    return render(request, 'manage_ontology/manage_ontology.html')

def index(request):
    return render(request, 'manage_ontology/manage_ontology_add.html')


def add_elements(request):
    if request.method == 'POST':
        form_add = AddElements(request.POST)
        if form_add.is_valid():
            test_add_func(form_add.cleaned_data)
        else:
            return redirect('home')
    else:
        form_add = AddElements()
    return render(request, 'manage_ontology/manage_ontology_add.html', {'form_add': form_add})


def test_add_func(a):
    ontology = Graph()
    ontology.parse(os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
    object_name = a['object_name']
    predicat_name = a['predicat_name']
    subject_name = a['subject_name']
    s_uid = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + subject_name)
    p_uid = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + predicat_name)
    o_uid = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + object_name)
    ontology.add((s_uid, p_uid, o_uid))
    ontology.serialize(format="xml", destination=os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))


def delete_elements(request):
    if request.method == 'POST':
        form_del = DeleteElements(request.POST)
        if form_del.is_valid():
            print(form_del.cleaned_data)
            test_delete_func(form_del.cleaned_data)
        else:
            return redirect('home')
    else:
        form_del = DeleteElements()
    return render(request, 'manage_ontology/manage_ontology_del_all.html', {'form_del': form_del})


def test_delete_func(a):
    ontology = Graph()
    ontology.parse(os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
    element_name = a['element_name']
    e_name = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + element_name)
    if (e_name, None, None) in ontology:
        for s, p, o in ontology.triples((e_name, None, None)):
            ontology.remove((s, p, o))

    ontology.serialize(format="xml", destination=os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))


def delete_one_element(request):
    if request.method == 'POST':
        form_del_one = DeleteOneElement(request.POST)
        if form_del_one.is_valid():
            print(form_del_one.cleaned_data)
            test_delete_one_func(form_del_one.cleaned_data)
        else:
            return redirect('home')
    else:
        form_del_one = DeleteOneElement()
    return render(request, 'manage_ontology/manage_ontology_del_one.html', {'form_del_one': form_del_one})


def test_delete_one_func(a):
    ontology = Graph()
    ontology.parse(os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
    object_name = a['object_name']
    predicat_name = a['predicat_name']
    subject_name = a['subject_name']
    s_uid = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + subject_name)
    p_uid = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + predicat_name)
    o_uid = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + object_name)
    ontology.remove((s_uid, p_uid, o_uid))
    print('uhuuuuu')
    ontology.serialize(format="xml", destination=os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))


def return_random_element(request):
    sub_list = ''
    if request.method == 'POST':
        form_return_random = ReturnRandom(request.POST)
        if form_return_random.is_valid():
            sub_list = test_return_random(form_return_random.cleaned_data)
        else:
            return redirect('home')
    else:
        form_return_random = ReturnRandom()
    return render(request, 'manage_ontology/return_random.html',
                  {'form_return_random': form_return_random, 'subj': sub_list})


def test_return_random(a):
    ontology = Graph()
    ontology.parse(os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
    property_name = a['property']
    object_name = a['obj']
    property_uid = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + property_name)
    object_uid = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + object_name)
    sub_list = []
    for s, p, o in ontology.triples((None, property_uid, object_uid)):
        res = str(s).split('#')[1]
        sub_list.append(res)

    return random.choice(sub_list)

from django.http import JsonResponse


def my_view(request):
    # генерируем новые данные
    data = {'edges': [{'from': 0, 'to': 3, 'label': 'subClassOf'},
  {'from': 3, 'to': 80, 'label': 'subClassOf'},
  {'from': 7, 'to': 240, 'label': 'subClassOf'},
  {'from': 8, 'to': 7, 'label': 'subClassOf'},
  {'from': 9, 'to': 225, 'label': 'subClassOf'},
  {'from': 9, 'to': 260, 'label': 'subClassOf'},
  {'from': 11, 'to': 7, 'label': 'subClassOf'},
  {'from': 11, 'to': 241, 'label': 'subClassOf'},
  {'from': 12, 'to': 225, 'label': 'subClassOf'},
  {'from': 12, 'to': 260, 'label': 'subClassOf'},
  {'from': 14, 'to': 161, 'label': 'subClassOf'},
  {'from': 15, 'to': 225, 'label': 'subClassOf'},
  {'from': 15, 'to': 260, 'label': 'subClassOf'},
  {'from': 22, 'to': 192, 'label': 'subClassOf'},
  {'from': 23, 'to': 108, 'label': 'subClassOf'},
  {'from': 29, 'to': 7, 'label': 'subClassOf'},
  {'from': 29, 'to': 241, 'label': 'subClassOf'},
  {'from': 30, 'to': 172, 'label': 'subClassOf'},
  {'from': 31, 'to': 225, 'label': 'subClassOf'},
  {'from': 31, 'to': 260, 'label': 'subClassOf'},
  {'from': 32, 'to': 105, 'label': 'subClassOf'},
  {'from': 34, 'to': 183, 'label': 'subClassOf'},
  {'from': 35, 'to': 23, 'label': 'subClassOf'},
  {'from': 37, 'to': 3, 'label': 'subClassOf'},
  {'from': 38, 'to': 82, 'label': 'subClassOf'},
  {'from': 39, 'to': 105, 'label': 'subClassOf'},
  {'from': 44, 'to': 170, 'label': 'has_bodice'},
  {'from': 44, 'to': 166, 'label': 'has_neckline'},
  {'from': 44, 'to': 1, 'label': 'has_skirt'},
  {'from': 44, 'to': 55, 'label': 'has_sleeves'},
  {'from': 47, 'to': 52, 'label': 'subClassOf'},
  {'from': 48, 'to': 52, 'label': 'subClassOf'},
  {'from': 51, 'to': 48, 'label': 'subClassOf'},
  {'from': 51, 'to': 222, 'label': 'subClassOf'},
  {'from': 52, 'to': 80, 'label': 'subClassOf'},
  {'from': 53, 'to': 183, 'label': 'subClassOf'},
  {'from': 56, 'to': 7, 'label': 'subClassOf'},
  {'from': 56, 'to': 241, 'label': 'subClassOf'},
  {'from': 57, 'to': 152, 'label': 'subClassOf'},
  {'from': 58, 'to': 270, 'label': 'subClassOf'},
  {'from': 59, 'to': 192, 'label': 'subClassOf'},
  {'from': 60, 'to': 48, 'label': 'subClassOf'},
  {'from': 60, 'to': 222, 'label': 'subClassOf'},
  {'from': 61, 'to': 218, 'label': 'subPropertyOf'},
  {'from': 61, 'to': 179, 'label': 'range'},
  {'from': 63, 'to': 213, 'label': 'subClassOf'},
  {'from': 63, 'to': 59, 'label': 'subClassOf'},
  {'from': 66, 'to': 172, 'label': 'subClassOf'},
  {'from': 68, 'to': 218, 'label': 'subPropertyOf'},
  {'from': 68, 'to': 171, 'label': 'range'},
  {'from': 70, 'to': 161, 'label': 'subClassOf'},
  {'from': 73, 'to': 192, 'label': 'subClassOf'},
  {'from': 75, 'to': 7, 'label': 'subClassOf'},
  {'from': 75, 'to': 241, 'label': 'subClassOf'},
  {'from': 81, 'to': 225, 'label': 'subClassOf'},
  {'from': 81, 'to': 260, 'label': 'subClassOf'},
  {'from': 82, 'to': 179, 'label': 'subClassOf'},
  {'from': 83, 'to': 3, 'label': 'subClassOf'},
  {'from': 86, 'to': 213, 'label': 'subClassOf'},
  {'from': 86, 'to': 59, 'label': 'subClassOf'},
  {'from': 87, 'to': 97, 'label': 'subClassOf'},
  {'from': 91, 'to': 52, 'label': 'subClassOf'},
  {'from': 92, 'to': 218, 'label': 'subPropertyOf'},
  {'from': 92, 'to': 186, 'label': 'range'},
  {'from': 93, 'to': 48, 'label': 'subClassOf'},
  {'from': 93, 'to': 222, 'label': 'subClassOf'},
  {'from': 94, 'to': 82, 'label': 'subClassOf'},
  {'from': 96, 'to': 105, 'label': 'subClassOf'},
  {'from': 97, 'to': 52, 'label': 'subClassOf'},
  {'from': 98, 'to': 253, 'label': 'subPropertyOf'},
  {'from': 98, 'to': 52, 'label': 'domain'},
  {'from': 98, 'to': 52, 'label': 'range'},
  {'from': 101, 'to': 80, 'label': 'subClassOf'},
  {'from': 102, 'to': 161, 'label': 'subClassOf'},
  {'from': 103, 'to': 276, 'label': 'has_skirt'},
  {'from': 104, 'to': 238, 'label': 'subClassOf'},
  {'from': 105, 'to': 179, 'label': 'subClassOf'},
  {'from': 107, 'to': 225, 'label': 'subClassOf'},
  {'from': 107, 'to': 260, 'label': 'subClassOf'},
  {'from': 108, 'to': 80, 'label': 'subClassOf'},
  {'from': 117, 'to': 3, 'label': 'subClassOf'},
  {'from': 118, 'to': 185, 'label': 'subClassOf'},
  {'from': 121, 'to': 22, 'label': 'subClassOf'},
  {'from': 121, 'to': 91, 'label': 'subClassOf'},
  {'from': 122, 'to': 47, 'label': 'subClassOf'},
  {'from': 122, 'to': 73, 'label': 'subClassOf'},
  {'from': 123, 'to': 80, 'label': 'subClassOf'},
  {'from': 125, 'to': 47, 'label': 'subClassOf'},
  {'from': 125, 'to': 73, 'label': 'subClassOf'},
  {'from': 126, 'to': 295, 'label': 'subPropertyOf'},
  {'from': 127, 'to': 185, 'label': 'subClassOf'},
  {'from': 129, 'to': 227, 'label': 'subClassOf'},
  {'from': 134, 'to': 218, 'label': 'subPropertyOf'},
  {'from': 134, 'to': 52, 'label': 'domain'},
  {'from': 134, 'to': 240, 'label': 'range'},
  {'from': 137, 'to': 68, 'label': 'subPropertyOf'},
  {'from': 139, 'to': 170, 'label': 'has_bodice'},
  {'from': 139, 'to': 190, 'label': 'has_neckline'},
  {'from': 140, 'to': 218, 'label': 'subPropertyOf'},
  {'from': 140, 'to': 192, 'label': 'range'},
  {'from': 142, 'to': 238, 'label': 'subClassOf'},
  {'from': 144, 'to': 161, 'label': 'subClassOf'},
  {'from': 148, 'to': 225, 'label': 'subClassOf'},
  {'from': 148, 'to': 260, 'label': 'subClassOf'},
  {'from': 152, 'to': 123, 'label': 'subClassOf'},
  {'from': 154, 'to': 198, 'label': 'domain'},
  {'from': 161, 'to': 179, 'label': 'subClassOf'},
  {'from': 163, 'to': 172, 'label': 'subClassOf'},
  {'from': 171, 'to': 3, 'label': 'subClassOf'},
  {'from': 172, 'to': 108, 'label': 'subClassOf'},
  {'from': 174, 'to': 225, 'label': 'subClassOf'},
  {'from': 174, 'to': 260, 'label': 'subClassOf'},
  {'from': 178, 'to': 48, 'label': 'subClassOf'},
  {'from': 178, 'to': 222, 'label': 'subClassOf'},
  {'from': 179, 'to': 101, 'label': 'subClassOf'},
  {'from': 181, 'to': 253, 'label': 'subPropertyOf'},
  {'from': 181, 'to': 80, 'label': 'domain'},
  {'from': 181, 'to': 80, 'label': 'range'},
  {'from': 182, 'to': 253, 'label': 'subPropertyOf'},
  {'from': 182, 'to': 52, 'label': 'domain'},
  {'from': 182, 'to': 108, 'label': 'range'},
  {'from': 183, 'to': 240, 'label': 'subClassOf'},
  {'from': 185, 'to': 52, 'label': 'subClassOf'},
  {'from': 186, 'to': 123, 'label': 'subClassOf'},
  {'from': 189, 'to': 48, 'label': 'subClassOf'},
  {'from': 189, 'to': 222, 'label': 'subClassOf'},
  {'from': 191, 'to': 238, 'label': 'subClassOf'},
  {'from': 192, 'to': 101, 'label': 'subClassOf'},
  {'from': 197, 'to': 35, 'label': 'subClassOf'},
  {'from': 198, 'to': 3, 'label': 'subClassOf'},
  {'from': 200, 'to': 22, 'label': 'subClassOf'},
  {'from': 200, 'to': 91, 'label': 'subClassOf'},
  {'from': 202, 'to': 3, 'label': 'subClassOf'},
  {'from': 206, 'to': 47, 'label': 'subClassOf'},
  {'from': 206, 'to': 73, 'label': 'subClassOf'},
  {'from': 209, 'to': 48, 'label': 'subClassOf'},
  {'from': 209, 'to': 222, 'label': 'subClassOf'},
  {'from': 210, 'to': 35, 'label': 'subClassOf'},
  {'from': 211, 'to': 238, 'label': 'subClassOf'},
  {'from': 212, 'to': 7, 'label': 'subClassOf'},
  {'from': 213, 'to': 52, 'label': 'subClassOf'},
  {'from': 214, 'to': 227, 'label': 'subClassOf'},
  {'from': 215, 'to': 183, 'label': 'subClassOf'},
  {'from': 217, 'to': 68, 'label': 'subPropertyOf'},
  {'from': 218, 'to': 253, 'label': 'subPropertyOf'},
  {'from': 218, 'to': 98, 'label': 'inverseOf'},
  {'from': 218, 'to': 52, 'label': 'domain'},
  {'from': 218, 'to': 52, 'label': 'range'},
  {'from': 220, 'to': 152, 'label': 'subClassOf'},
  {'from': 221, 'to': 3, 'label': 'subClassOf'},
  {'from': 222, 'to': 192, 'label': 'subClassOf'},
  {'from': 225, 'to': 52, 'label': 'subClassOf'},
  {'from': 227, 'to': 23, 'label': 'subClassOf'},
  {'from': 232, 'to': 7, 'label': 'subClassOf'},
  {'from': 233, 'to': 7, 'label': 'subClassOf'},
  {'from': 233, 'to': 241, 'label': 'subClassOf'},
  {'from': 237, 'to': 111, 'label': 'has_bodice'},
  {'from': 237, 'to': 219, 'label': 'has_trousers'},
  {'from': 238, 'to': 240, 'label': 'subClassOf'},
  {'from': 240, 'to': 101, 'label': 'subClassOf'},
  {'from': 241, 'to': 240, 'label': 'subClassOf'},
  {'from': 242, 'to': 82, 'label': 'subClassOf'},
  {'from': 243, 'to': 52, 'label': 'domain'},
  {'from': 249, 'to': 270, 'label': 'subClassOf'},
  {'from': 250, 'to': 161, 'label': 'subClassOf'},
  {'from': 251, 'to': 225, 'label': 'subClassOf'},
  {'from': 251, 'to': 260, 'label': 'subClassOf'},
  {'from': 256, 'to': 48, 'label': 'subClassOf'},
  {'from': 256, 'to': 222, 'label': 'subClassOf'},
  {'from': 257, 'to': 218, 'label': 'subPropertyOf'},
  {'from': 257, 'to': 97, 'label': 'range'},
  {'from': 260, 'to': 192, 'label': 'subClassOf'},
  {'from': 261, 'to': 161, 'label': 'subClassOf'},
  {'from': 263, 'to': 238, 'label': 'subClassOf'},
  {'from': 264, 'to': 270, 'label': 'subClassOf'},
  {'from': 267, 'to': 238, 'label': 'subClassOf'},
  {'from': 270, 'to': 179, 'label': 'subClassOf'},
  {'from': 274, 'to': 82, 'label': 'subClassOf'},
  {'from': 277, 'to': 82, 'label': 'subClassOf'},
  {'from': 278, 'to': 7, 'label': 'subClassOf'},
  {'from': 278, 'to': 241, 'label': 'subClassOf'},
  {'from': 280, 'to': 227, 'label': 'subClassOf'},
  {'from': 287, 'to': 218, 'label': 'subPropertyOf'},
  {'from': 287, 'to': 185, 'label': 'range'},
  {'from': 288, 'to': 48, 'label': 'subClassOf'},
  {'from': 288, 'to': 222, 'label': 'subClassOf'},
  {'from': 291, 'to': 238, 'label': 'subClassOf'},
  {'from': 292, 'to': 161, 'label': 'subClassOf'},
  {'from': 295, 'to': 218, 'label': 'subPropertyOf'},
  {'from': 295, 'to': 198, 'label': 'range'},
  {'from': 297, 'to': 68, 'label': 'subPropertyOf'},
  {'from': 300, 'to': 225, 'label': 'subClassOf'},
  {'from': 300, 'to': 260, 'label': 'subClassOf'},
  {'from': 308, 'to': 167, 'label': 'has_bodice'},
  {'from': 308, 'to': 116, 'label': 'has_fasteners'},
  {'from': 308, 'to': 62, 'label': 'has_neckline'},
  {'from': 308, 'to': 294, 'label': 'has_sleeves'},
  {'from': 312, 'to': 213, 'label': 'subClassOf'},
  {'from': 312, 'to': 59, 'label': 'subClassOf'},
  {'from': 313, 'to': 295, 'label': 'subPropertyOf'},
  {'from': 316, 'to': 47, 'label': 'subClassOf'},
  {'from': 316, 'to': 73, 'label': 'subClassOf'},
  {'from': 317, 'to': 185, 'label': 'subClassOf'}],
 'nodes': [{'id': 0, 'label': 'layer_1'},
  {'id': 1, 'label': 'skirt_0010'},
  {'id': 2, 'label': 'skirt_0015'},
  {'id': 3, 'label': 'OUTFIT'},
  {'id': 4, 'label': 'neckline_0017'},
  {'id': 5, 'label': 'bodice_0036'},
  {'id': 6, 'label': 'bodice_0017'},
  {'id': 7, 'label': 'shoulder_product_length'},
  {'id': 8, 'label': 'shoulder_product_length_waist_high'},
  {'id': 9, 'label': 'neckline_open_cut'},
  {'id': 10, 'label': 'Class'},
  {'id': 11, 'label': 'shoulder_product_length_knee_high'},
  {'id': 12, 'label': 'neckline_V_figurative_cut'},
  {'id': 13, 'label': 'skirt_0019'},
  {'id': 14, 'label': 'sleeves_fitting_wide_strap'},
  {'id': 15, 'label': 'neckline_straight_cut'},
  {'id': 16, 'label': 'sleeves_0034'},
  {'id': 17, 'label': 'sleeves_0003'},
  {'id': 18, 'label': 'bodice_0008'},
  {'id': 19, 'label': 'bodice_0027'},
  {'id': 20, 'label': 'neckline_0004'},
  {'id': 21, 'label': 'skirt_0004'},
  {'id': 22, 'label': 'sleeve_cut'},
  {'id': 23, 'label': 'historical_reconstruction'},
  {'id': 24, 'label': 'skirt_0002'},
  {'id': 25, 'label': 'trousers_0001'},
  {'id': 26, 'label': 'sleeves_0024'},
  {'id': 27, 'label': 'sleeves_0032'},
  {'id': 28, 'label': 'neckline_0007'},
  {'id': 29, 'label': 'shoulder_product_length_ancle'},
  {'id': 30, 'label': 'epic_fantasy'},
  {'id': 31, 'label': 'neckline_under_throat_cut'},
  {'id': 32, 'label': 'bodice_fitting_fit'},
  {'id': 33, 'label': 'bodice_0041'},
  {'id': 34, 'label': 'waist_level_low'},
  {'id': 35, 'label': 'european_countries'},
  {'id': 36, 'label': 'trousers_0000'},
  {'id': 37, 'label': 'layer_5'},
  {'id': 38, 'label': 'skirt_fitting_A_line'},
  {'id': 39, 'label': 'bodice_fitting_loose'},
  {'id': 40, 'label': 'skirt_0000'},
  {'id': 41, 'label': 'bodice_0022'},
  {'id': 42, 'label': 'bodice_0007'},
  {'id': 43, 'label': 'bodice_0013'},
  {'id': 44, 'label': 'outfit_000000'},
  {'id': 45, 'label': 'FunctionalProperty'},
  {'id': 46, 'label': 'sleeves_0014'},
  {'id': 47, 'label': 'trousers'},
  {'id': 48, 'label': 'bodice'},
  {'id': 49, 'label': 'sleeves_0008'},
  {'id': 50, 'label': 'bodice_0028'},
  {'id': 51, 'label': 'bodice_drapery_cut'},
  {'id': 52, 'label': 'COMPONENTS'},
  {'id': 53, 'label': 'waist_level_normal'},
  {'id': 54, 'label': 'sleeves_0019'},
  {'id': 55, 'label': 'sleeves_0005'},
  {'id': 56, 'label': 'shoulder_product_length_mid_shin'},
  {'id': 57, 'label': 'fabric_dense'},
  {'id': 58, 'label': 'trousers_fitting_skinny'},
  {'id': 59, 'label': 'skirt_cut'},
  {'id': 60, 'label': 'corset_baroque__cut'},
  {'id': 61, 'label': 'has_product_fit'},
  {'id': 62, 'label': 'neckline_0001'},
  {'id': 63, 'label': 'skirt_wedges_cut'},
  {'id': 64, 'label': 'trousers_0020'},
  {'id': 65, 'label': 'trousers_0017'},
  {'id': 66, 'label': 'fairy_tales'},
  {'id': 67, 'label': 'sleeves_0031'},
  {'id': 68, 'label': 'has_a_shoulder_part'},
  {'id': 69, 'label': 'sleeves_0027'},
  {'id': 70, 'label': 'sleeves_fitting_X_X_wide'},
  {'id': 71, 'label': 'neckline_0015'},
  {'id': 72, 'label': 'sleeves_0012'},
  {'id': 73, 'label': 'trousers_cut'},
  {'id': 74, 'label': 'sleeves_0025'},
  {'id': 75, 'label': 'shoulder_product_length_to_floor'},
  {'id': 76, 'label': 'bodice_0030'},
  {'id': 77, 'label': 'skirt_0007'},
  {'id': 78, 'label': 'bodice_0006'},
  {'id': 79, 'label': 'trousers_0019'},
  {'id': 80, 'label': 'Сostume'},
  {'id': 81, 'label': 'neckline_boat_cut'},
  {'id': 82, 'label': 'skirt_fitting'},
  {'id': 83, 'label': 'layer_4'},
  {'id': 84, 'label': 'neckline_0014'},
  {'id': 85, 'label': 'trousers_0016'},
  {'id': 86, 'label': 'skirt_drapery_cut'},
  {'id': 87, 'label': 'decorative_elements_cuffs'},
  {'id': 88, 'label': 'trousers_0004'},
  {'id': 89, 'label': 'sleeves_0017'},
  {'id': 90, 'label': 'skirt_0023'},
  {'id': 91, 'label': 'sleeves'},
  {'id': 92, 'label': 'has_accessories'},
  {'id': 93, 'label': 'corsage_vest_cut'},
  {'id': 94, 'label': 'skirt_fitting_half_sun'},
  {'id': 95, 'label': 'trousers_0014'},
  {'id': 96, 'label': 'bodice_fitting_tight'},
  {'id': 97, 'label': 'decorative_elements'},
  {'id': 98, 'label': 'is_a_part_of'},
  {'id': 99, 'label': 'neckline_0012'},
  {'id': 100, 'label': 'bodice_0009'},
  {'id': 101, 'label': 'srax'},
  {'id': 102, 'label': 'sleeves_fitting_narrow'},
  {'id': 103, 'label': 'outfit_000003'},
  {'id': 104, 'label': 'sleeves_length_elbow_high'},
  {'id': 105, 'label': 'bodice_fitting'},
  {'id': 106, 'label': 'skirt_0021'},
  {'id': 107, 'label': 'neckline_high_collar_cut'},
  {'id': 108, 'label': 'STYLIZATION'},
  {'id': 109, 'label': 'sleeves_0035'},
  {'id': 110, 'label': 'sleeves_0009'},
  {'id': 111, 'label': 'bodice_0015'},
  {'id': 112, 'label': 'skirt_0030'},
  {'id': 113, 'label': 'trousers_0012'},
  {'id': 114, 'label': 'skirt_0020'},
  {'id': 115, 'label': 'TransitiveProperty'},
  {'id': 116, 'label': 'fasteners_zipper_0000'},
  {'id': 117, 'label': 'layer_3'},
  {'id': 118, 'label': 'fasteners_zipper'},
  {'id': 119, 'label': 'bodice_0012'},
  {'id': 120, 'label': 'skirt_0009'},
  {'id': 121, 'label': 'sleeve_flashlight_cut'},
  {'id': 122, 'label': 'trousers_cargo_cut'},
  {'id': 123, 'label': 'additional_components'},
  {'id': 124, 'label': 'sleeves_0039'},
  {'id': 125, 'label': 'trousers_joggers_cut'},
  {'id': 126, 'label': 'has_skirt'},
  {'id': 127, 'label': 'fasteners_buttons'},
  {'id': 128, 'label': 'sleeves_0022'},
  {'id': 129, 'label': 'chinese_style'},
  {'id': 130, 'label': 'bodice_0032'},
  {'id': 131, 'label': 'skirt_0016'},
  {'id': 132, 'label': 'trousers_0011'},
  {'id': 133, 'label': 'sleeves_0029'},
  {'id': 134, 'label': 'has_product_length'},
  {'id': 135, 'label': 'bodice_0024'},
  {'id': 136, 'label': 'bodice_0025'},
  {'id': 137, 'label': 'has_sleeves'},
  {'id': 138, 'label': 'bodice_0034'},
  {'id': 139, 'label': 'outfit_000002'},
  {'id': 140, 'label': 'has_product_cut'},
  {'id': 141, 'label': 'neckline_0016'},
  {'id': 142, 'label': 'sleeves_length_three_quarters'},
  {'id': 143, 'label': 'bodice_0050'},
  {'id': 144, 'label': 'sleeves_fitting_X_wide'},
  {'id': 145, 'label': 'skirt_0006'},
  {'id': 146, 'label': 'skirt_0028'},
  {'id': 147, 'label': 'skirt_0012'},
  {'id': 148, 'label': 'neckline_round_cut'},
  {'id': 149, 'label': 'neckline_0005'},
  {'id': 150, 'label': 'sleeves_0006'},
  {'id': 151, 'label': 'trousers_0013'},
  {'id': 152, 'label': 'fabrics'},
  {'id': 153, 'label': 'neckline_0002'},
  {'id': 154, 'label': 'has_waist_level'},
  {'id': 155, 'label': 'bodice_0049'},
  {'id': 156, 'label': 'sleeves_0007'},
  {'id': 157, 'label': 'neckline_0011'},
  {'id': 158, 'label': 'trousers_0003'},
  {'id': 159, 'label': 'bodice_0020'},
  {'id': 160, 'label': 'sleeves_0021'},
  {'id': 161, 'label': 'sleeves_fitting'},
  {'id': 162, 'label': 'skirt_0026'},
  {'id': 163, 'label': 'computer_games'},
  {'id': 164, 'label': 'sleeves_0002'},
  {'id': 165, 'label': 'sleeves_0016'},
  {'id': 166, 'label': 'neckline_0003'},
  {'id': 167, 'label': 'bodice_0010'},
  {'id': 168, 'label': 'neckline_0006'},
  {'id': 169, 'label': 'bodice_0031'},
  {'id': 170, 'label': 'bodice_0000'},
  {'id': 171, 'label': 'shoulder_product'},
  {'id': 172, 'label': 'fantasy_style'},
  {'id': 173, 'label': 'bodice_0039'},
  {'id': 174, 'label': 'neckline_wrapped_welt_cut'},
  {'id': 175, 'label': 'neckline_0008'},
  {'id': 176, 'label': 'sleeves_0030'},
  {'id': 177, 'label': 'bodice_0029'},
  {'id': 178, 'label': 'corsage_flat_cut'},
  {'id': 179, 'label': 'product_fitting'},
  {'id': 180, 'label': 'neckline_0019'},
  {'id': 181, 'label': 'is_a_subclass_of'},
  {'id': 182, 'label': 'has_a_style'},
  {'id': 183, 'label': 'waist_level'},
  {'id': 184, 'label': 'neckline_0020'},
  {'id': 185, 'label': 'fasteners'},
  {'id': 186, 'label': 'accessories'},
  {'id': 187, 'label': 'bodice_0037'},
  {'id': 188, 'label': 'sleeves_0038'},
  {'id': 189, 'label': 'corset_classic_cut'},
  {'id': 190, 'label': 'neckline_0000'},
  {'id': 191, 'label': 'sleeves_length_wrist'},
  {'id': 192, 'label': 'product_cut'},
  {'id': 193, 'label': 'bodice_0045'},
  {'id': 194, 'label': 'trousers_0018'},
  {'id': 195, 'label': 'bodice_0014'},
  {'id': 196, 'label': 'skirt_0008'},
  {'id': 197, 'label': 'english_style'},
  {'id': 198, 'label': 'waist_product'},
  {'id': 199, 'label': 'sleeves_0015'},
  {'id': 200, 'label': 'sleeve_flounce_cut'},
  {'id': 201, 'label': 'bodice_0044'},
  {'id': 202, 'label': 'full_product'},
  {'id': 203, 'label': 'sleeves_0040'},
  {'id': 204, 'label': 'sleeves_0010'},
  {'id': 205, 'label': 'trousers_0007'},
  {'id': 206, 'label': 'trousers_bloomers_cut'},
  {'id': 207, 'label': 'skirt_0003'},
  {'id': 208, 'label': 'bodice_0011'},
  {'id': 209, 'label': 'bodice_wrapped_cut'},
  {'id': 210, 'label': 'scandinavian_style'},
  {'id': 211, 'label': 'sleeves_length_strap'},
  {'id': 212, 'label': 'shoulder_product_length_waist'},
  {'id': 213, 'label': 'skirt'},
  {'id': 214, 'label': 'japanese_style'},
  {'id': 215, 'label': 'waist_level_high'},
  {'id': 216, 'label': 'sleeves_0004'},
  {'id': 217, 'label': 'has_bodice'},
  {'id': 218, 'label': 'has_a_part'},
  {'id': 219, 'label': 'trousers_0015'},
  {'id': 220, 'label': 'fabric_thin'},
  {'id': 221, 'label': 'layer_2'},
  {'id': 222, 'label': 'bodice_cut'},
  {'id': 223, 'label': 'trousers_0009'},
  {'id': 224, 'label': 'sleeves_0028'},
  {'id': 225, 'label': 'neckline'},
  {'id': 226, 'label': 'bodice_0001'},
  {'id': 227, 'label': 'asian_countries'},
  {'id': 228, 'label': 'sleeves_0033'},
  {'id': 229, 'label': 'neckline_0010'},
  {'id': 230, 'label': 'bodice_0043'},
  {'id': 231, 'label': 'neckline_0013'},
  {'id': 232, 'label': 'shoulder_product_length_hip'},
  {'id': 233, 'label': 'shoulder_product_length_knee'},
  {'id': 234, 'label': 'sleeves_0026'},
  {'id': 235, 'label': 'sleeves_0023'},
  {'id': 236, 'label': 'sleeves_0018'},
  {'id': 237, 'label': 'outfit_000001'},
  {'id': 238, 'label': 'sleeves_length'},
  {'id': 239, 'label': 'bodice_0016'},
  {'id': 240, 'label': 'product_length'},
  {'id': 241, 'label': 'waist_product_length'},
  {'id': 242, 'label': 'skirt_fitting_tight'},
  {'id': 243, 'label': 'has_product_fitting'},
  {'id': 244, 'label': 'skirt_0027'},
  {'id': 245, 'label': 'neckline_0018'},
  {'id': 246, 'label': 'sleeves_0037'},
  {'id': 247, 'label': 'trousers_0005'},
  {'id': 248, 'label': 'bodice_0023'},
  {'id': 249, 'label': 'trousers_fitting_wide'},
  {'id': 250, 'label': 'sleeves_fitting_straight'},
  {'id': 251, 'label': 'neckline_square_cut'},
  {'id': 252, 'label': 'skirt_0017'},
  {'id': 253, 'label': 'related'},
  {'id': 254, 'label': 'bodice_0026'},
  {'id': 255, 'label': 'bodice_0005'},
  {'id': 256, 'label': 'bodice_embossed_tucks_cut'},
  {'id': 257, 'label': 'has_decorative_elements'},
  {'id': 258, 'label': 'sleeves_0020'},
  {'id': 259, 'label': 'sleeves_0001'},
  {'id': 260, 'label': 'neckline_cut'},
  {'id': 261, 'label': 'sleeves_fitting_wide'},
  {'id': 262, 'label': 'bodice_0002'},
  {'id': 263, 'label': 'sleeves_length_seven_eights'},
  {'id': 264, 'label': 'trousers_fitting_straight'},
  {'id': 265, 'label': 'skirt_0013'},
  {'id': 266, 'label': 'sleeves_0013'},
  {'id': 267, 'label': 'sleeves_length_elbow'},
  {'id': 268, 'label': 'bodice_0004'},
  {'id': 269, 'label': 'sleeves_0036'},
  {'id': 270, 'label': 'trousers_fitting'},
  {'id': 271, 'label': 'bodice_0033'},
  {'id': 272, 'label': 'NamedIndividual'},
  {'id': 273, 'label': 'outfit_000005'},
  {'id': 274, 'label': 'skirt_fitting_straight'},
  {'id': 275, 'label': 'skirt_0001'},
  {'id': 276, 'label': 'skirt_0024'},
  {'id': 277, 'label': 'skirt_fitting_sun'},
  {'id': 278, 'label': 'shoulder_product_length_mid_thigh'},
  {'id': 279, 'label': 'bodice_0019'},
  {'id': 280, 'label': 'korean_style'},
  {'id': 281, 'label': 'bodice_0035'},
  {'id': 282, 'label': 'trousers_0006'},
  {'id': 283, 'label': 'bodice_0046'},
  {'id': 284, 'label': 'bodice_0038'},
  {'id': 285, 'label': 'skirt_0005'},
  {'id': 286, 'label': 'neckline_0009'},
  {'id': 287, 'label': 'has_fasteners'},
  {'id': 288, 'label': 'bodice_classic_cut'},
  {'id': 289, 'label': 'bodice_0040'},
  {'id': 290, 'label': 'skirt_0022'},
  {'id': 291, 'label': 'sleeves_length_long'},
  {'id': 292, 'label': 'sleeves_fitting_narrow_strap'},
  {'id': 293, 'label': 'trousers_0008'},
  {'id': 294, 'label': 'sleeves_0000'},
  {'id': 295, 'label': 'has_a_waist_part'},
  {'id': 296, 'label': 'bodice_0042'},
  {'id': 297, 'label': 'has_neckline'},
  {'id': 298, 'label': 'ObjectProperty'},
  {'id': 299, 'label': 'bodice_0021'},
  {'id': 300, 'label': 'neckline_heart_cut'},
  {'id': 301, 'label': 'skirt_0014'},
  {'id': 302, 'label': 'DatatypeProperty'},
  {'id': 303, 'label': 'bodice_0003'},
  {'id': 304, 'label': 'skirt_0029'},
  {'id': 305, 'label': 'trousers_0010'},
  {'id': 306, 'label': 'skirt_0025'},
  {'id': 307, 'label': 'sleeves_0011'},
  {'id': 308, 'label': 'outfit_000004'},
  {'id': 309, 'label': 'bodice_0047'},
  {'id': 310, 'label': 'trousers_0002'},
  {'id': 311, 'label': 'bodice_0018'},
  {'id': 312, 'label': 'skirt_wrapped_cut'},
  {'id': 313, 'label': 'has_trousers'},
  {'id': 314, 'label': 'bodice_0048'},
  {'id': 315, 'label': 'skirt_0011'},
  {'id': 316, 'label': 'trousers_classic_cut'},
  {'id': 317, 'label': 'fasteners_lacing'},
  {'id': 318, 'label': 'skirt_0018'}]}
    # возвращаем данные в формате JSON
    return JsonResponse(data)


def visual(request):

    return render(request, 'manage_ontology/ontology_visualization.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'manage_ontology/register.html', {'form': form})


from django.contrib import messages


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    return render(request, 'manage_ontology/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return render(request, 'manage_ontology/logout.html')


from googletrans import Translator


def get_stylizations():
    stylizations = []
    g = Graph()
    g.parse(os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
    for ind, (sub, pred, obj) in enumerate(g):
        if 'subClassOf' in pred and 'STYLIZATION' in obj:
            stylization = sub.split('#')[1]
            stylization_to_translate = stylization.replace('_', ' ')
            translator = Translator()
            stylization_translated = translator.translate(stylization_to_translate, dest='ru')
            mini = (stylization, stylization_translated.text)
            stylizations.append(mini)
    return stylizations


def choose_stylization(request):
    if request.method == 'POST':
        form = ChooseStylization(request.POST or None)
        if form.is_valid():
            # Обработка действий при валидной форме
            stylizations = form.cleaned_data['stylizations']
            # Дополнительные действия
    else:
        form = ChooseStylization(request.POST or None)

    return render(request, 'manage_ontology/choose_stylization.html', {'form': form})
