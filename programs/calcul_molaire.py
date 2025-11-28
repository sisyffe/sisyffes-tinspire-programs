# Calculateur d'équilibrage d'équations chimiques

# Utiliser des valeurs aproximatives
# (simule un calcul sans logiciel)
USE_ROUNDED_VALUES = True
PRECISION = 4


import re

if not USE_ROUNDED_VALUES:
  NA = 6.02214076e23
  AM = {
    'H': 1.008, 'He': 4.0026022, 'Li': 6.94, 'Be': 9.01218315,
    'B': 10.81, 'C': 12.011, 'N': 14.007, 'O': 15.999,
    'F': 18.9984031636, 'Ne': 20.17976, 'Na': 22.989769282, 'Mg': 24.305,
    'Al': 26.98153857, 'Si': 28.085, 'P': 30.9737619985, 'S': 32.06,
    'Cl': 35.45, 'Ar': 39.9481, 'K': 39.09831, 'Ca': 40.0784,
    'Sc': 44.9559085, 'Ti': 47.8671, 'V': 50.94151, 'Cr': 51.99616,
    'Mn': 54.9380443, 'Fe': 55.8452, 'Co': 58.9331944, 'Ni': 58.69344,
    'Cu': 63.5463, 'Zn': 65.382, 'Ga': 69.7231, 'Ge': 72.6308,
    'As': 74.9215956, 'Se': 78.9718, 'Br': 79.904, 'Kr': 83.7982,
    'Rb': 85.46783, 'Sr': 87.621, 'Y': 88.905842, 'Zr': 91.2242,
    'Nb': 92.906372, 'Mo': 95.951, 'Tc': 98, 'Ru': 101.072,
    'Rh': 102.905502, 'Pd': 106.421, 'Ag': 107.86822, 'Cd': 112.4144,
    'In': 114.8181, 'Sn': 118.7107, 'Sb': 121.7601, 'Te': 127.603,
    'I': 126.904473, 'Xe': 131.2936, 'Cs': 132.905451966, 'Ba': 137.3277,
    'La': 138.905477, 'Ce': 140.1161, 'Pr': 140.907662, 'Nd': 144.2423,
    'Pm': 145, 'Sm': 150.362, 'Eu': 151.9641, 'Gd': 157.253,
    'Tb': 158.925352, 'Dy': 162.5001, 'Ho': 164.930332, 'Er': 167.2593,
    'Tm': 168.934222, 'Yb': 173.0451, 'Lu': 174.96681, 'Hf': 178.492,
    'Ta': 180.947882, 'W': 183.841, 'Re': 186.2071, 'Os': 190.233,
    'Ir': 192.2173, 'Pt': 195.0849, 'Au': 196.9665695, 'Hg': 200.5923,
    'Tl': 204.38, 'Pb': 207.21, 'Bi': 208.980401, 'Po': 209,
    'At': 210, 'Rn': 222, 'Fr': 223, 'Ra': 226,
    'Ac': 227, 'Th': 232.03774, 'Pa': 231.035882, 'U': 238.028913,
    'Np': 237, 'Pu': 244, 'Am': 243, 'Cm': 247,
    'Bk': 247, 'Cf': 251, 'Es': 252, 'Fm': 257,
    'Md': 258, 'No': 259, 'Lr': 266, 'Rf': 267,
    'Db': 268, 'Sg': 269, 'Bh': 270, 'Hs': 269,
    'Mt': 278, 'Ds': 281, 'Rg': 282, 'Cn': 285,
    'Nh': 286, 'Fl': 289, 'Mc': 289, 'Lv': 293,
    'Ts': 294, 'Og': 294, 'Uue': 315
  }
