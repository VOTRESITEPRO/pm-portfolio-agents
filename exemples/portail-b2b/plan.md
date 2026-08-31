> Genere depuis `plan.yaml` par `render.py`. Ne pas editer ce fichier : toute correction se fait dans le YAML, puis on regenere.

# Plan de projet, jalons et chemin critique

> Fourchettes non empiriques. Aucune donnee de velocite ni d'historique projet. Support d'atelier d'estimation, jamais un engagement.


## Work breakdown structure

| Lot | Intitulé | Livrables | Durée |
|---|---|---|---|
| 1 | Cadrage et contractualisation | *conduite* | 10-14 sem. |
| &nbsp;&nbsp;&nbsp;&nbsp;1.1 | Cadrage detaille et validation du perimetre | *conduite* | 3-4 sem. |
| &nbsp;&nbsp;&nbsp;&nbsp;1.2 | Analyse de la volumetrie et typologie des appels | D8 | 3-4 sem. |
| &nbsp;&nbsp;&nbsp;&nbsp;1.3 | Etude d'exposition des donnees ERP | D6 | 4-5 sem. |
| &nbsp;&nbsp;&nbsp;&nbsp;1.4 | Mesure de la base de depart | D8 | 2-3 sem. |
| &nbsp;&nbsp;&nbsp;&nbsp;1.5 | Appel d'offres et selection du prestataire | *conduite* | 6-8 sem. |
| &nbsp;&nbsp;&nbsp;&nbsp;1.6 | Contractualisation | *conduite* | 3-5 sem. |
| 2 | Conception | *conduite* | 8-11 sem. |
| &nbsp;&nbsp;&nbsp;&nbsp;2.1 | Identification des parcours auto-resolvables | D1, D2, D3, D4 | 3-4 sem. |
| &nbsp;&nbsp;&nbsp;&nbsp;2.2 | Architecture d'information et parcours cibles | D1, D2, D3, D4 | 4-5 sem. |
| &nbsp;&nbsp;&nbsp;&nbsp;2.3 | Design system responsive | D5 | 4-6 sem. |
| &nbsp;&nbsp;&nbsp;&nbsp;2.4 | Architecture technique et interface ERP | D6 | 4-5 sem. |
| 3 | Realisation iterative | *conduite* | 26-34 sem. |
| &nbsp;&nbsp;&nbsp;&nbsp;3.1 | Socle technique, authentification, performance | D5 | 6-8 sem. |
| &nbsp;&nbsp;&nbsp;&nbsp;3.2 | Interface ERP en lecture | D6 | 6-8 sem. |
| &nbsp;&nbsp;&nbsp;&nbsp;3.3 | Parcours consultation des devis | D1 | 4-5 sem. |
| &nbsp;&nbsp;&nbsp;&nbsp;3.4 | Parcours consultation des commandes | D2 | 4-5 sem. |
| &nbsp;&nbsp;&nbsp;&nbsp;3.5 | Parcours consultation des factures | D3 | 3-4 sem. |
| &nbsp;&nbsp;&nbsp;&nbsp;3.6 | Parcours de commande sur catalogue | D4 | 8-11 sem. |
| &nbsp;&nbsp;&nbsp;&nbsp;3.7 | Conformite responsive (transverse) | D5 | 0-0 sem. |
| 4 | Reprise et bascule | *conduite* | 9-13 sem. |
| &nbsp;&nbsp;&nbsp;&nbsp;4.1 | Reprise des comptes clients | D7 | 4-6 sem. |
| &nbsp;&nbsp;&nbsp;&nbsp;4.2 | Recette fonctionnelle et UAT | D1, D2, D3, D4, D5, D6, D7 | 5-7 sem. |
| &nbsp;&nbsp;&nbsp;&nbsp;4.3 | Validation de conformite RGPD | D3, D7 | 2-3 sem. |
| &nbsp;&nbsp;&nbsp;&nbsp;4.4 | Mise en service et bascule | D1, D2, D3, D4, D5, D6, D7 | 2-3 sem. |
| 5 | Post-mise en service | *conduite* | 12-12 sem. |
| &nbsp;&nbsp;&nbsp;&nbsp;5.1 | Support renforce (hypercare) | *conduite* | 6-6 sem. |
| &nbsp;&nbsp;&nbsp;&nbsp;5.2 | Mesure de O1 et O2 | D8 | 12-12 sem. |

## Chemin critique

1.3 → 1.5 → 1.6 → 2.4 → 3.1 → 3.2 → 3.3 → 3.6 → 4.1 → 4.2 → 4.4

Durée : **50 semaines à 67 semaines**

> Les totaux sont recalculés par le validateur à partir des durées de lots. Voir `RAPPORT-COHERENCE.md`.

## Jalons

| # | Jalon | Cible | Nature |
|---|---|---|---|
| J1 | Perimetre valide et base de mesure etablie | 2026-12-31 | interne |
| J2 | Prestataire contractualise | 2027-03-31 | **contractuel** |
| J3 | Conception validee, architecture ERP arretee | 2027-06-30 | **contractuel** |
| J4 | Parcours de consultation en production | 2027-09-30 | **contractuel** |
| J5 | Parcours de commande en production | 2027-12-31 | **contractuel** |
| J6 | Mise en service complete | 2027-12-31 | **contractuel** |
| J7 | Mesure des objectifs O1 et O2 | 2028-03-31 | interne |

## Dérogations déclarées

Visibles et contestables — une dérogation n'est jamais silencieuse.

| Règle | Élément | Motif |
|---|---|---|
| R1 | 1.1 | Lot de conduite de projet — cadrage |
| R1 | 1.5 | Lot de conduite de projet — appel d'offres |
| R1 | 1.6 | Lot de conduite de projet — contractualisation |
| R1 | 5.1 | Lot de conduite de projet — support post-mise en service |
