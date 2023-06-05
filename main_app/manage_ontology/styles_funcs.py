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


def get_sub_stylizations():
    stylizations_tuple = get_stylizations()
    stylizations_list = [i[0] for i in stylizations_tuple]
    res = {}
    for stylization in stylizations_list:
        res[stylization] = []

    for stylization in stylizations_list:

        sub_stylizations = []
        g = Graph()
        g.parse(os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
        for ind, (sub, pred, obj) in enumerate(g):
            if stylization in obj:
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
        res[stylization].append(sub_stylizations)
    return res

def get_current_sub_style(style):
    print(style)
    sub_styles_dict = get_sub_stylizations()
    print(sub_styles_dict[style][0])
    return sub_styles_dict[style][0]

def check_if_size_exists(substyle):
    size_stylizations = []
    g = Graph()
    g.parse(os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
    for ind, (sub, pred, obj) in enumerate(g):
        if substyle in obj:
            stylization = sub.split('#')[1]
            stylization_to_translate = stylization.replace('_', ' ')
            substyle_ = sub.split('#')[1]
            substyle_to_translate = substyle_.replace('_', ' ')

            while True:
                try:
                    translator = Translator()
                    substyle_translated = translator.translate(substyle_to_translate, dest='ru')
                except:
                    continue
                else:
                    break
            mini = (substyle_, substyle_translated.text)
            size_stylizations.append(mini)
    if size_stylizations == []:
        return False
    return size_stylizations