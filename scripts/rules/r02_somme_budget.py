"""R2 — Le budget total annonce == somme des postes, recalculee."""
from pmlib import Ecart, liste, valeur_de

ID = "R2"
LIBELLE = "Somme des postes budgétaires == budget total annoncé"
REQUIERT = ["budget"]
DEROGATION_ADMISE = False


def verifier(pf):
    ecarts = []
    budget = pf.get("budget")
    postes = liste(budget.get("postes"))
    total = sum(float(valeur_de(p.get("montant")) or 0) for p in postes)
    annonce = valeur_de((budget.get("total") or {}))
    if annonce is not None and abs(float(annonce) - total) > 0.01:
        ecarts.append(Ecart(ID, "bloquant", "pm-budget-achats",
                            f"Budget total : {annonce} annoncé, {total:g} recalculé",
                            f"écart de {total - float(annonce):+g}"))
    # Chaque poste trace vers un lot de la WBS
    if "plan" in pf:
        lots = {str(l.get("id")) for l in liste(pf.get("plan").get("lots"))}
        for p in postes:
            lot = str(p.get("lot")) if p.get("lot") is not None else None
            if lot not in lots:
                ecarts.append(Ecart(ID, "bloquant", "pm-budget-achats",
                                    f"Poste '{p.get('libelle')}' rattaché au lot {lot}, absent de la WBS"))
    return ecarts
