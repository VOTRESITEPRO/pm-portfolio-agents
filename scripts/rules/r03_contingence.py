"""R3 — La reserve de contingence est justifiee par des risques cotes, pas par un
pourcentage arbitraire."""
from pmlib import Ecart, liste, valeur_de

ID = "R3"
LIBELLE = "Réserve de contingence justifiée par des risques cotés"
REQUIERT = ["budget", "risques"]
DEROGATION_ADMISE = False


def verifier(pf):
    ecarts = []
    conting = pf.get("budget").get("contingence") or {}
    risques_ids = {r.get("id") for r in liste(pf.get("risques").get("registre"))}
    justif = liste(conting.get("risques_couverts"))

    if not justif:
        ecarts.append(Ecart(ID, "bloquant", "pm-budget-achats",
                            "Réserve de contingence sans risque justificatif",
                            "Un pourcentage forfaitaire n'est pas une justification"))
    for rid in justif:
        if rid not in risques_ids:
            ecarts.append(Ecart(ID, "bloquant", "pm-budget-achats",
                                f"Contingence justifiée par le risque {rid}, absent du registre"))

    montant = valeur_de(conting.get("montant"))
    expo = sum(float(valeur_de(x.get("exposition")) or 0)
               for x in liste(pf.get("risques").get("registre"))
               if x.get("id") in set(justif))
    if montant is not None and expo and abs(float(montant) - expo) > 0.01:
        ecarts.append(Ecart(ID, "bloquant", "pm-budget-achats",
                            f"Contingence : {montant} annoncé, {expo:g} recalculé depuis les expositions"))
    return ecarts
