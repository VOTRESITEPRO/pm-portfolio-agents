> Généré depuis `contexte.yaml` par `render.py`. Ne pas éditer ce fichier : toute correction se fait dans le YAML, puis on régénère.

# Dossier de contexte

| Champ | Valeur |
|---|---|
| Nom | Refonte du portail client B2B |
| Commanditaire | Direction générale |
| Secteur | Distribution de matériel industriel |
| Description | Portail client de 2016 : consultation des devis, commandes et factures, commande sur catalogue. Juge lent et inutilisable sur mobile. |

## Repères chiffrés

| Repère | Valeur |
|---|---|
| Effectif | 180 salaries |
| Clients | 2400 clients professionnels |
| Appels par jour | 60 appels/jour |
| Coût unitaire d'un appel | **[À SOURCER]** |

## Contraintes

| Contrainte | Valeur |
|---|---|
| Budget plafond | 400000 EUR |
| Échéance | 2027-12-31 |
| ERP source de vérité | True |
| ETP interne | 1.5 ETP |

**Fenêtre calendaire** : 2026-09-01 → 2027-12-31

## Registre des lacunes d'information

Le registre est un livrable, pas une note de travail : il énonce ce que le système refuse de combler par plausibilité.

| # | Lacune | Gravité | Statut | Arbitrage / conversion |
|---|---|---|---|---|
| L1 | Exercice fiscal non defini, échéance non datee | **bloquante** | arbitrée | Année civile. Échéance ferme au 31/12/2027, avant le pic commercial de janvier. |
| L2 | Budget evoque en comité, non voté. Plafond ou cible ? | **bloquante** | arbitrée | 400 k EUR = plafond voté, non extensible. |
| L3 | Espace de devis en ligne : dans le périmètre ou non ? | **bloquante** | arbitrée | Hors périmètre v1, inscrit en évolution post-mise en service. |
| L4 | Part des 4 personnes IT réellement allouee | dégradante | arbitrée | 1,5 ETP alloue sur la durée. |
| L5 | Typologie et volumétrie detaillees des 60 appels/jour | dégradante | convertie en risque | R-07 |
| L6 | Cadre RGPD, DPO identifie ? | mineure | arbitrée | DPO externe mandate, à associer au cadrage. |
| L7 | Aucun critère de succès chiffré | **bloquante** | arbitrée | Réduction de 40 % des appels auto-résolvables, cible 36 appels/jour. |

**Verdict : AVANCER** — 0 lacune(s) bloquante(s) ouverte(s).
