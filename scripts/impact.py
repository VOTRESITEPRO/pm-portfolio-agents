#!/usr/bin/env python3
"""Calcule l'impact aval d'une modification portee sur un ou plusieurs artefacts deja
produits.

Jumeau invers de tranche.py : tranche.py remonte l'arbre AMONT pour une production
(« pour produire X, que faut-il d'abord ? ») ; impact.py descend l'arbre AVAL pour une
modification (« ce fait a change, qu'est-ce qui devient potentiellement obsolete ? »).
Meme principe D11 : ce calcul est mecanique, jamais laisse au raisonnement du skill.

    python3 scripts/impact.py --modifie contexte
    python3 scripts/impact.py --modifie plan --json

Sortie : les artefacts en aval (fermeture transitive), leur agent producteur, et un
rappel — CE SCRIPT NE RELANCE RIEN. Relancer chaque agent releve du skill appelant, et
CHAQUE agent repasse par ses propres points de validation obligatoire (methodologie,
estimations, cotations...) : aucun artefact n'est reecrit sans repasser par l'humain qui
l'a deja valide une fois.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pmlib import ARTEFACTS, DEPENDANCES, fermeture_transitive_aval  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--modifie", required=True,
                    help="artefact(s) dont une information a change, séparés par des virgules "
                         "(ex: contexte,charte)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    modifie = [a.strip() for a in args.modifie.split(",") if a.strip()]
    inconnus = [a for a in modifie if a not in DEPENDANCES]
    if inconnus:
        print(f"Artefact(s) inconnu(s) : {', '.join(inconnus)}", file=sys.stderr)
        print(f"Artefacts valides : {', '.join(sorted(DEPENDANCES))}", file=sys.stderr)
        return 1

    fermeture = fermeture_transitive_aval(modifie)
    ordre_complet = [a for a in DEPENDANCES if a in fermeture]  # DEPENDANCES est deja topologique
    aval = [a for a in ordre_complet if a not in modifie]
    agents = [ARTEFACTS[a] for a in aval]

    if args.json:
        print(json.dumps({"modifie": modifie, "aval": aval, "agents": agents}, ensure_ascii=False, indent=2))
    else:
        print(f"Modifié : {', '.join(modifie)}")
        if not aval:
            print("Aucun artefact en aval — rien à reconfirmer.")
        else:
            print(f"Potentiellement obsolète en aval ({len(aval)} artefact(s)) : {', '.join(aval)}")
            print(f"Agents à relancer, dans cet ordre : {', '.join(agents)}")
        print("\nCe script ne relance rien. Ne relance que les artefacts ci-dessus qui existent "
              "réellement dans pm-portfolio/ — pas ceux jamais produits. Chaque agent relancé "
              "repasse par ses propres points de validation obligatoire ; aucune réécriture "
              "silencieuse d'une valeur déjà validée par l'humain.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
