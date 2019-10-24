#!/usr/bin/env python

#######################################
# CI3715 Traductores e Interpretadores
# Entrega 2. 
# Fernando Gonzalez 08-10464
# Kevin Mena 13-10869
#######################################
import ply.yacc as yacc
from g_lexer import *
from g_AbsSyntaxTree import *



        


#WRITE RULES BELOW

# Regla para definir las instrucciones permitidas por Setlan.
def p_inst(p):
    print('HOLAAAA')
    if (len(p)==4):
        if (p[1]=='|['):
            p[0] = Block(None,p[0])

    elif (len(p)==5):
        if (p[1]=='|['):
            p[0] = Block(p[2],p[3])



# Regla para poder encontrar los errores sintácticos.
def p_error(p):
    global parser_error
    if (p is not None):
        msg = "Error de sintaxis. Se encontró token " + str(p.value) + " en la linea "
        msg += str(p.lineno) + ", columna " + str(find_column(p.lexer.lexdata,p))
    else:
        msg = "Error de sintaxis al final del archivo"
    print (msg)
    parser_error = True

# Variable global del primer error del parser si existe.
global parser_error
parser_error = False

# Funcion que se encarga de construir el parser.
def parser_builder(meta_program):
    parser = yacc.yacc(debug=True)
    out = parser.parse(meta_program)
    if not(parser_error):
        return (out.toString(0))