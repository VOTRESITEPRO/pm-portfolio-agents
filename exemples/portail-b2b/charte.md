> Genere depuis `charte.yaml` par `render.py`. Ne pas editer ce fichier : toute correction se fait dans le YAML, puis on regenere.

# Charte de projet

| Rôle | Référence | Statut |
|---|---|---|
| Chef de projet | PP12 | a_nommer |

## Objectifs SMART

### O1

> Reduire de 40 % le volume d'appels entrants auto-resolvables, de 60 a 36 appels/jour en moyenne mensuelle, mesure au 31/03/2028.

Cible : 36 appels/jour

| Critère | Vérification |
|---|---|
| S | volume d'appels entrants |
| M | source : outil de telephonie |
| A | sous reserve de R-07 |
| R | coherent budget/echeance |
| T | 31/03/2028 |

### O2

> Atteindre 30 % de sessions mobile/tablette au 31/03/2028, la base de depart etant mesuree au lot 1.4.

Cible : 30 % *(seuil proposé, **à arbitrer**)*

| Critère | Vérification |
|---|---|
| S | part de sessions mobile |
| M | analytics, base mesuree au lot 1.4 |
| A | conditionnel a la base |
| R | a confirmer |
| T | 31/03/2028 |

### O3

> Mettre en service le portail refondu au plus tard le 31/12/2027, parcours de consultation et de commande operationnels et alimentes par l'ERP.

| Critère | Vérification |
|---|---|
| S | parcours nommes |
| M | en production oui/non |
| A | sous reserve des estimations |
| R | sous reserve du plafond |
| T | 31/12/2027 |

## Périmètre

### Inclus

- Parcours de consultation : devis, commandes, factures
- Parcours de commande sur catalogue
- Conception responsive mobile et tablette
- Interfacage ERP en lecture
- Reprise des comptes clients existants
- Instrumentation analytique

### Exclus explicitement

- Espace de devis en ligne (arbitrage L3, evolution post-mise en service)
- Modification de l'ERP
- Refonte du catalogue produit
- Application mobile native
- Demarche d'amelioration continue du process de service client
- Migration du systeme de facturation

> La section « exclus » est aussi contraignante que la section « inclus ». C'est le premier rempart contre le scope creep.

## Livrables et critères de succès

| # | Livrable | Critère de succès |
|---|---|---|
| D1 | Parcours de consultation des devis | consultation sans appel ; chargement sous le seuil de performance retenu |
| D2 | Parcours de consultation des commandes | statut a jour depuis l'ERP |
| D3 | Parcours de consultation des factures | telechargement PDF operationnel |
| D4 | Parcours de commande sur catalogue | commande arrivee complete dans l'ERP sans ressaisie |
| D5 | Socle responsive | tous les parcours passent les criteres d'acceptation mobile |
| D6 | Interface ERP | aucune divergence sur un echantillon de controle |
| D7 | Reprise des comptes clients | 100 % des comptes actifs migres et fonctionnels |
| D8 | Dispositif de mesure | O1 et O2 mesurables des la mise en service |

## Hypothèses

| # | Hypothèse | Risque associé |
|---|---|---|
| H1 | Une part significative des appels est auto-resolvable | R-07 |
| H2 | L'ERP expose les donnees necessaires en lecture | R-02 |
| H3 | Un prestataire peut etre contractualise dans les delais | R-04 |
| H4 | 1,5 ETP interne suffit a l'encadrement et a la recette | R-05 |
