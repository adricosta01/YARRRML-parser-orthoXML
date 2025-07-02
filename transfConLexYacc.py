import ply.lex as lex;
import ply.yacc as yacc;
import funcionesAuxiliares as funcAux;
import argparse;

destination = ""

class Resultado:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __str__(self):
        return f"valor={self.valor}, tipo={self.tipo}"

resultado = []

tokens = (
    'KEY', 'VALUE','LBRACKET', 'RBRACKET', 'COMMA', 'HYPHEN','PREDICATE',
    'PREDICATEOBJECT', 'OBJECT', 'MAPPINGS',"SUBJECT", "PREFIXES", 
    "CONDITION", "PARAMETERS", "FUNCTION", "MAPPING"
)

last_indentation = 0
indent_stack = []


def t_PREFIXES(t):
    r'prefixes:[\s\n ]'
    t.value = t.value[:-1]
    return t

def t_MAPPINGS(t):
    r'mappings:[\s\n ]'
    t.value = t.value[:-1]
    return t

def t_SUBJECT(t):
    r'(s:|subject:)[\s\n ]'
    t.value = t.value[:-1]
    return t

def t_PREDICATEOBJECT(t):
    r'(po:|predicateobjects:)[\s\n ]'
    t.value = t.value[:-1]
    return t

def t_PREDICATE(t):
    r'(p:|predicate:)[\s\n ]'
    t.value = t.value[:-1]
    return t

def t_OBJECT(t):
    r'(o:|object:)[\s\n ]'
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
    r'parameters:[\s\n ]'
    t.value = t.value[:-1]
    return t

def t_KEY(t):
    r'[a-zA-Z0-9_-]*:[\s\n ]'
    t.value = t.value[:-1]
    return t

def t_VALUE(t):
    r'([a-zA-Z:/.@~_0-9#]+)|(\'[^\']+\')'
    t.value = t.value.replace("'", "").strip()
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

duplas_po = {}

def p_yaml(p):
    '''yaml : prefixes mappings'''
    p[0] = funcAux.cabecera()
    p[0] += p[2]
    p[0] += funcAux.orthoFinal()

def p_prefixes(p):
    '''prefixes : PREFIXES sources'''

def p_sources(p):
    '''sources : KEY VALUE
               | sources KEY VALUE
               | '''
    
def p_mappings(p):
    '''mappings : MAPPINGS mapping_entries'''
    p[0] = p[2][0]+p[2][1]+p[2][2] #Ordenamos

def p_mapping_entries(p):
    '''mapping_entries : key
                       | mapping_entries key'''
    p[0] = ["","",""]
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0][0] = p[1][0] + p[2][0] #Arch2Class
        p[0][1] = p[1][1] + p[2][1] #Arch2Prop
        p[0][2] = p[1][2] + p[2][2] #Arch2Rel

def p_key(p):
    '''key : KEY SUBJECT VALUE PREDICATEOBJECT predicateobject '''
    subject = p[3]
    po = p[5]
    
    p[0] = ["","",""]

    label_id = ""
    class_id = ""
    for pred, obj in po: #Detectamos la clase y guardamos el class_id
        if pred[0] == 'a':
            class_id = obj
        elif pred[0] == "rdfs:label":
            label_id = obj
        if label_id != "" and class_id != "":
            break

    if class_id == "":
        destination.write("Error no hay clase en el mapeo con subject "+p[3])
        print("Error no hay clase en el mapeo con subject "+p[3])
        raise SyntaxError("Error en la producción de 'predicateobject': debe haber al menos una regla entidad.")

    
    if label_id != "": #Si hay etiqueta generamos el Arch2Class correspondiente
        p[0][0] = funcAux.generarArch2ClassLabel(subject, class_id, label_id)
    else:
        p[0][0] = funcAux.generarArch2Class(subject, class_id)

    for pred, obj in po:
        if pred[0] != 'a' and pred[0] != "rdfs:label":
            if isinstance(obj, list):
                p[0][2] += funcAux.generarArch2Rel(subject, class_id, pred[0], obj[1], obj[0])
            else:
                p[0][1] += funcAux.generarArch2Prop(subject, class_id, pred[0], obj)

def p_predicateobject(p):
    '''predicateobject : HYPHEN LBRACKET VALUE COMMA VALUE RBRACKET
                       | HYPHEN PREDICATE VALUE OBJECT VALUE
                       | HYPHEN PREDICATE VALUE OBJECT relacion
                       | predicateobject HYPHEN PREDICATE VALUE OBJECT VALUE
                       | predicateobject HYPHEN PREDICATE VALUE OBJECT relacion
                       | predicateobject HYPHEN LBRACKET VALUE COMMA VALUE RBRACKET
                       | '''
    
    if len(p) == 1: # Si no hay nada devuelvo lista vacía
        p[0] = []
    elif len(p) == 6: # Caso - p: VALOR - o: VALOR || - p: VALOR - o: relacion
        p[0] = [(p[3], p[5])]
    elif len(p) == 7: 
        if p[3] == "p:": # Caso predicateobject - p: VALOR - o: VALOR || -p: VALOR -o: relacion
            p[0] = p[1]
            p[0].append(([p[4]],p[6]))
        else:                   
            p[0] = [(p[3],p[5])] # Caso - po: [VALOR, VALOR]
    else: 
        p[0] = p[1] #Caso predicateobject - po: [VALOR, VALOR]
        p[0].append(([p[4]],p[6]))

def p_relacion(p):
    '''relacion : MAPPING VALUE CONDITION FUNCTION VALUE PARAMETERS HYPHEN LBRACKET VALUE COMMA VALUE COMMA VALUE RBRACKET HYPHEN LBRACKET VALUE COMMA VALUE COMMA VALUE RBRACKET'''
    
    p[0] = [p[11], p[19]]

compilador = yacc.yacc()

def pruebaLexico(data):
    global resultado
    lexer.input(data)

    resultado.clear()
    while True:
        tok = lexer.token()
        if not tok:
            break
        resultado.append(Resultado(tok.type, tok.value))
    return resultado


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transform a yarrrml file into an _ file.')
    parser.add_argument('source', type=argparse.FileType('r'), help='yarrrml source file to be transformed')
    parser.add_argument('destination', type=argparse.FileType('w'), help='file that will contain the result')
    parser.add_argument('--debug', help='print debug messages', action='store_true')
    

    args = parser.parse_args()
    source = args.source
    destination = args.destination
    
    yaml = source.read()


    orthoXML = compilador.parse(yaml)
    destination.write(orthoXML)

