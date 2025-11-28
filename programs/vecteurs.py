
# Calcul vectoriel

from math import *


PRECISION = 3


opp = lambda u: (-u[0], -u[1])
add = lambda u, v: (u[0] + v[0], u[1] + v[1])
sub = lambda u, v: (u[0] - v[0], u[1] - v[1])
mul = lambda k, u: (k * u[0], k * u[1])
norm = lambda u: sqrt(u[0] ** 2 + u[1] ** 2)
norz = lambda u: (0, 0) if norm(u) == 0 else (u[0] / norm(u), u[1] / norm(u))
dot = lambda u, v: u[0] * v[0] + u[1] * v[1]
det = lambda u, v: u[0] * v[1] - u[1] * v[0]
is_eq = lambda u, v: u == v

fr_pt = lambda xa, ya, xb, yb: (xb - xa, yb - ya)

NAMES = {
  "u": ["1"],
  "v": ["2"],
  "k": ["3"],
  "-u": ["4"],
  "-v": ["5"],
  "u+v": ["7", "+"],
  "u-v": ["8", "++"],
  "v-u": ["9"],
  "ku": ["11", "*"],
  "kv": ["13", "**"],
  "=u": ["14", "("],
  "=v": ["16", ")"],
  "/u": ["17", "/"],
  "/v": ["19", "//"],
  "u*v": ["21", "."],
  "u,v": ["24", ","],
  "v,u": ["26", ",,"],
  "u=v": ["23", "=", "=="]
}

ns = {}
for k, v in NAMES.items():
  ns[k] = k
  ns[k.replace("u", "1").replace("v", "2")] = k
  for n in v:
    ns[n] = k


HELP = {
  "u": "Vecteur u",
  "v": "Vecteur v",
  "k": "Nombre réel k",
  "-u": "Opposé de u",
  "-v": "Opposé de v",
  "u+v": "Somme de u et v",
  "u-v": "Différence de u et v",
  "v-u": "Différence de v et u",
  "ku": "Produit de k par u",
  "kv": "Produit de k par v",
  "=u": "Norme de u",
  "=v": "Norme de v",
  "/u": "Normaliser u",
  "/v": "Normaliser v",
  "u*v": "Produit scalaire de u et v",
  "u,v": "Déterminant de u et v",
  "v,u": "Déterminant de v et u",
  "u=v": "Égalité des vecteurs u et v"
}

VARS = ["u", "v", "k", "-u", "-v", "u+v", "u-v",
  "v-u", "ku", "kv", "=u", "=v", "/u", "/v", "u*v",
  "u,v", "v,u", "u=v"]


def proc(u, v, k):
  du, dv, dk = u is not None, \
    v is not None, k is not None
  duv = u and dv

  d = {}
  def f(v, s, e):
    if v:
      d[s] = e()

  f(du, "u", lambda: u)
  f(dv, "v", lambda: v)
  f(dk, "k", lambda: k)
  f(du, "-u", lambda: opp(u))
  f(dv, "-v", lambda: opp(v))
  f(duv, "u+v", lambda: add(u, v))
  f(duv, "u-v", lambda: sub(u, v))
  f(duv, "v-u", lambda: sub(v, u))
  f(dk and du, "ku", lambda: mul(k, u))
  f(dk and dv, "kv", lambda: mul(k, v))
  f(du, "=u", lambda: norm(u))
  f(dv, "=v", lambda: norm(v))
  f(du, "/u", lambda: norz(u))
  f(dv, "/v", lambda: norz(v))
  f(duv, "u*v", lambda: dot(u, v))
  f(duv, "u,v", lambda: det(u, v))
  f(duv, "v,u", lambda: det(v, u))
  f(duv, "u=v", lambda: is_eq(u, v))

  return d


