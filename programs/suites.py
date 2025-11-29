# Programme de modélisation de suite arithmétiques
from math import *
import sys


PRECISION = 4

class CancelException(BaseException):
  pass

def do_exit():
  print(" \nSortie du programme.")
  sys.exit()

def req_int(msg, df, alwd=None):
  while True:
    i = input("    %s" % msg).strip()
    if i.lower() == "q":
      raise CancelException()
    if not i:
      return df
    if not i.isdigit():
      print("Veuillez entrer un entier naturel.")
      continue
    n = int(i)
    if alwd is not None and n not in alwd:
      print("Entrée non autorisée")
      continue
    return n

def req_fn(msg, vars, prev=None):
  vs = ", ".join(vars)
  while True:
    i = input("    %s" % msg).strip()
    if i.lower() == "q":
      raise CancelException()
    if not i:
      if prev is not None:
        return prev, eval("lambda %s: %s" % (vs, prev))
      else:
        print("Veuillez entrer une expression valide.")
        continue
    try:
      f = eval("lambda %s: %s" % (vs, i))
    except (SyntaxError, NameError, AttributeError):
      print("Une erreur de syntaxe a été détectée.")
      continue
    return i, f

def get_e(prev=None):
  if not prev:
    i0 = prev["i"] if prev else None
    print(" \nVeuillez entrer l'expression explicite de la")
    print("suite (u) en fonction de \"n\", l'indice du terme.")
    print("(expression interprétable en python) :")
    i, f = req_fn("u(n) = ", ["n"], i0)
  else:
    i, f = prev["i"], prev["f"]
  p0 = prev["p"] if prev else 0
  print(" \nVeuillez entrer l'entier p, limite inférieure")
  print("entière de la suite (par défaut : %d) :" % p0)
  p = req_int("p = ", p0)
  return {"t": "e", "i": i, "f": f, "p": p}

def get_r(prev=None):
  if not prev:
    i0 = prev["i"] if prev else None
    print(" \nVeuillez entrer l'expression (par réccurence) de")
    print("u(n+1) en fonction de \"un\", le terme précédent.")
    print("(expression interprétable en python) :")
    i, f = req_fn("u(n+1) = ", ["un"], i0)
  else:
    i, f = prev["i"], prev["f"]
  p0 = prev["p"] if prev else 0
  print(" \nVeuillez entrer l'entier p, limite inférieure")
  print("entière de la suite (par défaut : %d) :" % p0)
  p = req_int("p = ", p0)
  up0 = prev.get("up", 1) if prev else 1
  print(" \nVeuillez entrer le terme u(p), le terme initial")
  print("entier de la suite (par défaut : %d) :" % up0)
  up = req_int("u(p) = ", up0)
  return {"t": "r", "i": i, "f": f, "p": p, "up": up}

def get_s(first=False, prev=None):
  print(" \nChoisissez un type de suite :")
  print("(1) Formule explicite")
  print("(2) Relation de récurrence")
  if first:
    print("(3) Quitter")
  c = req_int("> ", None, [1,2,3])
  if c == 1:
    return get_e(prev=prev)
  if c == 2:
    return get_r(prev=prev)
  if c == 3 and first:
    do_exit()
  raise CancelException()

def suite_to_str(c):
  if c is None:
    return "aucune suite"
  t = S[c]["t"] == "e"
  s = S[c]
  what = "u(n)" if t else "u(n+1)"
  txt = (s["i"] if t else s["i"].replace("un","u(n)"))
  up = (", u(p) = %s" % s['up']) if not t else ""
  r = "[%d] %s = %s, p = %d%s" % (c + 1, what, txt, s['p'], up)

  return r

def pause():
  input("<Appuyez sur 'entrer' pour continuer>")

def paged(lines):
  cnt = 0
  for ln in lines:
    print(ln)
    cnt += 1
    if cnt == 10:
      pause()
      cnt = 0
  if cnt > 0:
    pause()

def fmt(x):
  try:
    if abs(x - int(x)) < 1e-9:
      return str(int(x))
  except: pass
  return ("%%.%dg" % PRECISION) % x

