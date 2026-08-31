"""R1 — Chaque livrable de la charte est couvert par au moins un lot de la WBS,
et tout lot ne tracant vers aucun livrable est declare comme lot de conduite."""
from pmlib import Ecart, liste

ID = "R1"
LIBELLE = "Perimetre de la charte == somme des lots de la WBS"
REQUIERT = ["charte", "plan"]
DEROGATION_ADMISE = True


def verifier(pf):
    ecarts = []
    livrables = {d["id"] for d in liste(pf.get("charte").get("livrables"))}
    lots = liste(pf.get("plan").get("lots"))

    couverts = set()
    for lot in lots:
        couverts |= set(liste(lot.get("livrables")))

    for d in sorted(livrables - couverts):
        ecarts.append(Ecart(ID, "bloquant", "pm-planificateur-wbs",
                            f"Livrable {d} de la charte couvert par aucun lot de la WBS"))

    for d in sorted(couverts - livrables):
        ecarts.append(Ecart(ID, "bloquant", "pm-planificateur-wbs",
                            f"Lot rattache au livrable {d}, absent de la charte"))

    # Lot sans livrable : acceptable s'il est declare de conduite (derogation structurelle)
    for lot in lots:
        if not liste(lot.get("livrables")) and lot.get("type") != "conduite":
            ecarts.append(Ecart(ID, "mineur", "pm-planificateur-wbs",
                                f"Lot {lot.get('id')} ne trace vers aucun livrable",
                                "Le declarer type: conduite s'il s'agit d'un lot de conduite de projet"))
    return ecarts
