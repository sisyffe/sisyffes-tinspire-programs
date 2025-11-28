# Programme tableur statistiques

from math import *


PRECISION = 2

SEP_CHAR = ' | '
FILLER_CHAR = '_'
HALF_FILLER_CHAR = ' '

MAJ_SCALE = 1.25
SPACE_SCALE = 2
HYPHEN_SCALE = 1.125
DOT_SCALE = 0.625

SCREEN_WIDTH = 39
HEAD_WIDTH = 2.5


def get_float(value):
  try:
    return float(value)
  except ValueError:
    return None


def get_int(value):
  try:
    return int(value)
  except ValueError:
    return None


def try_eval(expr):
  try:
    return eval(str(expr))
  except ValueError:
    return None


def length_to_screen_width(string):
  count = 0
  len_count = 0
  for char in string:
    len_count += 1
    if char in (' ', '|', ':', ','):
      count += 1 / SPACE_SCALE
    elif char in ('-',):
      count += 1 / HYPHEN_SCALE
    elif char in ('.',):
      count += 1 / DOT_SCALE
    elif char.lower() == char:  # any char
      count += 1
    else:  # upper case
      count += 1 / MAJ_SCALE
    if count >= SCREEN_WIDTH - HEAD_WIDTH:
      return len_count
  return len_count


def true_len(string):
  count = 0
  for char in string:
    if char in (' ', '|', ':', ','):
      count += 1 / SPACE_SCALE
    elif char in ('-',):
      count += 1 / HYPHEN_SCALE
    elif char in ('.',):
      count += 1 / DOT_SCALE
    elif char.lower() == char:  # any char
      count += 1
    else:  # upper case
      count += 1 / MAJ_SCALE
  return count


def format_spaces(obj, spacing = 3, spacer = ' ', pos_end = False):
  s = str(obj)
  spaces_to_go = max(spacing - true_len(s), 0)
  whole_sep, part_sep = divmod(spaces_to_go, 1)
  spaces = spacer * int(whole_sep) + HALF_FILLER_CHAR * round(part_sep * 2)
  return spaces + s if pos_end else s + spaces


def load_test(tbl):
  tbl.set_to(
    [2, 10, 2.5, 100, 5, 8.01, 50, 2.34, 20, 21, 512, 1024],
    [3, 5.666, 6, 5.334, 5.34, 2, 100, 1.5, 30.16, 31, 64, 1.024]
  )


