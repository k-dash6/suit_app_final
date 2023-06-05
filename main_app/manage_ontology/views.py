import os
from pathlib import Path

from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages

import ontor
from rdflib import Graph

from custom_auth.decorators import admin_required

from .models import Collection
from .forms import AddNewElements, AddOldElements, DeleteElements, \
    DeleteOneElement, StyleForm, SubSubStyleForm, CostumeForm, ChooseColorForm
from .styles_funcs import get_current_sub_style, check_if_size_exists
from .images_funcs import update_images
from .generation_funcs import return_outfit
from .edit_ontology_funcs import add_new_element, add_new_triple, \
    delete_all_triples_with_elem, delete_one_triple

BASE_DIR = Path(__file__).resolve().parent.parent


@login_required
def home(request):
    return render(request, 'manage_ontology/home.html')


@login_required
def info(request):
    return render(request, 'manage_ontology/info.html')


@login_required
def my_profile(request):
    collections = Collection.objects.filter(user=request.user)
    return render(request, 'manage_ontology/my_profile.html', {'user': request.user, 'collections': collections})


@admin_required
def manage_ontology(request):
    return render(request, 'manage_ontology/manage_ontology.html')


@admin_required
def add_elements(request):
    return render(request, 'manage_ontology/manage_ontology_add.html')


@admin_required
def delete(request):
    return render(request, 'manage_ontology/manage_ontology_del.html')


@admin_required
def manage_update_img(request):
    if request.method == 'POST':
        update_images()
        messages.info(request, "База успешно обновлена")
        return redirect("manage_update_img")
    return render(request, 'manage_ontology/manage_ontology_update_img.html')


@admin_required
def add_new_element_view(request):
    if request.method == 'POST':
        form_add = AddNewElements(request.POST)
        if form_add.is_valid():
            add_new_element(form_add.cleaned_data)
    else:
        form_add = AddNewElements()
    return render(request, 'manage_ontology/manage_ontology_add_with_new.html', {'form_add': form_add})


@admin_required
def add_triple_view(request):
    if request.method == 'POST':
        form_add = AddOldElements(request.POST)
        if form_add.is_valid():
            add_new_triple(form_add.cleaned_data)
        else:
            return redirect('home')
    else:
        form_add = AddOldElements()
    return render(request, 'manage_ontology/manage_ontology_add_with_old.html', {'form_add': form_add})


@admin_required
def delete_all_triples_with_elem_view(request):
    if request.method == 'POST':
        form_del = DeleteElements(request.POST)
        if form_del.is_valid():
            delete_all_triples_with_elem(form_del.cleaned_data)
        else:
            return redirect('home')
    else:
        form_del = DeleteElements()
    return render(request, 'manage_ontology/manage_ontology_del_all.html', {'form_del': form_del})


@admin_required
def delete_triple_view(request):
    if request.method == 'POST':
        form_del_one = DeleteOneElement(request.POST)
        if form_del_one.is_valid():
            delete_one_triple(form_del_one.cleaned_data)
        else:
            return redirect('home')
    else:
        form_del_one = DeleteOneElement()
    return render(request, 'manage_ontology/manage_ontology_del_one.html', {'form_del_one': form_del_one})


