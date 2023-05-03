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
#             from_node_name = str(s).split('#')[1]
#             to_node_name = str(o).split('#')[1]
#             edge_name = str(p).split('#')[1]
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
#
#     return updated_dict

def my_view(request):
    # генерируем новые данные
    # data = update_nodes_edges()
    data = {'edges': [{'from': 0, 'to': 10, 'label': 'subClassOf'},
  {'from': 1, 'to': 0, 'label': 'subClassOf'},
  {'from': 2, 'to': 10, 'label': 'subClassOf'},
  {'from': 3, 'to': 0, 'label': 'subClassOf'},
  {'from': 4, 'to': 0, 'label': 'subClassOf'},
  {'from': 5, 'to': 0, 'label': 'subClassOf'},
  {'from': 6, 'to': 0, 'label': 'subClassOf'},
  {'from': 7, 'to': 0, 'label': 'subClassOf'},
  {'from': 9, 'to': 0, 'label': 'subClassOf'},
  {'from': 11, 'to': 10, 'label': 'subClassOf'},
  {'from': 13, 'to': 14, 'label': 'subClassOf'},
  {'from': 14, 'to': 2, 'label': 'subClassOf'},
  {'from': 15, 'to': 1, 'label': 'subClassOf'},
  {'from': 25, 'to': 13, 'label': 'subClassOf'},
  {'from': 26, 'to': 27, 'label': 'subClassOf'},
  {'from': 27, 'to': 2, 'label': 'subClassOf'},
  {'from': 33, 'to': 34, 'label': 'subClassOf'},
  {'from': 34, 'to': 14, 'label': 'subClassOf'},
  {'from': 35, 'to': 27, 'label': 'subClassOf'},
  {'from': 39, 'to': 27, 'label': 'subClassOf'},
  {'from': 44, 'to': 13, 'label': 'subClassOf'},
  {'from': 45, 'to': 13, 'label': 'subClassOf'},
  {'from': 51, 'to': 1, 'label': 'subClassOf'},
  {'from': 64, 'to': 34, 'label': 'subClassOf'},
  {'from': 76, 'to': 3, 'label': 'subClassOf'},
  {'from': 89, 'to': 1, 'label': 'subClassOf'},
  {'from': 107, 'to': 3, 'label': 'subClassOf'}],
 'nodes': [{'id': 0, 'label': 'COMPONENTS'},
  {'id': 1, 'label': 'shoulder_product'},
  {'id': 2, 'label': 'STYLIZATION'},
  {'id': 3, 'label': 'waist_product'},
  {'id': 4, 'label': 'accessories'},
  {'id': 5, 'label': 'decorative_elements'},
  {'id': 6, 'label': 'fasteners'},
  {'id': 7, 'label': 'product_cut'},
  {'id': 8, 'label': 'product_fitting'},
  {'id': 9, 'label': 'product_length'},
  {'id': 10, 'label': 'Сostume'},
  {'id': 11, 'label': 'OUTFIT'},
  {'id': 12, 'label': 'additional_components'},
  {'id': 13, 'label': 'asian_countries'},
  {'id': 14, 'label': 'historical_reconstruction'},
  {'id': 15, 'label': 'bodice'},
  {'id': 16, 'label': 'bodice_classic_cut'},
  {'id': 17, 'label': 'bodice_cut'},
  {'id': 18, 'label': 'bodice_drapery_cut'},
  {'id': 19, 'label': 'bodice_embossed_tucks_cut'},
  {'id': 20, 'label': 'bodice_fitting'},
  {'id': 21, 'label': 'bodice_fitting_fit'},
  {'id': 22, 'label': 'bodice_fitting_loose'},
  {'id': 23, 'label': 'bodice_fitting_tight'},
  {'id': 24, 'label': 'bodice_wrapped_cut'},
  {'id': 25, 'label': 'chinese_style'},
  {'id': 26, 'label': 'computer_games'},
  {'id': 27, 'label': 'fantasy_style'},
  {'id': 28, 'label': 'corsage_flat_cut'},
  {'id': 29, 'label': 'corsage_vest_cut'},
  {'id': 30, 'label': 'corset_baroque__cut'},
  {'id': 31, 'label': 'corset_classic_cut'},
  {'id': 32, 'label': 'decorative_elements_cuffs'},
  {'id': 33, 'label': 'english_style'},
  {'id': 34, 'label': 'european_countries'},
  {'id': 35, 'label': 'epic_fantasy'},
  {'id': 36, 'label': 'fabric_dense'},
  {'id': 37, 'label': 'fabrics'},
  {'id': 38, 'label': 'fabric_thin'},
  {'id': 39, 'label': 'fairy_tales'},
  {'id': 40, 'label': 'fasteners_buttons'},
  {'id': 41, 'label': 'fasteners_lacing'},
  {'id': 42, 'label': 'fasteners_zipper'},
  {'id': 43, 'label': 'full_product'},
  {'id': 44, 'label': 'japanese_style'},
  {'id': 45, 'label': 'korean_style'},
  {'id': 46, 'label': 'layer_1'},
  {'id': 47, 'label': 'layer_2'},
  {'id': 48, 'label': 'layer_3'},
  {'id': 49, 'label': 'layer_4'},
  {'id': 50, 'label': 'layer_5'},
  {'id': 51, 'label': 'neckline'},
  {'id': 52, 'label': 'neckline_V_figurative_cut'},
  {'id': 53, 'label': 'neckline_cut'},
  {'id': 54, 'label': 'neckline_boat_cut'},
  {'id': 55, 'label': 'neckline_heart_cut'},
  {'id': 56, 'label': 'neckline_high_collar_cut'},
  {'id': 57, 'label': 'neckline_open_cut'},
  {'id': 58, 'label': 'neckline_round_cut'},
  {'id': 59, 'label': 'neckline_square_cut'},
  {'id': 60, 'label': 'neckline_straight_cut'},
  {'id': 61, 'label': 'neckline_under_throat_cut'},
  {'id': 62, 'label': 'neckline_wrapped_welt_cut'},
  {'id': 63, 'label': 'srax'},
  {'id': 64, 'label': 'scandinavian_style'},
  {'id': 65, 'label': 'shoulder_product_length'},
  {'id': 66, 'label': 'shoulder_product_length_ancle'},
  {'id': 67, 'label': 'waist_product_length'},
  {'id': 68, 'label': 'shoulder_product_length_hip'},
  {'id': 69, 'label': 'shoulder_product_length_knee'},
  {'id': 70, 'label': 'shoulder_product_length_knee_high'},
  {'id': 71, 'label': 'shoulder_product_length_mid_shin'},
  {'id': 72, 'label': 'shoulder_product_length_mid_thigh'},
  {'id': 73, 'label': 'shoulder_product_length_to_floor'},
  {'id': 74, 'label': 'shoulder_product_length_waist'},
  {'id': 75, 'label': 'shoulder_product_length_waist_high'},
  {'id': 76, 'label': 'skirt'},
  {'id': 77, 'label': 'skirt_cut'},
  {'id': 78, 'label': 'skirt_drapery_cut'},
  {'id': 79, 'label': 'skirt_fitting'},
  {'id': 80, 'label': 'skirt_fitting_A_line'},
  {'id': 81, 'label': 'skirt_fitting_half_sun'},
  {'id': 82, 'label': 'skirt_fitting_straight'},
  {'id': 83, 'label': 'skirt_fitting_sun'},
  {'id': 84, 'label': 'skirt_fitting_tight'},
  {'id': 85, 'label': 'skirt_wedges_cut'},
  {'id': 86, 'label': 'skirt_wrapped_cut'},
  {'id': 87, 'label': 'sleeve_cut'},
  {'id': 88, 'label': 'sleeve_flashlight_cut'},
  {'id': 89, 'label': 'sleeves'},
  {'id': 90, 'label': 'sleeve_flounce_cut'},
  {'id': 91, 'label': 'sleeves_fitting'},
  {'id': 92, 'label': 'sleeves_fitting_X_X_wide'},
  {'id': 93, 'label': 'sleeves_fitting_X_wide'},
  {'id': 94, 'label': 'sleeves_fitting_narrow'},
  {'id': 95, 'label': 'sleeves_fitting_narrow_strap'},
  {'id': 96, 'label': 'sleeves_fitting_straight'},
  {'id': 97, 'label': 'sleeves_fitting_wide'},
  {'id': 98, 'label': 'sleeves_fitting_wide_strap'},
  {'id': 99, 'label': 'sleeves_length'},
  {'id': 100, 'label': 'sleeves_length_elbow'},
  {'id': 101, 'label': 'sleeves_length_elbow_high'},
  {'id': 102, 'label': 'sleeves_length_long'},
  {'id': 103, 'label': 'sleeves_length_seven_eights'},
  {'id': 104, 'label': 'sleeves_length_strap'},
  {'id': 105, 'label': 'sleeves_length_three_quarters'},
  {'id': 106, 'label': 'sleeves_length_wrist'},
  {'id': 107, 'label': 'trousers'},
  {'id': 108, 'label': 'trousers_bloomers_cut'},
  {'id': 109, 'label': 'trousers_cut'},
  {'id': 110, 'label': 'trousers_cargo_cut'},
  {'id': 111, 'label': 'trousers_classic_cut'},
  {'id': 112, 'label': 'trousers_fitting'},
  {'id': 113, 'label': 'trousers_fitting_skinny'},
  {'id': 114, 'label': 'trousers_fitting_straight'},
  {'id': 115, 'label': 'trousers_fitting_wide'},
  {'id': 116, 'label': 'trousers_joggers_cut'},
  {'id': 117, 'label': 'waist_level'},
  {'id': 118, 'label': 'waist_level_high'},
  {'id': 119, 'label': 'waist_level_low'},
  {'id': 120, 'label': 'waist_level_normal'},
  {'id': 121, 'label': 'bodice_0000'},
  {'id': 122, 'label': 'bodice_0001'},
  {'id': 123, 'label': 'bodice_0002'},
  {'id': 124, 'label': 'bodice_0003'},
  {'id': 125, 'label': 'bodice_0004'},
  {'id': 126, 'label': 'bodice_0005'},
  {'id': 127, 'label': 'bodice_0006'},
  {'id': 128, 'label': 'bodice_0007'},
  {'id': 129, 'label': 'bodice_0008'},
  {'id': 130, 'label': 'bodice_0009'},
  {'id': 131, 'label': 'bodice_0010'},
  {'id': 132, 'label': 'bodice_0011'},
  {'id': 133, 'label': 'bodice_0012'},
  {'id': 134, 'label': 'bodice_0013'},
  {'id': 135, 'label': 'bodice_0014'},
  {'id': 136, 'label': 'bodice_0015'},
  {'id': 137, 'label': 'bodice_0016'},
  {'id': 138, 'label': 'bodice_0017'},
  {'id': 139, 'label': 'bodice_0018'},
  {'id': 140, 'label': 'bodice_0019'},
  {'id': 141, 'label': 'bodice_0020'},
  {'id': 142, 'label': 'bodice_0021'},
  {'id': 143, 'label': 'bodice_0022'},
  {'id': 144, 'label': 'bodice_0023'},
  {'id': 145, 'label': 'bodice_0024'},
  {'id': 146, 'label': 'bodice_0025'},
  {'id': 147, 'label': 'bodice_0026'},
  {'id': 148, 'label': 'bodice_0027'},
  {'id': 149, 'label': 'bodice_0028'},
  {'id': 150, 'label': 'bodice_0029'},
  {'id': 151, 'label': 'bodice_0030'},
  {'id': 152, 'label': 'bodice_0031'},
  {'id': 153, 'label': 'bodice_0032'},
  {'id': 154, 'label': 'bodice_0033'},
  {'id': 155, 'label': 'bodice_0034'},
  {'id': 156, 'label': 'bodice_0035'},
  {'id': 157, 'label': 'bodice_0036'},
  {'id': 158, 'label': 'bodice_0037'},
  {'id': 159, 'label': 'bodice_0038'},
  {'id': 160, 'label': 'bodice_0039'},
  {'id': 161, 'label': 'bodice_0040'},
  {'id': 162, 'label': 'bodice_0041'},
  {'id': 163, 'label': 'bodice_0042'},
  {'id': 164, 'label': 'bodice_0043'},
  {'id': 165, 'label': 'bodice_0044'},
  {'id': 166, 'label': 'bodice_0045'},
  {'id': 167, 'label': 'bodice_0046'},
  {'id': 168, 'label': 'bodice_0047'},
  {'id': 169, 'label': 'bodice_0048'},
  {'id': 170, 'label': 'bodice_0049'},
  {'id': 171, 'label': 'bodice_0050'},
  {'id': 172, 'label': 'fasteners_zipper_0000'},
  {'id': 173, 'label': 'neckline_0000'},
  {'id': 174, 'label': 'neckline_0001'},
  {'id': 175, 'label': 'neckline_0002'},
  {'id': 176, 'label': 'neckline_0003'},
  {'id': 177, 'label': 'neckline_0004'},
  {'id': 178, 'label': 'neckline_0005'},
  {'id': 179, 'label': 'neckline_0006'},
  {'id': 180, 'label': 'neckline_0007'},
  {'id': 181, 'label': 'neckline_0008'},
  {'id': 182, 'label': 'neckline_0009'},
  {'id': 183, 'label': 'neckline_0010'},
  {'id': 184, 'label': 'neckline_0011'},
  {'id': 185, 'label': 'neckline_0012'},
  {'id': 186, 'label': 'neckline_0013'},
  {'id': 187, 'label': 'neckline_0014'},
  {'id': 188, 'label': 'neckline_0015'},
  {'id': 189, 'label': 'neckline_0016'},
  {'id': 190, 'label': 'neckline_0017'},
  {'id': 191, 'label': 'neckline_0018'},
  {'id': 192, 'label': 'neckline_0019'},
  {'id': 193, 'label': 'neckline_0020'},
  {'id': 194, 'label': 'outfit_000000'},
  {'id': 195, 'label': 'skirt_0010'},
  {'id': 196, 'label': 'sleeves_0005'},
  {'id': 197, 'label': 'outfit_000001'},
  {'id': 198, 'label': 'trousers_0015'},
  {'id': 199, 'label': 'outfit_000002'},
  {'id': 200, 'label': 'outfit_000003'},
  {'id': 201, 'label': 'skirt_0024'},
  {'id': 202, 'label': 'outfit_000004'},
  {'id': 203, 'label': 'sleeves_0000'},
  {'id': 204, 'label': 'outfit_000005'},
  {'id': 205, 'label': 'skirt_0000'},
  {'id': 206, 'label': 'skirt_0001'},
  {'id': 207, 'label': 'skirt_0002'},
  {'id': 208, 'label': 'skirt_0003'},
  {'id': 209, 'label': 'skirt_0004'},
  {'id': 210, 'label': 'skirt_0005'},
  {'id': 211, 'label': 'skirt_0006'},
  {'id': 212, 'label': 'skirt_0007'},
  {'id': 213, 'label': 'skirt_0008'},
  {'id': 214, 'label': 'skirt_0009'},
  {'id': 215, 'label': 'skirt_0011'},
  {'id': 216, 'label': 'skirt_0012'},
  {'id': 217, 'label': 'skirt_0013'},
  {'id': 218, 'label': 'skirt_0014'},
  {'id': 219, 'label': 'skirt_0015'},
  {'id': 220, 'label': 'skirt_0016'},
  {'id': 221, 'label': 'skirt_0017'},
  {'id': 222, 'label': 'skirt_0018'},
  {'id': 223, 'label': 'skirt_0019'},
  {'id': 224, 'label': 'skirt_0020'},
  {'id': 225, 'label': 'skirt_0021'},
  {'id': 226, 'label': 'skirt_0022'},
  {'id': 227, 'label': 'skirt_0023'},
  {'id': 228, 'label': 'skirt_0025'},
  {'id': 229, 'label': 'skirt_0026'},
  {'id': 230, 'label': 'skirt_0027'},
  {'id': 231, 'label': 'skirt_0028'},
  {'id': 232, 'label': 'skirt_0029'},
  {'id': 233, 'label': 'skirt_0030'},
  {'id': 234, 'label': 'sleeves_0001'},
  {'id': 235, 'label': 'sleeves_0002'},
  {'id': 236, 'label': 'sleeves_0003'},
  {'id': 237, 'label': 'sleeves_0004'},
  {'id': 238, 'label': 'sleeves_0006'},
  {'id': 239, 'label': 'sleeves_0007'},
  {'id': 240, 'label': 'sleeves_0008'},
  {'id': 241, 'label': 'sleeves_0009'},
  {'id': 242, 'label': 'sleeves_0010'},
  {'id': 243, 'label': 'sleeves_0011'},
  {'id': 244, 'label': 'sleeves_0012'},
  {'id': 245, 'label': 'sleeves_0013'},
  {'id': 246, 'label': 'sleeves_0014'},
  {'id': 247, 'label': 'sleeves_0015'},
  {'id': 248, 'label': 'sleeves_0016'},
  {'id': 249, 'label': 'sleeves_0017'},
  {'id': 250, 'label': 'sleeves_0018'},
  {'id': 251, 'label': 'sleeves_0019'},
  {'id': 252, 'label': 'sleeves_0020'},
  {'id': 253, 'label': 'sleeves_0021'},
  {'id': 254, 'label': 'sleeves_0022'},
  {'id': 255, 'label': 'sleeves_0023'},
  {'id': 256, 'label': 'sleeves_0024'},
  {'id': 257, 'label': 'sleeves_0025'},
  {'id': 258, 'label': 'sleeves_0026'},
  {'id': 259, 'label': 'sleeves_0027'},
  {'id': 260, 'label': 'sleeves_0028'},
  {'id': 261, 'label': 'sleeves_0029'},
  {'id': 262, 'label': 'sleeves_0030'},
  {'id': 263, 'label': 'sleeves_0031'},
  {'id': 264, 'label': 'sleeves_0032'},
  {'id': 265, 'label': 'sleeves_0033'},
  {'id': 266, 'label': 'sleeves_0034'},
  {'id': 267, 'label': 'sleeves_0035'},
  {'id': 268, 'label': 'sleeves_0036'},
  {'id': 269, 'label': 'sleeves_0037'},
  {'id': 270, 'label': 'sleeves_0038'},
  {'id': 271, 'label': 'sleeves_0039'},
  {'id': 272, 'label': 'sleeves_0040'},
  {'id': 273, 'label': 'trousers_0000'},
  {'id': 274, 'label': 'trousers_0001'},
  {'id': 275, 'label': 'trousers_0002'},
  {'id': 276, 'label': 'trousers_0003'},
  {'id': 277, 'label': 'trousers_0004'},
  {'id': 278, 'label': 'trousers_0005'},
  {'id': 279, 'label': 'trousers_0006'},
  {'id': 280, 'label': 'trousers_0007'},
  {'id': 281, 'label': 'trousers_0008'},
  {'id': 282, 'label': 'trousers_0009'},
  {'id': 283, 'label': 'trousers_0010'},
  {'id': 284, 'label': 'trousers_0011'},
  {'id': 285, 'label': 'trousers_0012'},
  {'id': 286, 'label': 'trousers_0013'},
  {'id': 287, 'label': 'trousers_0014'},
  {'id': 288, 'label': 'trousers_0016'},
  {'id': 289, 'label': 'trousers_0017'},
  {'id': 290, 'label': 'trousers_0018'},
  {'id': 291, 'label': 'trousers_0019'},
  {'id': 292, 'label': 'trousers_0020'}]}
    # возвращаем данные в формате JSON
    return JsonResponse(data)


def visual(request):

    return render(request, 'manage_ontology/ontology_visualization.html')
