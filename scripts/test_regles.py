#!/usr/bin/env python3
"""Tests de non-régression des règles de cohérence.

Chaque test construit un portfolio minimal en mémoire et vérifie que la règle
DÉTECTE ce qu'elle prétend détecter — et, tout aussi important, qu'elle ne
déclenche PAS sur un cas conforme.

    python3 scripts/test_regles.py
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml  # noqa: E402

from pmlib import Portfolio  # noqa: E402
from validate import charger_regles, charger_portes, evaluer  # noqa: E402

REGLES = {m.ID: m for m in charger_regles() + charger_portes()}
ECHECS = []


def portfolio(_tranche=None, **artefacts) -> Portfolio:
    d = tempfile.mkdtemp()
    if _tranche is not None:
        with open(os.path.join(d, "tranche.yaml"), "w", encoding="utf-8") as fh:
            yaml.safe_dump({"artefacts": _tranche}, fh)
    for nom, contenu in artefacts.items():
        with open(os.path.join(d, f"{nom.replace('_','-')}.yaml"), "w", encoding="utf-8") as fh:
            yaml.safe_dump(contenu, fh, allow_unicode=True)
    return Portfolio(d)


def verifie(nom, regle, pf, etat_attendu, motif_attendu=None):
    res = evaluer(REGLES[regle], pf)
    ok = res.etat == etat_attendu
    if ok and motif_attendu:
        ok = any(motif_attendu.lower() in (e.libelle + e.detail).lower() for e in res.ecarts)
    statut = "ok  " if ok else "ECHEC"
    print(f"  [{statut}] {nom}")
    if not ok:
        ECHECS.append(nom)
        print(f"         attendu {etat_attendu}"
              + (f" contenant '{motif_attendu}'" if motif_attendu else "")
              + f", obtenu {res.etat} : {[str(e) for e in res.ecarts]}")


print("R1 — couverture des livrables")
verifie("livrable non couvert par un lot", "R1",
        portfolio(charte={"livrables": [{"id": "D1"}, {"id": "D2"}]},
                  plan={"lots": [{"id": "1", "livrables": ["D1"]}]}),
        "ecart", "D2")
verifie("lot sans livrable non déclaré conduite", "R1",
        portfolio(charte={"livrables": [{"id": "D1"}]},
                  plan={"lots": [{"id": "1", "livrables": ["D1"]}, {"id": "2"}]}),
        "ecart", "ne trace vers aucun livrable")
verifie("lot de conduite accepté", "R1",
        portfolio(charte={"livrables": [{"id": "D1"}]},
                  plan={"lots": [{"id": "1", "livrables": ["D1"]}, {"id": "2", "type": "conduite"}]}),
        "conforme")

print("R5 — RACI")
verifie("deux Accountable", "R5",
        portfolio(parties_prenantes={"raci": [{"livrable": "D1", "a": ["PP1", "PP2"], "r": ["PP3"]}]}),
        "ecart", "2 Accountable")
verifie("aucun Responsible", "R5",
        portfolio(parties_prenantes={"raci": [{"livrable": "D1", "a": "PP1", "r": []}]}),
        "ecart", "aucun Responsible")
verifie("RACI correct", "R5",
        portfolio(parties_prenantes={"raci": [{"livrable": "D1", "a": "PP1", "r": ["PP2"]}]}),
        "conforme")

print("R7 — chemin critique couvert par les risques")
verifie("lot critique sans risque", "R7",
        portfolio(plan={"lots": [{"id": "1.1"}], "chemin_critique": ["1.1", "1.2"]},
                  risques={"registre": [{"id": "R-01", "lots_couverts": ["1.1"]}]}),
        "ecart", "1.2")

print("R9 — catégories de valeur")
verifie("valeur sans statut = donnée factuelle générée", "R9",
        portfolio(charte={"cout": {"valeur": 12, "unite": "EUR"}}),
        "ecart", "sans statut")
verifie("statut inconnu", "R9",
        portfolio(charte={"cout": {"valeur": 12, "statut": "estime"}}),
        "ecart", "statut inconnu")
verifie("a_sourcer avec une valeur renseignée", "R9",
        portfolio(charte={"cout": {"valeur": 12, "statut": "a_sourcer"}}),
        "ecart", "a_sourcer mais une valeur")
verifie("seuil correctement marqué", "R9",
        portfolio(charte={"seuil": {"valeur": 70, "statut": "seuil_propose", "arbitre": False}}),
        "conforme")

print("R10 — rôle pourvu")
verifie("propriétaire au statut a_nommer", "R10",
        portfolio(parties_prenantes={"registre": [{"id": "PP1", "nom": "CP", "statut": "a_nommer"}], "raci": []},
                  risques={"registre": [{"id": "R-01", "proprietaire": "PP1"}]}),
        "ecart", "non pourvu")
verifie("propriétaire en libellé libre au lieu d'une référence", "R10",
        portfolio(parties_prenantes={"registre": [{"id": "PP1", "nom": "CP", "statut": "confirme"}], "raci": []},
                  risques={"registre": [{"id": "R-01", "proprietaire": "le chef de projet"}]}),
        "ecart", "absent du registre")
verifie("propriétaire pourvu", "R10",
        portfolio(parties_prenantes={"registre": [{"id": "PP1", "nom": "CP", "statut": "confirme"}], "raci": []},
                  risques={"registre": [{"id": "R-01", "proprietaire": "PP1"}]}),
        "conforme")

print("R11 — cohérence arithmétique")
verifie("total annoncé faux", "R11",
        portfolio(plan={"lots": [{"id": "a", "duree": {"min": 4, "max": 5}},
                                 {"id": "b", "duree": {"min": 6, "max": 8}}],
                        "chemin_critique": ["a", "b"],
                        "totaux_annonces": {"chemin_critique": {"min": {"valeur": 10, "statut": "source"},
                                                                "max": {"valeur": 12, "statut": "source"}}}}),
        "ecart", "13 recalculé")
verifie("total annoncé juste", "R11",
        portfolio(plan={"lots": [{"id": "a", "duree": {"min": 4, "max": 5}},
                                 {"id": "b", "duree": {"min": 6, "max": 8}}],
                        "chemin_critique": ["a", "b"],
                        "totaux_annonces": {"chemin_critique": {"min": {"valeur": 10, "statut": "source"},
                                                                "max": {"valeur": 13, "statut": "source"}}}}),
        "conforme")
verifie("échéance intenable détectée", "R11",
        portfolio(contexte={"fenetre": {"debut": "2026-09-01", "fin": "2026-12-31"}},
                  plan={"lots": [{"id": "a", "duree": {"min": 20, "max": 30}}],
                        "chemin_critique": ["a"]}),
        "ecart", "intenable")
verifie("lot du chemin critique inexistant", "R11",
        portfolio(plan={"lots": [{"id": "a", "duree": {"min": 1, "max": 1}}],
                        "chemin_critique": ["a", "zzz"]}),
        "ecart", "inexistant")

print("R8 — applicabilité conditionnelle (corrections C1 et C2)")
verifie("drapeau agile faux -> non applicable", "R8",
        portfolio(charte={"livrables": [{"id": "D1"}]}, methodologie={"drapeau_agile": False}),
        "non_applicable")
verifie("backlog hors tranche -> non applicable, mais avec avertissement", "R8",
        portfolio(charte={"livrables": [{"id": "D1"}]}, methodologie={"drapeau_agile": True}),
        "non_applicable")
res = evaluer(REGLES["R8"], portfolio(charte={"livrables": [{"id": "D1"}]},
                                      methodologie={"drapeau_agile": True}))
_ok = "ATTENTION" in res.motif_non_applicable
print(f"  [{'ok  ' if _ok else 'ECHEC'}] l'avertissement signale que la branche agile est active")
if not _ok:
    ECHECS.append("avertissement R8 hors tranche")
verifie("backlog DANS la tranche mais absent -> ÉCART, pas non applicable", "R8",
        portfolio(_tranche=["backlog"],
                  charte={"livrables": [{"id": "D1"}]}, methodologie={"drapeau_agile": True}),
        "ecart", "attendu et manquant")

print("C1 — fermeture transitive des dépendances")
from pmlib import fermeture_transitive
_ft = fermeture_transitive(["risques"])
_att = {"risques", "plan", "charte", "methodologie", "contexte"}
_ok = _ft == _att
print(f"  [{'ok  ' if _ok else 'ECHEC'}] déclarer 'risques' entraîne {sorted(_att)}")
if not _ok:
    ECHECS.append("fermeture transitive")
    print(f"         obtenu {sorted(_ft)}")

print("Règles hors périmètre (correction C2)")
verifie("R2 sans budget -> non applicable avec motif", "R2",
        portfolio(plan={"lots": []}), "non_applicable")

print("Dérogations (correction C6)")
verifie("dérogation refusée sur une règle qui n'en admet pas", "R5",
        portfolio(parties_prenantes={"raci": [{"livrable": "D1", "a": "PP1", "r": ["PP2"]}],
                                     "derogations": [{"regle": "R5", "element": "D1", "motif": "parce que"}]}),
        "ecart", "n'admet pas de dérogation")

print("G1 — plans d'atténuation et de secours (criticité ≥ 15)")
verifie("criticité ≥ 15 sans plans", "G1",
        portfolio(risques={"registre": [{"id": "R-01", "p": 3, "i": 5}]}),
        "ecart", "manquant")
verifie("criticité ≥ 15 avec plans", "G1",
        portfolio(risques={"registre": [{"id": "R-01", "p": 3, "i": 5,
                                         "attenuation": "...", "plan_de_secours": "..."}]}),
        "conforme")
verifie("criticité < 15 sans plans -> hors périmètre de la porte", "G1",
        portfolio(risques={"registre": [{"id": "R-01", "p": 2, "i": 3}]}),
        "conforme")

print("G2 — critères SMART")
verifie("critère T manquant", "G2",
        portfolio(charte={"objectifs_smart": [{"id": "O1",
                                                "smart": {"s": "x", "m": "x", "a": "x", "r": "x"}}]}),
        "ecart", "T")
verifie("cinq critères renseignés", "G2",
        portfolio(charte={"objectifs_smart": [{"id": "O1",
                                                "smart": {"s": "x", "m": "x", "a": "x", "r": "x", "t": "x"}}]}),
        "conforme")

print("G3 — critère de succès par livrable")
verifie("livrable sans critère de succès", "G3",
        portfolio(charte={"livrables": [{"id": "D1"}]}),
        "ecart", "aucun critère")
verifie("livrable avec critère de succès", "G3",
        portfolio(charte={"livrables": [{"id": "D1", "critere_succes": "mesurable"}]}),
        "conforme")

print("G4 — grille méthodologique")
verifie("moins de 5 critères motivés", "G4",
        portfolio(methodologie={"criteres": [{"id": "C1", "constat": "x", "pousse_vers": "agile"}],
                                "alternatives_ecartees": [{"nom": "x", "motif": "x"}]}),
        "ecart", "critère")
verifie("aucune alternative motivée", "G4",
        portfolio(methodologie={"criteres": [{"id": f"C{i}", "constat": "x", "pousse_vers": "agile"}
                                             for i in range(5)],
                                "alternatives_ecartees": [{"nom": "x"}]}),
        "ecart", "alternative")
verifie("grille conforme", "G4",
        portfolio(methodologie={"criteres": [{"id": f"C{i}", "constat": "x", "pousse_vers": "agile"}
                                             for i in range(5)],
                                "alternatives_ecartees": [{"nom": "x", "motif": "x"}]}),
        "conforme")

print("G5 — lacune bloquante ouverte")
verifie("lacune bloquante ouverte", "G5",
        portfolio(contexte={"lacunes": [{"id": "L1", "gravite": "bloquante", "statut": "ouverte"}]}),
        "ecart", "L1")
verifie("lacune bloquante arbitrée", "G5",
        portfolio(contexte={"lacunes": [{"id": "L1", "gravite": "bloquante", "statut": "arbitree"}]}),
        "conforme")
verifie("lacune mineure ouverte -> hors périmètre de la porte", "G5",
        portfolio(contexte={"lacunes": [{"id": "L1", "gravite": "mineure", "statut": "ouverte"}]}),
        "conforme")

print("R12 — lacune convertie_en_risque tracée")
verifie("conversion annoncée, risque absent", "R12",
        portfolio(contexte={"lacunes": [{"id": "L5", "statut": "convertie_en_risque", "converti_en": "R-07"}]},
                  risques={"registre": [{"id": "R-01"}]}),
        "ecart", "R-07")
verifie("conversion annoncée, risque présent", "R12",
        portfolio(contexte={"lacunes": [{"id": "L5", "statut": "convertie_en_risque", "converti_en": "R-07"}]},
                  risques={"registre": [{"id": "R-07"}]}),
        "conforme")

print("R13 — hypothèse de la charte couverte")
verifie("risque associé absent du registre", "R13",
        portfolio(charte={"hypotheses": [{"id": "H1", "risque_associe": "R-02"}]},
                  risques={"registre": [{"id": "R-01"}]}),
        "ecart", "R-02")
verifie("risque associé présent", "R13",
        portfolio(charte={"hypotheses": [{"id": "H1", "risque_associe": "R-02"}]},
                  risques={"registre": [{"id": "R-02"}]}),
        "conforme")

print()
if ECHECS:
    print(f"{len(ECHECS)} test(s) en échec : {ECHECS}")
    sys.exit(1)
print("Tous les tests passent.")
