#######################################
# CI3715 Traductores e Interpretadores
# Entrega 3. 
# Fernando Gonzalez 08-10464
# Kevin Mena 13-10869
#######################################
from g_utils import *

# En este File reposa las clases y metodos para la construccion e 
# impresion del Arbol Sintactico de nuestro programa

class SyntaxLeaf:
    """ Definicion del objeto [SyntaxLeaf], el cual representa cada hoja y/o
    ramificacion de nuestro arbol.
    
    inicializa con: 
            p_type : tipo de objeto sintactico a ser representado en la hoja.
            p_value : valor del objeto sintactico de la hoja (de existir).
            childs : lista de objetos sintacticos hijos(de existir).
            ----------
            c_type : tipo de objeto sintactico a ser asignado en contexto.
            c_lexeme : valores terminales a ser asignados en el contexto.
            c_array : estructuras representables en arreglos a ser asignadas en contexto.
    """
    def __init__(self, p_type, p_value = None, childs = None):
        self.p_type = p_type
        self.p_value = p_value
        self.c_type = None
        self.c_array = None
        self.c_lexeme = None
        self.visited = False
        if childs:
            self.childs = childs
        else:
            self.childs = []


def SyntaxTreePrinter(syntaxLeaf, identation):
    """ Definicion del metodo [SyntaxTreePrinter], el cual se encarga de imprimir
    la estructura mas externa del arbol sintactico [Declare/Content].
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
    """
    if (syntaxLeaf):
        if(len(syntaxLeaf.childs) > 0):
            printer(identation, syntaxLeaf.p_type)
            identation = identation + TAB

            for leaf in syntaxLeaf.childs:
                if (leaf.p_type == "Declare"):
                    printer(identation, leaf.p_type)
                    identation = identation + TAB
                    PrintDeclaration(leaf, identation)
                elif (leaf.p_type == "Content"):
                    PrintContent(leaf, identation)


def PrintDeclaration(syntaxLeaf, identation):
    """ Definicion del metodo [PrintDeclaration], el cual se encarga de imprimir
    la estructura [Declare] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
    """
    for leaf in syntaxLeaf.childs:
        if(leaf== ";"):
            printseq(identation)        
        elif(leaf.p_type == "Variable"):
            PrintVariable(leaf, identation+TAB)
        elif(leaf.p_type == "Declare"):
            PrintDeclaration(leaf, identation)


def PrintContent(syntaxLeaf, identation):
    """ Definicion del metodo [PrintContent], el cual se encarga de imprimir
    la estructura [Content] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
    """
    if (len(syntaxLeaf.childs) == 1):
        child = syntaxLeaf.childs[0]

        if (child.p_type == "Instruction"):
            PrintInstruction(child, identation)
        elif (child.p_type == "Block"):
            SyntaxTreePrinter(child, identation)
    elif (len(syntaxLeaf.childs) >= 2):
        for leaf in syntaxLeaf.childs:
            if (leaf==';'):
                printseq(identation)
            elif(leaf.p_type == "Instruction"):
                PrintInstruction(leaf, identation)
            elif(leaf.p_type == "Block"):
                SyntaxTreePrinter(leaf, identation)
            elif(leaf.p_type == "Content"):
                PrintContent(leaf, identation)


def PrintInstruction(syntaxLeaf, identation):
    """ Definicion del metodo [PrintInstruction], el cual se encarga de imprimir
    la estructura [Instruction] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
    """
    child = syntaxLeaf.childs[0]

    if(child.p_type == "Conditional"):
        printer(identation, "If")
        identation = identation + TAB
        PrintConditional(child, identation)
    elif(child.p_type == "Forloop"):
        printer(identation, "For\n",identation+ TAB, "In")
        PrintForLoop(child,identation+ TAB)
    elif(child.p_type == "Doloop"):
        printer(identation, "Do")
        PrintDoLoop(child,identation+ TAB)
    elif(child.p_type == "Asign"):
        PrintAsign(child, identation)
    elif(child.p_type == "Input"):
        PrintInput(child, identation)
    elif(child.p_type == "Output"):
        PrintOutput(child, identation)


def PrintForLoop(syntaxLeaf, identation):
    """ Definicion del metodo [PrintForLoop], el cual se encarga de imprimir
    la estructura iterativa [ForLoop] junto con sus [Guard] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
    """
    print(identation+TAB, "Ident:", syntaxLeaf.p_value)
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        if(leaf.p_type == "Content"):
            PrintContent(leaf, identation)
        elif (leaf.p_type == "Expression"):
            printExp(identation)
            PrintExpression(leaf, identation+TAB)


