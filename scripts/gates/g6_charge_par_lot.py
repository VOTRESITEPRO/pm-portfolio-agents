"""G6 - Chaque lot portant une duree porte aussi une charge (personne-
semaines). Sans elle, R15 (charge cumulee vs capacite de l'equipe interne)
ne peut rien confronter et le passe en silence -- exactement le defaut que
les gates G1-G5 corrigent deja pour d'autres agents : une porte declaree
(voir agents-src/pm-planificateur-wbs.md, section "Porte de sortie") mais
non verifiee par code."""
from pmlib import Ecart, liste

ID = "G6"
LIBELLE = "Chaque lot portant une durée porte aussi une charge"
REQUIERT = ["plan"]
DEROGATION_ADMISE = True


def verifier(pf):
    ecarts = []
    for lot in liste(pf.get("plan").get("lots")):
        if lot.get("duree") and not lot.get("charge"):
            ecarts.append(Ecart(ID, "bloquant", "pm-planificateur-wbs",
                                f"Lot {lot.get('id', '?')} : durée déclarée sans charge",
                                "sans charge, R15 ne peut pas confronter la charge cumulée à la "
                                "capacité de l'équipe interne"))
    return ecarts
