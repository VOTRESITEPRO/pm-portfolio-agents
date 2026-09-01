#!/usr/bin/env python3
"""Calcule la fermeture transitive d'une tranche d'exécution.

Le skill `pm-portfolio` (et, à terme, `pm-orchestrateur-pm`) ne doit jamais énumérer
lui-même les dépendances d'une tranche par raisonnement : c'est exactement le type de
calcul mécanique que ce projet confie au code, pas au jugement d'un modèle (voir
docs/document-raisonnement.md, décision D11).

    python3 scripts/tranche.py --cible risques,parties-prenantes
    python3 scripts/tranche.py --cible budget --json

Sortie : la liste des artefacts de la fermeture transitive (triée, dépendances comprises),
leur agent producteur, et — pour information — les artefacts inconnus signalés en erreur.
Écrit aussi, en clair, le contenu YAML prêt à coller dans `tranche.yaml` : ce bloc doit être
copié tel quel, jamais reconstruit de mémoire par l'agent appelant.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pmlib import ARTEFACTS, DEPENDANCES, fermeture_transitive  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--cible", required=True,
                    help="artefacts visés, séparés par des virgules (ex: risques,budget)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    cible = [a.strip() for a in args.cible.split(",") if a.strip()]
    inconnus = [a for a in cible if a not in DEPENDANCES]
    if inconnus:
        print(f"Artefact(s) inconnu(s) : {', '.join(inconnus)}", file=sys.stderr)
        print(f"Artefacts valides : {', '.join(sorted(DEPENDANCES))}", file=sys.stderr)
        return 1

    fermeture = fermeture_transitive(cible)
    ordre = [a for a in DEPENDANCES if a in fermeture]  # DEPENDANCES est déjà dans un ordre topologique valide
    agents = [ARTEFACTS[a] for a in ordre]

    if args.json:
        print(json.dumps({"cible": cible, "fermeture": ordre, "agents": agents}, ensure_ascii=False, indent=2))
    else:
        print(f"Cible : {', '.join(cible)}")
        print(f"Fermeture transitive ({len(ordre)} artefact(s)) : {', '.join(ordre)}")
        print(f"Agents à lancer, dans cet ordre : {', '.join(agents)}")
        print("\ntranche.yaml :")
        print("artefacts:")
        for a in ordre:
            print(f"  - {a}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
