"""G1 - Plan d'attenuation et plan de secours pour tout risque de criticite
(p x i) >= 15. Porte declaree par pm-risques, jamais verifiee par code : un
registre passait avec des plans vides."""
from pmlib import Ecart, liste

ID = "G1"
LIBELLE = "Plans d'atténuation et de secours pour toute criticité (p × i) ≥ 15"
REQUIERT = ["risques"]
DEROGATION_ADMISE = True
ORIGINE = {"type": "choix_architecture", "reference":
    "La grille probabilité x impact est un standard de gestion des risques (Google PM Cert Cours 3) ; le seuil précis '15' est un seuil de gestion arbitraire propre à ce système (cf. décision D9 — seuil de gestion proposé, pas une donnée factuelle)."}


def verifier(pf):
    ecarts = []
    for r in liste(pf.get("risques").get("registre")):
        try:
            criticite = float(r.get("p")) * float(r.get("i"))
        except (TypeError, ValueError):
            continue  # p/i absents ou non numeriques : hors perimetre de cette porte
        if criticite < 15:
            continue
        manquants = [champ for champ in ("attenuation", "plan_de_secours")
                    if not str(r.get(champ) or "").strip()]
        if manquants:
            ecarts.append(Ecart(ID, "bloquant", "pm-risques",
                                f"Risque {r.get('id', '?')} (criticité {criticite:g}) : "
                                f"{', '.join(manquants)} manquant(s)",
                                f"p={r.get('p')}, i={r.get('i')}"))
    return ecarts
