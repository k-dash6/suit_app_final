import os
import random

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *

from rdflib import URIRef, BNode, Literal, Namespace, Graph, RDF
from rdflib.namespace import FOAF, DCTERMS, XSD

from ..main_app.settings import BASE_DIR


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
    ontology.parse("C:/Users/kdash/suit_app/CostumesRDF.owl")
    object_name = a['object_name']
    predicat_name = a['predicat_name']
    subject_name = a['subject_name']
    s_uid = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + subject_name)
    p_uid = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + predicat_name)
    o_uid = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + object_name)
    ontology.add((s_uid, p_uid, o_uid))
    ontology.serialize(format="xml", destination="C:/Users/kdash/suit_app/CostumesRDF.owl")


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
    ontology.parse("C:/Users/kdash/suit_app/CostumesRDF.owl")
    element_name = a['element_name']
    e_name = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + element_name)
    if (e_name, None, None) in ontology:
        for s, p, o in ontology.triples((e_name, None, None)):
            ontology.remove((s, p, o))

    ontology.serialize(format="xml", destination="C:/Users/kdash/suit_app/CostumesRDF.owl")


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
    ontology.parse("C:/Users/kdash/suit_app/CostumesRDF.owl")
    object_name = a['object_name']
    predicat_name = a['predicat_name']
    subject_name = a['subject_name']
    s_uid = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + subject_name)
    p_uid = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + predicat_name)
    o_uid = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + object_name)
    ontology.remove((s_uid, p_uid, o_uid))
    print('uhuuuuu')
    ontology.serialize(format="xml", destination="C:/Users/kdash/suit_app/CostumesRDF.owl")


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
    ontology.parse(os.path.join(os.path.dirname(BASE_DIR), "deployment", "media"))
    property_name = a['property']
    object_name = a['obj']
    property_uid = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + property_name)
    object_uid = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + object_name)
    sub_list = []
    for s, p, o in ontology.triples((None, property_uid, object_uid)):
        res = str(s).split('#')[1]
        sub_list.append(res)

    return random.choice(sub_list)

