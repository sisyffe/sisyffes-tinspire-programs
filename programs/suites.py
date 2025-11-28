from math import *
import sys


def do_exit():
  print("Sortie du programme.")
  sys.exit()

def req_int(msg, df, alwd=None):
  while True:
    i = input("    %s" % msg).strip()
    if i.lower() == "q":
      do_exit()
    if not i:
      return df
    elif not i.isdigit():
      print("Veuillez entrer un entier naturel.")
      continue
    n = int(i)
    if alwd is not None and n not in alwd:
      print("Entrée non autorisée")
      continue
    return n

def req_fn(msg, vars):
  vs = ", ".join(vars)
  while True:
    i = input("    %s" % msg).strip()
    if i.lower() == "q":
      print("Sortie du programme.")
      sys.exit()
    try:
      f = eval("lambda %s: %s" % (vs, i))
    except SyntaxError:
      print("Une erreur de syntaxe a été détectée.")
      continue
    else:
      return i, f

def get_e():
  print(" \nVeuillez entrer l'expression explicite de la")
  print("suite (u) en fonction de \"n\", l'indice du terme.")
  print("(expression interprétable en python) :")
  i, f = req_fn("u(n) = ", ["n"])
  print(" \nVeuillez entrer l'entier p, limite inférieure")
  print("de la suite (par défaut : 0) :")
  p = req_int("p = ", 0)
  return {"t": "e", "i": i, "f": f, "p": p}

def get_r():
  print(" \nVeuillez entrer l'expression (par réccurence) de")
  print("u(n+1) en fonction de \"un\", le terme précédent.")
  print("(expression interprétable en python) :")
  i, f = req_fn("u(n+1) = ", ["un"])
  print(" \nVeuillez entrer l'entier p, limite inférieure")
  print("entière de la suite (par défaut : 0) :")
  p = req_int("p = ", 0)
  print(" \nVeuillez entrer le terme u(p), le terme initial")
  print("entier de la suite (par défaut : 1) :")
  up = req_int("u(p) = ", 1)
  return {"t": "r", "i": i, "f": f, "p": p, "up": up}

def show_s(s):
  t = s["t"] == "e"
  print("u(n) = " if t else "u(n+1) = ", end="")
  print(s["i"] if t else s["i"].replace("un", "u(n)"), end=", ")
  print("p = %d" % s["p"], end="")
  print(", u(p) = %d" % s["up"] if not t else "")

def get_s():
  print(" \nVeuilliez choisir un type de suite :")
  print("(1) Suite définie par une formule explicite")
  print("(2) Suite définie par une relation de réccurence")
  print("(q / autre) Quitter")
  c = req_int("> ", None, [1, 2])
  if c == 1:
    s = get_e()
  elif c == 2:
    s = get_r()
  else :
    do_exit()
  
  return s


def help():
  print("UTILITAIRE DE MODÉLISATION DE SUITES")
  print("0 : Afficher ce menu d'aide.")
  print("1 : Entrer une nouvelle suite.")
  print("2 : Supprimer une suite.")
  print("3 : Afficher les suites.")
  print("4 : Afficher les 10 premiers termes.")
  print("5 : Afficher une intervalle de termes.")
  print("6 : Afficher le n-ième terme.")
  print("7 : Modifier une suite.")
  print("9 : Quitter le programme.")
  input("<Appuiez sur 'entrer' pour continuer>")

s = None

def main():
  global s
  print("UTILITAIRE DE MODÉLISATION DE SUITES")
  print("À tout moment, entrez \"q\" pour quitter.")
  
  s = get_s()
  running = True
  while running:
    print(" \n    Suite : ", end="")
    show_s(s)
    print("    Entrez votre commande (\"0\" pour de l'aide)")
    break


main()
