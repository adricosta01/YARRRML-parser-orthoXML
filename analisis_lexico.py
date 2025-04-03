import ply.lex as lex;

class Resultado:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __str__(self):
        return f"valor={self.valor}, tipo={self.tipo}"

resultado = []

tokens = (
    'KEY', 'VALUE', 'DASH', 'COLON', 'NEWLINE', 'LBRACKET', 'RBRACKET'
    ,'COMMA', 'HYPHEN', 'PREDICATE', 'PREDICATEOBJECT', 'OBJECT', 'MAPPINGS'
    ,"SUBJECT", "PREFIX", "CONDITION", "PARAMETERS", "FUNCTION", "MAPPING"
)

last_indentation = 0
indent_stack = []


def t_PREFIX(t):
    r'prefix:[\s\n ]'
    t.value = t.value[:-1]
    return t

def t_MAPPINGS(t):
    r'mappings:[\s\n ]'
    t.value = t.value[:-1]
    return t

def t_SUBJECT(t):
    r'subject:[\s\n ]'
    t.value = t.value[:-1]
    return t

def t_PREDICATEOBJECT(t):
    r'po:[\s\n ]'
    t.value = t.value[:-1]
    return t

def t_PREDICATE(t):
    r'p:[\s\n ]'
    t.value = t.value[:-1]
    return t

def t_OBJECT(t):
    r'o:[\s\n ]'
    t.value = t.value[:-1]
    return t

def t_MAPPING(t):
    r'mapping:[\s\n ]'
    t.value = t.value[:-1]
    return t

def t_CONDITION(t):
    r'condition:[\s\n ]'
    t.value = t.value[:-1]
    return t

def t_FUNCTION(t):
    r'function:[\s\n ]'
    t.value = t.value[:-1]
    return t

def t_PARAMETERS(t):
    r'paramters:[\s\n ]'
    t.value = t.value[:-1]
    return t

def t_KEY(t):
    r'[a-zA-Z0-9_-]*:[\s\n ]'
    t.value = t.value[:-1]
    return t

def t_VALUE(t):
    r'[a-zA-Z:/.@~_0-9#]+'
    t.value = t.value.strip()
    return t

def t_LBRACKET(t):
    r'\['
    return t

def t_RBRACKET(t):
    r'\]'
    return t

def t_COMMA(t):
    r','
    return t

def t_HYPHEN(t):
    r'-'
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Caracter ilegal: '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def prueba(data):
    global resultado

    lexer.input(data)

    resultado.clear()
    while True:
        tok = lexer.token()
        if not tok:
            break
        # print("lexema de "+tok.type+" valor "+tok.value+" linea "tok.lineno)
        resultado.append(Resultado(tok.type, tok.value))
    return resultado


if __name__ == '__main__':
    data = '''prefixes:
  ex: http://www.example.com/
  e: http://myontology.com/
  dbo: http://dbpedia.org/ontology/
  grel: http://users.ugent.be/~bjdmeest/function/grel.ttl#
mappings:
  cluster:
    subject: //orthologGroup
    po: 
      - [a, http://miuras.inf.um.es/ontologies/OGO.owl#Cluster]
  gene:
    subject: /orthoXML/species/database/genes/gene/@id
    po: 
      - [a, http://miuras.inf.um.es/ontologies/OGO.owl#Gene]
      - [http://miuras.inf.um.es/ontologies/OGO.owl#Identifier, ../@geneId]
  NCB1:
    subject: /orthoXML/species/@NCBITaxId
    po:
      - [a, http://um.es/ncbi.owl#NCBI_1]
      - [rdfs:label, /orthoXML/species/@name]

  resource:
    subject: /orthoXML/species/database/@name
    po: 
      - [a, http://miuras.inf.um.es/ontologies/OGO.owl#Resource]
  protein:
    subject: /orthoXML/species/database/genes/gene/@id
    po:
      - [a, http://miuras.inf.um.es/ontologies/OGO.owl#Protein]
      - [http://miuras.inf.um.es/ontologies/OGO.owl#Identifier, ../@protId]
  
  paralogous:
    subject: //paralogGroup
    po: 
      - [a, http://miuras.inf.um.es/ontologies/swit/OGO.owl#ParalogousCluster]
  '''
    prueba(data)
    with open("pruebaLexico.txt", "w") as archivo:
        for elemento in resultado:
            archivo.write(str(elemento)+ "\n")
