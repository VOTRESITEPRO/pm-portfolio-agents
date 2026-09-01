"""G2 - Les cinq criteres SMART (s, m, a, r, t) sont renseignes pour chaque
objectif de la charte. Porte declaree par pm-charte-objectifs, jamais
verifiee par code."""
from pmlib import Ecart, liste

ID = "G2"
LIBELLE = "Les 5 critères SMART sont renseignés pour chaque objectif"
REQUIERT = ["charte"]
DEROGATION_ADMISE = False

CRITERES = ("s", "m", "a", "r", "t")


def verifier(pf):
    ecarts = []
    for obj in liste(pf.get("charte").get("objectifs_smart")):
        smart = obj.get("smart") or {}
        manquants = [c.upper() for c in CRITERES if not str(smart.get(c) or "").strip()]
        if manquants:
            ecarts.append(Ecart(ID, "bloquant", "pm-charte-objectifs",
                                f"Objectif {obj.get('id', '?')} : critère(s) SMART manquant(s) : "
                                f"{', '.join(manquants)}"))
    return ecarts