def PrintDoLoop(syntaxLeaf, identation):
    """ Definicion del metodo [PrintForLoop], el cual se encarga de imprimir
    la estructura iterativa [DoLoop] junto con sus [Guard] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
    """
    for leaf in syntaxLeaf.childs:
        if(leaf.p_type == "Expression"):
            printExp(identation)
            PrintExpression(leaf, identation)
        elif(leaf.p_type == "Content"):
            PrintContent(leaf, identation)
        elif(leaf.p_type == "Guard"):
            PrintConditional(leaf, identation)


def PrintConditional(syntaxLeaf, identation):
    """ Definicion del metodo [PrintConditional], el cual se encarga de imprimir
    las estructuras [Conditional, Guard] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
    """
    printer(identation, "Guard")
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        if(leaf.p_type == "Expression"):
            PrintExpression(leaf, identation)
        elif(leaf.p_type == "Content"):
            PrintContent(leaf, identation)
        elif(leaf.p_type == "Guard"):
            PrintConditional(leaf, identation)


def PrintAsign(syntaxLeaf, identation):
    """ Definicion del metodo [PrintAsign], el cual se encarga de imprimir
    la estructura [Asign] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
    """
    printer(identation, "Asig")
    identation = identation + TAB
    print(identation, "Ident:", syntaxLeaf.p_value)
    identation = identation + TAB
    printExp(identation)
    PrintExpression(syntaxLeaf.childs[0], identation)


def PrintInput(syntaxLeaf, identation):
    """ Definicion del metodo [PrintInput], el cual se encarga de imprimir
    la estructura [Read] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
    """
    printer(identation, "Read")
    identation = identation + TAB
    print(identation, "Ident:", syntaxLeaf.childs[0])