def term(s, n):
  p = s["p"]
  if n < p:
    raise ValueError
  if s["t"] == "e":
    return s["f"](n)
  else:
    if n == s["p"]:
      return s["up"]
    return s["f"](term(s, n - 1))

def term_str(lines, s, n):
  try:
    v = term(s,n)
    lines.append("u(%d) = %s" % (n, fmt(v)))
  except:
    lines.append("u(%d) = undef" % n)

def guard_empty_suites():
  if not S:
    print(" \nAucune suite.")
    raise CancelException
  else:
    print(" ")

def cmd_new():
  global S, c
  s = get_s()
  S.append(s)
  c = len(S)-1
  print("Suite ajoutée.")

def cmd_change():
  global S, c
  cmd_show()
  i = req_int("Suite à séléctionner : ", c + 1, list(range(1, len(S) + 1))) - 1
  if c == i:
    print("La suite est déjà séléctionnée.")
    return
  c = i
  print("Suite courante modifiée.")

def cmd_del():
  global S, c
  cmd_show()
  i = req_int("Index à supprimer (rien pour annuler) : ", None, list(range(1, len(S) + 1)))
  if i is None:
    print("Supression annulée.")
    return
  else:
    i -= 1
  S.pop(i)
  print("Suite supprimée.")
  if not S:
    s = get_s()
    S.append(s)
    c = 0
  else:
    c = min(i, len(S)-1)

def cmd_show():
  guard_empty_suites()
  lines = []
  for idx, s in enumerate(S):
    lines.append(suite_to_str(idx))
  paged(lines)

def cmd_first10():
  guard_empty_suites()
  p = S[c]["p"]
  lines = []
  for n in range(p, p+10):
    term_str(lines, S[c], n)
  paged(lines)

def cmd_interval():
  guard_empty_suites()
  p = S[c]["p"]
  print("    Veuillez saisir une intervalle :")
  a = req_int("n du début (par défaut %d) : " % p, p)
  b = req_int("n de la fin (par défaut %d) : " % (p + 9), p+9)
  if b < a:
    print("Intervalle invalide.")
    return
  lines = []
  for n in range(a, b+1):
    term_str(lines, S[c], n)
  paged(lines)

def cmd_nth():
  guard_empty_suites()
  s = S[c]
  p = s["p"]
  print("    Veulliez saisir un rang n :")
  n = req_int("n (par défaut %d) : " % p, p)
  try:
    v = term(s,n)
    print("u(%d) = %s" % (n, fmt(v)))
  except:
    print("Impossible de calculer u(%d)." % n)

def cmd_mod():
  global S, c
  cmd_change()
  S[c] = get_s(prev=S[c])
  print("Suite modifiée.")

def help():
  print(" \nUTILITAIRE DE MODÉLISATION DE SUITES")
  print("0 : Aide")
  print("1 : Nouvelle suite")
  print("2 : Changer la suite courante")
  print("3 : Supprimer une suite")
  print("4 : Afficher les suites")
  print("5 : Afficher les 10 premiers termes")
  print("6 : Afficher une intervalle")
  print("7 : Afficher u(n)")
  print("8 : Modifier suite")
  print("9 : Quitter")
  pause()


S = []
c = 0
def main():
  global S, c
  print("UTILITAIRE DE MODÉLISATION DE SUITES")
  print("À tout moment, entrez 'q' pour quitter.")

  S = []
  c = None
  try:
    S.append(get_s(first=True))
    c = 0
  except CancelException:
    pass

  running = True
  while running:
    print(" \n    Suite courante : %s" % suite_to_str(c))
    cmd = req_int("Entrez votre commande (\"0\" pour de l'aide) : ",
        0, [0,1,2,3,4,5,6,7,8,9])

    try:
      if cmd == 0:
        help()
      elif cmd == 1:
        cmd_new()
      elif cmd == 2:
        cmd_change()
      elif cmd == 3:
        cmd_del()
      elif cmd == 4:
        cmd_show()
      elif cmd == 5:
        cmd_first10()
      elif cmd == 6:
        cmd_interval()
      elif cmd == 7:
        cmd_nth()
      elif cmd == 8:
        cmd_mod()
      elif cmd == 9:
        do_exit()
    except CancelException:
      continue

main()
