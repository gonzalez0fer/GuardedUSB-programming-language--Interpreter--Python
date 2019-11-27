#######################################
# CI3715 Traductores e Interpretadores
# Entrega 3. 
# Fernando Gonzalez 08-10464
# Kevin Mena 13-10869
#######################################
from g_utils import *
from g_context_utils import *

# En este File reposa las clases y metodos para la construccion e 
# impresion del Arbol Sintactico de nuestro programa

class SyntaxLeaf:
    """ Definicion del objeto [SyntaxLeaf], el cual representa cada hoja y/o
    ramificacion de nuestro arbol.
    
    inicializa con: 
            p_type : tipo de objeto sintactico a ser representado en la hoja.
            p_line : linea del objeto representado en la hoja.
            p_column : columna del objeto representado en la hoja.
            p_value : valor del objeto sintactico de la hoja (de existir).
            childs : lista de objetos sintacticos hijos(de existir).
            ----------
            c_type : tipo de objeto sintactico a ser asignado en contexto.
            c_lexeme : valores terminales a ser asignados en el contexto.
            c_array : estructuras representables en arreglos a ser asignadas en contexto.
    """
    def __init__(self, p_type, p_value = None, childs = None, p_line = None, p_column = None):
        self.p_type = p_type
        self.p_value = p_value
        self.p_line = p_line
        self.p_column = p_column
        self.c_type = None
        self.c_array = None
        self.c_lexeme = None
        if childs:
            self.childs = childs
        else:
            self.childs = []


def SyntaxTreePrinter(syntaxLeaf, identation, contex_scope = None):
    """ Definicion del metodo [SyntaxTreePrinter], el cual se encarga de imprimir
    la estructura mas externa del arbol sintactico [Declare/Content].
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
            context_scope : pila de scopes que contienen las tablas de simbolos.
    """
    if (syntaxLeaf):
        if(len(syntaxLeaf.childs) > 0):
            printer(identation, syntaxLeaf.p_type)
            identation = identation + TAB

            for leaf in syntaxLeaf.childs:
                if (leaf.p_type == "Declare"):
                    #printer(identation, leaf.p_type)
                    identation = identation + TAB
                    PrintSymbolTable(contex_scope, identation)
                    #PrintDeclaration(leaf, identation)
                elif (leaf.p_type == "Content"):
                    PrintContent(leaf, identation, contex_scope)


def PrintDeclaration(syntaxLeaf, identation, contex_scope = None):
    """ Definicion del metodo [PrintDeclaration], el cual se encarga de imprimir
    la estructura [Declare] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
            context_scope : pila de scopes que contienen las tablas de simbolos.
    """
    for leaf in syntaxLeaf.childs:
        if(leaf== ";"):
            printseq(identation)        
        elif(leaf.p_type == "Variable"):
            PrintVariable(leaf, identation+TAB,contex_scope)
        elif(leaf.p_type == "Declare"):
            PrintDeclaration(leaf, identation,contex_scope)


def PrintContent(syntaxLeaf, identation, contex_scope = None):
    """ Definicion del metodo [PrintContent], el cual se encarga de imprimir
    la estructura [Content] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
            context_scope : pila de scopes que contienen las tablas de simbolos.
    """
    if (len(syntaxLeaf.childs) == 1):
        child = syntaxLeaf.childs[0]

        if (child.p_type == "Instruction"):
            PrintInstruction(child, identation, contex_scope)
        elif (child.p_type == "Block"):
            SyntaxTreePrinter(child, identation, contex_scope)
    elif (len(syntaxLeaf.childs) >= 2):
        for leaf in syntaxLeaf.childs:
            if (leaf==';'):
                printseq(identation)
            elif(leaf.p_type == "Instruction"):
                PrintInstruction(leaf, identation,contex_scope)
            elif(leaf.p_type == "Block"):
                SyntaxTreePrinter(leaf, identation,contex_scope)
            elif(leaf.p_type == "Content"):
                PrintContent(leaf, identation, contex_scope)


def PrintInstruction(syntaxLeaf, identation, contex_scope = None):
    """ Definicion del metodo [PrintInstruction], el cual se encarga de imprimir
    la estructura [Instruction] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
            context_scope : pila de scopes que contienen las tablas de simbolos.
    """
    child = syntaxLeaf.childs[0]

    if(child.p_type == "Conditional"):
        printer(identation, "If")
        identation = identation + TAB
        PrintConditional(child, identation,contex_scope)
    elif(child.p_type == "Forloop"):
        printer(identation, "For\n",identation+ TAB, "In")
        PrintForLoop(child,identation+ TAB,contex_scope)
    elif(child.p_type == "Doloop"):
        printer(identation, "Do")
        PrintDoLoop(child,identation+ TAB,contex_scope)
    elif(child.p_type == "Asign"):
        PrintAsign(child, identation,contex_scope)
    elif(child.p_type == "Input"):
        PrintInput(child, identation,contex_scope)
    elif(child.p_type == "Output"):
        PrintOutput(child, identation,contex_scope)


