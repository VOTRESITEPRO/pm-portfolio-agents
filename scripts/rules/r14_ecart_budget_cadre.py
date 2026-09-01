"""R14 - Generalisation du patron R11 au budget : le budget total recalcule
depuis les postes (aval) est confronte au budget cadre du contexte (amont),
fixe independamment du budget lui-meme.

Specifie dans docs/cartographie-agents-pm.yaml (budget-achats.porte_qualite.
coherence_arithmetique : "ecart au budget cadre == budget total - budget
cadre, recalcule") mais jamais code : R2 recalcule le total, jamais
confronte au plafond amont.
"""
from pmlib import Ecart, liste, valeur_de

ID = "R14"
LIBELLE = "Budget total recalculé confronté au budget cadre du contexte"
REQUIERT = ["budget", "contexte"]
DEROGATION_ADMISE = False


def verifier(pf):
    ecarts = []
    postes = liste(pf.get("budget").get("postes"))
    total = sum(float(valeur_de(p.get("montant")) or 0) for p in postes)

    plafond = valeur_de((pf.get("contexte").get("contraintes") or {}).get("budget_plafond"))
    if plafond is None:
        return ecarts  # pas de budget cadre declare en amont : rien a confronter

    ecart = total - float(plafond)
    if ecart > 0.01:
        ecarts.append(Ecart(ID, "bloquant", "pm-budget-achats",
                            f"Budget recalculé ({total:g}) dépasse le budget cadre du contexte "
                            f"({float(plafond):g})",
                            f"dépassement de {ecart:+g}"))
    return ecarts
