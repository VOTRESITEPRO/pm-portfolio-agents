"""G7 - La prose d'un artefact francophone contient des caracteres accentues.

Origine : au run palier 4 (01/09/2026), pm-contexte-projet et pm-charte-objectifs ont
produit une prose entierement sans accents ("Perimetre", "depassable", "concernes")
tandis que pm-planificateur-wbs et pm-risques ecrivaient un francais correct sur le meme
run. Aucune regle ni porte ne le detectait — defaut de forme pur, jamais verifie
mecaniquement jusqu'ici. Meme principe que les autres portes (D6, document-raisonnement.md) :
un signal de forme se verifie par du code, pas par la seule discipline d'un prompt.

Heuristique volontairement grossiere : sur un volume de prose suffisant (>= 150 lettres
cumulees sur l'artefact), un texte francais authentique contient necessairement quelques
caracteres accentues. Zero accent sur ce volume est un signal fort, pas une preuve
absolue — d'ou une derogation admise (ex : artefact au vocabulaire technique anglophone).
"""
import re

from pmlib import ARTEFACTS, Ecart, parcourir_chaines

ID = "G7"
LIBELLE = "La prose d'un artefact contient des caractères accentués (pas de prose 100 % ASCII)"
REQUIERT = []          # s'applique à tous les artefacts présents
DEROGATION_ADMISE = True
ORIGINE = {"type": "choix_architecture", "reference":
    "Défaut trouvé au run palier 4 (01/09/2026) : deux agents sur six ont produit une "
    "prose sans accent sur le même run, sans qu'aucune règle ne le détecte."}

SEUIL_LETTRES = 150
ACCENTS = "éèêëàâäîïôöùûüçÉÈÊËÀÂÄÎÏÔÖÙÛÜÇ"
RE_LETTRE = re.compile(r"[A-Za-zÀ-ÿ]")
RE_ACCENT = re.compile(f"[{ACCENTS}]")


def verifier(pf):
    ecarts = []
    for nom, contenu in pf.data.items():
        texte = " ".join(v for _, v in parcourir_chaines(contenu))
        nb_lettres = len(RE_LETTRE.findall(texte))
        if nb_lettres < SEUIL_LETTRES:
            continue  # volume insuffisant pour que l'absence d'accent soit un signal fiable
        nb_accents = len(RE_ACCENT.findall(texte))
        if nb_accents == 0:
            ecarts.append(Ecart(ID, "mineur", ARTEFACTS.get(nom, f"agent producteur de {nom}"),
                                f"{nom}.yaml : {nb_lettres} lettres de prose, aucun caractère "
                                f"accentué — probable perte d'accents à la génération",
                                "Dérogation possible si le vocabulaire de l'artefact est "
                                "légitimement non accentué (ex : contenu technique anglophone)"))
    return ecarts
