> Généré depuis `parties-prenantes.yaml` par `render.py`. Ne pas éditer ce fichier : toute correction se fait dans le YAML, puis on régénère.

# Parties prenantes et matrice RACI

## Registre

| # | Nom | Rôle | Pouvoir | Intérêt | Statut |
|---|---|---|---|---|---|
| PP1 | Direction générale | Sponsor, arbitrage budgétaire | eleve | moyen | confirmé |
| PP2 | Direction commerciale | Demandeur du devis en ligne | eleve | eleve | confirmé |
| PP3 | Responsable service client | Bénéficiaire de O1 | moyen | eleve | confirmé |
| PP4 | Conseillers service client | Source de la donnée d'appels | faible | eleve | confirmé |
| PP5 | Responsable IT | Garant de l'intégration ERP | eleve | eleve | confirmé |
| PP6 | Équipe IT | Réalisation et recette internes | moyen | eleve | confirmé |
| PP7 | Prestataire externe | Realisation | moyen | moyen | **à contractualiser** |
| PP8 | Clients professionnels | Utilisateurs finaux | faible | eleve | confirmé |
| PP9 | Clients pilotes | Validation itérative | faible | eleve | **à constituer** |
| PP10 | DPO externe | Conformité RGPD | moyen | faible | confirmé |
| PP11 | Direction administrative et financière | Suivi budgétaire | eleve | faible | **à confirmer** |
| PP12 | Chef de projet | Pilotage | moyen | eleve | **à nommer** |

## Matrice RACI

| Livrable | A (approuve) | R (réalise) | C (consulté) | I (informé) |
|---|---|---|---|---|
| D1 | **PP5** | PP6, PP7 | PP2, PP3, PP9 | PP1, PP10 |
| D2 | **PP5** | PP6, PP7 | PP2, PP3, PP9 | PP1, PP10 |
| D3 | **PP5** | PP6, PP7 | PP3, PP9, PP10 | PP1, PP2 |
| D4 | **PP2** | PP6, PP7 | PP3, PP5, PP9 | PP1, PP10 |
| D5 | **PP5** | PP7 | PP6, PP9 | PP1, PP2 |
| D6 | **PP5** | PP6 | PP7, PP10 | PP1 |
| D7 | **PP5** | PP6 | PP3, PP7, PP10 | PP1 |
| D8 | **PP1** | PP3, PP6 | PP2, PP5, PP7 | PP10 |

## Dérogations déclarées

Visibles et contestables — une dérogation n'est jamais silencieuse.

| Règle | Élément | Motif |
|---|---|---|
| R4 | PP4 | Consultés comme source de donnée, non responsables d'un livrable. Rattaches à PP3. |
| R4 | PP8 | Destinataires finaux, non responsables. Représentés par PP9. |
| R4 | PP11 | Hors chaîne de production des livrables ; intervient au suivi budgétaire, tracé au plan de communication. |
