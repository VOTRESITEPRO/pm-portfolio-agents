"""G8 - Les champs utiles projet.commanditaire et projet.secteur sont renseignes, ou leur
absence est tracee par une derogation.

Origine : seules les 4 lacunes classees "bloquantes" par pm-contexte-projet (echeance,
budget, perimetre, critere de succes) declenchaient une question a l'humain. Un champ
utile mais non bloquant comme le commanditaire pouvait rester silencieusement vide, sans
que rien ne distingue « jamais demande » de « demande et decline ». Cette porte rend
visible ce qui etait invisible, sans le rendre bloquant : severite mineure, avec
derogation admise si l'information a ete explicitement declinee ou n'est pas pertinente.
"""
from pmlib import ARTEFACTS, Ecart

ID = "G8"
LIBELLE = "projet.commanditaire et projet.secteur sont renseignés, ou leur absence est tracée"
REQUIERT = ["contexte"]
DEROGATION_ADMISE = True
ORIGINE = {"type": "choix_architecture", "reference":
    "Complète la qualification des lacunes de pm-contexte-projet (docs/document-raisonnement.md, "
    "D14) : un champ utile laissé vide sans être demandé n'était distingué en rien d'un "
    "champ explicitement décliné."}


def verifier(pf):
    ecarts = []
    projet = pf.get("contexte").get("projet") or {}
    for champ in ("commanditaire", "secteur"):
        v = projet.get(champ)
        if not v or not str(v).strip():
            ecarts.append(Ecart(ID, "mineur", ARTEFACTS["contexte"],
                                f"contexte.yaml : projet.{champ} est vide",
                                "Dérogation possible si l'information a été explicitement "
                                "déclinée par l'utilisateur ou n'est pas pertinente pour ce projet"))
    return ecarts
