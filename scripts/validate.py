#!/usr/bin/env python3
"""Moteur de validation du portfolio PM — portes qualite deterministes.

    python3 validate.py <dossier-portfolio> [--rapport] [--json]

Sortie : RAPPORT-COHERENCE.md dans le dossier, et un code de retour exploitable
par un hook Claude Code / Cowork :
    0 = aucun ecart bloquant
    2 = ecart bloquant — l'action appelante doit etre refusee

Le moteur ne juge rien. Il applique les regles, gere leur applicabilite et
enregistre les derogations declarees par les agents.
"""
from __future__ import annotations

import argparse
import importlib
import json
import os
import pkgutil
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pmlib import ARTEFACTS, Portfolio, ResultatRegle  # noqa: E402


def charger_regles():
    import rules
    mods = []
    for info in pkgutil.iter_modules(rules.__path__):
        if not info.name.startswith("r"):
            continue
        mods.append(importlib.import_module(f"rules.{info.name}"))
    return sorted(mods, key=lambda m: int(m.ID[1:]))


def condition_supplementaire_satisfaite(mod, pf) -> bool | None:
    """None si la regle n'a pas de condition supplementaire."""
    cond = getattr(mod, "CONDITION_SUPPLEMENTAIRE", None)
    if cond is None:
        return None
    artefact, champ, attendu = cond
    if artefact not in pf:
        return None          # indeterminable : l'artefact porteur manque aussi
    return pf.get(artefact).get(champ) == attendu


def evaluer(mod, pf) -> ResultatRegle:
    res = ResultatRegle(regle=mod.ID, libelle=mod.LIBELLE, etat="conforme")
    manquants = pf.agents_manquants(getattr(mod, "REQUIERT", []))
    cond = condition_supplementaire_satisfaite(mod, pf)

    # Condition explicitement non satisfaite -> non applicable, quoi qu'il manque
    if cond is False:
        res.etat = "non_applicable"
        art, champ, attendu = mod.CONDITION_SUPPLEMENTAIRE
        res.motif_non_applicable = f"condition non satisfaite : {art}.{champ} != {attendu}"
        return res

    # La tranche declaree est une decision explicite de l'utilisateur : elle prime
    # sur la condition d'activation. Mais quand la condition EST satisfaite, le motif
    # doit le dire — sinon on masque le fait que la branche agile tourne sans backlog.
    requis = getattr(mod, "REQUIERT", [])
    hors_tranche = [a for a in requis if not pf.dans_la_tranche(a)]
    if hors_tranche:
        res.etat = "non_applicable"
        res.motif_non_applicable = ("hors tranche déclarée : "
                                    + ", ".join(ARTEFACTS[a] for a in hors_tranche))
        if cond is True:
            art, champ, attendu = mod.CONDITION_SUPPLEMENTAIRE
            res.motif_non_applicable += (f" — ATTENTION : {art}.{champ} == {attendu}, "
                                         "cet artefact est attendu dès que la tranche s'élargit")
        return res

    if manquants:
        if cond is True or all(pf.dans_la_tranche(a) for a in requis):
            # La condition EXIGE ces artefacts : leur absence est un ecart, pas une
            # non-applicabilite (correction C2).
            from pmlib import Ecart
            res.etat = "ecart"
            motif = ("la condition d'activation est satisfaite"
                     if cond is True else "artefact déclaré dans la tranche")
            res.ecarts = [Ecart(mod.ID, "bloquant", ", ".join(manquants),
                                "Artefact attendu et manquant",
                                f"{motif} ; requis : {manquants}")]
            return res
        res.etat = "non_applicable"
        res.motif_non_applicable = "agent(s) hors périmètre : " + ", ".join(manquants)
        return res

    ecarts = mod.verifier(pf)

    # Derogations declarees par les agents (correction C6)
    if getattr(mod, "DEROGATION_ADMISE", False):
        derogs = pf.derogations(mod.ID)
        couverts = {str(d.get("element")) for d in derogs}
        retenus, accordes = [], []
        for e in ecarts:
            if any(str(c) and str(c) in e.libelle for c in couverts):
                accordes.append(e)
            else:
                retenus.append(e)
        res.derogations = [d for d in derogs]
        ecarts = retenus
    else:
        refusees = pf.derogations(mod.ID)
        if refusees:
            from pmlib import Ecart
            for d in refusees:
                ecarts.append(Ecart(mod.ID, "bloquant", d.get("artefact", "?"),
                                    f"Dérogation refusée sur {mod.ID} : cette règle n'admet pas de dérogation",
                                    f"élément : {d.get('element')}"))

    res.ecarts = ecarts
    if ecarts:
        res.etat = "ecart"
    elif res.derogations:
        res.etat = "derogation_accordee"
    return res


