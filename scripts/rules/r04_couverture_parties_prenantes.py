"""R4 — Toute partie prenante du registre apparait dans le RACI et le plan de
communication, ou fait l'objet d'une derogation motivee."""
from pmlib import Ecart, liste

ID = "R4"
LIBELLE = "Toute partie prenante presente dans le RACI et le plan de communication"
REQUIERT = ["parties-prenantes", "communications"]
DEROGATION_ADMISE = True


def verifier(pf):
    ecarts = []
    pps = {pp.get("id"): pp for pp in liste(pf.get("parties-prenantes").get("registre"))}

    dans_raci = set()
    for ligne in liste(pf.get("parties-prenantes").get("raci")):
        for cle in ("a", "r", "c", "i"):
            dans_raci |= set(liste(ligne.get(cle)))

    dans_com = set()
    for ligne in liste(pf.get("communications").get("plan")):
        dans_com |= set(liste(ligne.get("destinataires")))

    for pid, pp in pps.items():
        if pid not in dans_raci:
            ecarts.append(Ecart(ID, "mineur", "pm-parties-prenantes",
                                f"{pid} ({pp.get('nom')}) absent du RACI",
                                "Derogation possible si non responsable d'un livrable, avec rattachement explicite"))
        if pid not in dans_com:
            ecarts.append(Ecart(ID, "mineur", "pm-communications",
                                f"{pid} ({pp.get('nom')}) absent du plan de communication"))
    return ecarts
