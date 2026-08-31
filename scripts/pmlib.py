"""Socle commun des validateurs du portfolio PM.

Principe directeur : le LLM produit, le code vérifie. Aucune fonction de ce module
n'émet de jugement qualitatif — elle compte, recalcule, croise et trace.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    raise SystemExit(
        "PyYAML est requis : pip install pyyaml (ou pip install --break-system-packages pyyaml)"
    )

# --- Artefacts du portfolio, et agent producteur de chacun -------------------

ARTEFACTS = {
    "contexte": "pm-contexte-projet",
    "methodologie": "pm-methodologue",
    "charte": "pm-charte-objectifs",
    "parties-prenantes": "pm-parties-prenantes",
    "plan": "pm-planificateur-wbs",
    "risques": "pm-risques",
    # increment 2 — déclarés ici pour que les règles sachent les attendre
    "budget": "pm-budget-achats",
    "communications": "pm-communications",
    "qualite": "pm-qualite-suivi",
    "cloture": "pm-equipe-cloture",
    "backlog": "pm-backlog-stories",
    "sprint": "pm-sprint",
}

INCREMENT_ACTUEL = {
    "contexte", "methodologie", "charte", "parties-prenantes", "plan", "risques",
}

# --- Dépendances entre artefacts (correction C1) -----------------------------
# Une tranche d'exécution se définit comme la FERMETURE TRANSITIVE des dépendances
# des agents visés, jamais comme une sélection d'agents. Sélectionner un agent,
# c'est sélectionner tout son arbre amont.

DEPENDANCES = {
    "contexte": [],
    "methodologie": ["contexte"],
    "charte": ["methodologie"],
    "parties-prenantes": ["charte"],
    "plan": ["charte"],
    "risques": ["plan"],
    "budget": ["plan", "risques"],
    "communications": ["parties-prenantes", "plan"],
    "qualite": ["plan", "budget", "communications"],
    "cloture": ["parties-prenantes", "qualite"],
    "backlog": ["charte", "methodologie"],
    "sprint": ["backlog"],
}


def fermeture_transitive(artefacts) -> set[str]:
    """Retourne les artefacts visés PLUS tout leur arbre amont."""
    vus, pile = set(), list(artefacts)
    while pile:
        a = pile.pop()
        if a in vus or a not in DEPENDANCES:
            continue
        vus.add(a)
        pile.extend(DEPENDANCES[a])
    return vus

# --- Categories de valeur (correction C4 de la cartographie) ----------------
# Une valeur chiffrée porte toujours un statut. C'est la structure qui fait
# respecter la règle, pas la bonne volonté de l'agent.

STATUTS_VALEUR = {
    "source",          # traçable vers le contexte ou un arbitrage humain — autorisée
    "seuil_propose",   # proposition de pilotage — autorisée SI marquée et non engageante
    "a_sourcer",       # donnée absente, explicitement non produite — autorisée
}

STATUTS_NON_POURVU = {"a_nommer", "a_confirmer", "a_constituer", "a_contractualiser"}


# --- Modele de resultat -----------------------------------------------------

@dataclass
class Ecart:
    regle: str
    gravite: str          # "bloquant" | "mineur"
    agent: str            # agent responsable de la correction
    libelle: str
    detail: str = ""

    def __str__(self) -> str:
        return f"[{self.regle}] {self.libelle}"


@dataclass
class ResultatRegle:
    regle: str
    libelle: str
    etat: str                       # conforme | ecart | non_applicable | derogation_accordee
    ecarts: list[Ecart] = field(default_factory=list)
    derogations: list[dict] = field(default_factory=list)
    motif_non_applicable: str = ""


# --- Chargement -------------------------------------------------------------

class Portfolio:
    """Vue en lecture des artefacts présents sur disque."""

    def __init__(self, racine: str):
        self.racine = racine
        self.data: dict[str, Any] = {}
        self.erreurs_chargement: list[str] = []
        self.tranche: set[str] | None = None
        self.tranche_incomplete: list[str] = []
        for nom in ARTEFACTS:
            chemin = os.path.join(racine, f"{nom}.yaml")
            if not os.path.isfile(chemin):
                continue
            try:
                with open(chemin, encoding="utf-8") as fh:
                    self.data[nom] = yaml.safe_load(fh) or {}
            except yaml.YAMLError as exc:
                self.erreurs_chargement.append(f"{nom}.yaml illisible : {exc}")
        self._charger_tranche()

    def _charger_tranche(self):
        """tranche.yaml déclare le périmètre d'exécution voulu (correction C1).

        Absent : la tranche est déduite des artefacts présents, ce qui revient à
        dire que l'utilisateur n'a pas déclaré d'intention — les règles portant sur
        un artefact absent sont alors non applicables.
        """
        chemin = os.path.join(self.racine, "tranche.yaml")
        if os.path.isfile(chemin):
            try:
                with open(chemin, encoding="utf-8") as fh:
                    decl = (yaml.safe_load(fh) or {}).get("artefacts") or []
                self.tranche = fermeture_transitive(decl)
            except yaml.YAMLError as exc:
                self.erreurs_chargement.append(f"tranche.yaml illisible : {exc}")
                self.tranche = set(self.data)
        else:
            self.tranche = set(self.data)
        # Un artefact de la tranche déclarée mais absent du disque est un manque réel
        self.tranche_incomplete = sorted(self.tranche - set(self.data))

    def dans_la_tranche(self, artefact: str) -> bool:
        return self.tranche is None or artefact in self.tranche

    def __contains__(self, nom: str) -> bool:
        return nom in self.data

    def get(self, nom: str, defaut=None):
        return self.data.get(nom, defaut if defaut is not None else {})

    @property
    def presents(self) -> set[str]:
        return set(self.data)

    def agents_manquants(self, artefacts_requis: list[str]) -> list[str]:
        return [ARTEFACTS[a] for a in artefacts_requis if a not in self.data]

    def derogations(self, regle: str) -> list[dict]:
        """Dérogations déclarées par les agents, tous artefacts confondus (correction C6)."""
        out = []
        for nom, contenu in self.data.items():
            for d in (contenu or {}).get("derogations", []) or []:
                if d.get("regle") == regle:
                    out.append({**d, "artefact": nom})
        return out


# --- Utilitaires de lecture tolérante ---------------------------------------

def liste(valeur) -> list:
    if valeur is None:
        return []
    return valeur if isinstance(valeur, list) else [valeur]


def valeur_de(champ) -> Any:
    """Extrait la valeur d'un champ chiffré structuré {valeur, statut}."""
    if isinstance(champ, dict):
        return champ.get("valeur")
    return champ


def statut_de(champ) -> str | None:
    if isinstance(champ, dict):
        return champ.get("statut")
    return None


def parcourir_valeurs(noeud, chemin="") -> list[tuple[str, dict]]:
    """Retourne tous les champs structurés {valeur: ...} du document, avec leur chemin."""
    trouves = []
    if isinstance(noeud, dict):
        if "valeur" in noeud and not isinstance(noeud.get("valeur"), (dict, list)):
            trouves.append((chemin or "<racine>", noeud))
        for cle, sous in noeud.items():
            trouves += parcourir_valeurs(sous, f"{chemin}.{cle}" if chemin else str(cle))
    elif isinstance(noeud, list):
        for i, sous in enumerate(noeud):
            trouves += parcourir_valeurs(sous, f"{chemin}[{i}]")
    return trouves


def somme_bornes(items, cle="duree") -> tuple[float, float]:
    """Somme les bornes min/max d'une liste d'éléments portant {cle: {min, max}}."""
    mn = mx = 0.0
    for it in items:
        d = (it or {}).get(cle) or {}
        mn += float(d.get("min") or 0)
        mx += float(d.get("max") or 0)
    return mn, mx
