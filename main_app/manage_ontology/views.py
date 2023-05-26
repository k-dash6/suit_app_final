import os
import random

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from .forms import *
from .models import Collection

from PIL import Image
from kandinsky2 import get_kandinsky2
import torch
from googletrans import Translator
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from rdflib import URIRef, BNode, Literal, Namespace, Graph, RDF
from rdflib.namespace import FOAF, DCTERMS, XSD
from pathlib import Path
import json
import ontor

BASE_DIR = Path(__file__).resolve().parent.parent


def home(request):
    return render(request, 'manage_ontology/home.html')

def info(request):
    return render(request, 'manage_ontology/info.html')

def result(request):
    return render(request, 'manage_ontology/result.html')

# login_required decoreator
def my_profile(request):
    if request.user.is_anonymous:
        return redirect(reverse('login')) # settings.login_redirect_url
    # TODO: make sure user is authenticated
    collections = Collection.objects.filter(user=request.user)
    return render(request, 'manage_ontology/my_profile.html', {'name': 'Dasha', 'user': request.user, 'collections': collections})

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


def my_view(request):
    # генерируем новые данные
    g = Graph()
    g.parse(os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
    ontor3 = ontor.OntoEditor(os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"),
                              os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
    nodes_classes = [p.name for p in ontor3.get_elems()[0]]
    nodes_properties = [p.name for p in ontor3.get_elems()[1]]
    nodes_individuals = [p.name for p in ontor3.get_elems()[3]]

    print()
    print('nodes_classes')
    print(nodes_classes)
    print()

    nodes_dict = {}
    data_nodes_classes = []
    for i in range(len(nodes_classes)):
        data_nodes_classes.append({
            'id': i,
            'label': nodes_classes[i],
            'color': "#b59653"
        })
    len_classes = len(data_nodes_classes)
    data_nodes_individuals = []
    for i in range(len(nodes_individuals)):
        data_nodes_individuals.append({
            'id': i + len_classes,
            'label': nodes_individuals[i],
            'color': "#8cbd77"
        })
    len_individuals = len(data_nodes_individuals)
    data_nodes_properties = []
    for i in range(len(nodes_properties)):
        data_nodes_properties.append({
            'id': i + len_classes + len_individuals,
            'label': nodes_properties[i],
            'color': "#8e948f"
        })
    nodes = data_nodes_classes + data_nodes_individuals + data_nodes_properties

    # print()
    # print('nodes')
    # print(nodes)
    # print()

    nodes_dict = {}
    for d in nodes:
        nodes_dict[d['label']] = d['id']
    edges = []
    trash_pred = ['related', 'range', 'domain']
    trash_obj_sub = ['Class', 'DatatypeProperty', 'FunctionalProperty', 'ObjectProperty', 'TransitiveProperty',
                     'NamedIndividual']
    for ind, (sub, pred, obj) in enumerate(g):
        if not '#' in sub or not '#' in pred or not '#' in obj:
            continue
        if str(pred).split('#')[1] in trash_pred:
            continue
        if str(sub).split('#')[1] in trash_obj_sub:
            continue
        if str(obj).split('#')[1] in trash_obj_sub:
            continue
        from_node_name = str(sub).split('#')[1]
        to_node_name = str(obj).split('#')[1]
        edge_name = str(pred).split('#')[1]
        magic_dict = {'from': from_node_name, 'to': to_node_name, 'label': edge_name}
        edges.append(magic_dict)
    # print()
    # print('nodes_dict')
    # print(nodes_dict)
    # print()

    for d in edges:
        for key, value in d.items():
            if key == 'label' or key == 'color':
                continue
            d[key] = nodes_dict[value]
    data = {'edges': edges, 'nodes': nodes}

    # возвращаем данные в формате JSON
    return JsonResponse(data)


def visual(request):
    return render(request, 'manage_ontology/ontology_visualization.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'manage_ontology/register.html', {'form': form})


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


# def choose_stylization(request):
#     if request.method == 'POST':
#         form = ChooseStylizationForm(request.POST)
#         if form.is_valid():
#             stylization = form.cleaned_data['stylizations']
#             substyle_form = ChooseSubstyleForm(stylization=stylization)
#
#             return render(request, 'manage_ontology/choose_sub_style.html', {'substyle_form': substyle_form})
#     else:
#         form = ChooseStylizationForm()
#
#     return render(request, 'manage_ontology/choose_stylization.html', {'form': form})


def check_if_size_exists(substyle):
    print('Давай поищем подстили для подстиля', substyle)
    size_stylizations = []
    g = Graph()
    g.parse(os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
    for ind, (sub, pred, obj) in enumerate(g):
        if substyle in obj:
            print()
            print('Я пытаюсь найти подстили для подстиля')
            print('*')
            print(sub.split('#')[1], pred.split('#')[1], obj.split('#')[1])
            print('*')
            print()
            stylization = sub.split('#')[1]
            stylization_to_translate = stylization.replace('_', ' ')
            substyle = sub.split('#')[1]
            substyle_to_translate = substyle.replace('_', ' ')

            while True:
                try:
                    translator = Translator()
                    substyle_translated = translator.translate(substyle_to_translate, dest='ru')
                except:
                    continue
                else:
                    break
            mini = (substyle, substyle_translated.text)
            size_stylizations.append(mini)
    if size_stylizations == []:
        return False
    return size_stylizations


def choose_stylization(request):
    if request.method == 'POST':
        form = CostumeForm(request.POST)
        # form = ChooseStylizationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            # 1. create an image from the cleaned_data
            # 2. save the image to the disk
            image_path = '/static/manage_ontology/images/clothes/dasha6/outfit_00002_green.jpg'
            # 3. return a template with the path to this image (so it could display it and send it with the "add to collecitons" button)
            return render(request, 'manage_ontology/result.html', { 'image_path': image_path })
    else:
        form = CostumeForm()

    return render(request, 'manage_ontology/choose_stylization.html', {'form': form})

def choose_sub_style(request, stylization):
    if request.method == 'POST':
        substyle_form = ChooseSubstyleForm(request.POST, stylization=stylization)
        if substyle_form.is_valid():
            substyle = substyle_form.cleaned_data['substyles']
            size_stylizations = check_if_size_exists(substyle)
            if size_stylizations:
                return redirect('choose_size', size_stylizations=size_stylizations)
            else:
                return redirect('choose_color')
    else:
        substyle_form = ChooseSubstyleForm(stylization=stylization)

    return render(request, 'manage_ontology/choose_sub_style.html', {'substyle_form': substyle_form})

def choose_size(request, size_stylizations):
    if request.method == 'POST':
        size_form = ChooseSizeForm(request.POST)
        if size_form.is_valid():
            # color_form = ChooseColorForm()
            return redirect('choose_color')
    else:
        size_form = ChooseSizeForm(size_stylizations=size_stylizations)

    return render(request, 'manage_ontology/choose_size.html', {'size_form': size_form})

def choose_color(request):
    if request.method == 'POST':
        color_form = ChooseColorForm(request.POST)
        if color_form.is_valid():
            return redirect('result')
    else:
        color_form = ChooseColorForm()

    return render(request, 'manage_ontology/choose_size.html', {'color_form': color_form})


def save_image(image, filename):
    folder_path = os.path.join(os.path.dirname(BASE_DIR), "main_app/manage_ontology/static/manage_ontology/images/outfits")
    image_path = os.path.join(folder_path, filename)
    image.save(image_path)
    print(f"Изображение сохранено: {image_path}")


def get_outfits_dict():
    g = Graph()
    g.parse(os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
    ontor3 = ontor.OntoEditor("CostumesRDF.owl", "CostumesRDF.owl")
    magic_list_3 = [p.name for p in ontor3.get_elems()[3]]
    ready_elements = []
    for ind, (sub, pred, obj) in enumerate(g):
        if not '#' in sub or not '#' in pred or not '#' in obj or 'NamedIndividual' in obj:
            continue
        if 'outfit' in sub.split('#')[1] and obj.split('#')[1] in magic_list_3:
            ready_elements.append(obj.split('#')[1])

    outfits = set()
    for ind, (sub, pred, obj) in enumerate(g):
        if not '#' in sub or not '#' in pred or not '#' in obj or 'NamedIndividual' in obj:
            continue
        if 'outfit' in sub.split('#')[1]:
            outfits.add(sub.split('#')[1])
        if 'outfit' in obj.split('#')[1]:
            outfits.add(obj.split('#')[1])

    list_outfits = sorted(list(outfits))

    outfits_dict = {}
    for outfit in list_outfits:
        outfits_dict[outfit] = []

    for outfit in outfits:
        for ind, (sub, pred, obj) in enumerate(g):
            if not '#' in sub or not '#' in pred or not '#' in obj or 'NamedIndividual' in obj:
                continue
            if 'outfit' in sub.split('#')[1] and obj.split('#')[1] in ready_elements:
                if obj.split('#')[1] not in outfits_dict[sub.split('#')[1]]:
                    outfits_dict[sub.split('#')[1]].append(obj.split('#')[1])
    return outfits_dict


def generate_outfit_img(request, outfits_dict):
    g = Graph()
    g.parse(os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
    # outfits_dict = get_outfits_dict()

    outfits_description_dict = {}

    for item in outfits_dict.items():
        if outfits_dict[item[0]]:
            outfits_description_dict[item[0]] = []
        for ind, (sub, pred, obj) in enumerate(g):
            if not '#' in sub or not '#' in pred or not '#' in obj or 'NamedIndividual' in obj:
                continue
            if sub.split('#')[1] in item[1]:
                outfits_description_dict[item[0]].append(obj.split('#')[1].replace('_', ' '))

    # color "green" "red" "blue"
    # costume "fairy_tales"

    description_prefix = 'On a white background: Costume on mannequin: '

    for item in outfits_description_dict.items():
        full_description = description_prefix + ' '.join(item[1])
        outfits_description_dict[item[0]] = full_description

    device = "cuda" if torch.cuda.is_available() else torch.device('cpu')

    model = get_kandinsky2(device, task_type='text2img', cache_dir='/img', model_version='2.1',
                           use_flash_attention=False)

    for item in outfits_description_dict.items():
        images = model.generate_text2img(item[1], num_steps=100,
                                         batch_size=1, guidance_scale=4,
                                         h=768, w=768, sampler='p_sampler', prior_cf_scale=4,
                                         prior_steps="5", )
        filename = f"{item[0]}.jpg"
        save_image(images[0], filename)


def add_to_collection(request):
    # TODO: make sure add_to_collection only receives POST request
    # TODO: make sure that request.user is authenticated

    image_path = request.POST.get('image_path')

    # TODO: what to do if image_path is empty?
    # TODO: what if user already has it in collection?

    collection = Collection.objects.create(user=request.user, image_path=image_path)

    return redirect(reverse("my_profile"))

