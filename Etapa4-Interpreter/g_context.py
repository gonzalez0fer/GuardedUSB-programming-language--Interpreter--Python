#######################################
# CI3715 Traductores e Interpretadores
# Entrega 4. 
# Fernando Gonzalez 08-10464
# Kevin Mena 13-10869
#######################################

import sys, re
from g_utils import *
from g_AbsSyntaxTree import *

# En este File reposa las clases y metodos relativos a
# aumentar y enriquecer Arbol Sintactico de nuestro programa
# con informacion de contexto y tabla de simbolos.

global_control_vars = []

class ContextSymbol():
    """ Definicion del objeto [ContextSymbol], el cual representa la estructura de un simbolo
    a agregar en cada una de las tablas de hash de nuestra pila.

    inicializa con: 
            s_type : almacena el tipaje de la hoja que generara el simbolo.
            s_value : identificador o valor de la hoja que generara el simbolo.
            s_asignvalue : valor del simbolo si la hoja es de tipo Variable.
            is_index : almacena si el valor de la hoja es usado como contador de un loop.
            array_indexes : almacena los index superior e inferior del arreglo.
            array_toList : almacena los enteros contenidos en el arreglo.
    """
    def __init__(self, s_value, s_type):
        self.s_type = s_type 
        self.s_value = s_value 
        self.s_asignvalue = None 
        self.is_index = None 
        self.is_array = False
        self.array_indexes = []
        self.array_toList = []


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
        self.c_auxScopes = []
        self.c_currentLine = 1


    def ExpressionAnalizer(self, expression):
        """ Definicion del metodo [ExpressionAnalizer], el cual se encarga de revisar 
        linea a linea de forma recursiva todos los componentes del Arbol Sintactico
        generado por el parser que se encuentran relacionados a las diversas estructuras 
        agrupadas bajo el termino [expresion] de gusb.
        
        recibe: expression : Estructura completa del arbol sintactico a analizar.
        """
        for child in expression.childs:
            if (child.p_type == 'BooleanOperator'):
                oprator1 = child.childs[0]
                oprator2 = child.childs[1]
                type1 = self.ExpressionAnalizer(oprator1)
                type2 = self.ExpressionAnalizer(oprator2)
                if (type1 != type2 != 'bool'):
                    print("[Context Error] line " + str(child.p_line) + ' column '+\
                        str(child.p_column)+  '. Boolean operator wrong var types.')
                    sys.exit(0)
                else:
                    return 'bool'
            
            elif(child.p_type == 'UnaryBooleanOperator'):
                operator0 = child.childs[0]
                type0 = self.ExpressionAnalizer(operator0)

                if(type0 != 'bool'):
                    print("[Context Error] line " + str(child.p_line) + ' column '+\
                        str(child.p_column)+ '. Boolean operator wrong var types.')
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
                        print("[Context Error] line " + str(child.p_line) + ' column '+\
                            str(child.p_column)+ '. Relational operator wrong var types.')
                        sys.exit(0)
                if (type1 != type2):
                    print("[Context Error] line " + str(child.p_line) + ' column '+\
                        str(child.p_column)+ '. Relational operator wrong var types.')
                    sys.exit(0)
                else:
                    return "bool"

            elif(child.p_type == 'AritmeticOperator'):
                oprator1 = child.childs[0]
                oprator2 = child.childs[1]
                type1 = self.ExpressionAnalizer(oprator1)
                type2 = self.ExpressionAnalizer(oprator2)
                if (type1 != type2 != 'int'):
                    print("[Context Error] line " + str(child.p_line) + ' column '+\
                        str(child.p_column)+ '. Aritmetic operator wrong var types.')
                    sys.exit(0)
                else:
                    return 'int'
            
            elif(child.p_type == 'UnaryAritmeticOperator'):
                operator0 = child.childs[0]
                type0 = self.ExpressionAnalizer(operator0)

                if(type0 != 'int'):
                    print("[Context Error] line " + str(child.p_line) + ' column '+\
                        str(child.p_column)+ '. Aritmetic operator wrong var types.')
                    sys.exit(0)
                else:
                    return 'int'

            elif(child.p_type == 'ArrayExpression'):
                if(len(child.childs) == 1):

                    if(isinstance(child.p_value, SyntaxLeaf)):
                        self.ExpressionAnalizer(child.p_value)
                        t = self.GetVariableArray(child.p_value,[child.p_line,child.p_column])
                    else:
                        t = self.CheckId(child.p_value,[child.p_line,child.p_column])
                    
                    if(not t.is_array):
                        print("[Context Error] line " + str(child.p_line) + ' column '+\
                            str(child.p_column)+ '. Variable ' + t.s_value + 'is not array.')
                        sys.exit(0)

                    operator1 = child.childs[0]
                    type1 = self.ExpressionAnalizer(operator1)

                    if(type1 != 'int'):
                        print("[Context Error] line " + str(child.p_line) + ' column '+\
                            str(child.p_column)+ '. Array expression wrong type.')
                        sys.exit(0)
                    
                    index = operator1.childs[0].c_lexeme

                    if(operator1.childs[0].c_type == 'var'):
                        # Cableado porque no sabemos su valor
                        index = t.array_indexes[0]

                    if(index > t.array_indexes[1] or index < t.array_indexes[0]):
                        print("[Context Error] line " + str(child.p_line) + ' column '+\
                            str(child.p_column)+ '. Array expression out of boundaries.')
                        sys.exit(0)

                    return type1

                else:
                    if(isinstance(child.p_value, SyntaxLeaf)):
                        self.ExpressionAnalizer(child.p_value)
                        t = self.GetVariableArray(child.p_value,[child.p_line,child.p_column])
                    else:
                        t = self.CheckId(child.p_value,[child.p_line,child.p_column])
                    
                    if(not t.is_array):
                        print("[Context Error] line " + str(child.p_line) + ' column '+\
                            str(child.p_column)+ '. Variable ' + t.s_value + 'is not array.')
                        sys.exit(0)
                    
                    operator1 = child.childs[0]
                    operator2 = child.childs[1]
                    type1 = self.ExpressionAnalizer(operator1)
                    type2 = self.ExpressionAnalizer(operator2)

                    if(type1 != type2 != 'int'):
                        print("[Context Error] line " + str(child.p_line) + ' column '+\
                            str(child.p_column)+ '. Array expression wrong type.')
                        sys.exit(0)
                    
                    if(operator1.childs[0].c_lexeme > t.array_indexes[1] or operator1.childs[0].c_lexeme < t.array_indexes[0]):
                        print("[Context Error] line " + str(child.p_line) + ' column '+\
                            str(child.p_column)+ '. Array expression out of boundaries.')
                        sys.exit(0)
                    
                    return type1

            elif(child.p_type == 'ArrayOperator'):
                operator1 = child.childs[0]
                type1 = self.CheckId(operator1,[[child.p_line,child.p_column]])

                if(not type1.is_array):
                    print("[Context Error] line " + str(child.p_line) + ' column '+\
                        str(child.p_column)+ '. Array operation invalid or variable not array.')
                    sys.exit(0)
                return 'int'

            elif(child.p_type == 'Terminal'):
                if (len(child.childs)>0):
                    for h in child.childs:
                        t = self.ExpressionAnalizer(h)
                        return t
                else:
                    if (child.c_type == 'var'):
                        t = self.CheckId(child.c_lexeme,[child.p_line,child.p_column])
                        return t.s_type
                    else:
                        return child.c_type
            elif(child.p_type == 'ConcatExpression'):
                for leaf in child.childs:
                    self.ExpressionAnalizer(leaf)
       

    def AppendContextSymbol(self, leaf, s_type, is_array, is_index = False):
        """ Definicion del metodo [AppendContextSymbol], el cual se encarga de la creacion del
        objeto simbolo el cual sera insertado en la tabla de hash (diccionario) que se encuentra
        en el tope de la pila.
        
        recibe: leaf : hoja a analizar.
                s_type : tipaje de la hoja.
                is_array : booleano si es un arreglo.
        """
        
        if(len(self.c_scopes) == 0):
            new_scope ={}
            self.c_scopes.insert(0,new_scope)
            self.c_secScopes.append(self.c_scopes[0])
            self.c_auxScopes.append(self.c_scopes[0])
        
        stack_top = self.c_scopes[0]
        if leaf.p_value in stack_top:
            print("[Context Error] Line " + str(leaf.p_line) + ' column '+\
                str(leaf.p_column)+ '. Variable ' + leaf.p_value + ' has been declared before.')
            sys.exit(0)
        
        new_type = s_type.p_value

        if(is_array):
            new_type = "array"
        
        new_symbol = ContextSymbol(leaf.p_value, new_type)
        new_symbol.is_array = is_array
        new_symbol.is_index = is_index

        if(is_array):
            new_symbol.array_indexes.append(s_type.p_value.childs[0])
            new_symbol.array_indexes.append(s_type.p_value.childs[1])
        
        stack_top[leaf.p_value] = new_symbol

        if ((len(leaf.childs))>0):
            for leaf in leaf.childs:
                if (leaf.p_type == 'Variable'):
                    if(len(s_type.childs) > 0):
                        is_array = self.CheckIfArray(s_type.childs[0].p_value)
                        self.AppendContextSymbol(leaf, s_type.childs[0], is_array)
                    else:
                        self.AppendContextSymbol(leaf, s_type, is_array)
                elif (leaf.p_type == 'Expression'):
                    t = self.ExpressionAnalizer(leaf)
                    if (t != s_type.p_value):
                        print("[Context Error] line " + str(leaf.p_line) + ' column '+\
                            str(leaf.p_column)+  'Variable types does not match.')
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
            if(child != ';'):
                if (child.p_type == 'Declare'):
                    self.c_currentLine += 1
                    self.CreateContextScope(child)
                elif (child.p_type == 'Variable'):
                    countVar = self.CountChilds(child)
                    countDatatypes = self.CountChilds(leaf_type)

                    if(countVar > 0 and countDatatypes > 1 and countVar != countDatatypes):
                        print("[Context Error] line " + str(child.p_line) + ' column '+\
                            str(child.p_column)+  ' Variables has to be equal in number than datatypes.')
                        sys.exit(0)
                    
                    # Verificar si la variable es arreglo o no
                    is_array = self.CheckIfArray(leaf_type.p_value)
                    self.AppendContextSymbol(child, leaf_type, is_array)


    def ContentAnalyzer(self, content):
        """ Definicion del metodo [ContentAnalyzer], el cual se encarga de revisar 
        linea a linea de forma recursiva todos los componentes del Arbol Sintactico
        generado por el parser que se encuentran relacionados a la estructura denominada
        [contenido] de gusb.
        
        recibe: instruction : Estructura completa del arbol sintactico a analizar.
        """
        if(len(content.childs) > 0):
            for leaf in content.childs:
                if(leaf != ';'):
                    if(leaf.p_type == "Instruction"):
                        self.InstructionAnalyzer(leaf)
                    elif(leaf.p_type == "Block"):
                        self.c_currentLine+=1
                        self.ContextAnalyzer(leaf)
                        if(len(self.c_scopes) > 0):
                            self.c_scopes.pop(0)
                    elif(leaf.p_type == "Content"):
                        self.c_currentLine+=1
                        self.ContentAnalyzer(leaf)
    

    def InstructionAnalyzer(self, instruction):
        """ Definicion del metodo [InstructionAnalyzer], el cual se encarga de revisar 
        linea a linea de forma recursiva todos los componentes del Arbol Sintactico
        generado por el parser que se encuentran relacionados a la estructura denominada
        [instruccion] de gusb.
        
        recibe: instruction : Estructura completa del arbol sintactico a analizar.
        """
        if(len(instruction.childs) > 0):
            for leaf in instruction.childs:
                if (leaf.p_type  == 'Asign'):
                    self.c_currentLine += 1

                    # Verificar que la variable este declarada
                    var = self.CheckId(leaf.p_value,[leaf.p_line,leaf.p_column])

                    # if (var.is_index):
                    #     print("[Context Error] line " + str(leaf.p_line) + ' column '+\
                    #         str(leaf.p_column)+  ". tries to modify variable " + leaf.p_value + " of iteration.")
                    #     sys.exit(0)
                    
                    # Verificar si la variable es de tipo arreglo o no
                    exp_type = self.AssignationAnalyzer(leaf.childs[0])

                    if(not var.is_array):
                        # if(var.is_index):
                        #     print("[Context Error] line " + str(leaf.p_line) + ' column '+\
                        #         str(leaf.p_column)+  ". Trying to asign to a control variable.")
                        #     sys.exit(0)

                        if (var.s_type != exp_type and not var.is_index):
                            #print(var.is_index)
                            print("[Context Error] line " + str(leaf.p_line) + ' column '+\
                                str(leaf.p_column)+  ". Different variable types.")
                            sys.exit(0)
                    else:

                        if(exp_type != 'int'):
                            print("[Context Error] line " + str(leaf.p_line) + ' column '+\
                                str(leaf.p_column)+  ". Trying to asign array other type different than Integer.")
                            sys.exit(0)
                        
                        exp_asign = leaf.childs[0].childs[0].childs[0]

                        if(exp_asign.p_type == 'ArrayExpression'):
                            exp = exp_asign.p_value

                            if(isinstance(exp, SyntaxLeaf)):
                                print("Entre")
                                asignvar = self.GetVariableArray(exp,[exp_asign.p_line,exp_asign.p_column])
                            else:
                                asignvar = self.CheckId(exp)
                            
                            var_count = (var.array_indexes[1] - var.array_indexes[0]) + 1
                            asign_var_count = (asignvar.array_indexes[1] - asignvar.array_indexes[0]) + 1

                            if(var_count != asign_var_count):
                                print("[Context Error] line " + str(leaf.p_line) + ' column '+\
                                    str(leaf.p_column)+  ". Trying to asign different Array.")
                                sys.exit(0)
                            
                            return

                        count = self.CheckCountExp(leaf.childs[0])

                        if(count != (var.array_indexes[1] - var.array_indexes[0]) + 1):
                            print("[Context Error] line " + str(leaf.p_line) + ' column '+\
                                str(leaf.p_column)+  ". Trying to asign different number of elements in the array " + var.s_value)
                            sys.exit(0)

                elif(leaf.p_type == 'Conditional' or leaf.p_type == 'Guard'):
                    self.c_currentLine += 1
                    for child in leaf.childs:
                        if (child.p_type == 'Content'):
                            self.ContentAnalyzer(child)
                        elif ( child.p_type == 'Guard'):
                            self.GuardAnalyzer(child)
                        else:
                            t = self.ExpressionAnalizer(child)
                            if (t != 'bool'):
                                print("[Context Error] line " + str(child.p_line) + ' column '\
                                    +str(child.p_column)+  ". Conditional variables are of a different types.")
                                sys.exit(0) 


                elif(leaf.p_type == 'Forloop'):
                    self.c_currentLine += 1
                    
                    # Colocar la variable dummy de control en el arreglo global
                    cont_symbol = ContextSymbol(leaf.p_value,'int')
                    cont_symbol.is_index = True
                    global_control_vars.append(cont_symbol)
                    
                    oprator1 = leaf.childs[0]
                    oprator2 = leaf.childs[1]
                    type1 = self.ExpressionAnalizer(oprator1)
                    type2 = self.ExpressionAnalizer(oprator2)

                    if (type1 != 'int' or type2 != 'int'):
                        print("[Context Error] line " + str(leaf.p_line) + ' column '+str(leaf.p_column)+  \
                            ". For expressions are different type.")
                        sys.exit(0)
                    
                    if(not self.SeeIfVarExist(leaf.p_value)):
                        pass
                        #self.AppendContextSymbol(SyntaxLeaf('Terminal', leaf.p_value), \
                            #SyntaxLeaf('Datatype', 'int'), False, True)
                    else:
                        t = self.CheckId(leaf.p_value)
                        t.is_index = True

                    #GOKU
                    try:
                        if (leaf.childs[2].childs[0].childs[0].p_type == 'Declare'):
                            t = self.CheckId(leaf.childs[2].childs[0].childs[0].childs[0].p_value)
                            if t.is_index == True:
                                break
                    except:
                        pass

                    self.ContextAnalyzer(leaf.childs[2])

                    
                    if(self.SeeIfVarExist(leaf.p_value)):
                        t.is_index = None
                    
                    # Liberar esa variable para no ocasionar errores
                    global_control_vars.pop(global_control_vars.index(cont_symbol))


                elif (leaf.p_type == 'Doloop'):
                    self.c_currentLine += 1

                    oprator1 = leaf.childs[0]
                    type1 = self.ExpressionAnalizer(oprator1)

                    if (type1 != 'bool'):
                        print("[Context Error] line " + str(child.p_line) + ' column '+str(child.p_column)+  \
                            ". Do expression is not a boolean.")
                        sys.exit(0)
                    
                    for child in leaf.childs:
                        if(child.p_type == 'Content'):
                            self.ContentAnalyzer(child)
                        elif(child.p_type == 'Guard'):
                            self.GuardAnalyzer(child)

                elif(leaf.p_type == 'Input'):
                    self.c_currentLine += 1
                    var = self.CheckId(leaf.childs[0], [leaf.p_line,leaf.p_column])

                else:
                    if (leaf.p_type =='Output'):
                        self.c_currentLine += 1
                        for child in leaf.childs:
                            self.ExpressionAnalizer(child)                    


    def GuardAnalyzer(self, leaf):
        """ Definicion del metodo [GuardAnalyzer], el cual se encarga de revisar 
        linea a linea de forma recursiva todos los componentes del Arbol Sintactico
        generado por el parser que se encuentran relacionados a la estructura denominada
        [guard] de gusb.
        
        recibe: leaf : Estructura completa del arbol sintactico a analizar.
        """
        self.c_currentLine += 1
        for child in leaf.childs:
            if (child.p_type == 'Content'):
                self.ContentAnalyzer(child)
            elif ( child.p_type == 'Guard'):
                self.GuardAnalyzer(child)
            else:
                t = self.ExpressionAnalizer(child)
                if (t != 'bool'):
                    print("[Context Error] line " + str(child.p_line) + ' column '+str(child.p_column)+  \
                        ". Conditional variables are of a different types.")
                    sys.exit(0)


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
                        if(len(self.c_scopes) > 0):
                            self.c_scopes.pop(0)

                    elif (leaf.p_type == 'Declare'):
                        self.c_currentLine+=1
                        new_scope ={}
                        self.c_scopes.insert(0,new_scope)
                        self.CreateContextScope(leaf)
                        self.c_secScopes.append(self.c_scopes[0])
                        self.c_auxScopes.append(self.c_scopes[0])

                    elif (leaf.p_type  == 'Content'):
                        self.c_currentLine+=1
                        self.ContentAnalyzer(leaf)                
        else:
            print('[Context Error]: No SyntaxTreeStructure')


    def AssignationAnalyzer(self, assignation):
        """ Definicion del metodo [AssignationAnalyzer], el cual se encarga de revisar 
        linea a linea de forma recursiva todos los componentes del Arbol Sintactico
        generado por el parser que se encuentran relacionados a la estructura [asignacion] 
        de gusb.
        
        recibe: assignation : Estructura completa del arbol sintactico a analizar.
        """

        if(len(assignation.childs) == 1):
            return self.ExpressionAnalizer(assignation.childs[0])
        else:
            type1 = self.ExpressionAnalizer(assignation.childs[0])

            type2 = self.AssignationAnalyzer(assignation.childs[1])

            if(type1 != type2):
                print("[Context Error] line " + str(assignation.p_line) + ' column '+str(assignation.p_column)+ \
                    '. Trying to asign list of expressions of different types.')
                sys.exit(0)
            
            return type1
    

    def GetVariableArray(self, exp, index_f_c=None):
        """ Definicion del metodo de apoyo [GetVariableArray], el cual se encarga de encontrar la
        variable que se utiliza en un ArrayExpression.
        
        recibe: exp : hoja a analizar.
                index_f_c : lista que contiene fila y columna actual.
        """
        if(isinstance(exp, SyntaxLeaf)):
            return self.GetVariableArray(exp.p_value)
        else:
            return self.CheckId(exp,index_f_c)


    def CheckIfArray(self, id_type):
        """ Definicion del metodo de apoyo [CheckIfArray], el cual se encarga de verificar si una instancia
        de syntaxleaf (hoja) es un arreglo.
        
        recibe: id_type : hoja a analizar.
        """
        if(isinstance(id_type, SyntaxLeaf)):
            return True
        else:
            return False
    

    def CheckCountExp(self, expression):
        """ Definicion del metodo de apoyo [CheckCountExp], el cual se encarga de contabilizar el numero de
        elementos que tiene una asingacion para verificar si es igual al numero de elementos de la declaracion de
        un array.
        
        recibe: expression : hoja a analizar.
        """
        if(len(expression.childs) > 1):
            return 1 + self.CheckCountExp(expression.childs[1])
        else:
            return len(expression.childs)


    def SeeIfVarExist(self, id_var):
        """ Definicion del metodo de apoyo [SeeIfVarExist], el cual se encarga de retornar un booleano en caso de
        haber sido declarada previamente una variable.
        
        recibe: id_var : variable a checkear.
        """
        if(len(self.c_secScopes) > 0):
            for scope in self.c_secScopes:
                if (len(scope) > 0):
                    if id_var in scope:
                        return True        
        return False


    def CheckId(self, id_var, index_f_c=None):
        """ Definicion del metodo de apoyo [CheckId], el cual se encarga de retornar un la variable
        en caso de haber sido declarada previamente.
        
        recibe: id_var : variable a checkear.
                index_f_c: lista que contiene fila y columna actual.
        """
        found = False
        if(len(self.c_secScopes) > 0):
            for scope in self.c_secScopes:
                if (len(scope) > 0):
                    if id_var in scope:
                        found = True
                        var = scope[id_var]
                    
        if(found):
            return var
        
        # Si no se encuentra se verifica que no este en las variables de control
        for c_var in global_control_vars:
            if(id_var == c_var.s_value):
                return c_var

        if index_f_c:
            print("[Context Error] line " + str(index_f_c[0]) +' column: '+str(index_f_c[1]) +\
                '. Variable ' + id_var + ' has not been declared before.')
            sys.exit(0)
        print("[Context Error] line " + str(self.c_currentLine) +'. Variable ' + id_var + \
            ' has not been declared before.')
        sys.exit(0)
    

    def CountChilds(self, leaf):
        """ Definicion del metodo de apoyo [CountChilds], el cual se encarga de retornar el numero de
        hijos de una determinada hoja.
        
        recibe: leaf : hoja a checkear.
        """
        if(len(leaf.childs) > 0):
            return 1 + self.CountChilds(leaf.childs[0])
        else:
            return 1 
