"""R15 - Generalisation du patron R11 aux ressources : la charge cumulee
(personne-semaines, hypothese haute) recalculee depuis les lots (aval) est
confrontee a la capacite de l'equipe interne (amont) = etp_interne x duree
de la fenetre calendaire.

N'etait specifie nulle part dans docs/cartographie-agents-pm.yaml v1.1 (a la
difference du budget) : le champ 'charge' par lot est une extension du
schema de plan.yaml decidee et ajoutee dans cette session, distincte de
'duree' (calendaire, parallelisable) qui ne dit rien de la saturation de
l'equipe.
"""
from datetime import date

from pmlib import Ecart, liste, somme_bornes, valeur_de

ID = "R15"
LIBELLE = "Charge cumulée confrontée à la capacité de l'équipe interne"
REQUIERT = ["plan", "contexte"]
DEROGATION_ADMISE = False


def verifier(pf):
    ecarts = []
    porteurs = [lot for lot in liste(pf.get("plan").get("lots")) if lot.get("charge")]
    if not porteurs:
        return ecarts  # aucun lot ne declare de charge : rien a confronter

    _, charge_max = somme_bornes(porteurs, cle="charge")

    contraintes = pf.get("contexte").get("contraintes") or {}
    etp = valeur_de(contraintes.get("etp_interne"))
    fenetre = pf.get("contexte").get("fenetre") or {}
    debut, fin = fenetre.get("debut"), fenetre.get("fin")
    if etp is None or not debut or not fin:
        return ecarts  # capacite amont non renseignee : rien a confronter

    debut = debut if isinstance(debut, date) else date.fromisoformat(str(debut))
    fin = fin if isinstance(fin, date) else date.fromisoformat(str(fin))
    semaines = (fin - debut).days / 7
    capacite = float(etp) * semaines
    marge = capacite - charge_max

    if marge < 0:
        ecarts.append(Ecart(ID, "bloquant", "pm-planificateur-wbs",
                            f"Charge en hypothèse haute ({charge_max:g} personne-semaines) dépasse la "
                            f"capacité de l'équipe interne ({capacite:.1f} = {etp:g} ETP × {semaines:.1f} "
                            "semaines)",
                            f"marge de {marge:+.1f} personne-semaine(s) — renfort ou réduction de périmètre "
                            "nécessaire"))
    return ecarts
