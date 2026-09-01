"""R13 - Toute hypothese de la charte portant un risque_associe est couverte
par le registre des risques. Croise charte et risques : une hypothese peut
citer un risque qui n'existe pas (voir docs/ecarts-spec-implementation.md)."""
from pmlib import Ecart, liste

ID = "R13"
LIBELLE = "Hypothèse de la charte couverte par le registre des risques"
REQUIERT = ["charte", "risques"]
DEROGATION_ADMISE = True


def verifier(pf):
    ecarts = []
    ids_risques = {r.get("id") for r in liste(pf.get("risques").get("registre"))}
    for hyp in liste(pf.get("charte").get("hypotheses")):
        cible = hyp.get("risque_associe")
        if cible and cible not in ids_risques:
            ecarts.append(Ecart(ID, "bloquant", "pm-risques",
                                f"Hypothèse {hyp.get('id', '?')} : risque associé {cible} "
                                "absent du registre des risques"))
    return ecarts
