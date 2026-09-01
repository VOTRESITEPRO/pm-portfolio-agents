"""G5 - Aucune lacune bloquante du contexte au statut ouverte. Porte
declaree par pm-contexte-projet ; doit refuser un contexte.yaml incomplet
independamment du mode d'execution de l'agent (pas seulement de sa
discipline a s'arreter)."""
from pmlib import Ecart, liste

ID = "G5"
LIBELLE = "Aucune lacune bloquante au statut ouverte"
REQUIERT = ["contexte"]
DEROGATION_ADMISE = False


def verifier(pf):
    ecarts = []
    for lac in liste(pf.get("contexte").get("lacunes")):
        if lac.get("gravite") == "bloquante" and lac.get("statut") == "ouverte":
            ecarts.append(Ecart(ID, "bloquant", "pm-contexte-projet",
                                f"Lacune {lac.get('id', '?')} bloquante et encore ouverte : "
                                f"{lac.get('libelle', '')}"))
    return ecarts
