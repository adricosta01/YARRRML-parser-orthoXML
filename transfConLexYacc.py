import ply.lex as lex;
import ply.yacc as yacc;

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
    ,"SUBJECT", "PREFIXES", "CONDITION", "PARAMETERS", "FUNCTION", "MAPPING"
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

duplas_po = {}

def p_yaml(p):
    '''yaml : prefixes mappings'''

def p_prefixes(p):
    '''prefixes : PREFIXES sources'''

def p_sources(p):
    '''sources : KEY VALUE
               | sources KEY VALUE
               | '''
    
def p_mappings(p):
    '''mappings : MAPPINGS mapping_entries'''

def p_mapping_entries(p):
    '''mapping_entries : key
                       | mapping_entries key'''

def p_key(p):
    '''key : KEY SUBJECT VALUE PREDICATEOBJECT predicateobject '''
    subject = p[3]
    po = p[5]
    print(f"Subject: {subject}")
    for pred, obj in po.items():
        print(f"  Predicate: {pred} -> Object: {obj}")
        resultado.append(Resultado("PO", (subject, pred, obj)))

def p_predicateobject(p):
    '''predicateobject : HYPHEN LBRACKET VALUE COMMA VALUE RBRACKET
                       | predicateobject HYPHEN LBRACKET VALUE COMMA VALUE RBRACKET
                       | '''
    
    if len(p) == 1:
        p[0] = {}
    elif len(p) == 7:
        p[0] = {p[3]: p[5]}
    else:
        p[0] = p[1]
        p[0][p[4]] = p[6]

parser = yacc.yacc()

def pruebaSintactico(data):
    parser.parse(data)


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
    data = ""
    with open("ficheros/mapping.yaml", "r", encoding="utf-8") as file:
        data = file.read()
    pruebaSintactico(data)