def PrintForLoop(syntaxLeaf, identation, contex_scope = None):
    """ Definicion del metodo [PrintForLoop], el cual se encarga de imprimir
    la estructura iterativa [ForLoop] junto con sus [Guard] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
            context_scope : pila de scopes que contienen las tablas de simbolos.
    """
    print(identation+TAB, "Ident:", syntaxLeaf.p_value)
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        if(leaf.p_type == "Content"):
            PrintContent(leaf, identation,contex_scope)
        elif (leaf.p_type == "Expression"):
            printExp(identation)
            PrintExpression(leaf, identation+TAB,contex_scope)


def PrintDoLoop(syntaxLeaf, identation, contex_scope = None):
    """ Definicion del metodo [PrintForLoop], el cual se encarga de imprimir
    la estructura iterativa [DoLoop] junto con sus [Guard] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
            context_scope : pila de scopes que contienen las tablas de simbolos.
    """
    for leaf in syntaxLeaf.childs:
        if(leaf.p_type == "Expression"):
            printExp(identation)
            PrintExpression(leaf, identation,contex_scope)
        elif(leaf.p_type == "Content"):
            PrintContent(leaf, identation,contex_scope)
        elif(leaf.p_type == "Guard"):
            PrintConditional(leaf, identation,contex_scope)


def PrintConditional(syntaxLeaf, identation, contex_scope):
    """ Definicion del metodo [PrintConditional], el cual se encarga de imprimir
    las estructuras [Conditional, Guard] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
            context_scope : pila de scopes que contienen las tablas de simbolos.
    """
    printer(identation, "Guard")
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        if(leaf.p_type == "Expression"):
            PrintExpression(leaf, identation, contex_scope)
        elif(leaf.p_type == "Content"):
            PrintContent(leaf, identation,contex_scope)
        elif(leaf.p_type == "Guard"):
            PrintConditional(leaf, identation,contex_scope)


def PrintAsign(syntaxLeaf, identation,contex_scope):
    """ Definicion del metodo [PrintAsign], el cual se encarga de imprimir
    la estructura [Asign] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
            context_scope : pila de scopes que contienen las tablas de simbolos.
    """
    printer(identation, "Asig")
    identation = identation + TAB
    print(identation, "Ident:", syntaxLeaf.p_value)
    identation = identation + TAB
    PrintAssignation(syntaxLeaf.childs[0], identation,contex_scope)

def PrintAssignation(syntaxLeaf, identation, contex_scope):
    """ Definicion del metodo [PrintAssignation], el cual se encarga de imprimir
    las/la [Expression] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
            context_scope : pila de scopes que contienen las tablas de simbolos.
    """

    if(len(syntaxLeaf.childs) == 1):
        PrintExpression(syntaxLeaf.childs[0], identation, contex_scope)
    else:
        PrintExpression(syntaxLeaf.childs[0], identation, contex_scope)
        #printExp(identation)
        PrintAssignation(syntaxLeaf.childs[1], identation, contex_scope)

def PrintInput(syntaxLeaf, identation, contex_scope):
    """ Definicion del metodo [PrintInput], el cual se encarga de imprimir
    la estructura [Read] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
            context_scope : pila de scopes que contienen las tablas de simbolos.
    """
    printer(identation, "Read")
    identation = identation + TAB
    print(identation, "Ident:", syntaxLeaf.childs[0])


def PrintOutput(syntaxLeaf, identation, contex_scope):
    """ Definicion del metodo [PrintOutput], el cual se encarga de imprimir
    la estructura [Print/Println] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
            context_scope : pila de scopes que contienen las tablas de simbolos.
    """
    if(syntaxLeaf.p_value == "print"):
        printer(identation, "Print")
        identation = identation + TAB
    elif(syntaxLeaf.p_value == "println"):
        printer(identation, "Println")
        identation = identation + TAB
    
    to_do = []

    for leaf in syntaxLeaf.childs:
        if(leaf.p_type == "Expression"):
            to_do.append((leaf,identation))
        else:
            PrintConcatExp(leaf, identation + TAB, to_do, contex_scope)

    for sleaf in to_do:
        if(sleaf[0].p_type == "Expression"):
            PrintExpression(sleaf[0],sleaf[1]+TAB*len(to_do),contex_scope )
        elif(sleaf[0].p_type == "Terminal"):
            PrintTerminal(sleaf[0],sleaf[1]+TAB*len(to_do),contex_scope ) 
        else:
            pass

