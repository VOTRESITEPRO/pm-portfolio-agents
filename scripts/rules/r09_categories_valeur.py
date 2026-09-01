"""R9 — Toute valeur chiffree porte un statut reconnu (correction C4).

Trois categories : source (autorisee), seuil_propose (autorisee si marquee),
a_sourcer (autorisee). Une valeur sans statut est une donnee factuelle generee.
"""
from pmlib import Ecart, STATUTS_VALEUR, parcourir_valeurs

ID = "R9"
LIBELLE = "Toute valeur chiffrée appartient à une catégorie de valeur déclarée"
REQUIERT = []          # s'applique a tous les artefacts presents
DEROGATION_ADMISE = False
ORIGINE = {"type": "choix_architecture", "reference":
    "Mitigation de l'hallucination LLM — décision D9 de document-raisonnement.md, propre à ce système."}


def verifier(pf):
    ecarts = []
    for nom, contenu in pf.data.items():
        for chemin, champ in parcourir_valeurs(contenu):
            statut = champ.get("statut")
            if statut is None:
                ecarts.append(Ecart(ID, "bloquant", f"agent producteur de {nom}",
                                    f"{nom}.yaml : valeur sans statut en {chemin}",
                                    "Donnée factuelle générée — marquer source / seuil_propose / a_sourcer"))
            elif statut not in STATUTS_VALEUR:
                ecarts.append(Ecart(ID, "bloquant", f"agent producteur de {nom}",
                                    f"{nom}.yaml : statut inconnu '{statut}' en {chemin}",
                                    f"attendus : {sorted(STATUTS_VALEUR)}"))
            elif statut == "a_sourcer" and champ.get("valeur") is not None:
                ecarts.append(Ecart(ID, "bloquant", f"agent producteur de {nom}",
                                    f"{nom}.yaml : statut a_sourcer mais une valeur est renseignée en {chemin}",
                                    "Une donnée à sourcer ne porte pas de valeur produite par le modèle"))
    return ecarts
