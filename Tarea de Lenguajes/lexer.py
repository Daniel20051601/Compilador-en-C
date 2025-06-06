# lexer.py
import ply.lex as lex

# Definición de palabras reservadas de C (subconjunto)
reserved = {
    'int':    'TYPE',
    'float':  'TYPE',
    'if':     'IF',
    'else':   'ELSE',
    'return': 'RETURN'
}

# Lista de tokens
tokens = [
    'ID', 'NUMBER',
    # Operadores aritméticos
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    # Operador de asignación
    'EQUALS',
    # Operadores relacionales
    'LT', 'GT', 'LE', 'GE', 'EQ', 'NEQ',
    # Delimitadores
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'SEMICOLON', 'COMMA'
] + list(reserved.values())

# Reglas para tokens simples (símbolos)
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_EQUALS    = r'='

t_LT        = r'<'
t_GT        = r'>'
t_LE        = r'<='
t_GE        = r'>='
t_EQ        = r'=='
t_NEQ       = r'!='

t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_SEMICOLON = r';'
t_COMMA     = r','

# Ignorar espacios y tabs
t_ignore = ' \t'

# Manejo de saltos de línea para contar líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Identificadores y palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Revisa si es palabra reservada
    return t

# Números (enteros y flotantes)
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

# Comentarios estilo C (/* ... */)
def t_comment(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass  # Ignora el comentario

# Comentarios de línea (//...)
def t_comment_line(t):
    r'//.*'
    pass

# Error léxico: símbolo no reconocido
def t_error(t):
    print(f"[Lexical Error] Línea {t.lexer.lineno}: símbolo no reconocido '{t.value[0]}'")
    t.lexer.skip(1)

# Construye el lexer
def build_lexer(**kwargs):
    lexer = lex.lex(**kwargs)
    lexer.lineno = 1
    return lexer

if __name__ == "__main__":
    # Prueba rápida del lexer por consola
    data = ''
    print("Ingresa código C (Ctrl+D para terminar):")
    try:
        while True:
            line = input()
            data += line + '\n'
    except EOFError:
        pass

    lexer = build_lexer()
    lexer.input(data)
    for tok in lexer:
        print(f"{tok.type}({tok.value}) en línea {tok.lineno}")
