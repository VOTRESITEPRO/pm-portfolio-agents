"""R12 - Toute lacune du contexte au statut convertie_en_risque existe dans
le registre des risques sous l'identifiant annonce (champ converti_en).
Croise contexte et risques : une conversion peut etre annoncee sans etre
faite (voir docs/ecarts-spec-implementation.md)."""
from pmlib import Ecart, liste

ID = "R12"
LIBELLE = "Lacune convertie_en_risque tracée dans le registre des risques"
REQUIERT = ["contexte", "risques"]
DEROGATION_ADMISE = True
ORIGINE = {"type": "choix_architecture", "reference":
    "Mécanique interne de traçabilité du registre des lacunes (décision D3), propre à ce système."}


def verifier(pf):
    ecarts = []
    ids_risques = {r.get("id") for r in liste(pf.get("risques").get("registre"))}
    for lac in liste(pf.get("contexte").get("lacunes")):
        if lac.get("statut") != "convertie_en_risque":
            continue
        cible = lac.get("converti_en")
        if not cible:
            ecarts.append(Ecart(ID, "bloquant", "pm-risques",
                                f"Lacune {lac.get('id', '?')} : statut convertie_en_risque "
                                "sans identifiant converti_en"))
        elif cible not in ids_risques:
            ecarts.append(Ecart(ID, "bloquant", "pm-risques",
                                f"Lacune {lac.get('id', '?')} : conversion annoncée vers "
                                f"{cible}, absent du registre des risques"))
    return ecarts
