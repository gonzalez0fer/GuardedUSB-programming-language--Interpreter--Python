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