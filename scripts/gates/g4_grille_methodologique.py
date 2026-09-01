"""G4 - Au moins 5 criteres de choix motives et au moins 1 alternative
ecartee motivee, dans la methodologie. Porte declaree par pm-methodologue,
jamais verifiee par code."""
from pmlib import Ecart, liste

ID = "G4"
LIBELLE = "Au moins 5 critères motivés et 1 alternative écartée motivée"
REQUIERT = ["methodologie"]
DEROGATION_ADMISE = False
ORIGINE = {"type": "choix_architecture", "reference":
    "Les seuils '5 critères' et '1 alternative motivée' sont fixés par le concepteur du système ; le Google PM Cert Cours 1 recommande de comparer les méthodologies sans fixer de nombre."}


def verifier(pf):
    ecarts = []
    meth = pf.get("methodologie")

    criteres = liste(meth.get("criteres"))
    motives = [c for c in criteres if str(c.get("constat") or "").strip() and c.get("pousse_vers")]
    if len(motives) < 5:
        ecarts.append(Ecart(ID, "bloquant", "pm-methodologue",
                            f"{len(motives)} critère(s) motivé(s) (constat + pousse_vers) sur "
                            f"{len(criteres)} déclaré(s) — 5 attendus"))

    alternatives = liste(meth.get("alternatives_ecartees"))
    motivees = [a for a in alternatives if str(a.get("motif") or "").strip()]
    if not motivees:
        ecarts.append(Ecart(ID, "bloquant", "pm-methodologue",
                            "Aucune alternative écartée motivée"))
    return ecarts