def rapport_markdown(racine, resultats, pf) -> str:
    bloquants = [e for r in resultats for e in r.ecarts if e.gravite == "bloquant"]
    mineurs = [e for r in resultats for e in r.ecarts if e.gravite == "mineur"]
    derogs = [d for r in resultats for d in r.derogations]

    verdict = "**RETRAVAILLER**" if bloquants else ("**AVANCER avec écarts mineurs**" if mineurs else "**AVANCER**")

    L = [
        "# Rapport de cohérence inter-artefacts",
        "",
        f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')} par `validate.py` "
        "(contrôle déterministe, sans intervention d'un modèle de langage).",
        "",
        f"**Artefacts présents** : {', '.join(sorted(pf.presents)) or 'aucun'}",
        "",
        (f"**Tranche déclarée** : {', '.join(sorted(pf.tranche))}"
         if os.path.isfile(os.path.join(racine, 'tranche.yaml'))
         else "**Tranche** : non déclarée — déduite des artefacts présents"),
        "",
        (f"**Manquants dans la tranche déclarée** : {', '.join(pf.tranche_incomplete)}"
         if pf.tranche_incomplete else ""),
        "",
        f"## Verdict : {verdict}",
        "",
        f"{len(bloquants)} écart(s) bloquant(s) · {len(mineurs)} mineur(s) · "
        f"{len(derogs)} dérogation(s) accordée(s)",
        "",
        "## Exécution des règles",
        "",
        "| Règle | Libellé | État | Détail |",
        "|---|---|---|---|",
    ]
    sym = {"conforme": "conforme", "ecart": "**ÉCART**", "non_applicable": "non applicable",
           "derogation_accordee": "dérogation"}
    for r in resultats:
        detail = r.motif_non_applicable or (f"{len(r.ecarts)} écart(s)" if r.ecarts else "")
        L.append(f"| {r.regle} | {r.libelle} | {sym[r.etat]} | {detail} |")

    exec_ = sum(1 for r in resultats if r.etat != "non_applicable")
    L += ["", f"**{exec_} règle(s) sur {len(resultats)} exécutée(s).** Une règle non applicable "
              "l'est par condition déclarée, jamais par absence constatée d'artefact.", ""]

    for titre, lot in (("Écarts bloquants", bloquants), ("Écarts mineurs", mineurs)):
        if not lot:
            continue
        L += [f"## {titre}", ""]
        for e in lot:
            L.append(f"### [{e.regle}] {e.libelle}")
            if e.detail:
                L.append(f"\n{e.detail}")
            L.append(f"\n*Agent responsable de la correction : `{e.agent}`*\n")

    if derogs:
        L += ["## Dérogations accordées", "",
              "Visibles et contestables — une dérogation n'est jamais silencieuse.", "",
              "| Règle | Élément | Motif | Déclarée dans |", "|---|---|---|---|"]
        for d in derogs:
            L.append(f"| {d.get('regle')} | {d.get('element')} | {d.get('motif','')} | {d.get('artefact')}.yaml |")
        L.append("")

    if bloquants:
        agents = sorted({e.agent for e in bloquants})
        L += ["## Renvoi aux agents", "",
              "Les écarts bloquants sont renvoyés à leur agent auteur :", ""]
        L += [f"- `{a}`" for a in agents]
        L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Valide un portfolio d'artefacts PM.")
    ap.add_argument("portfolio", nargs="?", default="pm-portfolio")
    ap.add_argument("--json", action="store_true", help="sortie JSON au lieu du rapport")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if not os.path.isdir(args.portfolio):
        print(f"Dossier introuvable : {args.portfolio}", file=sys.stderr)
        return 1

    pf = Portfolio(args.portfolio)
    if pf.erreurs_chargement:
        for err in pf.erreurs_chargement:
            print(err, file=sys.stderr)
        return 1
    if not pf.presents:
        print(f"Aucun artefact dans {args.portfolio}", file=sys.stderr)
        return 1

    resultats = [evaluer(m, pf) for m in charger_regles()]
    bloquants = [e for r in resultats for e in r.ecarts if e.gravite == "bloquant"]

    if args.json:
        print(json.dumps({
            "artefacts": sorted(pf.presents),
            "bloquants": len(bloquants),
            "regles": [{"id": r.regle, "etat": r.etat,
                        "ecarts": [{"gravite": e.gravite, "agent": e.agent,
                                    "libelle": e.libelle, "detail": e.detail} for e in r.ecarts],
                        "motif": r.motif_non_applicable} for r in resultats],
        }, ensure_ascii=False, indent=2))
    else:
        rapport = rapport_markdown(args.portfolio, resultats, pf)
        chemin = os.path.join(args.portfolio, "RAPPORT-COHERENCE.md")
        with open(chemin, "w", encoding="utf-8") as fh:
            fh.write(rapport)
        if not args.quiet:
            print(rapport)
        print(f"\n-> {chemin}", file=sys.stderr)

    if bloquants:
        print(f"\nBLOQUÉ : {len(bloquants)} écart(s) bloquant(s). "
              f"Voir {os.path.join(args.portfolio, 'RAPPORT-COHERENCE.md')}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
