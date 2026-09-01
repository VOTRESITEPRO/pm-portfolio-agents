"""R10 — Tout role proprietaire / approbateur est POURVU au registre des parties
prenantes (correction C5).

Origine : une porte avait valide "proprietaire nomme : 14/14" alors que quatre
proprietaires etaient "le chef de projet", role que la charte declarait a nommer.
La porte verifiait une chaine de caracteres, pas l'existence d'une personne.
"""
from pmlib import Ecart, STATUTS_NON_POURVU, liste

ID = "R10"
LIBELLE = "Tout rôle propriétaire ou approbateur est pourvu au registre des parties prenantes"
REQUIERT = ["parties-prenantes"]
DEROGATION_ADMISE = True
ORIGINE = {"type": "choix_architecture", "reference":
    "Corrige un défaut trouvé au test (correction C5 / risque S-08) : un rôle nommé doit être une personne réellement pourvue, pas un libellé."}


def _index(pf):
    idx = {}
    for pp in liste(pf.get("parties-prenantes").get("registre")):
        idx[pp.get("id")] = pp
    return idx


def verifier(pf):
    ecarts = []
    idx = _index(pf)

    def controler(ref, origine, role_libelle):
        if ref is None:
            ecarts.append(Ecart(ID, "bloquant", "pm-risques",
                                f"{origine} : aucun {role_libelle} désigné"))
            return
        pp = idx.get(ref)
        if pp is None:
            ecarts.append(Ecart(ID, "bloquant", "pm-risques",
                                f"{origine} : {role_libelle} '{ref}' absent du registre des parties prenantes",
                                "Le propriétaire doit être une référence PPx, pas un libellé libre"))
        elif pp.get("statut") in STATUTS_NON_POURVU:
            ecarts.append(Ecart(ID, "bloquant", "pm-parties-prenantes",
                                f"{origine} : {role_libelle} {ref} ({pp.get('nom')}) a le statut "
                                f"'{pp.get('statut')}' — rôle non pourvu",
                                "Dérogation possible si le pourvoi est tracé comme tâche du plan ou comme risque"))

    if "risques" in pf:
        for r in liste(pf.get("risques").get("registre")):
            controler(r.get("proprietaire"), f"Risque {r.get('id')}", "propriétaire")

    if "parties-prenantes" in pf:
        for ligne in liste(pf.get("parties-prenantes").get("raci")):
            for a in liste(ligne.get("a")):
                pp = idx.get(a)
                if pp and pp.get("statut") in STATUTS_NON_POURVU:
                    ecarts.append(Ecart(ID, "bloquant", "pm-parties-prenantes",
                                        f"RACI livrable {ligne.get('livrable')} : Accountable {a} "
                                        f"({pp.get('nom')}) non pourvu ('{pp.get('statut')}')"))
    return ecarts