else:
  NA = 6.02e23
  AM = {
    'H': 1.0, 'He': 4.0, 'Li': 6.9, 'Be': 9.0,
    'B': 10.8, 'C': 12.0, 'N': 14.0, 'O': 16.0,
    'F': 19.0, 'Ne': 20.2, 'Na': 23.0, 'Mg': 24.3,
    'Al': 27.0, 'Si': 28.1, 'P': 31.0, 'S': 32.1,
    'Cl': 35.5, 'Ar': 39.9, 'K': 39.1, 'Ca': 40.1,
    'Sc': 45.0, 'Ti': 47.9, 'V': 50.9, 'Cr': 52.0,
    'Mn': 54.9, 'Fe': 55.8, 'Co': 58.9, 'Ni': 58.7,
    'Cu': 63.6, 'Zn': 65.4, 'Ga': 69.7, 'Ge': 72.6,
    'As': 74.9, 'Se': 79.0, 'Br': 79.9, 'Kr': 83.8,
    'Rb': 85.5, 'Sr': 87.6, 'Y': 88.9, 'Zr': 91.2,
    'Nb': 92.9, 'Mo': 96.0, 'Tc': 98, 'Ru': 101.1,
    'Rh': 102.9, 'Pd': 106.4, 'Ag': 107.9, 'Cd': 112.4,
    'In': 114.8, 'Sn': 118.7, 'Sb': 121.8, 'Te': 127.6,
    'I': 126.9, 'Xe': 131.3, 'Cs': 132.9, 'Ba': 137.3,
    'La': 138.9, 'Ce': 140.1, 'Pr': 140.9, 'Nd': 144.2,
    'Pm': 145, 'Sm': 150.4, 'Eu': 152.0, 'Gd': 157.3,
    'Tb': 158.9, 'Dy': 162.5, 'Ho': 164.9, 'Er': 167.3,
    'Tm': 168.9, 'Yb': 173.0, 'Lu': 175.0, 'Hf': 178.5,
    'Ta': 180.9, 'W': 183.8, 'Re': 186.2, 'Os': 190.2,
    'Ir': 192.2, 'Pt': 195.1, 'Au': 197.0, 'Hg': 200.6,
    'Tl': 204.4, 'Pb': 207.2, 'Bi': 209.0, 'Po': 209,
    'At': 210, 'Rn': 222, 'Fr': 223, 'Ra': 226,
    'Ac': 227, 'Th': 232.0, 'Pa': 231.0, 'U': 238.0,
    'Np': 237, 'Pu': 244, 'Am': 243, 'Cm': 247,
    'Bk': 247, 'Cf': 251, 'Es': 252, 'Fm': 257,
    'Md': 258, 'No': 259, 'Lr': 266, 'Rf': 267,
    'Db': 268, 'Sg': 269, 'Bh': 270, 'Hs': 269,
    'Mt': 278, 'Ds': 281, 'Rg': 282, 'Cn': 285,
    'Nh': 286, 'Fl': 289, 'Mc': 289, 'Lv': 293,
    'Ts': 294, 'Og': 294, 'Uue': 315
  }


def conf(msg):
  i = input("Voulez-vous %s (O-/N) ? " % msg)
  return i.upper() in ("-", "O")


def gcd(*lst):
  g = 0
  for x in (abs(e) for e in lst):
    while x:
      g, x = x, g % x
  return g

def lcm(*lst):
  l = 1
  for x in (abs(e) for e in lst):
    l = l*x // gcd(l, x)
  return l

def isdecimal(s):
  for c in s:
    if not ('0' <= c <= '9'):
      return False
  return True


class Quo:
  def __init__(self,n,d=1):
    if d==0:
      raise ZeroDivisionError("den is 0")
    if d<0:
      n,d = -n,-d
    g = gcd(n,d)
    self.n = n//g
    self.d = d//g
  @staticmethod
  def zero():
    return R(0,1)
  def iszero(self):
    return self.n==0
  def __add__(self,o):
    return Quo(self.n*o.d + o.n*self.d, self.d*o.d)
  def __sub__(self,o):
    return Quo(self.n*o.d - o.n*self.d, self.d*o.d)
  def __mul__(self,o):
    return Quo(self.n*o.n, self.d*o.d)
  def __truediv__(self,o):
    if o.n==0:
      raise ZeroDivisionError("den is 0")
    return Quo(self.n*o.d, self.d*o.n)
  def __neg__(self):
    return Quo(-self.n, self.d)
  def __eq__(self,o):
    return self.n==o.n and self.d==o.d
  def recip(self):
    if self.n==0:
      raise ZeroDivisionError("no reciprocal for 0")
    return Quo(self.d, self.n)
  def __repr__(self):
    if self.d==1:
      return str(self.n)
    return "%d/%d"%(self.n,self.d)

