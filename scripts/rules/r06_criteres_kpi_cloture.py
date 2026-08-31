"""R6 — Chaque critere de succes de la charte est couvert par un KPI et figure en
checklist de cloture."""
from pmlib import Ecart, liste

ID = "R6"
LIBELLE = "Chaque critère de succès couvert par un KPI et présent en checklist de clôture"
REQUIERT = ["charte", "qualite", "cloture"]
DEROGATION_ADMISE = False


def verifier(pf):
    ecarts = []
    livrables = liste(pf.get("charte").get("livrables"))
    kpi_cibles = set()
    for k in liste(pf.get("qualite").get("kpi")):
        kpi_cibles |= set(liste(k.get("couvre")))
        if not k.get("source_donnee"):
            ecarts.append(Ecart(ID, "bloquant", "pm-qualite-suivi",
                                f"KPI {k.get('id')} sans source de donnée identifiée"))
    checklist = set()
    for c in liste(pf.get("cloture").get("checklist")):
        checklist |= set(liste(c.get("couvre")))

    for d in livrables:
        if d["id"] not in kpi_cibles:
            ecarts.append(Ecart(ID, "bloquant", "pm-qualite-suivi",
                                f"Critère de succès du livrable {d['id']} couvert par aucun KPI"))
        if d["id"] not in checklist:
            ecarts.append(Ecart(ID, "bloquant", "pm-equipe-cloture",
                                f"Livrable {d['id']} absent de la checklist de clôture"))
    return ecarts
