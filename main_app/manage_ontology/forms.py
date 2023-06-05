from django import forms
import os
from pathlib import Path

from .styles_funcs import get_stylizations
import ontor

BASE_DIR = Path(__file__).resolve().parent.parent


class AddOldElements(forms.Form):
    sub = forms.ChoiceField()
    pred = forms.ChoiceField()
    obj = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub'].choices = get_existing_sub_obj()
        self.fields['pred'].choices = get_existing_pred() + [('type', 'type'), ('subClassOf', 'subClassOf')]
        self.fields['obj'].choices = get_existing_sub_obj()

class AddNewElements(forms.Form):
    sub = forms.CharField(max_length=100)
    type = forms.ChoiceField()
    pred = forms.ChoiceField()
    obj = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].choices = [('Class', 'Class'), ('NamedIndividual', 'NamedIndividual')]
        self.fields['pred'].choices = get_existing_pred()
        self.fields['obj'].choices = get_existing_sub_obj()

def get_existing_sub_obj():
    ontor3 = ontor.OntoEditor(os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"),
                              os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
    result = []
    for element in [p.name for p in ontor3.get_elems()[0]] + [p.name for p in ontor3.get_elems()[3]]:
        result.append((element, element))
    return result

def get_existing_pred():
    ontor3 = ontor.OntoEditor(os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"),
                              os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
    result = []
    for element in [p.name for p in ontor3.get_elems()[1]]:
        result.append((element, element))
    return result + [('type', 'type'), ('subClassOf', 'subClassOf')]


class ReturnRandom(forms.Form):
    property = forms.CharField(max_length=100, required=False)
    obj = forms.CharField(max_length=100, required=False)


class DeleteElements(forms.Form):
    element_name = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['element_name'].choices = get_existing_sub_obj() + get_existing_pred()

class DeleteOneElement(forms.Form):
    subject_name = forms.ChoiceField()
    predicat_name = forms.ChoiceField()
    object_name = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject_name'].choices = get_existing_sub_obj()
        self.fields['predicat_name'].choices = get_existing_pred() + [('type', 'type'), ('subClassOf', 'subClassOf')]
        self.fields['object_name'].choices = get_existing_sub_obj()


class StyleForm(forms.Form):
    style = forms.ChoiceField()


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['style'].choices = get_stylizations()


class CostumeForm(forms.Form):
    style = forms.ChoiceField(choices=[], widget=forms.Select)

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', [])
        super().__init__(*args, **kwargs)
        self.fields['style'].choices = choices

class SubSubStyleForm(forms.Form):
    style = forms.ChoiceField(choices=[], widget=forms.Select)

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', [])
        super().__init__(*args, **kwargs)
        self.fields['style'].choices = choices


class ChooseColorForm(forms.Form):
    COLOR_CHOICES = [
        ('red', 'Красный'),
        ('orange', 'Оранжевый'),
        ('yellow', 'Жёлтый'),
        ('green', 'Зеленый'),
        ('light blue', 'Голубой'),
        ('blue', 'Синий'),
        ('purple', 'Фиолетовый'),
        ('pink', 'Розовый'),
        ('white', 'Белый'),
        ('black', 'Чёрный'),
        ('gray', 'Серый'),
        ('brown', 'Коричневый'),
        ('beige', 'Бежевый'),
    ]
    color = forms.ChoiceField(choices=COLOR_CHOICES)