class Table:
  def __init__(self, values = None, effectifs = None):
    self.values = values if values is not None else []
    self.effectifs = effectifs if effectifs is not None else []
    self.eccs = []

    self.eff_total = 0
    self.length = 0
    self.refresh()

  @property
  def zip(self):
    assert self.length, "Table vide ou non calculée"
    return zip(self.values, self.effectifs, self.eccs)

  def add(self, value, eff):
    if eff == 0:
      raise ValueError("L'effictif ne peut pas être nul")
    self.values.append(value)
    self.effectifs.append(eff)
    self.length = 0

  def pop_back(self):
    self.length = 0
    return self.values.pop(), self.effectifs.pop()

  def set_to(self, values, effectifs):
    self.values = list(values)
    self.effectifs = list(effectifs)
    self.refresh()

  def refresh(self):
    length = len(self.values)
    assert length == len(self.effectifs), "invalid data"
    self.length = length

    self.eccs.clear()
    running_sum = 0
    for e in self.effectifs:
      running_sum += e
      self.eccs.append(running_sum)  # copy of running_sum
    self.eff_total = running_sum

  def average(self):
    # average
    assert self.length, "Table vide ou non calculée"

    weight = 0
    running_sum = 0
    for v, e, c in self.zip:
      running_sum += v * e
      weight += e
    return running_sum / weight

  def quartiles_plus(self):
    # (rang_quartile_1, quartile_1), (rang_mediane, mediane), (rq3, q3), ecart_inter_quartile
    assert self.length, "Table vide ou non calculée"

    sorted_table = sorted(
      zip(self.values, self.effectifs),
      key=lambda k: k[0]
    )

    def get_at_pos(pos_int):
      assert pos_int < self.eff_total, "index out of range"
      counter = 0
      for v, e in sorted_table:
        counter += e
        if counter > pos_int:
           return v

    def average_pos(pos_float, force_even = False):
      assert pos_float < self.eff_total, "index out of range"
      if pos_float % 1 == 0.0: # int
        return get_at_pos(int(pos_float))

      lower_pos, upper_pos = floor(pos_float), ceil(pos_float)
      lower, upper = get_at_pos(lower_pos), get_at_pos(upper_pos)

      if force_even:
        return (lower + upper) / 2
      coeff_lower, coeff_upper = upper_pos - pos_float, pos_float - lower_pos
      return lower * coeff_lower + upper * coeff_upper

    rq1 = self.eff_total * 0.25 - 1
    crq1 = ceil(rq1)
    rme = (self.eff_total - 1) * 0.5
    rq3 = self.eff_total * 0.75 - 1
    crq3 = ceil(rq3)

    q1 = get_at_pos(crq1 if crq1 < self.eff_total else self.eff_total - 1)
    me = average_pos(rme)
    q3 = get_at_pos(crq3 if crq3 < self.eff_total else self.eff_total - 1)
    ecart_itq = q3 - q1

    return (rq1, q1), (rme, me), (rq3, q3), ecart_itq

  def others(self, avg = None):
    # étendue, variance, ecart_type
    assert self.length, "Table vide ou non calculée"

    etendue = max(self.values) - min(self.values)
    avg = avg if avg is not None else self.average()

    running_sum = 0
    weight = 0
    for v, e, c in self.zip:
      running_sum += e * pow(v - avg, 2)
      weight += e
    variance = running_sum / weight

    ecart_type = sqrt(variance)

    return etendue, variance, ecart_type


