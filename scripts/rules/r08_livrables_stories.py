"""R8 — Si la branche agile est active, chaque livrable de la charte est couvert par
au moins une story.

Point de conception : si drapeau_agile == false, la regle est non_applicable par
CONDITION. Si drapeau_agile == true et que le backlog manque, c'est un ECART — pas
une non-applicabilite. C'est la distinction que la correction C2 a introduite.
"""
from pmlib import Ecart, liste

ID = "R8"
LIBELLE = "Chaque livrable de la charte couvert par au moins une story"
REQUIERT = ["charte", "backlog"]
DEROGATION_ADMISE = False
CONDITION_SUPPLEMENTAIRE = ("methodologie", "drapeau_agile", True)
ORIGINE = {"type": "choix_architecture", "reference":
    "Pont entre le vocabulaire waterfall (charte/livrables) et agile (stories) : propre à ce système à double registre, pas une règle du Scrum Guide."}


def verifier(pf):
    ecarts = []
    couverts = set()
    for s in liste(pf.get("backlog").get("stories")):
        couverts |= set(liste(s.get("couvre")))
    for d in liste(pf.get("charte").get("livrables")):
        if d["id"] not in couverts:
            ecarts.append(Ecart(ID, "bloquant", "pm-backlog-stories",
                                f"Livrable {d['id']} couvert par aucune story"))
    return ecarts
