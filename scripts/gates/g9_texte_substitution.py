"""G9 - Aucun texte de substitution (placeholder) residuel dans la prose d'un artefact.

Origine : analyse du 02/09/2026 de docforge-ai (Venkatesh188) — ce depot fait systeme-
atiquement passer chaque document genere par un filtre deterministe post-generation
(document_agents.py::_clean_output) qui detecte et retire les residus de generation
(TODO, TBD, [INSERT]...) avant toute verification de fond. Meme famille que G7/G8 :
un signal de forme se verifie par du code, jamais par la seule discipline d'un prompt.
Aucune porte de ce portfolio ne verifiait ce defaut jusqu'ici.
"""
import re

from pmlib import ARTEFACTS, Ecart, parcourir_chaines

ID = "G9"
LIBELLE = "Aucun texte de substitution (placeholder) résiduel dans la prose d'un artefact"
REQUIERT = []          # s'applique à tous les artefacts présents
DEROGATION_ADMISE = True
ORIGINE = {"type": "choix_architecture", "reference":
    "Inspiré du filtre déterministe post-génération de docforge-ai (Venkatesh188), "
    "analysé le 02/09/2026 : un pré-filtre gratuit, avant toute vérification de fond."}

MOTIFS = [
    r"\bTODO\b", r"\bTBD\b", r"\bPLACEHOLDER\b", r"\bFIXME\b", r"\bXXXX\b",
    r"lorem ipsum", r"\[INSERT\]", r"\[TO BE FILLED\]", r"\[INSERER\]",
    r"\[A COMPLETER\]", r"\[À COMPLÉTER\]",
]
RE_SUBSTITUTION = re.compile("|".join(MOTIFS), re.IGNORECASE)


def verifier(pf):
    ecarts = []
    for nom, contenu in pf.data.items():
        for chemin, texte in parcourir_chaines(contenu):
            m = RE_SUBSTITUTION.search(texte)
            if m:
                ecarts.append(Ecart(ID, "mineur", ARTEFACTS.get(nom, f"agent producteur de {nom}"),
                                    f"{nom}.yaml{chemin} : texte de substitution détecté "
                                    f"({m.group(0)!r})",
                                    "Dérogation possible si l'occurrence est un terme métier "
                                    "légitime et non un résidu de génération"))
    return ecarts