def PrintOutput(syntaxLeaf, identation):
    """ Definicion del metodo [PrintOutput], el cual se encarga de imprimir
    la estructura [Print/Println] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
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
            PrintConcatExp(leaf, identation + TAB, to_do)

    for sleaf in to_do:
        if(sleaf[0].p_type == "Expression"):
            PrintExpression(sleaf[0],sleaf[1]+TAB*len(to_do))
        elif(sleaf[0].p_type == "Terminal"):
            PrintTerminal(sleaf[0],sleaf[1]+TAB*len(to_do)) 
        else:
            pass

def PrintConcatExp(syntaxLeaf, identation, to_do):
    """ Definicion del metodo [PrintConcatExp], el cual se encarga de imprimir
    la estructura [Concat] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
    """
    for leaf in syntaxLeaf.childs:
        if(leaf.p_type == "Expression"):
            printer(identation, "Concat")
            to_do.append([leaf,identation])
        elif(leaf.p_type == "Terminal"):
            to_do.append([leaf,identation])
        else:
            identation = identation + TAB
            PrintConcatExp(leaf, identation,to_do)        
      

def PrintVariable(syntaxLeaf, identation):
    """ Definicion del metodo [PrintVariable], el cual se encarga de imprimir
    la estructura [Variable] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
    """
    if(len(syntaxLeaf.childs) > 0):
        print(identation, "Ident:", syntaxLeaf.p_value)

        PrintVariable(syntaxLeaf.childs[0], identation)
    else:
        print(identation, "Ident:", syntaxLeaf.p_value)
        identation = identation + TAB


def PrintExpression(syntaxLeaf, identation, uminus = False):
    """ Definicion del metodo [PrintExpression], el cual se encarga de imprimir
    la estructura [Expression] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
    """
    child = syntaxLeaf.childs[0]

    if (child.p_type == "AritmeticOperator"):
        identation = identation + TAB
        PrintAritmeticOp(child, identation) 
    elif (child.p_type == "Terminal"):
        PrintTerminal(child, identation)
    elif (child.p_type == "RelationalOperator"):
        #printExp(identation)
        identation = identation + TAB
        PrintRelationalOp(child, identation)
    elif (child.p_type == "BooleanOperator"):
        printExp(identation)
        identation = identation + TAB
        PrintBooleanOp(child, identation)
    elif (child.p_type == "StrOperator"):
        printExp(identation)
        identation = identation + TAB
        PrintStrOp(child, identation)
    elif (child.p_type == "ArrayOperator"):
        PrintArrayOp(child, identation)
    elif(child.p_type == "ArrayExpression"):
        #printExp(identation)
        identation = identation + TAB
        PrintArrayExp(child, identation)
    elif(child.p_type == "UnaryAritmeticOperator"):
        identation = identation + TAB
        PrintTerminal(child, identation, True)   



def PrintArrayExp(syntaxLeaf, identation):
    """ Definicion del metodo [PrintArrayExp], el cual se encarga de imprimir
    la estructura [Array] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
    """
    if(len(syntaxLeaf.childs) == 2):
        printer(identation, "ArrayAsign")
        identation = identation + TAB
        if(isinstance(syntaxLeaf.p_value, SyntaxLeaf)):
            PrintArrayExp(syntaxLeaf.p_value, identation)
        else:
            print(identation, "Ident:", syntaxLeaf.p_value)

        for leaf in syntaxLeaf.childs:
                PrintTerminal(leaf, identation)
    else:
        printer(identation, "EvalArray")
        identation = identation + TAB
        if(isinstance(syntaxLeaf.p_value, SyntaxLeaf)):
            PrintArrayExp(syntaxLeaf.p_value, identation)
        else:
            print(identation, "Ident:", syntaxLeaf.p_value)

        for leaf in syntaxLeaf.childs:
                printExp(identation)
                PrintTerminal(leaf, identation+TAB)


def PrintArrayOp(syntaxLeaf, identation):
    """ Definicion del metodo [PrintArrayOp], el cual se encarga de imprimir
    la estructura [ArrayOperator] de las funciones de manipulacion de funciones
    array del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
    """
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


def PrintUnaryAritmeticOp(syntaxLeaf, identation, uminus = False):
    """ Definicion del metodo [PrintUnaryAritmeticOp], el cual se encarga de imprimir
    la estructura [UnaryAritmeticOp] de los operadores aritmeticos del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
    """
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        PrintExpression(leaf, identation, True)


def PrintAritmeticOp(syntaxLeaf, identation):
    """ Definicion del metodo [PrintAritmeticOp], el cual se encarga de imprimir
    la estructura [AricmeticOperator] de los operadores aritmeticos del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
    """
    print(identation, symbols[syntaxLeaf.p_value])
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        PrintExpression(leaf, identation)


def PrintTerminal(syntaxLeaf, identation, uminus = False):
    """ Definicion del metodo [PrintTerminal], el cual se encarga de imprimir
    la estructura [Terminal] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
    """
    if (len(syntaxLeaf.childs) == 0):
        if(isinstance(syntaxLeaf.p_value, int) and uminus==True):
            print(identation, "Literal:", '-'+str(syntaxLeaf.p_value))
            identation = identation + TAB
        elif(isinstance(syntaxLeaf.p_value, int)):
            print(identation, "Literal:", syntaxLeaf.p_value)
            identation = identation + TAB
        elif(syntaxLeaf.p_value.isalpha() and len(syntaxLeaf.p_value) == 1):
            print(identation, "Ident:", syntaxLeaf.p_value)
            identation = identation + TAB
        elif(syntaxLeaf.p_value != "True" and syntaxLeaf.p_value != "False"):
            print(identation + '"%s"' % syntaxLeaf.p_value)
            identation = identation + TAB
        else:
            print(identation, syntaxLeaf.p_value)
            identation = identation + TAB
    else:
        PrintTerminal(syntaxLeaf.childs[0], identation, uminus)


def PrintRelationalOp(syntaxLeaf, identation):
    """ Definicion del metodo [PrintRelationalOp], el cual se encarga de imprimir
    la estructura [RelationalOperator] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
    """
    print(identation, symbols[syntaxLeaf.p_value])
    identation = identation + TAB
    for leaf in syntaxLeaf.childs:
        PrintExpression(leaf, identation)


def PrintBooleanOp(syntaxLeaf, identation):
    """ Definicion del metodo [PrintBooleanOp], el cual se encarga de imprimir
    la estructura [BooleanOperator] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
    """
    print(identation, symbols[syntaxLeaf.p_value])
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        PrintExpression(leaf, identation)


def PrintStrOp(syntaxLeaf, identation):
    """ Definicion del metodo [PrintStrOp], el cual se encarga de imprimir
    la estructura [StrOperator] del arbol sintactico.
    
    recibe: syntaxLeaf : objeto sintactico a ser analizado.
            identation : numero de tabs para margen izquierdo.
    """
    print(identation, "Concat")
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        print(identation, leaf)