def PrintConcatExp(syntaxLeaf, identation, to_do, contex_scope):
    """ Definicion del metodo [PrintConcatExp], el cual se encarga de imprimir
    la estructura [Concat] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
            context_scope : pila de scopes que contienen las tablas de simbolos.
    """
    for leaf in syntaxLeaf.childs:
        if(leaf.p_type == "Expression"):
            printer(identation, "Concat")
            to_do.append([leaf,identation])
        elif(leaf.p_type == "Terminal"):
            to_do.append([leaf,identation])
        else:
            identation = identation + TAB
            PrintConcatExp(leaf, identation,to_do, contex_scope)        
      

def PrintVariable(syntaxLeaf, identation, contex_scope):
    """ Definicion del metodo [PrintVariable], el cual se encarga de imprimir
    la estructura [Variable] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
            context_scope : pila de scopes que contienen las tablas de simbolos.
    """
    if(len(syntaxLeaf.childs) > 0):
        print(identation, "Ident:", syntaxLeaf.p_value)

        PrintVariable(syntaxLeaf.childs[0], identation, contex_scope)
    else:
        print(identation, "Ident:", syntaxLeaf.p_value)
        identation = identation + TAB


def PrintExpression(syntaxLeaf, identation,contex_scope, uminus = False):
    """ Definicion del metodo [PrintExpression], el cual se encarga de imprimir
    la estructura [Expression] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
            context_scope : pila de scopes que contienen las tablas de simbolos.
    """
    child = syntaxLeaf.childs[0]

    if (child.p_type == "AritmeticOperator"):
        identation = identation + TAB
        PrintAritmeticOp(child, identation, contex_scope) 
    elif (child.p_type == "Terminal"):
        PrintTerminal(child, identation, contex_scope, uminus)
    elif (child.p_type == "RelationalOperator"):
        identation = identation + TAB
        PrintRelationalOp(child, identation, contex_scope)
    elif (child.p_type == "BooleanOperator"):
        printExp(identation)
        identation = identation + TAB
        PrintBooleanOp(child, identation, contex_scope)
    elif (child.p_type == "StrOperator"):
        printExp(identation)
        identation = identation + TAB
        PrintStrOp(child, identation, contex_scope)
    elif (child.p_type == "ArrayOperator"):
        PrintArrayOp(child, identation, contex_scope)
    elif(child.p_type == "ArrayExpression"):
        identation = identation + TAB
        PrintArrayExp(child, identation, contex_scope)
    elif(child.p_type == "UnaryAritmeticOperator"):
        identation = identation + TAB
        PrintExpression(child.childs[0], identation, contex_scope, True)   



def PrintArrayExp(syntaxLeaf, identation, contex_scope):
    """ Definicion del metodo [PrintArrayExp], el cual se encarga de imprimir
    la estructura [Array] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
            context_scope : pila de scopes que contienen las tablas de simbolos.
    """
    if(len(syntaxLeaf.childs) == 2):
        printer(identation, "ArrayAsign")
        identation = identation + TAB
        if(isinstance(syntaxLeaf.p_value, SyntaxLeaf)):
            PrintArrayExp(syntaxLeaf.p_value, identation, contex_scope)
        else:
            print(identation, "Ident:", syntaxLeaf.p_value)

        for leaf in syntaxLeaf.childs:
                PrintTerminal(leaf, identation, contex_scope)
    else:
        printer(identation, "EvalArray")
        identation = identation + TAB
        if(isinstance(syntaxLeaf.p_value, SyntaxLeaf)):
            PrintArrayExp(syntaxLeaf.p_value, identation, contex_scope)
        else:
            print(identation, "Ident:", syntaxLeaf.p_value)

        for leaf in syntaxLeaf.childs:
                PrintTerminal(leaf, identation+TAB, contex_scope)


