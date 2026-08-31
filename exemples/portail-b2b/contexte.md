> Genere depuis `contexte.yaml` par `render.py`. Ne pas editer ce fichier : toute correction se fait dans le YAML, puis on regenere.

# Dossier de contexte

| Champ | Valeur |
|---|---|
| Nom | Refonte du portail client B2B |
| Commanditaire | Direction generale |
| Secteur | Distribution de materiel industriel |
| Description | Portail client de 2016 : consultation des devis, commandes et factures, commande sur catalogue. Juge lent et inutilisable sur mobile.
 |

## Repères chiffrés

| Repère | Valeur |
|---|---|
| effectif | 180 salaries |
| clients | 2400 clients professionnels |
| appels_jour | 60 appels/jour |
| cout_unitaire_appel | **[À SOURCER]** |

## Contraintes

| Contrainte | Valeur |
|---|---|
| budget_plafond | 400000 EUR |
| echeance | 2027-12-31 |
| erp_source_de_verite | True |
| etp_interne | 1.5 ETP |

**Fenêtre calendaire** : 2026-09-01 → 2027-12-31

## Registre des lacunes d'information

Le registre est un livrable, pas une note de travail : il énonce ce que le système refuse de combler par plausibilité.

| # | Lacune | Gravité | Statut | Arbitrage / conversion |
|---|---|---|---|---|
| L1 | Exercice fiscal non defini, echeance non datee | **bloquante** | arbitree | Annee civile. Echeance ferme au 31/12/2027, avant le pic commercial de janvier. |
| L2 | Budget evoque en comite, non vote. Plafond ou cible ? | **bloquante** | arbitree | 400 k EUR = plafond vote, non extensible. |
| L3 | Espace de devis en ligne : dans le perimetre ou non ? | **bloquante** | arbitree | Hors perimetre v1, inscrit en evolution post-mise en service. |
| L4 | Part des 4 personnes IT reellement allouee | degradante | arbitree | 1,5 ETP alloue sur la duree. |
| L5 | Typologie et volumetrie detaillees des 60 appels/jour | degradante | convertie_en_risque | R-07 |
| L6 | Cadre RGPD, DPO identifie ? | mineure | arbitree | DPO externe mandate, a associer au cadrage. |
| L7 | Aucun critere de succes chiffre | **bloquante** | arbitree | Reduction de 40 % des appels auto-resolvables, cible 36 appels/jour. |

**Verdict : AVANCER** — 0 lacune(s) bloquante(s) ouverte(s).
