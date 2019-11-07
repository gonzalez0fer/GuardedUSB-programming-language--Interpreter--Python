#######################################
# CI3715 Traductores e Interpretadores
# Entrega 2. 
# Fernando Gonzalez 08-10464
# Kevin Mena 13-10869
#######################################
from g_utils import *


class SyntaxLeaf:

    def __init__(self, _type, value = None, childs = None):
        self._type = _type
        self.value = value
        self.visited = False
        if childs:
            self.childs = childs
        else:
            self.childs = []


def SyntaxTreePrinter(syntaxLeaf, identation):
    if (syntaxLeaf):
        if(len(syntaxLeaf.childs) > 0):
            printer(identation, syntaxLeaf._type)
            identation = identation + TAB

            for leaf in syntaxLeaf.childs:
                if (leaf._type == "Declare"):
                    printer(identation, leaf._type)
                    identation = identation + TAB
                    PrintDeclaration(leaf, identation)
                elif (leaf._type == "Content"):
                    PrintContent(leaf, identation)

def PrintDeclaration(syntaxLeaf, identation):
    for leaf in syntaxLeaf.childs:
        #print('<<<',leaf.value,' ',leaf._type) ####PARA DEBUG
        if(leaf== ";"):
            printseq(identation)        
        elif(leaf._type == "Variable"):
            PrintVariable(leaf, identation+TAB)
        elif(leaf._type == "Declare"):
            PrintDeclaration(leaf, identation)

def PrintContent(syntaxLeaf, identation):
    if (len(syntaxLeaf.childs) == 1):
        child = syntaxLeaf.childs[0]

        if (child._type == "Instruction"):
            PrintInstruction(child, identation)
        elif (child._type == "Block"):
            SyntaxTreePrinter(child, identation)
    elif (len(syntaxLeaf.childs) >= 2):
        for leaf in syntaxLeaf.childs:
            if (leaf==';'):
                printseq(identation)
            elif(leaf._type == "Instruction"):
                PrintInstruction(leaf, identation)
            elif(leaf._type == "Block"):
                SyntaxTreePrinter(leaf, identation)
            elif(leaf._type == "Content"):
                PrintContent(leaf, identation)


def PrintInstruction(syntaxLeaf, identation):
    child = syntaxLeaf.childs[0]

    if(child._type == "Conditional"):
        printer(identation, "If")
        identation = identation + TAB
        PrintConditional(child, identation)
    elif(child._type == "Forloop"):
        printer(identation, "For\n",identation+ TAB, "In")
        PrintForLoop(child,identation+ TAB)
    elif(child._type == "Doloop"):
        printer(identation, "Do")
        PrintDoLoop(child,identation+ TAB)
    elif(child._type == "Asign"):
        PrintAsign(child, identation)
    elif(child._type == "Input"):
        PrintInput(child, identation)
    elif(child._type == "Output"):
        PrintOutput(child, identation)


def PrintForLoop(syntaxLeaf, identation):
    print(identation+TAB, "Ident:", syntaxLeaf.value)
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        if(leaf._type == "Content"):
            PrintContent(leaf, identation)
        elif (leaf._type == "Expression"):
            PrintExpression(leaf, identation)


def PrintDoLoop(syntaxLeaf, identation):
    #printer(identation+TAB, "Exp\n")
    #print(identation+TAB, "Ident:", syntaxLeaf.value)
    #identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        if(leaf._type == "Expression"):
            PrintExpression(leaf, identation)
        elif(leaf._type == "Content"):
            PrintContent(leaf, identation)
        elif(leaf._type == "Guard"):
            PrintConditional(leaf, identation)


def PrintConditional(syntaxLeaf, identation):
    printer(identation, "Guard")
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        if(leaf._type == "Expression"):
            PrintExpression(leaf, identation)
        elif(leaf._type == "Content"):
            PrintContent(leaf, identation)
        elif(leaf._type == "Guard"):
            PrintConditional(leaf, identation)


def PrintAsign(syntaxLeaf, identation):
    printer(identation, "Asig")
    identation = identation + TAB
    print(identation, "Ident:", syntaxLeaf.value)
    identation = identation + TAB

    PrintExpression(syntaxLeaf.childs[0], identation)


def PrintInput(syntaxLeaf, identation):
    printer(identation, "Read")
    identation = identation + TAB

    print(identation, "Ident:", syntaxLeaf.childs[0])

def PrintOutput(syntaxLeaf, identation):
    if(syntaxLeaf.value == "print"):
        printer(identation, "Print")
        identation = identation + TAB
    elif(syntaxLeaf.value == "println"):
        printer(identation, "Println")
        identation = identation + TAB
    
    for leaf in syntaxLeaf.childs:
        if(leaf._type == "Expression"):
            PrintExpression(leaf, identation + TAB)
        else:
            PrintConcatExp(leaf, identation + TAB)