class Molecule:
  def __init__(self, atoms, formula):
    self.atoms = atoms
    assert all(isinstance(k, str) for k in atoms.keys()), "invalid atom"
    assert all(isinstance(v, int) for v in atoms.values()), "invalid atom count"
    for n in atoms.keys():
      if n not in AM.keys() and n != "_q":
        raise ValueError("l'atome %s n'existe pas" % n)
    self.formula = formula
  @classmethod
  def from_str(cls, s):
    atoms = pf(s)
    charge = atoms.get('_q', 0)

    end = len(s)
    while s[end - 1] in ("+", '-'):
      end -= 1
    formula = s[:end]
    if charge != 0:
      formula += "^"
      if abs(charge) != 1:
        formula += str(abs(charge))
      formula += ('+' if charge > 0 else '-')

    return cls(atoms, formula)

def rref(matrix):
  A = [row[:] for row in matrix]
  rows = len(A)
  cols = len(A[0]) if rows > 0 else 0
  pivots = []
  r = 0

  for c in range(cols):
    pivot_row = None
    for i in range(r, rows):
      if not A[i][c].iszero():
          pivot_row = i
          break

    if pivot_row is None:
      continue

    A[r], A[pivot_row] = A[pivot_row], A[r]
    pivot = A[r][c]
    inv_pivot = pivot.recip()

    A[r] = [val * inv_pivot for val in A[r]]

    for i in range(rows):
      if i == r:
        continue
      factor = A[i][c]
      if not factor.iszero():
        A[i] = [A[i][j] - factor * A[r][j] for j in range(cols)]

    pivots.append(c)
    r += 1
    if r == rows:
      break

  return A, pivots

# null space basis
def nsb(matrix):
  if not matrix:
    return []

  R, pivots = rref(matrix)
  rows = len(R)
  cols = len(R[0]) if rows > 0 else 0
  pivot_set = set(pivots)
  free_vars = [j for j in range(cols) if j not in pivot_set]
  basis = []

  for f in free_vars:
    vector = [Quo(0, 1) for _ in range(cols)]
    vector[f] = Quo(1, 1)

    for ri, pc in enumerate(pivots):
      coef = R[ri][f]
      if not coef.iszero():
        vector[pc] = -coef
      else:
        vector[pc] = Quo(0, 1)

    basis.append(vector)

  return basis

