"""R5 — Un seul Accountable par livrable, au moins un Responsible."""
from pmlib import Ecart, liste

ID = "R5"
LIBELLE = "Un seul Accountable par livrable dans le RACI"
REQUIERT = ["parties-prenantes"]
DEROGATION_ADMISE = False


def verifier(pf):
    ecarts = []
    for ligne in liste(pf.get("parties-prenantes").get("raci")):
        liv = ligne.get("livrable", "?")
        a = liste(ligne.get("a"))
        r = liste(ligne.get("r"))
        if len(a) != 1:
            ecarts.append(Ecart(ID, "bloquant", "pm-parties-prenantes",
                                f"Livrable {liv} : {len(a)} Accountable (exactement 1 attendu)",
                                f"trouves : {a or 'aucun'}"))
        if not r:
            ecarts.append(Ecart(ID, "bloquant", "pm-parties-prenantes",
                                f"Livrable {liv} : aucun Responsible"))
    return ecarts
