#######################################
# CI3715 Traductores e Interpretadores
# Entrega 4. 
# Fernando Gonzalez 08-10464
# Kevin Mena 13-10869
#######################################

import sys
from g_utils import color

# En este File reposa el metodo de impresion para las tablas
# de simbolos, el cual sera llamado desde el arbol sintactico
# para decorarlo.

def PrintSymbolTable(c_auxScopes, identation):
    """ Definicion del metodo [PrintSymbolTable], el cual se encarga del recorrido,
    interpretacion y posterior impresion de la pila de tabla de hash conocida como
    scope en forma de tablas de simbolos amigables a la lectura en cada declaracion
    de gusb. 
    
    recibe: c_auxScopes : Estructura de pila que contiene cada tabla de hash generada por gusb.
            identation : identacion que presentara la tabla en la impresion.
    """    
    c_auxScopes.pop(0)
    values =[]
    types =[]
    for scope in c_auxScopes:
        for var in scope:
            values.append(scope[var].s_value)
            types.append(scope[var].s_type)
        
    sortpre =sorted(values, key=len)
    sorttyp = sorted(types, key=len)
    longest_val = len(sortpre[-1])
    longest_type = len(sorttyp[-1])
    margin_table = ' '*(((longest_val+longest_type)//2)+8)

    print(identation+color.BLUWHITE +margin_table+ "SYMBOLS TABLE"+margin_table+ color.END)
    scope = c_auxScopes[0]
    for i in scope:
        if len(scope[i].s_value) < longest_val:
            if len(scope[i].s_value) % 2 == 0:
                print(' '+identation+color.BLUE+'Variable '+color.END+' '*((longest_val-len(scope[i].s_value)))+scope[i].s_value+\
                    ' '+color.BLUE+'|'+color.END+ ' '+ color.BLUE+'Type '+color.END+scope[i].s_type)
            else:
                print(' '+identation+color.BLUE+'Variable '+color.END+' '*((longest_val-len(scope[i].s_value)))+scope[i].s_value+\
                    ' '+color.BLUE+'|'+color.END+ ' '+ color.BLUE+'Type '+color.END+scope[i].s_type)
        else:
            if (scope[i].is_array):
                print(' '+identation+color.BLUE+'Variable '+color.END+scope[i].s_value+' ' +color.BLUE+'|'+color.END+ ' '+ \
                    color.BLUE+'Type '+color.END+scope[i].s_type + '[' + str(scope[i].array_indexes[0]) + '..' + str(scope[i].array_indexes[1]) + ']')
            else:
                print(' '+identation+color.BLUE+'Variable '+color.END+scope[i].s_value+' ' +color.BLUE+'|'+color.END+ ' '+ \
                    color.BLUE+'Type '+color.END+scope[i].s_type)
    print('\n')



def PrintFinalValueTable(c_auxScopes,identation):
    """ Definicion del metodo [PrintFinalValueTable], el cual se encarga del recorrido,
    interpretacion y posterior impresion de la pila de tabla de hash conocida como
    scope en forma de tablas de simbolos amigables a la lectura en cada declaracion
    de gusb para mostrar la evolucion de sus valores en cada declaracion. 
    
    recibe: c_auxScopes : Estructura de pila que contiene cada tabla de hash generada por gusb.
            identation : identacion que presentara la tabla en la impresion.
    """    
    ini = 0
    c_auxScopes.pop(0)
    values =[]
    types =[]
    for scope in c_auxScopes:
        for var in scope:
            values.append(scope[var].s_value)
            types.append(scope[var].s_type)
        
    sortpre =sorted(values, key=len)
    sorttyp = sorted(types, key=len)
    longest_val = len(sortpre[-1])
    longest_type = len(sorttyp[-1])
    margin_table = ' '*(((longest_val+longest_type)//2)+8)
    print(identation+color.REWHITE +margin_table+ "FINAL VALUES TABLE"+margin_table+ color.END)

    for scope in c_auxScopes:
        for i in scope:
            if (len(str(scope[i].s_asignvalue)) < longest_val):
                if len(str(scope[i].s_asignvalue)) % 2 == 0:
                    print('     '+identation+color.RED+'Variable '+color.END+' '*((longest_val-len(str(scope[i].s_value))))+str(scope[i].s_asignvalue)+\
                        ' '+color.RED+'|'+color.END+ ' '+ color.RED+'Value '+color.END+str(scope[i].s_asignvalue))
                else:
                    print('     '+identation+color.RED+'Variable '+color.END+' '*((longest_val-len(str(scope[i].s_value))))+str(scope[i].s_asignvalue)+\
                        ' '+color.RED+'|'+color.END+ ' '+ color.RED+'Value '+color.END+str(scope[i].s_asignvalue))
            else:
                if (scope[i].is_array):
                    print('     '+identation+color.RED+'Variable '+color.END+str(scope[i].s_value)+' ' +color.RED+'|'+color.END+ ' '+ \
                        color.RED+'Value '+color.END+str(scope[i].s_asignvalue))
                else:
                    print('     '+identation+color.RED+'Variable '+color.END+str(scope[i].s_value)+' ' +color.RED+'|'+color.END+ ' '+ \
                        color.RED+'Value '+color.END+str(scope[i].s_asignvalue))
    print('\n')