"""R7 — Chaque lot du chemin critique est couvert par au moins un risque analyse."""
from pmlib import Ecart, liste

ID = "R7"
LIBELLE = "Chaque tâche du chemin critique couverte par un risque analysé"
REQUIERT = ["plan", "risques"]
DEROGATION_ADMISE = False


def verifier(pf):
    ecarts = []
    critique = liste(pf.get("plan").get("chemin_critique"))
    couverts = set()
    for r in liste(pf.get("risques").get("registre")):
        couverts |= {str(x) for x in liste(r.get("lots_couverts"))}

    for lot in critique:
        if str(lot) not in couverts:
            ecarts.append(Ecart(ID, "bloquant", "pm-risques",
                                f"Lot {lot} du chemin critique couvert par aucun risque"))
    return ecarts
