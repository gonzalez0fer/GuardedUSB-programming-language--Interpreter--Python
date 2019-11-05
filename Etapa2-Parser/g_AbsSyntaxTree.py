#######################################
# CI3715 Traductores e Interpretadores
# Entrega 2. 
# Fernando Gonzalez 08-10464
# Kevin Mena 13-10869
#######################################

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


def printer(*args):
    print(color.RED,*args,color.END)
def printseq(identation):
    print(color.BLUE,identation,'Sequencing',color.END)

# Defino una variable global que fija un Tab de
#espacio para la identacion del arbol.
TAB = '  '

# Diccionario de simbolos
symbols = {
    "+": color.RED+"Plus"+color.END,
    "-": color.RED+"Minus"+color.END,
    "*": color.RED+"Mult"+color.END,
    "/": color.RED+"Div"+color.END,
    "%": color.RED+"Mod"+color.END,
    "\\/": color.RED+"Or"+color.END,
    "/\\": color.RED+"And"+color.END,
    "!": color.RED+"Not"+color.END,
    "<": color.RED+"Less"+color.END,
    "<=": color.RED+"Leq"+color.END,
    ">=": color.RED+"Geq"+color.END,
    ">": color.RED+"Greater"+color.END,
    "==": color.RED+"Equal"+color.END,
    "!=": color.RED+"NotEqual"+color.END
}

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
        elif (leaf._type == "Terminal"):
            PrintTerminal(leaf, identation)

def PrintDoLoop(syntaxLeaf, identation):
    printer(identation+TAB, "Exp\n")
    print(identation+TAB, "Ident:", syntaxLeaf.value)
    identation = identation + TAB

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
    printer(identation, syntaxLeaf.value)
    identation = identation + TAB

    print(identation, "Ident:", syntaxLeaf.childs[0])

def PrintOutput(syntaxLeaf, identation):
    if(syntaxLeaf.value == "Print"):
        printer(identation, "Print")
        identation = identation + TAB
    elif(syntaxLeaf.value == "Println"):
        printer(identation, "Println")
        identation = identation + TAB
    
    for leaf in syntaxLeaf.childs:
        if(leaf._type == "Expression"):
            PrintExpression(leaf, identation)
        else:
            PrintConcatExp(leaf, identation)

def PrintConcatExp(syntaxLeaf, identation):
    printer(identation, "Concat")
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        if(leaf._type == "Expression"):
            PrintExpression(leaf, identation)
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
    #elif (child._type == "ArrayOperator"):
        #PrintArrayOp
    #elif(child._type == "ArrayExpression"):
        #PrintArrayExp

# TO DO: Tal vez unir todas las funciones que son de esta forma en una sola
#        que se llame PrintOperations o algo asi
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
        else:
            print(identation, syntaxLeaf.value)
            identation = identation + TAB
    else:
        PrintTerminal(syntaxLeaf.childs[0], identation)


def PrintRelationalOp(syntaxLeaf, identation):
    print(identation, syntaxLeaf.value)
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        PrintExpression(leaf, identation)


def PrintBooleanOp(syntaxLeaf, identation):
    print(identation, syntaxLeaf.value)
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        PrintExpression(leaf, identation)

def PrintStrOp(syntaxLeaf, identation):
    print(identation, "Concat")
    identation = identation + TAB

    for leaf in syntaxLeaf.childs:
        print(identation, leaf)