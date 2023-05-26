from django import forms

from .models import *
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'username',)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class AddElements(forms.Form):
    subject_name = forms.CharField(max_length=100, required=False)
    predicat_name = forms.CharField(max_length=100, required=False)
    object_name = forms.CharField(max_length=100, required=False)


class ReturnRandom(forms.Form):
    property = forms.CharField(max_length=100, required=False)
    obj = forms.CharField(max_length=100, required=False)


class DeleteElements(forms.Form):
    element_name = forms.CharField(max_length=100, required=False)


class DeleteOneElement(forms.Form):
    subject_name = forms.CharField(max_length=100, required=False)
    predicat_name = forms.CharField(max_length=100, required=False)
    object_name = forms.CharField(max_length=100, required=False)

from googletrans import Translator
import os
from rdflib import Graph
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

def get_stylizations():
    stylizations = []
    g = Graph()
    g.parse(os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
    for ind, (sub, pred, obj) in enumerate(g):
        if 'subClassOf' in pred and 'STYLIZATION' in obj:
            stylization = sub.split('#')[1]
            stylization_to_translate = stylization.replace('_', ' ')
            while True:
                try:
                    translator = Translator()
                    stylization_translated = translator.translate(stylization_to_translate, dest='ru')
                except:
                    continue
                else:
                    break
            mini = (stylization, stylization_translated.text)
            stylizations.append(mini)
    return stylizations


def get_sub_stylizations(stylization):
    sub_stylizations = []
    g = Graph()
    g.parse(os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
    for ind, (sub, pred, obj) in enumerate(g):
        if stylization in obj:
            print()
            print('Я пытаюсь найти подстили для стиля', stylization)
            print('*')
            print(sub.split('#')[1], pred.split('#')[1], obj.split('#')[1])
            print('*')
            print()
            stylization_ = sub.split('#')[1]
            stylization_to_translate = stylization_.replace('_', ' ')
            while True:
                try:
                    translator = Translator()
                    stylization_translated = translator.translate(stylization_to_translate, dest='ru')
                except:
                    continue
                else:
                    break
            mini = (stylization_, stylization_translated.text)
            sub_stylizations.append(mini)
    return sub_stylizations



class ChooseStylizationForm(forms.Form):
    stylizations = forms.ChoiceField(
        required=False,
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, **kwargs):
        super(ChooseStylizationForm, self).__init__(*args, **kwargs)
        self.fields['stylizations'].choices = get_stylizations()


class ChooseSubstyleForm(forms.Form):
    substyles = forms.ChoiceField(
        required=False,
        widget=forms.RadioSelect,
    )

    def __init__(self, stylization, *args, **kwargs):
        super(ChooseSubstyleForm, self).__init__(*args, **kwargs)
        self.fields['substyles'].choices = get_sub_stylizations(stylization)


class ChooseSizeForm(forms.Form):
    size = forms.ChoiceField(
        required=False,
        widget=forms.RadioSelect,
    )

    def __init__(self, size_stylizations, *args, **kwargs):
        super(ChooseSizeForm, self).__init__(*args, **kwargs)
        self.fields['size'].choices = size_stylizations


class ChooseColorForm(forms.Form):
    color = forms.ChoiceField(
        required=False,
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, **kwargs):
        super(ChooseColorForm, self).__init__(*args, **kwargs)
        self.fields['color'].choices = [('green', 'Зеленый'), ('red', 'Красный'), ('blue', 'Голубой')]


class CostumeForm(forms.Form):
    COLOR_CHOICES = [
        ('green', 'Зеленый'),
        ('red', 'Красный'),
        ('blue', 'Голубой'),
    ]

    style = forms.ChoiceField()
    color = forms.ChoiceField(choices=COLOR_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['style'].choices = get_style_choices()


def get_style_choices() -> list[tuple[str, str]]:
    # TODO: implement this.
    return [
        ('computer_games', 'Компьютерные игры'),
        ('english_style', ' Английский стиль'),
    ]