def PrintConcatExp(syntaxLeaf, identation):
    printer(identation, "Concat")
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        if(leaf._type == "Expression"):
            PrintExpression(leaf, identation + TAB)
        else:
            PrintConcatExp(leaf, identation)

def PrintVariable(syntaxLeaf, identation):
    #print('>>>',syntaxLeaf.value) ####PARA DEBUG
    if(len(syntaxLeaf.childs) > 0):
        print(identation, "Ident:", syntaxLeaf.value)

        PrintVariable(syntaxLeaf.childs[0], identation)
    else:
        print(identation, "Ident:", syntaxLeaf.value)
        identation = identation + TAB


def PrintExpression(syntaxLeaf, identation):
    child = syntaxLeaf.childs[0]

    if (child._type == "AritmeticOperator"):
        print(identation, "Exp")
        identation = identation + TAB
        PrintAritmeticOp(child, identation) 
    elif (child._type == "Terminal"):
        PrintTerminal(child, identation)
    elif (child._type == "RelationalOperator"):
        print(identation, "Exp")
        identation = identation + TAB
        PrintRelationalOp(child, identation)
    elif (child._type == "BooleanOperator"):
        print(identation, "Exp")
        identation = identation + TAB
        PrintBooleanOp(child, identation)
    elif (child._type == "StrOperator"):
        print(identation, "Exp")
        identation = identation + TAB
        PrintStrOp(child, identation)
    elif (child._type == "ArrayOperator"):
        PrintArrayOp(child, identation)
    elif(child._type == "ArrayExpression"):
        print(identation, "Exp")
        identation = identation + TAB
        PrintArrayExp(child, identation)


def PrintArrayExp(syntaxLeaf, identation):
    if(len(syntaxLeaf.childs) == 2):
        printer(identation, "ArrayAsign")
        identation = identation + TAB
        if(isinstance(syntaxLeaf.value, SyntaxLeaf)):
            PrintArrayExp(syntaxLeaf.value, identation)
        else:
            print(identation, "Ident:", syntaxLeaf.value)

        for leaf in syntaxLeaf.childs:
                PrintTerminal(leaf, identation)
    else:
        printer(identation, "EvalArray")
        identation = identation + TAB
        if(isinstance(syntaxLeaf.value, SyntaxLeaf)):
            PrintArrayExp(syntaxLeaf.value, identation)
        else:
            print(identation, "Ident:", syntaxLeaf.value)

        for leaf in syntaxLeaf.childs:
                PrintTerminal(leaf, identation)


def PrintArrayOp(syntaxLeaf, identation):
    if(syntaxLeaf.value == "size"):
        printer(identation, "Size")
        identation = identation + TAB
    elif(syntaxLeaf.value == "max"):
        printer(identation, "Max")
        identation = identation + TAB
    elif(syntaxLeaf.value == "min"):
        printer(identation, "Min")
        identation = identation + TAB
    elif(syntaxLeaf.value == "atoi"):
        printer(identation, "Atoi")
        identation = identation + TAB
    
    child = syntaxLeaf.childs[0]

    if(isinstance(child, SyntaxLeaf)):
        print(identation, "Placeholder")
    else:
        print(identation, "Ident:", child)

def PrintAritmeticOp(syntaxLeaf, identation):
    print(identation, symbols[syntaxLeaf.value])
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        PrintExpression(leaf, identation)


def PrintTerminal(syntaxLeaf, identation):
    if (len(syntaxLeaf.childs) == 0):
        if(isinstance(syntaxLeaf.value, int)):
            print(identation, "Literal:", syntaxLeaf.value)
            identation = identation + TAB
        elif(syntaxLeaf.value.isalpha() and len(syntaxLeaf.value) == 1):
            print(identation, "Ident:", syntaxLeaf.value)
            identation = identation + TAB
        elif(syntaxLeaf.value != "True" and syntaxLeaf.value != "False"):
            print(identation + '"%s"' % syntaxLeaf.value)
            identation = identation + TAB
        else:
            print(identation, syntaxLeaf.value)
            identation = identation + TAB
    else:
        PrintTerminal(syntaxLeaf.childs[0], identation)


def PrintRelationalOp(syntaxLeaf, identation):
    print(identation, symbols[syntaxLeaf.value])
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        PrintExpression(leaf, identation)


def PrintBooleanOp(syntaxLeaf, identation):
    print(identation, symbols[syntaxLeaf.value])
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        PrintExpression(leaf, identation)

def PrintStrOp(syntaxLeaf, identation):
    print(identation, "Concat")
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        print(identation, leaf)