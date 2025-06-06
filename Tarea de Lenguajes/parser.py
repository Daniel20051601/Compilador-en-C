# parser.py
import ply.yacc as yacc
from lexer import tokens, build_lexer

# Precedencia de operadores para evitar ambigüedades:
# 1) * y / (izquierda)
# 2) + y - (izquierda)
# 3) Relacionales (<, >, <=, >=, ==, !=) (izquierda)
# 4) Asignación = (derecha)
precedence = (
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NEQ'),
    ('right', 'EQUALS'),
)

# -----------------------------------
# Definición de la gramática de C (subconjunto mejorado)
# -----------------------------------

def p_program(p):
    '''program : function_list'''
    pass

def p_function_list(p):
    '''function_list : function_list function
                     | function'''
    pass

# Función sin parámetros: int main() { ... }
def p_function(p):
    '''function : TYPE ID LPAREN RPAREN compound_stmt'''
    pass

def p_compound_stmt(p):
    '''compound_stmt : LBRACE stmt_list RBRACE'''
    pass

def p_stmt_list(p):
    '''stmt_list : stmt_list stmt
                 | empty'''
    pass

def p_stmt(p):
    '''stmt : declaration
            | if_stmt
            | return_stmt
            | expression_stmt'''
    pass

# Declaración sin inicialización: int x;
# Declaración con inicialización: int x = expr;
def p_declaration(p):
    '''declaration : TYPE ID SEMICOLON
                   | TYPE ID EQUALS expression SEMICOLON'''
    pass

# If / If-Else
def p_if_stmt(p):
    '''if_stmt : IF LPAREN expression RPAREN stmt
               | IF LPAREN expression RPAREN stmt ELSE stmt'''
    pass

# Return
def p_return_stmt(p):
    '''return_stmt : RETURN expression SEMICOLON'''
    pass

# Expresión seguida de punto y coma
def p_expression_stmt(p):
    '''expression_stmt : expression SEMICOLON'''
    pass

# Expresiones
def p_expression_assign(p):
    '''expression : ID EQUALS expression'''
    pass

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    pass

def p_expression_relop(p):
    '''expression : expression LT expression
                  | expression LE expression
                  | expression GT expression
                  | expression GE expression
                  | expression EQ expression
                  | expression NEQ expression'''
    pass

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    pass

def p_expression_number(p):
    'expression : NUMBER'
    pass

def p_expression_id(p):
    'expression : ID'
    pass

def p_empty(p):
    'empty :'
    pass

# -----------------------------------
# Manejo de errores sintácticos
# -----------------------------------
def p_error(p):
    if p:
        print(f"[Syntax Error] Línea {p.lineno}: token inesperado '{p.value}'")
        # Descarta tokens hasta punto y coma o llave de cierre para intentar recuperar
        while True:
            tok = parser.token()
            if not tok or tok.type in ('SEMICOLON', 'RBRACE'):
                break
        parser.errok()
    else:
        print("[Syntax Error] Fin de archivo inesperado")

# Construye el parser
parser = yacc.yacc()

def parse_code(data):
    lexer = build_lexer()
    parser.parse(data, lexer=lexer)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python parser.py <archivo.c>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: no se encuentra el archivo '{filename}'")
        sys.exit(1)

    parse_code(data)
