#######################################
# CI3715 Traductores e Interpretadores
# Entrega 3. 
# Fernando Gonzalez 08-10464
# Kevin Mena 13-10869
#######################################

import sys, re
from context_utils import *
from g_utils import *
from g_AbsSyntaxTree import *

# En este File reposa las clases y metodos relativos a
# aumentar y enriquecer Arbol Sintactico de nuestro programa
# con informacion de contexto y tabla de simbolos.

class ContextSymbol():
    """ Definicion del objeto [ContextSymbol], el cual representa la estructura de un simbolo
    a agregar en cada una de las tablas de hash de nuestra pila.

    inicializa con: 
            s_type : almacena el tipaje de la hoja que generara el simbolo.
            s_value : identificador o valor de la hoja que generara el simbolo.
            s_asignvalue : valor del simbolo si la hoja es de tipo Variable.
            is_index : almacena si el valor de la hoja es usado como contador de un loop.
            is_array : almacena si la hoja es de tipo arreglo.
    """
    def __init__(self, s_value, s_type):
        self.s_type = s_type 
        self.s_value = s_value 
        self.s_asignvalue = None 
        self.is_index = None 
        self.is_array = False
        self.array_indexes = []


class SyntaxTreeContext:
    """ Definicion del objeto [SyntaxTreeContext], el cual representa una estructura
    de pila conformada por tablas de Hash (en python, la estructura diccionario es,
    en realidad, el build in de una tabla de hash), de modo que crearemos una pila
    de diccionarios.

    inicializa con: 
            c_scopes : lista que se comportara a modo de pila para almacenar los diccionarios.
            c_secScopes : pila auxiliar para operaciones sobre la c_scopes.
            c_currentLine : entero que representa el numero de linea en proceso.
    """
    def __init__(self):
        self.c_scopes = []
        self.c_secScopes = []
        self.c_currentLine = 1


    def ExpressionAnalizer(self, expression):
        for child in expression.childs:
            if (child.p_type == 'BooleanOperator'):
                oprator1 = child.childs[0]
                oprator2 = child.childs[1]
                type1 = self.ExpressionAnalizer(oprator1)
                type2 = self.ExpressionAnalizer(oprator2)
                if (type1 != type2 != 'bool'):
                    print("[Context Error] line " + str(self.c_currentLine) + '. Boolean operator wrong type.')
                    sys.exit(0)
                else:
                    return 'bool'
            
            elif(child.p_type == 'UnaryBooleanOperator'):
                operator0 = child.childs[0]
                type0 = self.ExpressionAnalizer(operator0)

                if(type0 != 'bool'):
                    print("[Context Error] line " + str(self.c_currentLine) +'. Boolean operator wrong type.')
                    sys.exit(0)
                else:
                    return 'bool'

            elif (child.p_type == 'RelationalOperator'):
                oprator1 = child.childs[0]
                oprator2 = child.childs[1]
                type1 = self.ExpressionAnalizer(oprator1)
                type2 = self.ExpressionAnalizer(oprator2)
                if (child.p_value != '!=' and child.p_value != '==' and \
                    child.p_value != '<' and child.p_value != '>' and \
                    child.p_value != '<=' and child.p_value != '>='):
                    if (type1 != 'int' or type2 != 'int'):
                        print("[Context Error] line " + str(self.c_currentLine) +'. Relational operator wrong type.')
                        sys.exit(0)
                if (type1 != type2):
                    print("[Context Error] line " + str(self.c_currentLine) +'. Relational operator wrong type.')
                    sys.exit(0)
                else:
                    return "bool"

            elif(child.p_type == 'AritmeticOperator'):
                oprator1 = child.childs[0]
                oprator2 = child.childs[1]
                type1 = self.ExpressionAnalizer(oprator1)
                type2 = self.ExpressionAnalizer(oprator2)
                if (type1 != type2 != 'int'):
                    print("[Context Error] line " + str(self.c_currentLine) +'. Aritmetic operator wrong type.')
                    sys.exit(0)
                else:
                    return 'int'
            
            elif(child.p_type == 'UnaryAritmeticOperator'):
                operator0 = child.childs[0]
                type0 = self.ExpressionAnalizer(operator0)

                if(type0 != 'int'):
                    print("[Context Error] line " + str(self.c_currentLine) +'. Aritmetic operator wrong type.')
                    sys.exit(0)
                else:
                    return 'int'

            elif(child.p_type == 'ArrayExpression'):
                if(len(child.childs) > 1):
                    operator1 = child.childs[0]
                    type1 = self.ExpressionAnalizer(operator1)

                    if(type1 != 'int'):
                        print("[Context Error] line " + str(self.c_currentLine) +'. Array expression wrong type.')
                        sys.exit(0)
                    else:
                        return child.c_type
                    ##### FALTA VER SI EL ELEMENTO ESTA DENTRO DEL RANGO DEL ARREGLO
                else:
                    operator1 = child.childs[0]
                    operator2 = child.childs[1]
                    type1 = self.ExpressionAnalizer(operator1)
                    type2 = self.ExpressionAnalizer(operator2)

                    if(type1 != type2 != 'int'):
                        print("[Context Error] line " + str(self.c_currentLine) +'. Array expression wrong type.')
                        sys.exit(0)
                    else:
                        return child.c_type
                    ##### FALTA VER SI EL ELEMENTO 1 ESTA DENTRO DEL RANGO DEL ARREGLO

            elif(child.p_type == 'ArrayOperator'):
                operator1 = child.childs[0]
                type1 = self.CheckId(operator1)

                if(not type1.c_array):
                    print("[Context Error] line " + str(self.c_currentLine) +'. Array operation invalid or variable not array.')
                    sys.exit(0)
                return type1.c_type

            elif(child.p_type == 'Terminal'):
                if (len(child.childs)>0):
                    for h in child.childs:
                        t = self.ExpressionAnalizer(h)
                        return t
                else:
                    if (child.c_type == 'var'):
                        t = self.CheckId(child.lexeme)
                        return t.c_type
                    else:
                        return child.c_type
       

    def AppendContextSymbol(self, leaf, s_type, is_array):
        """ Definicion del metodo [AppendContextSymbol], el cual se encarga de la creacion del
        objeto simbolo el cual sera insertado en la tabla de hash (diccionario) que se encuentra
        en el tope de la pila.
        
        recibe: leaf : hoja a analizar.
                s_type : tipaje de la hoja.
                is_array : booleano si es un arreglo.
        """
        stack_top = self.c_scopes[0]
        if leaf.p_value in stack_top:
            print("[Context Error] Line " + str(self.c_currentLine) +'. Variable has been declared before.')
            sys.exit(0)
        
        new_type = s_type.p_value

        if(isinstance(new_type, SyntaxLeaf)):
            new_type = "array[" + str(s_type.p_value.childs[0]) + ".." + str(s_type.p_value.childs[1]) + "]"
        
        new_symbol = ContextSymbol(leaf.p_value, new_type)
        new_symbol.is_array = is_array

        if(is_array):
            new_symbol.array_indexes.append(s_type.p_value.childs[0])
            new_symbol.array_indexes.append(s_type.p_value.childs[1])
        
        stack_top[leaf.p_value] = new_symbol

        if ((len(leaf.childs))>0):
            for leaf in leaf.childs:
                if (leaf.p_type == 'Variable'):
                    is_array = self.CheckIfArray(s_type.childs[0].p_value)
                    self.AppendContextSymbol(leaf, s_type.childs[0], is_array)
                elif (leaf.p_type == 'Expression'):
                    t = self.ExpressionAnalizer(leaf)
                    if (t != s_type.p_value):
                        print("[Context Error] line " + str(self.c_currentLine) + 'Variable types does not match.')
                        sys.exit(0)
                    else:
                        stack_top[leaf.p_value].s_asignvalue = leaf

    def CreateContextScope(self, leaf):
        """ Definicion del metodo [CreateContextScope], el cual se encarga de hacer el manejo del
        metodo de creacion de simbolos en la tabla.
        
        recibe: leaf : hoja a analizar.
        """
        leaf_type = leaf.p_value

        for child in leaf.childs:
            if (child.p_type == 'Declare'):
                self.c_currentLine += 1
                self.CreateContextScope(child)
            elif (child.p_type == 'Variable'):
                # Verificar si la variable es arreglo o no
                is_array = self.CheckIfArray(leaf_type.p_value)
                self.AppendContextSymbol(child, leaf_type, is_array)
            # elif child.p_type == 'Array':
            #     p_type = self.getType(child)
            #     self.getArrayType(child)

    def ContentAnalyzer(self, content):
        if(len(content.childs) > 0):
            for leaf in content.childs:
                if(leaf != ';'):
                    if(leaf.p_type == "Instruction"):
                        self.InstructionAnalyzer(leaf)
                    elif(leaf.p_type == "Block"):
                        self.c_currentLine+=1
                        self.ContextAnalyzer(leaf)
                        self.c_scopes.pop(0)
                    elif(leaf.p_type == "Content"):
                        self.c_currentLine+=1
                        self.ContentAnalyzer(leaf)
    
    def InstructionAnalyzer(self, instruction):
        if(len(instruction.childs) > 0):
            for leaf in instruction.childs:
                if (leaf.p_type  == 'Asign'):
                    self.c_currentLine += 1

                    # Verificar que la variable este declarada
                    var = self.CheckId(leaf.p_value)

                    if (var.is_index):
                        print("[Context Error] line " + str(self.c_currentLine) + ". tries to modify varible" + leaf.p_value + "of iteration.")
                        sys.exit(0)
                    
                    # Verificar si la variable es de tipo arreglo o no
                    exp_type = self.AssignationAnalyzer(leaf.childs[0])

                    if(not var.is_array):
                        if (var.s_type != exp_type):
                            print("[Context Error] line " + str(self.c_currentLine) + ". Different variable types.")
                            sys.exit(0)
                    else:

                        if(exp_type != 'int'):
                            print("[Context Error] line " + str(self.c_currentLine) + ". Trying to asign array other type different than Integer.")
                            sys.exit(0)
                        
                        count = self.CheckCountExp(leaf.childs[0])

                        if(count != (var.array_indexes[1] - var.array_indexes[0]) + 1):
                            print("[Context Error] line " + str(self.c_currentLine) + ". Trying to asign more elements than range of Array.")
                            sys.exit(0)

                elif(leaf.p_type == 'Conditional'):
                    self.c_currentLine += 1
                    for child in leaf.childs:
                        if (child.p_type == 'Content'):
                            self.ContextAnalyzer(child)
                        else:
                            t = self.ExpressionAnalizer(child)
                            if (t != 'bool'):
                                print("[Context Error] line " + str(self.c_currentLine) + ". Conditional variables are of a different types.")
                                sys.exit(0) 

                elif (leaf.p_type == 'DoLoop'):
                    self.c_currentLine += 1
                    child = leaf.p_value
                    oprator1 = child.childs[0]
                    oprator2 = child.childs[1]
                    type1 = self.ExpressionAnalizer(oprator1)
                    type2 = self.ExpressionAnalizer(oprator2)
                    if (child.p_value != '!=' and child.p_value != '==' and \
                        child.p_value != '<' and child.p_value != '>' and \
                            child.p_value != '<=' and child.p_value != '>='):
                        if (type1 != 'int' or type2 != 'int'):
                            print("[Context Error] line " + str(self.c_currentLine) + ". Do variables are of a different types.")
                            sys.exit(0)
                    if (type1 != type2):
                        print("[Context Error] line " + str(self.c_currentLine) + ". Do variables are of a different types.")
                        sys.exit(0)
                    else:
                        t = 'bool'
                    if (t != 'bool'):
                        print("[Context Error] line " + str(self.c_currentLine) + ". Do variables are of a different types.")
                        sys.exit(0)
                    self.ContextAnalyzer(leaf.childs[0])

                else:
                    if (leaf.p_type =='Input' or leaf.p_type =='Output'):
                        self.c_currentLine += 1
                    self.ContextAnalyzer(leaf)                    

    def ContextAnalyzer(self, SyntaxTreeStructure):
        """ Definicion del metodo [ContextAnalyzer], el cual se encarga de revisar 
        linea a linea de forma recursiva todos los componentes del Arbol Sintactico
        generado por el parser.
        
        recibe: SyntaxTreeStructure : Estructura completa del arbol sintactico a analizar.
        """
        if SyntaxTreeStructure:
            if (len(SyntaxTreeStructure.childs) > 0):
                for leaf in SyntaxTreeStructure.childs:

                    if (leaf.p_type == 'Block'):
                        self.c_currentLine+=1
                        self.ContextAnalyzer(leaf)
                        self.c_scopes.pop(0)

                    elif (leaf.p_type == 'Declare'):
                        self.c_currentLine+=1
                        new_scope ={}
                        self.c_scopes.insert(0,new_scope)
                        self.CreateContextScope(leaf)
                        self.c_secScopes.append(self.c_scopes[0])

                    elif (leaf.p_type  == 'Content'):
                        self.c_currentLine+=1
                        self.ContentAnalyzer(leaf)
        else:
            print('[Context Error]: No SyntaxTreeStructure')

    def AssignationAnalyzer(self, assignation):

        if(len(assignation.childs) == 1):
            return self.ExpressionAnalizer(assignation.childs[0])
        else:
            type1 = self.ExpressionAnalizer(assignation.childs[0])

            type2 = self.AssignationAnalyzer(assignation.childs[1])

            if(type1 != type2):
                print("[Context Error] line " + str(self.c_currentLine) + ". Trying to asign list of expressions of different types.")
                sys.exit(0)
            
            return type1

    def CheckIfArray(self, id_type):
        if(isinstance(id_type, SyntaxLeaf)):
            return True
        else:
            return False
    
    def CheckCountExp(self, expression):
        if(len(expression.childs) > 1):
            return 1 + self.CheckCountExp(expression.childs[1])
        else:
            return len(expression.childs)

    def CheckId(self, id_var):
        if (len(self.c_scopes) > 0):
            for x in range(len(self.c_scopes)):
                if id_var in self.c_scopes[x]:
                    return self.c_scopes[x][id_var]
        
        print("[Context Error] line " + str(self.c_currentLine) +'. Variable ' + id_var + ' has not been declared before.')
        sys.exit(0)

    def PrintSymbolTable(self):
        values =[]
        types =[]
        for scope in self.c_secScopes:
            for var in scope:
                #print('hey',var)        
                #print('hey',scope[var].s_value,scope[var].s_type)        
                values.append(scope[var].s_value)
                types.append(scope[var].s_type)
            
        sortpre =sorted(values, key=len)
        sorttyp = sorted(types, key=len)
        longest_val = len(sortpre[-1])
        longest_type = len(sorttyp[-1])
        margin_table = ' '*(((longest_val+longest_type)//2)+4)

        print(color.BLUWHITE +margin_table+ "SYMBOL TABLE"+margin_table+ color.END)
        for scope in self.c_secScopes:
            for i in scope:
                if len(scope[i].s_value) < longest_val:
                    if len(scope[i].s_value) % 2 == 0:
                        print(color.BLUE+'Variable '+color.END+' '*((longest_val-len(scope[i].s_value)))+scope[i].s_value+\
                            ' '+color.BLUE+'|'+color.END+ ' '+ color.BLUE+'Type '+color.END+scope[i].s_type)
                    else:
                        print(color.BLUE+'Variable '+color.END+' '*((longest_val-len(scope[i].s_value)))+scope[i].s_value+\
                            ' '+color.BLUE+'|'+color.END+ ' '+ color.BLUE+'Type '+color.END+scope[i].s_type)

                else:
                    if re.match(r'array[[0-9]+\.\.[0-9]+]',scope[i].s_type):
                        print(color.BLUE+'Variable '+color.END+scope[i].s_value+' ' +color.BLUE+'|'+color.END+ ' '+ \
                            color.BLUE+'Type '+color.END+scope[i].s_type + ' int')
                    else:
                        print(color.BLUE+'Variable '+color.END+scope[i].s_value+' ' +color.BLUE+'|'+color.END+ ' '+ \
                            color.BLUE+'Type '+color.END+scope[i].s_type)