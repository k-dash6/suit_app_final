import os
from pathlib import Path
from kandinsky2 import get_kandinsky2
import ontor
from rdflib import Graph

BASE_DIR = Path(__file__).resolve().parent.parent


def save_image(image, folder_path, filename):
    image_path = os.path.join(folder_path, filename)
    image.save(image_path)


def update_images():
    # device = "cuda" if torch.cuda.is_available() else 'cpu'
    outfit_description_dict = get_outfits_descriptions()
    colors = ['red', 'orange', 'yellow', 'green', 'light blue', 'blue', 'purple', 'pink', 'white', 'black', 'gray',
              'brown', 'beige']
    save_folder = 'manage_ontology/static/manage_ontology/images/outfits'

    os.makedirs(save_folder, exist_ok=True)

    model = get_kandinsky2('cuda', task_type='text2img', cache_dir='/img', model_version='2.1',
                           use_flash_attention=False)
    for item in outfit_description_dict.items():
        for color in colors:
            color_postfix = f'in {color} color'
            images = model.generate_text2img(item[1] + color_postfix, num_steps=100,
                                             batch_size=1, guidance_scale=4,
                                             h=768, w=768, sampler='p_sampler', prior_cf_scale=4,
                                             prior_steps="5", )
            filename = f"{item[0]}_{color}.jpg"
            save_image(images[0], save_folder, filename)


def get_outfits_descriptions():
    g = Graph()
    g.parse(os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
    ontology = ontor.OntoEditor(os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"),
                              os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
    magic_list_3 = [p.name for p in ontology.get_elems()[3]]
    outfits_list = [element for element in magic_list_3 if 'outfit' in element]

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

    outfits_description_dict = {}

    for item in outfits_dict.items():
        if outfits_dict[item[0]]:
            outfits_description_dict[item[0]] = []
        for ind, (sub, pred, obj) in enumerate(g):
            if not '#' in sub:
                continue
            if sub.split('#')[1] in item[1] and 'has_product_' in pred and '#' not in obj:
                s = sub.split('#')[1][:-6]
                p = pred.split('#')[1].replace('_', ' ')
                o = obj
                outfits_description_dict[item[0]].append(s + ' ' + p + ' ' + o)

    description_prefix = 'On a white background: Costume on mannequin: '

    for item in outfits_description_dict.items():
        full_description = description_prefix + ' '.join(item[1])
        outfits_description_dict[item[0]] = full_description

    return outfits_description_dict
