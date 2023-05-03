import os
import random

import ontor
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *

from rdflib import URIRef, BNode, Literal, Namespace, Graph, RDF
from rdflib.namespace import FOAF, DCTERMS, XSD
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


def home(request):
    return render(request, 'manage_ontology/home.html')


def index(request):
    return render(request, 'manage_ontology/index.html')


def add_elements(request):
    if request.method == 'POST':
        form_add = AddElements(request.POST)
        if form_add.is_valid():
            test_add_func(form_add.cleaned_data)
        else:
            return redirect('home')
    else:
        form_add = AddElements()
    return render(request, 'manage_ontology/index.html', {'form_add': form_add})


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
    return render(request, 'manage_ontology/index_1.html', {'form_del': form_del})


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
    return render(request, 'manage_ontology/index_2.html', {'form_del_one': form_del_one})


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

# def update_nodes_edges():
#     ontor3 = ontor.OntoEditor("CostumesRDF.owl", "CostumesRDF.owl")
#     magic_list_0 = [p.name for p in ontor3.get_elems()[0]]
#     magic_list_1 = [p.name for p in ontor3.get_elems()[1]]
#     magic_list_3 = [p.name for p in ontor3.get_elems()[3]]
#
#     nodes = magic_list_0 + magic_list_3
#     edges = magic_list_1
#
#     # Получаем данные об узлах
#     data_nodes = []
#     for i in range(len(nodes)):
#         data_nodes.append({
#             'id': i,
#             'label': nodes[i]
#         })
#
#     nodes_dict = {}
#     for d in data_nodes:
#         nodes_dict[d['label']] = d['id']
#
#     g = Graph()
#     g.parse("CostumesRDFfromapp.owl")
#
#     magic_dict = {}
#     data_edges = []
#
#     for node_name in nodes:
#         sub = URIRef('http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#' + node_name)
#         for s, p, o in g.triples((sub, None, None)):
#             if '#type' in p or '#NamedIndividual' in o or '#' not in p or '#' not in o:
#                 continue
#             from_node_name = s.split('#')[1]
#             to_node_name = o.split('#')[1]
#             edge_name = p.split('#')[1]
#             magic_dict = {'from': from_node_name, 'to': to_node_name, 'label': edge_name}
#             data_edges.append(magic_dict)
#
#     for d in data_edges:
#         for key, value in d.items():
#             if key == 'label':
#                 continue
#             d[key] = nodes_dict[value]
#
#     updated_dict = {'edges': data_edges, 'nodes': data_nodes}
#     return updated_dict

def my_view(request):
    # генерируем новые данные
    data = {'edges': [
                  {'from': 0, 'to': 7, 'label': 'subClassOf'},
                  {'from': 1, 'to': 7, 'label': 'subClassOf'},
                  {'from': 2, 'to': 3, 'label': 'subClassOf'},
                  {'from': 3, 'to': 7, 'label': 'subClassOf'},
                  {'from': 4, 'to': 3, 'label': 'subClassOf'},
                  {'from': 5, 'to': 6, 'label': 'subClassOf'},
                  {'from': 6, 'to': 11, 'label': 'subClassOf'},
                  {'from': 7, 'to': 11, 'label': 'subClassOf'},
                  {'from': 8, 'to': 7, 'label': 'subClassOf'},
                  {'from': 9, 'to': 7, 'label': 'subClassOf'},
                  {'from': 10, 'to': 9, 'label': 'subClassOf'},
                  {'from': 12, 'to': 13, 'label': 'subClassOf'},
                  {'from': 13, 'to': 17, 'label': 'subClassOf'},
                  {'from': 14, 'to': 11, 'label': 'subClassOf'},
                  {'from': 15, 'to': 7, 'label': 'subClassOf'},
                  {'from': 16, 'to': 13, 'label': 'subClassOf'},
                  {'from': 17, 'to': 6, 'label': 'subClassOf'},
                  {'from': 18, 'to': 5, 'label': 'subClassOf'},
                  {'from': 19, 'to': 3, 'label': 'subClassOf'},
                  {'from': 20, 'to': 7, 'label': 'subClassOf'},
                  {'from': 21, 'to': 5, 'label': 'subClassOf'},
                  {'from': 22, 'to': 5, 'label': 'subClassOf'},
                  {'from': 23, 'to': 24, 'label': 'subClassOf'},
                  {'from': 24, 'to': 17, 'label': 'subClassOf'},
                  {'from': 25, 'to': 24, 'label': 'subClassOf'},
                  {'from': 26, 'to': 9, 'label': 'subClassOf'},
                  {'from': 27, 'to': 13, 'label': 'subClassOf'},
                  {'from': 28, 'to': 29, 'label': 'has_a_part'},
                  {'from': 28, 'to': 30, 'label': 'has_a_part'},
                  {'from': 28, 'to': 31, 'label': 'has_a_part'},
                  {'from': 28, 'to': 32, 'label': 'has_a_part'},
                  {'from': 28, 'to': 29, 'label': 'has_a_shoulder_part'},
                  {'from': 28, 'to': 30, 'label': 'has_a_shoulder_part'},
                  {'from': 28, 'to': 32, 'label': 'has_a_shoulder_part'},
                  {'from': 28, 'to': 31, 'label': 'has_a_waist_part'},
                  {'from': 29, 'to': 28, 'label': 'is_a_part_of'},
                  {'from': 30, 'to': 28, 'label': 'is_a_part_of'},
                  {'from': 31, 'to': 28, 'label': 'is_a_part_of'}],
            'nodes': [
                  {'id': 0, 'label': 'decorative_elements'},
                  {'id': 1, 'label': 'product_length'},
                  {'id': 2, 'label': 'bodice'},
                  {'id': 3, 'label': 'shoulder_product'},
                  {'id': 4, 'label': 'sleeves'},
                  {'id': 5, 'label': 'fantasy_style'},
                  {'id': 6, 'label': 'STYLIZATION'},
                  {'id': 7, 'label': 'COMPONENTS'},
                  {'id': 8, 'label': 'product_cut'},
                  {'id': 9, 'label': 'waist_product'},
                  {'id': 10, 'label': 'skirt'},
                  {'id': 11, 'label': 'Сostume'},
                  {'id': 12, 'label': 'japanese_style'},
                  {'id': 13, 'label': 'asian_countries'},
                  {'id': 14, 'label': 'OUTFIT'},
                  {'id': 15, 'label': 'accessories'},
                  {'id': 16, 'label': 'chinese_style'},
                  {'id': 17, 'label': 'historical_reconstruction'},
                  {'id': 18, 'label': 'fairy_tales'},
                  {'id': 19, 'label': 'neckline'},
                  {'id': 20, 'label': 'fasteners'},
                  {'id': 21, 'label': 'computer_games'},
                  {'id': 22, 'label': 'epic_fantasy'},
                  {'id': 23, 'label': 'english_style'},
                  {'id': 24, 'label': 'european_countries'},
                  {'id': 25, 'label': 'scandinavian_style'},
                  {'id': 26, 'label': 'trousers'},
                  {'id': 27, 'label': 'korean_style'},
                  {'id': 28, 'label': 'dress1'},
                  {'id': 29, 'label': 'bodice1'},
                  {'id': 30, 'label': 'neckline1'},
                  {'id': 31, 'label': 'skirt1'},
                  {'id': 32, 'label': 'sleeves1'}]}

    # возвращаем данные в формате JSON
    return JsonResponse(data)


def visual(request):

    return render(request, 'manage_ontology/ontology_visualization.html')
