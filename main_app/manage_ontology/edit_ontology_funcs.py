import os
from pathlib import Path
from rdflib import URIRef, Graph

BASE_DIR = Path(__file__).resolve().parent.parent

def add_new_element(a):
    ontology = Graph()
    ontology.parse(os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
    subject_name = a['sub']
    type_value = a['type']
    predicat_name = a['pred']
    object_name = a['obj']

    s_uid = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + subject_name)
    type_uid = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
    o_uid = URIRef("http://www.w3.org/2002/07/owl#" + object_name)
    type_value_uid = URIRef("http://www.w3.org/2002/07/owl#" + type_value)
    if predicat_name == 'subClassOf':
        p_uid = URIRef("http://www.w3.org/2000/01/rdf-schema#subClassOf")
    elif predicat_name == 'type':
        p_uid = type_uid
    else:
        p_uid = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + predicat_name)
    ontology.add((s_uid, type_uid, type_value_uid))
    ontology.serialize(format="xml", destination=os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))

    ontology.add((s_uid, p_uid, o_uid))
    ontology.serialize(format="xml", destination=os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))

    inverse_uid = URIRef("http://www.w3.org/2002/07/owl#inverseOf")

    for s, p, o in ontology.triples((None, inverse_uid, None)):
        inverse_sub = s
        inverse_obj = o
    if str(inverse_sub).split('#')[1] == predicat_name:
        ontology.add((o_uid, inverse_obj, s_uid))
        ontology.serialize(format="xml", destination=os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
    elif str(inverse_obj).split('#')[1] == predicat_name:
        ontology.add((o_uid, inverse_sub, s_uid))
        ontology.serialize(format="xml", destination=os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))


def add_new_triple(a):
    ontology = Graph()
    ontology.parse(os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
    object_name = a['obj']
    predicat_name = a['pred']
    subject_name = a['sub']
    s_uid = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + subject_name)
    if predicat_name == 'subClassOf':
        p_uid = URIRef("http://www.w3.org/2000/01/rdf-schema#" + predicat_name)
    else:
        p_uid = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + predicat_name)
    o_uid = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + object_name)
    ontology.add((s_uid, p_uid, o_uid))
    ontology.serialize(format="xml", destination=os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))


def delete_all_triples_with_elem(a):
    ontology = Graph()
    ontology.parse(os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
    element_name = a['element_name']
    element_uriref = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + element_name)
    if (element_uriref, None, None) in ontology:
        for s, p, o in ontology.triples((element_uriref, None, None)):
            ontology.remove((s, p, o))

    ontology.serialize(format="xml", destination=os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))


def delete_one_triple(a):
    ontology = Graph()
    ontology.parse(os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))
    object_name = a['object_name']
    predicat_name = a['predicat_name']
    subject_name = a['subject_name']
    s_uid = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + subject_name)
    p_uid = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + predicat_name)
    o_uid = URIRef("http://www.semanticweb.org/masha/ontologies/2022/9/Сostumes.owl#" + object_name)
    ontology.remove((s_uid, p_uid, o_uid))
    ontology.serialize(format="xml", destination=os.path.join(os.path.dirname(BASE_DIR), "CostumesRDF.owl"))