# rational vector to integers
def rvi(vector):
  dens = [v.d for v in vector if not v.iszero()]
  if not dens:
    return [0] * len(vector)

  mult = lcm(*dens)
  ints = [v.n * (mult // v.d) for v in vector]

  if all(x <= 0 for x in ints) and any(x < 0 for x in ints):
    ints = [-x for x in ints]

  nonz = [abs(x) for x in ints if x != 0]
  if nonz:
    g = gcd(*nonz)
    if g > 1:
      ints = [x // g for x in ints]

  return ints

# find integer solution
def fis(basis, max_coeff=6):
  if not basis:
    return None

  if len(basis) == 1:
    return rvi(basis[0])

  d = len(basis)
  rows = len(basis[0])
  best = None
  coeffs = [1] * d

  def recursive_search(i):
    nonlocal best, coeffs
    if i == d:
      v = [Quo(0, 1) for _ in range(rows)]
      for bi in range(d):
        c = coeffs[bi]
        for r in range(rows):
          v[r] = v[r] + (basis[bi][r] * Quo(c, 1))

      ints = rvi(v)
      if all(x >= 0 for x in ints) and any(x > 0 for x in ints):
        if best is None or sum(ints) < sum(best):
          best = ints[:]
      return

    for c in range(1, max_coeff + 1):
      coeffs[i] = c
      recursive_search(i + 1)

  recursive_search(0)
  return best if best is not None else rvi(basis[0])

# Balance reaction
def bal(reactants, products):
    elements = []
    for m in reactants + products:
        for e in m:
            if e not in elements:
                elements.append(e)

    n_reactants = len(reactants)
    n_products = len(products)

    matrix = []
    for el in elements:
        row = []
        for m in reactants:
            row.append(Quo(m.get(el, 0), 1))
        for m in products:
            row.append(Quo(-m.get(el, 0), 1))
        matrix.append(row)

    basis = nsb(matrix)
    if not basis:
        raise ValueError("pas de solution : espace nul vide.")

    solution = fis(basis, 8)
    if not solution:
        raise ValueError("pas de combinaison entière positive.")

    # Vérifie que la solution est valide
    if all(x <= 0 for x in solution) and any(x < 0 for x in solution):
        solution = [-x for x in solution]
    if any(x < 0 for x in solution):
        raise ValueError("solution avec coefficients négatifs.")
    if all(x == 0 for x in solution):
        raise ValueError("solution nulle.")

    nonz = [abs(x) for x in solution if x != 0]
    if nonz:
        g = gcd(*nonz)
        if g > 1:
            solution = [x // g for x in solution]

    reactant_coeffs = solution[:n_reactants]
    product_coeffs = solution[n_reactants:]

    return reactant_coeffs, product_coeffs


# Parse formula
def pf(formula):
  def parse_atom(s, start):
    if start >= len(s):
      return None, start

    if not s[start].isupper():
      return None, start

    i = start + 1
    while i < len(s) and s[i].islower():
      i += 1

    atom = s[start:i]
    j = i
    while j < len(s) and s[j].isdigit():
      j += 1

    count = int(s[i:j]) if i < j else 1
    return (atom, count), j

  def parse_group(s, start):
    if start >= len(s) or s[start] != '(':
      return None, start

    i = start + 1
    depth = 1
    group_start = i

    while i < len(s) and depth > 0:
      if s[i] == '(':
        depth += 1
      elif s[i] == ')':
        depth -= 1
      i += 1

    if depth != 0:
      return None, start

    group_content = s[group_start:i-1]
    j = i
    while j < len(s) and s[j].isdigit():
      j += 1

    multiplier = int(s[i:j]) if i < j else 1
    return (group_content, multiplier), j

  def parse_charge(s):
    charge = 0
    i = len(s) - 1
    while i > 0 and s[i] in ('+', '-'):
      if s[i] == '+':
        charge += 1
      elif s[i] == '-':
        charge -= 1
      i -= 1
    return charge

  molecule = {}
  i = 0
  n = len(formula)

  while i < n:
    group_info, new_i = parse_group(formula, i)
    if group_info is not None:
      group_content, multiplier = group_info
      group = pf(group_content)
      for atom, count in group.items():
        if atom == '_q':
          continue
        molecule[atom] = molecule.get(atom, 0) + count * multiplier
      i = new_i
    else:
      atom_info, new_i = parse_atom(formula, i)
      if atom_info is not None:
        atom, count = atom_info
        molecule[atom] = molecule.get(atom, 0) + count
        i = new_i
      else:
        i += 1

  charge = parse_charge(formula)
  molecule['_q'] = charge

  return molecule

# Masse molaire
def mmass(m):
  t = 0.0
  for e, c in m.items():
    if e in AM:
      t += AM[e] * c
  return t


HELP = [
  "=== Équilibreur de réactions ===",
  "0  : Aide",
  "1  : Ajouter réactif(s)",
  "2  : Ajouter produit(s)",
  "3  : Afficher les éléments",
  "4  : Modifier une formule",
  "5  : Équilibrer",
  "6  : Masse molaire",
  "7  : Quantité matière (1 g / 1 kg)",
  "8  : Masse d'une entité (g)",
  "9  : Effacer tout",
  "q  : Quitter",
]

PROMPT = []

reactants = []
products = []

H = 10

def draw(lines):
  maxl = H
  for i,l in enumerate(lines):
    if i >= maxl:
      rem = len(lines) - maxl
      input("... (%d lignes restantes) " % rem)
      maxl += H
    print(l)
  input("Appuyez sur Entrée pour continuer...")


def list_mol():
  lines = ["=== Réactifs ==="]
  i = 0
  for i, mol in enumerate(reactants, 1):
    lines.append("%d : %s" % (i, mol.formula))
  if len(reactants) == 0:
    lines.append("- aucun réactif -")
  lines.append(" ")
  lines.append("=== Produits ===")
  for i, mol in enumerate(products, i + 1):
    lines.append("%d : %s" % (i, mol.formula))
  if len(products) == 0:
    lines.append("- aucun produit -")
  lines.append(" ")
  draw(lines)

def select_mol(allow_new = True):
  list_mol()
  prompt = "Index du choix ou autre molécule :" if allow_new \
      else "Index de la molécule à choisir :"
  try:
    print(prompt)
    choice = input().strip()

    if isdecimal(choice):
      index = int(choice)
      if 1 <= index <= len(reactants):
        place = reactants, index - 1
      elif len(reactants) + 1 <= index <= len(reactants) + len(products):
        place = products, index - len(reactants) - 1
      else:
        raise ValueError

      mol = place[0][place[1]]
      print('Vous avez choisi %s.' % mol.formula)
      return mol, place

    elif allow_new:
      mol = Molecule.from_str(choice)
      place = None
      print('Vous avez choisi %s.' % mol.formula)
      return mol, place

    else:
      raise ValueError

  except ValueError:
    print('Molécule inexistante (index invalide ou mal formulée).')
    return None, None

def modify():
  global reactants, products
  try:
    mol, place = select_mol(allow_new=False)
    if mol is None:
      return
    new_formula = input("Nouvelle formule : ").strip()
    molecule = Molecule.from_str(new_formula)
    place[0][place[1]] = molecule
  except Exception as e:
    print("Erreur la modification : %s.\n." % e)


def cli():
  global reactants, products

  while True:
    print(" ")
    print("    Réactifs: %d | Produits: %d" % (len(reactants), len(products)))
    choice = input("    Équilibreur ('0' pour aide) > ").strip()
    print(" ")

    if choice == "0":
      draw(HELP)

    elif choice == "1":
      print("Formule(s) du/des réactifs(s)")
      print("(séparés par des espaces) : ")
      formulas = input().strip().split()
      for f in formulas:
        try:
          molecule = Molecule.from_str(f)
          reactants.append(molecule)
        except Exception as e:
          print("Erreur pour %s: %s. Ignoré" % (f, e))
      print("Réactifs ajoutés !")

    elif choice == "2":
      print("Formule(s) du/des produits(s)")
      print("(séparés par des espaces) : ")
      formulas = input().strip().split()
      for f in formulas:
        try:
          molecule = Molecule.from_str(f)
          products.append(molecule)
        except Exception as e:
          print("Erreur pour %s: %s. Ignoré" % (f, e))
      print("Produits ajoutés !")

    elif choice == "3":
      list_mol()
    elif choice == "4":
      modify()

    elif choice == "5":
      try:
        r_atoms = [mol.atoms for mol in reactants]
        p_atoms = [mol.atoms for mol in products]
        r_coeffs, p_coeffs = bal(r_atoms, p_atoms)
        lines = ["=== Réaction équilibrée ==="]
        for coeff, mol in zip(r_coeffs, reactants):
          lines.append("%d %s" % (coeff, mol.formula))
        lines.append("→")
        for coeff, mol in zip(p_coeffs, products):
          lines.append("%d %s" % (coeff, mol.formula))
        lines.append(" ")
        draw(lines)
      except Exception as e:
        print("Erreur lors de l'équilibrage : %s.\nVeuillez vérifier les molécules de la réaction." % e)

    elif choice == "6":
      mol, place = select_mol()
      if mol is None:
        continue
      m_mass = mmass(mol.atoms)
      print(("    %%s → %%.%dg g/mol" % PRECISION) % (mol.formula, m_mass))

    elif choice == "7":
      mol, place = select_mol()
      if mol is None:
        continue
      quantity = 1000 / mmass(mol.atoms)
      print(("    %%s → %%.%dg mol/kg" % PRECISION) % (mol.formula, quantity))

    elif choice == "8":
      mol, place = select_mol()
      if mol is None:
        continue
      mass = mmass(mol.atoms) / NA
      print(("    1 entité de %%s → %%.%dg g" % PRECISION) % (mol.formula, mass))

    elif choice == "9":
      if conf("effacer la mémoire"):
        reactants = []
        products = []
        print("Tout a été effacé.")

    elif choice.lower()=='q':
      if conf("quitter le programme"):
        print("Au revoir !")
        break

    else:
      print("Commande inconnue (tapez 0 pour l'aide).")

cli()
