#!/usr/bin/env python3
"""Contrôle pré-vol : à lancer AVANT d'installer le plugin, sur la machine cible.

    python3 scripts/preflight.py     (ou : python scripts\\preflight.py)

Vérifie l'environnement et l'intégrité du plugin. N'installe rien.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OK, KO = [], []


def test(nom, condition, detail=""):
    (OK if condition else KO).append((nom, detail))
    print(f"  [{'ok  ' if condition else 'ECHEC'}] {nom}" + (f"  — {detail}" if detail and not condition else ""))


ap = argparse.ArgumentParser(description="Contrôle pré-vol du plugin.")
ap.add_argument("--fix-hooks", action="store_true",
                help="réécrit hooks/hooks.json avec l'invocation Python qui fonctionne ici")
ARGS = ap.parse_args()

print(f"Plugin : {RACINE}\n")
print("Environnement")
test(f"Python {sys.version_info.major}.{sys.version_info.minor} (3.9+ requis)",
     sys.version_info >= (3, 9), f"version trouvée : {sys.version.split()[0]}")
print(f"         invocation à utiliser dans les commandes : {os.path.basename(sys.executable)}")
try:
    import yaml  # noqa: F401
    test("PyYAML disponible", True)
except ImportError:
    test("PyYAML disponible", False,
         f"installer : {os.path.basename(sys.executable)} -m pip install pyyaml")


def invocation_qui_marche() -> str | None:
    """Trouve l'invocation Python utilisable depuis un shell, pour les hooks.

    Sous Windows, `python` et `python3` sont souvent des alias du Microsoft Store
    qui échouent, alors que le launcher `py` fonctionne. L'inverse est vrai sous
    Linux et macOS. Les hooks ne peuvent pas deviner : il faut tester.
    """
    for cand in (["py", "-3"], ["python3"], ["python"]):
        exe = shutil.which(cand[0])
        if not exe:
            continue
        try:
            r = subprocess.run(cand + ["-c", "import sys; print(sys.version_info[0])"],
                               capture_output=True, text=True, timeout=15)
            if r.returncode == 0 and r.stdout.strip() == "3":
                return " ".join(cand)
        except (OSError, subprocess.SubprocessError):
            continue
    return None


INVOCATION = invocation_qui_marche()
test("une invocation Python fonctionne depuis un shell", INVOCATION is not None,
     "ni py, ni python3, ni python ne répondent")
if INVOCATION:
    print(f"         invocation retenue pour les hooks : {INVOCATION}")

print("\nStructure du plugin")
manifeste = os.path.join(RACINE, ".claude-plugin", "plugin.json")
test(".claude-plugin/plugin.json present", os.path.isfile(manifeste))
decl = {}
if os.path.isfile(manifeste):
    try:
        with open(manifeste, encoding="utf-8") as fh:
            decl = json.load(fh)
        test("plugin.json est un JSON valide", True)
        test("champ 'name' présent", bool(decl.get("name")))
    except json.JSONDecodeError as exc:
        test("plugin.json est un JSON valide", False, str(exc))

for chemin in decl.get("agents", []):
    p = os.path.join(RACINE, chemin.lstrip("./"))
    test(f"agent déclaré présent : {os.path.basename(chemin)}", os.path.isfile(p))

hooks = os.path.join(RACINE, "hooks", "hooks.json")
test("hooks/hooks.json présent", os.path.isfile(hooks))
if os.path.isfile(hooks):
    try:
        with open(hooks, encoding="utf-8") as fh:
            brut = fh.read()
        json.loads(brut)
        test("hooks.json est un JSON valide", True)

        # L'invocation écrite dans hooks.json doit être celle qui marche ICI.
        # Sinon les portes qualité ne s'exécutent jamais — en silence.
        actuelle = None
        for cand in ("py -3", "python3", "python"):
            if f'"command": "{cand} ' in brut:
                actuelle = cand
                break
        coherent = INVOCATION is not None and actuelle == INVOCATION
        test(f"hooks.json invoque une commande valide sur cette machine", coherent,
             f"hooks.json utilise '{actuelle}', or '{INVOCATION}' fonctionne ici — "
             f"relancer avec --fix-hooks")
        if not coherent and ARGS.fix_hooks and INVOCATION and actuelle:
            with open(hooks, "w", encoding="utf-8") as fh:
                fh.write(brut.replace(f'"command": "{actuelle} ',
                                      f'"command": "{INVOCATION} '))
            print(f"         -> hooks.json corrigé : '{actuelle}' remplace par '{INVOCATION}'")
            KO.pop()
            OK.append(("hooks.json corrigé", ""))
    except json.JSONDecodeError as exc:
        test("hooks.json est un JSON valide", False, str(exc))

print("\nIntégrité des agents")
dossier = os.path.join(RACINE, "agents")
for nom in sorted(os.listdir(dossier)) if os.path.isdir(dossier) else []:
    if not nom.endswith(".md"):
        continue
    with open(os.path.join(dossier, nom), encoding="utf-8") as fh:
        t = fh.read()
    base = nom[:-3]
    test(f"{base} : frontmatter name + description",
         bool(re.search(r"^name: ", t, re.M) and re.search(r"^description: ", t, re.M)))
    test(f"{base} : aucune référence @fichier résiduelle", "@_COMMUN.md" not in t)
    test(f"{base} : aucun ${{CLAUDE_PLUGIN_ROOT}} (non substitué dans un agent)",
         "CLAUDE_PLUGIN_ROOT" not in t)

print("\nChaîne de validation")
sys.path.insert(0, os.path.join(RACINE, "scripts"))
try:
    from validate import charger_regles
    regles = charger_regles()
    test(f"{len(regles)} règles chargées (11 attendues)", len(regles) == 11)
except Exception as exc:
    test("chargement des règles", False, str(exc))

exemple = os.path.join(RACINE, "exemples", "portail-b2b")
if os.path.isdir(exemple):
    import subprocess
    r = subprocess.run([sys.executable, os.path.join(RACINE, "scripts", "validate.py"),
                        exemple, "--json"], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
        test("l'exemple de référence détecte bien ses défauts volontaires",
             d["bloquants"] > 0, f"{d['bloquants']} écart(s) attendus")
    except Exception:
        test("exécution du validateur sur l'exemple", False, r.stderr[-200:])

print(f"\n{len(OK)} contrôle(s) OK, {len(KO)} en échec.")
if KO:
    print("\nÀ régler avant installation :")
    for nom, detail in KO:
        print(f"  - {nom}" + (f" ({detail})" if detail else ""))
    sys.exit(1)
print("Prêt pour l'installation. Voir INSTALLATION.md.")
if INVOCATION:
    print(f"\nUtilise « {INVOCATION} » pour toutes les commandes de ce plugin.")
