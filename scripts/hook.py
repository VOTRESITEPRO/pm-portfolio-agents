#!/usr/bin/env python3
"""Point d'entree des hooks : valide le portfolio apres ecriture, et au Stop.

Lit l'evenement sur stdin (JSON), decide, et sort :
  0 = laisser passer   2 = bloquer (stderr devient le retour a Claude)

Mode PostToolUse : informatif. On ne bloque pas une ecriture d'artefact au motif
que les artefacts suivants n'existent pas encore — la chaine est sequentielle.
Mode Stop : bloquant. Un tour ne se conclut pas sur un portfolio en ecart.
"""
import json
import os
import subprocess
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VALIDATE = os.path.join(RACINE, "scripts", "validate.py")


def trouver_portfolio(cwd: str) -> str | None:
    for cand in ("pm-portfolio", os.path.join("docs", "pm-portfolio")):
        p = os.path.join(cwd, cand)
        if os.path.isdir(p):
            return p
    return None


def main() -> int:
    try:
        evt = json.load(sys.stdin)
    except Exception:
        return 0                      # jamais bloquer sur un evenement illisible

    cwd = evt.get("cwd") or os.getcwd()
    event = evt.get("hook_event_name", "")
    portfolio = trouver_portfolio(cwd)
    if not portfolio:
        return 0

    # ${CLAUDE_PLUGIN_ROOT} n'est substitue que dans les JSON de hooks, jamais dans le
    # corps d'un agent ou d'un skill (bug connu anthropics/claude-code#9354). Le hook est
    # donc le seul endroit qui connaisse de facon fiable la racine du plugin : il la
    # depose dans le portfolio, ou les agents peuvent la lire.
    try:
        with open(os.path.join(portfolio, ".plugin-path"), "w", encoding="utf-8") as fh:
            fh.write(RACINE + "\n")
    except OSError:
        pass

    # PostToolUse : ne reagir qu'aux ecritures dans le portfolio
    if event.startswith("PostToolUse"):
        chemin = (evt.get("tool_input") or {}).get("file_path", "")
        if "pm-portfolio" not in chemin.replace("\\", "/") or not chemin.endswith(".yaml"):
            return 0

    res = subprocess.run([sys.executable, VALIDATE, portfolio, "--quiet"],
                         capture_output=True, text=True)

    # Codes de retour de validate.py :
    #   0 = conforme · 1 = rien a valider ou erreur d'usage · 2 = ecart bloquant
    # Seul le 2 justifie de bloquer. Traiter le 1 comme un ecart faisait echouer le
    # hook Stop sur un portfolio encore vide — ce qui n'a aucun sens et bloque la
    # chaine avant meme qu'elle ait produit quoi que ce soit.
    if res.returncode != 2:
        return 0

    rapport = os.path.join(portfolio, "RAPPORT-COHERENCE.md")
    resume = (res.stderr or "").strip().splitlines()
    resume = resume[-1] if resume else "ecarts detectes"

    if event == "Stop":
        print(f"Portfolio en ecart : {resume}\n"
              f"Lis {rapport}, corrige via l'agent responsable indique pour chaque ecart, "
              f"puis relance la validation. Ne conclus pas sur un portfolio en ecart bloquant.",
              file=sys.stderr)
        return 2

    # PostToolUse : informatif seulement
    nb = resume.split()[1] if resume.startswith("BLOQUE") else "?"
    print(f"[pm-portfolio] {nb} ecart(s) bloquant(s) — voir {rapport}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