@login_required
def my_view(request):
    g = Graph()
    g.parse(os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
    ontor3 = ontor.OntoEditor(os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"),
                              os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
    nodes_classes = [p.name for p in ontor3.get_elems()[0]]
    nodes_classes.remove('layer_1')
    nodes_classes.remove('layer_2')
    nodes_classes.remove('layer_3')
    nodes_classes.remove('layer_4')
    nodes_classes.remove('layer_5')
    nodes_obj_properties = [p.name for p in ontor3.get_elems()[1]]
    nodes_data_properties = [p.name for p in ontor3.get_elems()[2]]
    nodes_individuals = [p.name for p in ontor3.get_elems()[3]]

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
    data_nodes_obj_properties = []
    for i in range(len(nodes_obj_properties)):
        data_nodes_obj_properties.append({
            'id': i + len_classes + len_individuals,
            'label': nodes_obj_properties[i],
            'color': "#8e948f"
        })

    nodes = data_nodes_classes + data_nodes_individuals + data_nodes_obj_properties

    nodes_dict = {}
    for d in nodes:
        nodes_dict[d['label']] = d['id']

    edges = []
    trash_pred = ['related', 'range', 'domain']
    trash_obj_sub = ['Class', 'DatatypeProperty', 'FunctionalProperty', 'ObjectProperty', 'TransitiveProperty',
                     'NamedIndividual', 'subPropertyOf']
    for ind, (sub, pred, obj) in enumerate(g):
        if not '#' in obj and 'has_product' in pred:
            from_node_name = str(sub).split('#')[1]
            to_node_name = obj
            edge_name = str(pred).split('#')[1]
            magic_dict = {'from': from_node_name, 'to': to_node_name, 'label': edge_name}
            edges.append(magic_dict)

        elif not '#' in sub or not '#' in pred or not '#' in obj:
            continue
        elif str(sub).split('#')[1] in trash_obj_sub:
            continue
        elif str(obj).split('#')[1] in trash_obj_sub:
            continue
        elif str(pred).split('#')[1] in trash_pred:
            continue
        else:
            from_node_name = str(sub).split('#')[1]
            to_node_name = str(obj).split('#')[1]
            edge_name = str(pred).split('#')[1]
            magic_dict = {'from': from_node_name, 'to': to_node_name, 'label': edge_name}
            edges.append(magic_dict)

    for d in edges:
        for key, value in d.items():
            if key == 'label' or key == 'color':
                continue
            if value not in nodes_dict:
                nodes_dict[value] = len(nodes_dict)
                nodes.append({'id': len(nodes_dict), 'label': value, 'color': '#8ca8ba'}, )

            d[key] = nodes_dict[value]

    to_delete_list = []
    for dict_ in nodes:
        b = False
        for dict_edges in edges:
            if dict_['id'] == dict_edges['from']:
                b = True
            if dict_['id'] == dict_edges['to']:
                b = True
        if b == False:
            to_delete_list.append(dict_)

    for elem in to_delete_list:
        nodes.remove(elem)
    data = {'edges': edges, 'nodes': nodes}

    return JsonResponse(data)


@login_required
def visual(request):
    return render(request, 'manage_ontology/ontology_visualization.html')


@login_required
def choose_stylization(request):
    if request.method == 'POST':
        form = StyleForm(request.POST)
        if form.is_valid():
            style = form.cleaned_data['style']
            request.session['selected_style'] = style
            return redirect('choose_sub_stylization')
    else:
        form = StyleForm()

    return render(request, 'manage_ontology/choose_stylization.html', {'form': form})


@login_required
def choose_sub_stylization(request):
    style = request.session.get('selected_style')
    choices = get_current_sub_style(style)
    if request.method == 'POST':
        substyle_form = CostumeForm(request.POST, choices=choices)
        if substyle_form.is_valid():
            sub_style = substyle_form.cleaned_data['style']
            request.session['selected_sub_style'] = sub_style
            if check_if_size_exists(sub_style):
                return redirect('choose_sub_sub_style')
            else:
                return redirect('choose_color')
    else:
        substyle_form = CostumeForm(choices=choices)

    return render(request, 'manage_ontology/choose_sub_style.html', {'substyle_form': substyle_form})


@login_required
def choose_sub_sub_style(request):
    style = request.session.get('selected_style')
    sub_style = request.session.get('selected_sub_style')
    choices = check_if_size_exists(sub_style)
    if request.method == 'POST':
        sub_sub_style_form = SubSubStyleForm(request.POST, choices=choices)
        if sub_sub_style_form.is_valid():
            sub_sub_style = sub_sub_style_form.cleaned_data['style']
            request.session['selected_sub_sub_style'] = sub_sub_style
            return redirect('choose_color')
    else:
        sub_sub_style_form = SubSubStyleForm(choices=choices)

    return render(request, 'manage_ontology/choose_sub_sub_style.html', {'sub_sub_style_form': sub_sub_style_form})


@login_required
def choose_color(request):
    style = request.session.get('selected_style')
    sub_style = request.session.get('selected_sub_style')
    sub_sub_style = request.session.get('selected_sub_sub_style')
    if request.method == 'POST':
        color_form = ChooseColorForm(request.POST)
        if color_form.is_valid():
            color = color_form.cleaned_data['color']
            request.session['selected_color'] = color
            if sub_sub_style:
                data = [sub_sub_style, color]
            else:
                data = [sub_style, color]
            outfit, color = return_outfit(data)
            image_path = f'/static/manage_ontology/images/outfits/{outfit}_{color}.jpg'
            return render(request, 'manage_ontology/result.html', { 'image_path': image_path })
    else:
        color_form = ChooseColorForm()

    return render(request, 'manage_ontology/choose_color.html', {'color_form': color_form})


@login_required
def result(request):
    return render(request, 'manage_ontology/result.html')


@login_required
def add_to_collection(request):
    image_path = request.POST.get('image_path')

    collection = Collection.objects.create(user=request.user, image_path=image_path)
    return redirect(reverse("my_profile"))