class TableManager(Table):
  def __init__(self):
    super().__init__()
    self.table_buffer_cache = ""
    self.average_buffer_cache = ""

  @staticmethod
  def split_lines(*lines):
    whole_length = len(lines[0])
    start_index = 0
    while start_index < whole_length:
      end_index = start_index + length_to_screen_width(lines[0][start_index:])
      if end_index < whole_length:
        while not all(
            line[end_index - len(SEP_CHAR):end_index] == SEP_CHAR
            for line in lines
        ):
          assert end_index >= 0, "erreur de formattage"
          end_index -= 1

      yield tuple(line[start_index:end_index] for line in lines)
      start_index = end_index

  def refresh(self):
    super().refresh()

    if not self.length:
      self.table_buffer_cache = "[empty]"
      self.table_buffer_cache = "[empty]"
      return

    data = zip(
      ("#{}".format(n) for n in range(1, self.length + 1)),
      (int(v) if v % 1 == 0.0 else v for v in self.values),
      (int(e) if e % 1 == 0.0 else e for e in self.effectifs),
      (int(c) if c % 1 == 0.0 else c for c in self.eccs)
    )  # add index and remove unnecessary floating part
    str_data = (
      tuple(str(o).replace(".", ",") for o in t)  # gone through 2 times so tuple
      for t in data
    )  # converts everything to str
    length_data = (
      (d, max(true_len(x) for x in d))
      for d in str_data
    )  # compute the maximum length info
    spaced_data = (
      tuple(format_spaces(o, m, FILLER_CHAR) for o in t)
      for t, m in length_data
    )  # format everything with spaces

    lines = zip(*spaced_data)
    str_lines = (SEP_CHAR.join(l) for l in lines)
    splitted_lines = self.split_lines(*str_lines)

    average = self.average()
    (rq1, q1), (rme, me), (rq3, q3), ec_itq = self.quartiles_plus()
    etendue, var, ecty = self.others(average)

    table_buffer = ""
    for line_n, line_v, line_e, line_c in splitted_lines:
      table_buffer += "# : {}\n".format(line_n)
      table_buffer += "v : {}\n".format(line_v)
      table_buffer += "e : {}\n".format(line_e)
      table_buffer += "c : {}\n".format(line_c)
      table_buffer += "-"*ceil(SCREEN_WIDTH / HYPHEN_SCALE) + '\n'
    table_buffer = table_buffer[:-1].replace(FILLER_CHAR, "  ")

    average_buffer = ""
    average_buffer += "Moyenne : {}, médiane : {} (#{})\n".format(
      round(average, PRECISION), round(me, PRECISION),
      round(rme + 1, PRECISION))
    average_buffer += "Q1 : {} (#{}), Q3 : {} (#{})\n".format(
      round(q1, PRECISION), round(rq1 + 1, PRECISION),
      round(q3, PRECISION), round(rq3 + 1, PRECISION))
    average_buffer += "Étendue : {}, écart it-1/4 : {}\n".format(
      round(etendue, PRECISION), round(ec_itq, PRECISION))
    average_buffer += "Variance : {}, écart-type : {}\n".format(
      round(var, PRECISION), round(ecty, PRECISION))
    average_buffer += "Nombre d'entrées : {}, effectif total : {}".format(
      self.length, self.eff_total)
    # average_buffer = average_buffer.replace(".", ",")

    self.table_buffer_cache = table_buffer
    self.average_buffer_cache = average_buffer

  def ask_data(self):
    print("Entrez la valeur et l'effectif séparés par un '-'.")
    print("'enter' pour valider. 'x' pour annuler et quitter.")
    print("'-' pour resaisir.")

    count = self.length + 1
    additions = []
    deleted = []
    inp = ""
    abort = False

    while inp is not None:
      inp = input("Ajout #{} : ".format(count))

      if not inp:  # 'enter'
        print("Confirmer l'ajout des données saisies ? (0-/N) : ")
        conf = input()
        if conf not in ("O", "o", "-"):
          continue
        for add in additions:
          self.add(*add)
        break
      elif inp == "x":
        conf = input("Confirmer l'annulation de l'ajout ? (0-/N) : ")
        if conf not in ("O", "o", "-"):
          continue
        abort = True
        break
      elif inp == '-':
        if count <= 1:
          count = 1
          print("La première valeur est déjà atteinte.")
          continue
        count -= 1
        if additions:
          additions.pop()
        else:
          deleted.append(self.pop_back())
        continue

      splitted = inp.split('-')
      if len(splitted) != 2:
        print("Veuillez saisir deux valeurs séparés d'un '-'.")
        continue
      v = try_eval(splitted[0] if splitted[0] else 0)
      e = try_eval(splitted[1] if splitted[1] else 1)
      if v is None:
        print("La valeur '{}' est NaN. Resaisissez.".format(splitted[0]))
        continue
      elif e is None:
        print("L'effectif '{}' est NaN. Resaisissez.".format(splitted[1]))
        continue
      elif e == 0:
        print("L'effectif ne peut pas être nul. Resaisissez.")
        continue

      additions.append((v, e))
      count += 1

    if abort or (not additions and not deleted):
      for d in reversed(deleted):
        self.add(*d)
      self.refresh()
      return

    self.refresh()
    print("Succès de l'ajout !")

  def insert_data(self):
    print("Insersion de données non implémenté.")

  def delete_columns(self):
    print("Entrez les numéros des colonnes que vous")
    print("voulez supprimer, une par une, ou sous forme")
    print("d'intervalle 'x-y' avec x et y inclus.")
    print("'enter' pour valider. 'x' pour tout annuler")
    print("'a' pour tout supprimer. '-' pour resaisir")
    print("la précédente. '0' pour afficher la table.")

    count = 1
    deletions = []
    inp = ""
    abort = False

    while inp is not None:
      inp = input("#{} Supression : ".format(count))

      if not inp:  # 'enter'
        print("Confirmer la supression des données saisies ? (0-/N) : ")
        conf = input()
        if conf not in ("O", "o", "-"):
          continue
        deletions.sort(reverse=True)
        for d in deletions:
          del self.values[d]
          del self.effectifs[d]
        break

      elif inp == "x":
        print("Confirmer l'annulation de {} supression(s) ? (0-/N) : ".format(count - 1))
        conf = input()
        if conf not in ("O", "o", "-"):
          continue
        abort = True
        break

      elif inp == "a":
        print("Confirmer la supression de l'entièreté de la table ? (0-/N) : ")
        conf = input()
        if conf not in ("O", "o", "-"):
          continue
        self.values.clear()
        self.effectifs.clear()
        break

      elif inp == "-":
        if count <= 1:
          print("Aucune saisie à annuler.")
          continue
        s = deletions.pop()
        count -= 1
        print("Saisie '{}' annulée.".format(s + 1))
        continue

      elif inp == "0":
        print(self.table_buffer_cache)
        input("<'enter' pour continuer>")
        continue

      elif '-' in inp:
        splitted = inp.split('-')
        if len(splitted) != 2:
          print("L'intervalle a mal été saisie (plusieurs ':')")
          continue

        start = get_int(splitted[0])
        if start is None:
          print("La valeur '{}' est NaN. Resaisissez.".format(start))
          continue
        stop = get_int(splitted[1])
        if stop is None:
          print("La valeur '{}' est NaN. Resaisissez.".format(stop))
          continue

        print("Confirmer la supression de #{} à #{} ? (0-/N) : ".format(start, stop))
        conf = input()
        if conf not in ("O", "o", "-"):
          continue

        del self.values[start - 1:stop + 1 - 1]
        del self.effectifs[start - 1:stop + 1 - 1]
        break

      else:
        pos = get_int(inp)
        if pos is None:
          print("La valeur '{}' est NaN. Resaisissez.".format(pos))
          continue
        deletions.append(pos - 1)
        count += 1
        continue

    if abort:
      return

    self.refresh()
    print("Succès de la supression !")

  @staticmethod
  def print_about():
    print("_______________________________________")
    print(" ")
    print("Ce programme a été crée par Alexis Jomain en")
    print("2025 et concu pour la TI-nspire CX II-T CAS.")
    print("Il permet de modéliser une tableau de statis-")
    print("tiques, et d'en tirer plusieurs informations com-")
    print("me la moyenne, la médiane, etc. Il est contrôlé")
    print("par un system de 'prompt', en ligne de cmd.")
    input(" \n<'enter' pour continuer>")

  def control(self):
    self.refresh()

    WHOLE_PROMPT = (
      " \n"
      "    |   1 : aff. table, 2 : aff. stats, 3 : ajouter,\n"
      "    |   4 : insérer, 5 : supprimer, 6 : recalculer\n"
      "    |   7 : charger test, 8 quitter, 9 à propos"
    )
    SMALL_PROMPT = (
      " \n"
      "    |   Entrez '0' pour plus de commandes."
    )

    prompt = WHOLE_PROMPT

    inp = ""
    while inp is not None:
      print(prompt)
      inp = input("    >   Numéro de commande : ")
      print(" ")

      if inp == "0":
        prompt = WHOLE_PROMPT
        continue
      elif inp == "1":
        if not self.length:
          print("[Table vide ou non calculée]")
        else:
          print(self.table_buffer_cache)
          input("<'enter' pour continuer>")
      elif inp == "2":
        if not self.length:
          print("[Table vide ou non calculée]")
        else:
          print(self.average_buffer_cache)
          input(" \n<'enter' pour continuer>")
      elif inp == "3":
        self.ask_data()
      elif inp == "4":
        self.insert_data()
      elif inp == "5":
        if not self.length:
          print("[Table vide ou non calculée]")
        else:
          self.delete_columns()
      elif inp == "6":
        self.refresh()
        print("Table recalculée !")
      elif inp == "7":
        conf = input("Confirmer l'écrasement des données ? (0-/N) : ")
        if conf not in ("O", "o", "-"):
          continue
        load_test(self)
      elif inp == "8":
        conf = input("Confirmer l'arrêt du programme ? (0-/N) : ")
        if conf in ("O", "o", "-"):
          print("Fin du programme\n ")
          break
      elif inp == "9":
        self.print_about()
      else :
        print("Commande non comprise. Veuillez resaisir.")

      prompt = SMALL_PROMPT


def test():
  tbl = TableManager()
  load_test(tbl)
  tbl.control()


def main():
  tbl = TableManager()
  tbl.control()


main()
