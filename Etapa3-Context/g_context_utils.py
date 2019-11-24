import sys
from g_utils import color

def PrintSymbolTable(c_auxScopes, identation):
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
    margin_table = ' '*(((longest_val+longest_type)//2)+7)

    print(identation+color.BLUWHITE +margin_table+ "SYMBOLS TABLE"+margin_table+ color.END)
    scope = c_auxScopes[0]
    for i in scope:
        if len(scope[i].s_value) < longest_val:
            if len(scope[i].s_value) % 2 == 0:
                print(identation+color.BLUE+'Variable '+color.END+' '*((longest_val-len(scope[i].s_value)))+scope[i].s_value+\
                    ' '+color.BLUE+'|'+color.END+ ' '+ color.BLUE+'Type '+color.END+scope[i].s_type)
            else:
                print(identation+color.BLUE+'Variable '+color.END+' '*((longest_val-len(scope[i].s_value)))+scope[i].s_value+\
                    ' '+color.BLUE+'|'+color.END+ ' '+ color.BLUE+'Type '+color.END+scope[i].s_type)

        else:
            if (scope[i].is_array):
                print(identation+color.BLUE+'Variable '+color.END+scope[i].s_value+' ' +color.BLUE+'|'+color.END+ ' '+ \
                    color.BLUE+'Type '+color.END+scope[i].s_type + '[' + str(scope[i].array_indexes[0]) + '..' + str(scope[i].array_indexes[1]) + ']'+ ' int')
            else:
                print(identation+color.BLUE+'Variable '+color.END+scope[i].s_value+' ' +color.BLUE+'|'+color.END+ ' '+ \
                    color.BLUE+'Type '+color.END+scope[i].s_type)
    c_auxScopes.pop(0)