#!/usr/bin/env python3
"""Rendu Markdown des artefacts du portfolio.

    python3 render.py <dossier-portfolio>

Le Markdown est une SORTIE, jamais la source. Toute correction se fait dans le
YAML puis on regenere : un tableau Markdown n'est pas verifiable mecaniquement,
et c'est precisement ce qui rend les portes qualite possibles.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pmlib import Portfolio, liste  # noqa: E402

AVERTISSEMENT = ("> Genere depuis `{src}` par `render.py`. Ne pas editer ce fichier : "
                 "toute correction se fait dans le YAML, puis on regenere.\n")


def val(champ, defaut="—"):
    """Rend un champ chiffre {valeur, unite, statut} de facon lisible et honnete."""
    if not isinstance(champ, dict) or "valeur" not in champ:
        return str(champ) if champ is not None else defaut
    v, u, s = champ.get("valeur"), champ.get("unite", ""), champ.get("statut")
    if v is None and s == "a_sourcer":
        return "**[À SOURCER]**"
    txt = f"{v}{(' ' + u) if u else ''}"
    if s == "seuil_propose":
        etat = "arbitré" if champ.get("arbitre") else "**à arbitrer**"
        txt += f" *(seuil proposé, {etat})*"
    return txt


def tableau(entetes, lignes):
    out = ["| " + " | ".join(entetes) + " |",
           "|" + "|".join(["---"] * len(entetes)) + "|"]
    for l in lignes:
        out.append("| " + " | ".join("" if c is None else str(c) for c in l) + " |")
    return out + [""]


def r_contexte(d):
    L = ["# Dossier de contexte", ""]
    p = d.get("projet") or {}
    L += tableau(["Champ", "Valeur"],
                 [[k.capitalize(), v] for k, v in p.items()])
    if d.get("reperes"):
        L += ["## Repères chiffrés", ""]
        L += tableau(["Repère", "Valeur"], [[k, val(v)] for k, v in d["reperes"].items()])
    if d.get("contraintes"):
        L += ["## Contraintes", ""]
        L += tableau(["Contrainte", "Valeur"], [[k, val(v)] for k, v in d["contraintes"].items()])
    f = d.get("fenetre") or {}
    if f:
        L += [f"**Fenêtre calendaire** : {f.get('debut')} → {f.get('fin')}", ""]
    lac = liste(d.get("lacunes"))
    if lac:
        L += ["## Registre des lacunes d'information", "",
              "Le registre est un livrable, pas une note de travail : il énonce ce que le "
              "système refuse de combler par plausibilité.", ""]
        L += tableau(["#", "Lacune", "Gravité", "Statut", "Arbitrage / conversion"],
                     [[x.get("id"), x.get("libelle"),
                       f"**{x.get('gravite')}**" if x.get("gravite") == "bloquante" else x.get("gravite"),
                       x.get("statut"), x.get("arbitrage") or x.get("converti_en") or ""] for x in lac])
        ouvertes = [x for x in lac if x.get("gravite") == "bloquante" and x.get("statut") == "ouverte"]
        L += [f"**Verdict : {'ESCALADER' if ouvertes else 'AVANCER'}** — "
              f"{len(ouvertes)} lacune(s) bloquante(s) ouverte(s).", ""]
    return L


def r_methodologie(d):
    L = ["# Recommandation de méthodologie", "",
         f"## **{str(d.get('recommandation','')).upper()}** — {d.get('profil','')}", ""]
    if d.get("cadence"):
        L += [f"Cadence : {d['cadence']}", ""]
    L += ["## Analyse par critères", ""]
    L += tableau(["#", "Critère", "Constat dans ce contexte", "Pousse vers"],
                 [[c.get("id"), c.get("libelle"), c.get("constat"), c.get("pousse_vers")]
                  for c in liste(d.get("criteres"))])
    L += ["## Alternatives écartées", ""]
    L += tableau(["Alternative", "Motif d'écartement"],
                 [[a.get("nom"), a.get("motif")] for a in liste(d.get("alternatives_ecartees"))])
    L += [f"**Branche agile** : {'activée' if d.get('drapeau_agile') else 'non activée'}", "",
          "> **Reprise humaine obligatoire.** Le choix de méthodologie engage la "
          "contractualisation et le mode de collaboration. L'IA propose, le chef de projet tranche.",
          f"> Validation : {'acquise' if d.get('validation_humaine') else '**en attente**'}", ""]
    return L


def r_charte(d):
    L = ["# Charte de projet", ""]
    if d.get("roles"):
        L += tableau(["Rôle", "Référence", "Statut"],
                     [[r.get("role"), r.get("reference"), r.get("statut")] for r in liste(d["roles"])])
    L += ["## Objectifs SMART", ""]
    for o in liste(d.get("objectifs_smart")):
        L += [f"### {o.get('id')}", "", f"> {o.get('enonce')}", ""]
        if o.get("cible"):
            L += [f"Cible : {val(o['cible'])}", ""]
        s = o.get("smart") or {}
        L += tableau(["Critère", "Vérification"],
                     [[k.upper(), s.get(k, "")] for k in ("s", "m", "a", "r", "t")])
    per = d.get("perimetre") or {}
    L += ["## Périmètre", "", "### Inclus", ""] + [f"- {x}" for x in liste(per.get("inclus"))]
    L += ["", "### Exclus explicitement", ""] + [f"- {x}" for x in liste(per.get("exclus"))]
    L += ["", "> La section « exclus » est aussi contraignante que la section « inclus ». "
              "C'est le premier rempart contre le scope creep.", ""]
    L += ["## Livrables et critères de succès", ""]
    L += tableau(["#", "Livrable", "Critère de succès"],
                 [[x.get("id"), x.get("libelle"), x.get("critere_succes")]
                  for x in liste(d.get("livrables"))])
    if d.get("cout_benefice"):
        L += ["## Analyse coût-bénéfice", ""]
        L += tableau(["Élément", "Valeur"], [[k, val(v)] for k, v in d["cout_benefice"].items()
                                             if not isinstance(v, list)])
    if d.get("hypotheses"):
        L += ["## Hypothèses", ""]
        L += tableau(["#", "Hypothèse", "Risque associé"],
                     [[h.get("id"), h.get("libelle"), h.get("risque_associe")]
                      for h in liste(d["hypotheses"])])
    return L


def r_parties(d):
    L = ["# Parties prenantes et matrice RACI", "", "## Registre", ""]
    L += tableau(["#", "Nom", "Rôle", "Pouvoir", "Intérêt", "Statut"],
                 [[p.get("id"), p.get("nom"), p.get("role"), p.get("pouvoir"),
                   p.get("interet"),
                   f"**{p.get('statut')}**" if p.get("statut") != "confirme" else p.get("statut")]
                  for p in liste(d.get("registre"))])
    if d.get("engagement"):
        L += ["## Stratégie d'engagement par quadrant", ""]
        L += tableau(["Quadrant", "Parties prenantes"],
                     [[k.replace("_", " ").capitalize(), ", ".join(liste(v))]
                      for k, v in d["engagement"].items()])
    L += ["## Matrice RACI", ""]
    L += tableau(["Livrable", "A (approuve)", "R (réalise)", "C (consulté)", "I (informé)"],
                 [[r.get("livrable"), f"**{r.get('a')}**", ", ".join(liste(r.get("r"))),
                   ", ".join(liste(r.get("c"))), ", ".join(liste(r.get("i")))]
                  for r in liste(d.get("raci"))])
    return L


def r_plan(d):
    L = ["# Plan de projet, jalons et chemin critique", ""]
    if d.get("nature_des_estimations"):
        L += [f"> {d['nature_des_estimations']}", ""]
    L += ["## Work breakdown structure", ""]
    lignes = []
    for lot in liste(d.get("lots")):
        dur = lot.get("duree") or {}
        prof = str(lot.get("id", "")).count(".")
        lignes.append([("&nbsp;" * 4 * prof) + str(lot.get("id")),
                       lot.get("libelle"),
                       ", ".join(liste(lot.get("livrables"))) or ("*conduite*" if lot.get("type") == "conduite" else ""),
                       f"{dur.get('min','?')}-{dur.get('max','?')} sem."])
    L += tableau(["Lot", "Intitulé", "Livrables", "Durée"], lignes)
    cc = liste(d.get("chemin_critique"))
    if cc:
        L += ["## Chemin critique", "", " → ".join(str(x) for x in cc), ""]
        t = (d.get("totaux_annonces") or {}).get("chemin_critique") or {}
        if t:
            L += [f"Durée : **{val(t.get('min'))} à {val(t.get('max'))}**", "",
                  "> Les totaux sont recalculés par le validateur à partir des durées de lots. "
                  "Voir `RAPPORT-COHERENCE.md`.", ""]
    if d.get("jalons"):
        L += ["## Jalons", ""]
        L += tableau(["#", "Jalon", "Cible", "Nature"],
                     [[j.get("id"), j.get("libelle"), j.get("cible"),
                       f"**{j.get('nature')}**" if j.get("nature") == "contractuel" else j.get("nature")]
                      for j in liste(d["jalons"])])
    return L


def r_risques(d):
    reg = liste(d.get("registre"))
    L = ["# Registre des risques", "", "## Registre", ""]
    lignes = []
    for r in reg:
        p, i = r.get("p") or 0, r.get("i") or 0
        c = p * i
        dec = r.get("declencheur") or {}
        seuil = f" — seuil {val(dec['seuil'])}" if dec.get("seuil") else ""
        lignes.append([r.get("id"), r.get("libelle"), r.get("categorie"),
                       ", ".join(str(x) for x in liste(r.get("lots_couverts"))) or "—",
                       p, i, f"**{c}**" if c >= 15 else c, r.get("reponse"),
                       r.get("proprietaire"), (dec.get("libelle") or "") + seuil])
    L += tableau(["#", "Risque", "Catégorie", "Lots couverts", "P", "I", "C", "Réponse",
                  "Propriétaire", "Déclencheur"], lignes)
    majeurs = [r for r in reg if (r.get("p") or 0) * (r.get("i") or 0) >= 15]
    if majeurs:
        L += ["## Plans d'atténuation — criticité ≥ 15", ""]
        L += tableau(["#", "Atténuation", "Plan de secours"],
                     [[r.get("id"), r.get("attenuation", ""), r.get("plan_de_secours", "")]
                      for r in majeurs])
    return L


RENDUS = {"contexte": r_contexte, "methodologie": r_methodologie, "charte": r_charte,
          "parties-prenantes": r_parties, "plan": r_plan, "risques": r_risques}


def main():
    racine = sys.argv[1] if len(sys.argv) > 1 else "pm-portfolio"
    if not os.path.isdir(racine):
        print(f"Dossier introuvable : {racine}", file=sys.stderr)
        return 1
    pf = Portfolio(racine)
    n = 0
    for nom, fn in RENDUS.items():
        if nom not in pf:
            continue
        corps = fn(pf.get(nom))
        derogs = liste(pf.get(nom).get("derogations"))
        if derogs:
            corps += ["## Dérogations déclarées", "",
                      "Visibles et contestables — une dérogation n'est jamais silencieuse.", ""]
            corps += tableau(["Règle", "Élément", "Motif"],
                             [[x.get("regle"), x.get("element"), x.get("motif")] for x in derogs])
        txt = AVERTISSEMENT.format(src=f"{nom}.yaml") + "\n" + "\n".join(corps).rstrip() + "\n"
        with open(os.path.join(racine, f"{nom}.md"), "w", encoding="utf-8") as fh:
            fh.write(txt)
        n += 1
    print(f"{n} artefact(s) rendu(s) dans {racine}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