def req():
  global u, v

  def r(s):
    if s == "k":
      return rk()

    while True:
      print(" \nEntrez les coordonnées du vecteur %s," % s)
      print("sous forme de deux points : \"xA yA xB yB\",")
      print("ou directement en coordonnées : \"x%s y%s\"." % (s.upper(), s.upper()))
      print("Entrez \"q\" ou rien pour annuler.\n ")
      inp = input("Coordonnées ou points de %s: " % s).strip()
      print(" ")

      if not inp or inp.lower() == "q":
        print("Entrée annulée")
        return None
      if inp == "0":
        inp = "0 0"

      l = inp.split(" ")
      if len(l) not in (2, 4):
        print("Valeurs non conformes en nombre.")
        continue

      ns = []
      b = False
      for n in l:
        try:
          e = eval(n)
          if not isinstance(e, (int, float)):
            print("Classe de valeur invalide.")
          ns.append(e)
        except Exception:
          print("La valeur \"%s\" est invalide." % n)
          b = True
          break
      if b: continue

      if len(ns) == 2:
        r = ns[0], ns[1]
      elif len(ns) == 4:
        r = ns[2] - ns[0], ns[3] - ns[1]

      print(("Le vecteur {} a pour coords. ({:.%sf}; {:.%sf})" % (PRECISION, PRECISION)).format(s, r[0], r[1]))
      return r

  def rk():
    while True:
      print(" \nEntrez le coefficient multiplicateur k.")
      print("Entrez \"q\" ou rien pour annuler.\n ")
      inp = input("Coefficient multiplicateur k : ").strip()
      print(" ")

      if not inp or inp.lower() == "q":
        print("Entrée annulée")
        break

      try:
        e = eval(inp)
        if not isinstance(e, (int, float)):
          print("Classe de valeur invalide.")
        k = e
      except Exception:
        print("La valeur \"%s\" est invalide.")
        continue

      return k

  u = r("u")
  v = r("v")
  k = r("k")

  return u, v, k


def show():
  def quoted(s):
    return "\"{}\"".format(s)

  for i, e in enumerate(VARS):
    n = HELP[e]
    o = NAMES[e]
    o.insert(0, e.replace("u", "1").replace("v", "2"))
    o.insert(0, e)

    if (i + 1) % 6 == 0:
      input(" \n<\"enter\" pour continuer>")
      print(" ")

    print("{} : {}".format(n, ", ".join(quoted(s) for s in o)))


def main():
  u, v, k = req()
  d = proc(u, v, k)

  while True:
    print(" \nEntrez \"0\" pour plus de commandes.")
    print("Entrez \"-\" pour resaisir les variables.")
    inp = input("Commande (\"<enter>\" pour quitter): ").strip()
    print(" ")

    if inp == "":
      p = input("Confirmation de vouloir quitter (O-/N) : ")
      if p.lower() in ("-", "o"):
        print("Arrêt du programme.")
        break
    if inp == "0":
      show()
      continue
    if inp == "-":
      u2, v2, k2 = req()
      u = u2 if u2 is not None else u
      v = v2 if v2 is not None else v
      k = k2 if k2 is not None else k
      d = proc(u, v, k)
      continue
    if inp not in ns:
      print("Entrée \"%s\" invalide." % inp)
      continue

    e = ns[inp]
    if e not in d:
      print("Entrée \"%s\" (\"%s\") inexistante." % (inp, e))
      print("Ajoutez les variables necessaires (\"0\").")
      continue

    a = d[e]
    if isinstance(a, (int, float)):
      print(("{} ⇒ {:.%df}" % PRECISION).format(HELP[e], a))
    elif isinstance(a, tuple):
      print(("{} ⇒ ({:.%df}; {:.%df})" % (PRECISION, PRECISION)).format(HELP[e], *a))
    elif isinstance(a, bool):
      print("{} ⇒ {}".format(HELP[e], a))
    else:
      assert False
    if e in ("=u", "=v"):
      print("{} ⇒ sqrt({:.1f})".format(HELP[e], a ** 2))


main()