def PrintArrayOp(syntaxLeaf, identation, contex_scope):
    """ Definicion del metodo [PrintArrayOp], el cual se encarga de imprimir
    la estructura [ArrayOperator] de las funciones de manipulacion de funciones
    array del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
            context_scope : pila de scopes que contienen las tablas de simbolos.
    """
    printExp(identation,'Arith')
    if(syntaxLeaf.p_value == "size"):
        printer(identation, "Size")
        identation = identation + TAB
    elif(syntaxLeaf.p_value == "max"):
        printer(identation, "Max")
        identation = identation + TAB
    elif(syntaxLeaf.p_value == "min"):
        printer(identation, "Min")
        identation = identation + TAB
    elif(syntaxLeaf.p_value == "atoi"):
        printer(identation, "Atoi")
        identation = identation + TAB
    child = syntaxLeaf.childs[0]
    if(isinstance(child, SyntaxLeaf)):
        print(identation, "Placeholder")
    else:
        print(identation, "Ident:", child)


def PrintUnaryAritmeticOp(syntaxLeaf, identation,contex_scope, uminus = False):
    """ Definicion del metodo [PrintUnaryAritmeticOp], el cual se encarga de imprimir
    la estructura [UnaryAritmeticOp] de los operadores aritmeticos del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
            context_scope : pila de scopes que contienen las tablas de simbolos.
    """
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        PrintExpression(leaf, identation, contex_scope, True)


def PrintAritmeticOp(syntaxLeaf, identation, contex_scope):
    """ Definicion del metodo [PrintAritmeticOp], el cual se encarga de imprimir
    la estructura [AricmeticOperator] de los operadores aritmeticos del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
            context_scope : pila de scopes que contienen las tablas de simbolos.
    """
    printExp(identation, 'Arith')
    print(identation,symbols[syntaxLeaf.p_value])
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        PrintExpression(leaf, identation,contex_scope)


def PrintTerminal(syntaxLeaf, identation, contex_scope, uminus = False):
    """ Definicion del metodo [PrintTerminal], el cual se encarga de imprimir
    la estructura [Terminal] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
            context_scope : pila de scopes que contienen las tablas de simbolos.
    """
    if syntaxLeaf.c_type == "int":
        printExp(identation, 'Arith')
    elif syntaxLeaf.c_type == 'bool':
        printExp(identation, 'Boolean')
    else:
        pass
    if (syntaxLeaf.p_value is not None):
        if(syntaxLeaf.c_type == "int" and uminus==True):
            print(identation, "Literal:", '-'+str(syntaxLeaf.p_value))
            identation = identation + TAB
        elif(syntaxLeaf.c_type == "int"):
            print(identation, "Literal:", syntaxLeaf.p_value)
            identation = identation + TAB
        elif(syntaxLeaf.c_type == "var"):
            print(identation, "Ident:", syntaxLeaf.p_value)
            identation = identation + TAB
        elif(syntaxLeaf.p_value != "true" and syntaxLeaf.p_value != "false"):
            print(identation + '%s' % syntaxLeaf.p_value)
            identation = identation + TAB
        else:
            print(identation, syntaxLeaf.p_value)
            identation = identation + TAB
    if(len(syntaxLeaf.childs) > 0 ):
        PrintTerminal(syntaxLeaf.childs[0], identation, contex_scope, uminus)


def PrintRelationalOp(syntaxLeaf, identation, contex_scope):
    """ Definicion del metodo [PrintRelationalOp], el cual se encarga de imprimir
    la estructura [RelationalOperator] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
            context_scope : pila de scopes que contienen las tablas de simbolos.
    """
    printExp(identation, 'Bool')
    try:
        if (contex_scope[0][syntaxLeaf.childs[0].childs[0].p_value].s_type == 'int'):
            print(identation, color.RED+'Arith'+color.END+ symbols[syntaxLeaf.p_value])
        elif (contex_scope[0][syntaxLeaf.childs[0].childs[0].p_value].s_type == 'bool'):
            print(identation, color.RED+'Boolean'+color.END+ symbols[syntaxLeaf.p_value])
    except:
        pass

    identation = identation + TAB
    for leaf in syntaxLeaf.childs:
        PrintExpression(leaf, identation, contex_scope)


def PrintBooleanOp(syntaxLeaf, identation, contex_scope):
    """ Definicion del metodo [PrintBooleanOp], el cual se encarga de imprimir
    la estructura [BooleanOperator] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
            context_scope : pila de scopes que contienen las tablas de simbolos.
    """
    print(identation, symbols[syntaxLeaf.p_value])
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        PrintExpression(leaf, identation, contex_scope)


def PrintStrOp(syntaxLeaf, identation, contex_scope):
    """ Definicion del metodo [PrintStrOp], el cual se encarga de imprimir
    la estructura [StrOperator] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
            context_scope : pila de scopes que contienen las tablas de simbolos.
    """
    print(identation, "Concat")
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        print(identation, leaf)