from rdflib import Graph, URIRef, Literal, RDF, RDFS, OWL, XSD
from rdflib.term import _is_valid_uri as rdflib_is_valid_uri
from urllib.parse import quote, unquote
import yaml
import argparse
from funcionesAuxiliares import *

import re
import json

url_regex = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


SCHEMA = "1406106202578/orthoxml.xsd"
ONTOLOGIA = "1406106207741/OGO.owl"


# to find references ex: $(field_name)
REGEX_REFERENCES = re.compile('(\$\(.*?\))')
REGEX_UNREFERENCES = re.compile('\$\(.*?\)')
REGEX_REFERENCE_FIELD = re.compile('\$\((.*?)\)')

# Files default IRI's
DEFAULT_FILES_IRI = "http://example.org/{}"


YARRRML_KEYS = {
    'subjects': ['subjects', 's'],
    'mappings': ['mappings', 'mapping'],
    'predicateobjects': ['predicateobjects', 'predicateobject', 'po'],
    'predicates': ['predicates', 'predicate', 'p'],
    'objects': ['objects', 'object', 'o'],
    'value': ['value', 'v'],
    'parameters': ['parameters'],
    'condition': ['condition']
}


PREFIXES = {
    'rdfs:': str(RDFS),
    'rdf:': str(RDF),
    'owl:': str(OWL),
    'xsd:': str(XSD)
}

# Parser for RML YARRRML Syntax: http://rml.io/yarrrml/spec/


def main(source, destination, debug):
    try:
        mapping = yaml.safe_load(source)
        if debug:
            print('YARRRML Mapping Parsing: OK')
    except (yaml.parser.ParserError, yaml.scanner.ScannerError) as exception:
        print(f'YARRRML Mapping Syntax Error: {exception}')
        return
    orthoFile = cabecera(mapping)
    orthoFile += parse_to_file_ortho(mapping)
    orthoFile += orthoFinal()
    destination.write(orthoFile)
    print('End of transformation!')

def cabecera(rml_mapping):
    xml_template = f"""<?xml version="1.0" encoding="UTF-8" ?>
<Alignment>
<schemas><schema>{SCHEMA}</schema></schemas>
<xmls>{parse_sources(rml_mapping)}</xmls>
<ontotarget>{ONTOLOGIA}</ontotarget>"""
    return xml_template

def orthoFinal():
    return f"""
</Alignment>"""

def parse_sources(rml_mapping):
    sources = []
    for mapping_key, mapping in get_keys(rml_mapping, YARRRML_KEYS['mappings']).items():
        if 'sources' in mapping and mapping_key not in sources:
            archivo = mapping['sources'][0][0].split('~')[0]
            sources.append(archivo)
    xml_template = ""
    for source in sources:
        xml_template += f"""<xml>{source}<xml>
"""
    return xml_template

def parse_to_file_ortho(rml_mapping):
    prefixes = parse_prefixes(rml_mapping)
    resources  = parse_subjects(rml_mapping, prefixes)
    orthoFile = parse_predicate_objects(rml_mapping, resources, prefixes)
    return orthoFile


def parse_prefixes(rml_mapping):
    prefixes = PREFIXES
    if 'prefixes' in rml_mapping:
        for prefix, uri in rml_mapping['prefixes'].items():
            if prefix not in prefixes:
                prefixes[prefix] = uri
    return prefixes

def parse_subjects(rml_mapping, prefixes):
    resources = {}
    for mapping_key, mapping in get_keys(rml_mapping, YARRRML_KEYS['mappings']).items():
        if 'subject' in mapping and mapping_key not in resources:
            resources[mapping_key] = mapping['subject']
    return resources

def parse_predicate_objects(rml_mapping, resources, prefixes):
    orthoFile = ''
    orthoFileClass = ''
    orthoFileProp = ''
    orthoFileRel = ''

    for mapping_key, mapping in get_keys(rml_mapping, YARRRML_KEYS['mappings']).items():
        
        if mapping_key in resources:
            subject = resources[mapping_key]
            subjectR = ''
            classR_id = ''
            class_id = ''
            label_id = ''
            for predicate_object in get_keys(mapping, YARRRML_KEYS['predicateobjects']):
                
                if 'p' in predicate_object:
                
                    predicate = get_keys(predicate_object, YARRRML_KEYS['predicates'])
                    object = get_keys(predicate_object, YARRRML_KEYS['objects'])
                    if predicate == 'a':
                        class_id = object
                    elif predicate == 'rdfs:label':
                        label_id = object
                    elif 'mapping' in object:
                        condition = get_keys(object, YARRRML_KEYS['condition'])
                        for parameter in get_keys(condition, YARRRML_KEYS['parameters']):
                            if parameter[2] == 's':
                                subjectR = parameter[1]
                            elif parameter[2] == 'o':
                                classR_id = parameter[1]
                        orthoFileRel += generarArch2Rel(subject, class_id, predicate, classR_id, subjectR)
                    else:
                        orthoFileProp += generarArch2Prop(subject, class_id, predicate, object)

                elif predicate_object[0] == 'a':
                    class_id = predicate_object[1]

                elif predicate_object[0] == 'rdfs:label':
                    label_id = predicate_object[1]

                else:
                    orthoFileProp+=generarArch2Prop(subject, class_id, predicate_object[0], predicate_object[1])
            
            if label_id == '':
                orthoFileClass+=generarArch2Class(subject, class_id)
            else:
                orthoFileClass+=generarArch2ClassLabel(subject, class_id, label_id)
    
    orthoFile += orthoFileClass
    orthoFile += orthoFileProp
    orthoFile += orthoFileRel
    return orthoFile

def is_valid_uri(uri):
    return re.match(url_regex, uri) is not None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transform a yarrrml file into an _ file.')
    parser.add_argument('source', type=argparse.FileType('r'), help='yarrrml source file to be transformed')
    parser.add_argument('destination', type=argparse.FileType('w'), help='file that will contain the result')
    parser.add_argument('--debug', help='print debug messages', action='store_true')
    args = parser.parse_args()
    main(args.source, args.destination, args.debug)
