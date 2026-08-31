> Genere depuis `risques.yaml` par `render.py`. Ne pas editer ce fichier : toute correction se fait dans le YAML, puis on regenere.

# Registre des risques

## Registre

| # | Risque | Catégorie | Lots couverts | P | I | C | Réponse | Propriétaire | Déclencheur |
|---|---|---|---|---|---|---|---|---|---|
| R-01 | Le devis en ligne, exclu de la v1, est réintroduit en cours de projet | périmètre | — | 4 | 4 | **16** | éviter | PP12 | Demande d'évolution mentionnant le devis en comite de pilotage |
| R-02 | L'ERP n'expose pas les données nécessaires en lecture | technique | 1.3, 2.4, 3.2 | 3 | 5 | **15** | réduire | PP5 | Rapport d'étude 1.3 concluant à l'absence d'interface exploitable |
| R-03 | Le plafond de 400 k EUR est atteint avant la mise en service | budget | — | 3 | 5 | **15** | réduire | PP1 | Consommation au jalon J4 — seuil 70 % *(seuil proposé, **à arbitrer**)* |
| R-04 | L'appel d'offres et la contractualisation dépassent le délai prévu | délai | 1.5, 1.6 | 3 | 5 | **15** | réduire | PP12 | Absence de candidat retenu à J2 moins 4 semaines |
| R-05 | 1,5 ETP interne insuffisant pour l'encadrement et la recette | ressources | 4.2 | 4 | 4 | **16** | réduire | PP5 | Retard de validation sur deux sprints consecutifs — seuil 5 jours ouvres *(seuil proposé, **à arbitrer**)* |
| R-06 | L'organisation n'a pas la maturité agile supposee par la cadence de sprints | organisation | — | 3 | 3 | 9 | réduire | PP12 | Deux revues de sprint sans participation metier |
| R-07 | La part réellement auto-résolvable des appels est trop faible pour atteindre -40 % | métier | — | 3 | 5 | **15** | réduire | PP3 | Résultat du lot 1.2 : part auto-résolvable sous le seuil — seuil 40 % *(seuil proposé, **à arbitrer**)* |
| R-08 | La qualité des données des comptes empeche une reprise propre | données | 4.1 | 3 | 4 | 12 | réduire | PP5 | Taux d'anomalies sur un échantillon de contrôle — seuil 5 % *(seuil proposé, **à arbitrer**)* |
| R-09 | La validation RGPD intervient trop tard et bloque la mise en service | conformité | 4.4 | 2 | 5 | 10 | éviter | PP10 | DPO non saisi avant le jalon J4 |
| R-10 | L'exigence de performance n'est pas tenue par le socle technique | technique | 3.1 | 3 | 4 | 12 | réduire | PP7 | Mesure en recette de sprint au-delà du seuil de performance — seuil 2 s *(seuil proposé, **à arbitrer**)* |
| R-11 | Le panel de clients pilotes ne se constitue pas ou se démobilise | externe | — | 4 | 3 | 12 | réduire | PP2 | Moins de 5 pilotes actifs après deux sprints |
| R-12 | La concentration des approbations sur le responsable IT créé un goulot | organisation | — | 3 | 4 | 12 | réduire | PP12 | Délai moyen d'approbation — seuil 5 jours ouvres *(seuil proposé, **à arbitrer**)* |
| R-13 | L'échéance du 31/12/2027, adossée au pic commercial, n'a aucune fenêtre de report | délai | 4.4 | 4 | 5 | **20** | réduire | PP1 | Marge du chemin critique au jalon J4 — seuil 4 semaines *(seuil proposé, **à arbitrer**)* |
| R-14 | La complexite fonctionnelle du catalogue et des règles de commande B2B est sous-estimée | technique | 3.3, 3.6 | 4 | 4 | **16** | réduire | PP7 | Dépassement de l'estimation sur le lot 3.3 — seuil 30 % *(seuil proposé, **à arbitrer**)* |

## Plans d'atténuation — criticité ≥ 15

| # | Atténuation | Plan de secours |
|---|---|---|
| R-01 |  |  |
| R-02 |  |  |
| R-03 |  |  |
| R-04 |  |  |
| R-05 |  |  |
| R-07 |  |  |
| R-13 |  |  |
| R-14 |  |  |
