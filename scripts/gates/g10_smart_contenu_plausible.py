"""G10 - L'enonce de chaque objectif SMART de la charte contient un signal lexical de
mesure chiffree ET une echeance detectable — pas seulement les 5 champs smart renseignes.

Origine : analyse du 02/09/2026 de ConversationProjectInitiator (useffj) — ce depot
applique une heuristique lexicale equivalente (utils/validators.py::check_smart), en
COMPLEMENT, jamais en remplacement, de la validation qualitative par LLM. G2 verifie que
les 5 champs SMART (s/m/a/r/t) sont renseignes (non vides) ; G10 verifie que la phrase
`enonce` — le seul champ que lira un humain sans decortiquer le sous-objet `smart` — se lit
elle-meme comme un objectif mesurable et date.

Cible volontairement `enonce`, pas `smart.m`/`smart.t` : dans ce schema, `smart.m` documente
la SOURCE/methode de mesure (ex: "source : outil de telephonie"), pas la grandeur cible
elle-meme — celle-ci vit dans `enonce` et dans `cible.valeur` (deja gouverne par R9). Cibler
`smart.m` aurait produit un faux positif systematique sur l'exemple de reference
(portail-b2b) : verifie en le testant contre cet exemple avant integration.

Portee volontairement limitee, meme principe que ConversationProjectInitiator : les
criteres Specifique/Atteignable/Pertinent ne sont pas fiablement verifiables par regex sur
un texte libre et sont donc hors perimetre de cette porte. Un objectif-jalon binaire
(mise en service a une date, sans grandeur chiffree) est un cas legitime prevu par la
derogation, pas une exception a coder.
"""
import re

from pmlib import ARTEFACTS, Ecart, liste

ID = "G10"
LIBELLE = "L'énoncé de chaque objectif SMART contient une grandeur chiffrée et une échéance détectables"
REQUIERT = ["charte"]
DEROGATION_ADMISE = True
ORIGINE = {"type": "choix_architecture", "reference":
    "Heuristique équivalente à ConversationProjectInitiator (useffj), analysé le "
    "02/09/2026 : un pré-filtre lexical sans appel LLM, en complément de G2 qui ne "
    "vérifie que la présence des champs smart, pas la plausibilité de l'énoncé."}

RE_MESURABLE = re.compile(
    r"\d+\s*%|\d+\s*(jours?|semaines?|mois|heures?|utilisateurs?|clients?|appels?|"
    r"tickets?|articles?|€|eur\b|\$|k\b|million|points?|unit[ée]s?)",
    re.IGNORECASE,
)

RE_TEMPOREL = re.compile(
    r"\bT[1-4]\s*20\d{2}\b|\b\d{1,2}/\d{1,2}/20\d{2}\b|\b20\d{2}\b|"
    r"\b(janvier|f[ée]vrier|mars|avril|mai|juin|juillet|ao[uû]t|septembre|octobre|"
    r"novembre|d[ée]cembre)\b|\b(fin|d'ici|au plus tard|avant le|échéance)\b",
    re.IGNORECASE,
)


def verifier(pf):
    ecarts = []
    for obj in liste(pf.get("charte").get("objectifs_smart")):
        enonce = str(obj.get("enonce") or "").strip()
        if not enonce:
            continue   # champ absent : hors périmètre de cette porte, pas de double emploi
        oid = obj.get("id", "?")
        if not RE_MESURABLE.search(enonce):
            ecarts.append(Ecart(ID, "mineur", ARTEFACTS["charte"],
                                f"Objectif {oid} : énoncé sans grandeur chiffrée détectable",
                                "Dérogation possible si l'objectif est légitimement un jalon "
                                "binaire (ex : mise en service atteinte/non atteinte à une date)"))
        if not RE_TEMPOREL.search(enonce):
            ecarts.append(Ecart(ID, "mineur", ARTEFACTS["charte"],
                                f"Objectif {oid} : énoncé sans échéance détectable",
                                "Dérogation possible si l'échéance est portée uniquement par "
                                "un jalon nommé du plan, pas par une date dans l'énoncé"))
    return ecarts
