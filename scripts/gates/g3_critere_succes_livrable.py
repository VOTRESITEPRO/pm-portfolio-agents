"""G3 - Chaque livrable de la charte porte un critere de succes non vide.
Porte declaree par pm-charte-objectifs, jamais verifiee par code."""
from pmlib import Ecart, liste

ID = "G3"
LIBELLE = "Chaque livrable porte un critère de succès non vide"
REQUIERT = ["charte"]
DEROGATION_ADMISE = False
ORIGINE = {"type": "standard", "reference":
    "Un livrable sans critère de succès n'est pas un livrable géré — gestion de la qualité (Google PM Cert Cours 2/5)."}


def verifier(pf):
    ecarts = []
    for d in liste(pf.get("charte").get("livrables")):
        if not str(d.get("critere_succes") or "").strip():
            ecarts.append(Ecart(ID, "bloquant", "pm-charte-objectifs",
                                f"Livrable {d.get('id', '?')} : aucun critère de succès"))
    return ecarts
