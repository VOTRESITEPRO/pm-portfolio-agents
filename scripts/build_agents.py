#!/usr/bin/env python3
"""Assemble agents-src/*.md + agents-src/_COMMUN.md -> agents/*.md.

Pourquoi un build : les règles communes (catégories de valeur, dérogations,
non-délégables) doivent figurer dans CHAQUE agent, car Cowork ne résout pas les
références @fichier — elles y resteraient du texte littéral. Une source unique
évite la dérive ; le build produit des fichiers autonomes, portables des deux côtés.

    python3 scripts/build_agents.py
"""
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(RACINE, "agents-src")
DST = os.path.join(RACINE, "agents")
MARQUEUR = "@_COMMUN.md"

def main():
    commun_path = os.path.join(SRC, "_COMMUN.md")
    if not os.path.isfile(commun_path):
        print("agents-src/_COMMUN.md introuvable", file=sys.stderr)
        return 1
    with open(commun_path, encoding="utf-8") as fh:
        commun = fh.read().strip()
    # Le titre de niveau 1 du commun devient un titre de section dans l'agent
    commun = commun.replace("# Règles communes à tous les agents PM (rappel inséré dans chaque agent)",
                            "# Règles communes à tous les agents PM", 1)

    os.makedirs(DST, exist_ok=True)
    n = 0
    for nom in sorted(os.listdir(SRC)):
        if not nom.endswith(".md") or nom.startswith("_"):
            continue
        with open(os.path.join(SRC, nom), encoding="utf-8") as fh:
            contenu = fh.read()
        if MARQUEUR not in contenu:
            print(f"  ! {nom} : marqueur {MARQUEUR} absent, copié tel quel", file=sys.stderr)
        contenu = contenu.replace(MARQUEUR, commun)
        entete = ("<!-- FICHIER GÉNÉRÉ par scripts/build_agents.py — "
                  "ne pas éditer ici, éditer agents-src/ puis relancer le build -->\n")
        # L'entete se place APRES le frontmatter YAML
        if contenu.startswith("---"):
            fin = contenu.index("\n---", 3) + len("\n---\n")
            contenu = contenu[:fin] + entete + contenu[fin:]
        else:
            contenu = entete + contenu
        with open(os.path.join(DST, nom), "w", encoding="utf-8") as fh:
            fh.write(contenu)
        n += 1
    print(f"{n} agent(s) généré(s) dans agents/")
    return 0

if __name__ == "__main__":
    sys.exit(main())
