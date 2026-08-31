> Genere depuis `parties-prenantes.yaml` par `render.py`. Ne pas editer ce fichier : toute correction se fait dans le YAML, puis on regenere.

# Parties prenantes et matrice RACI

## Registre

| # | Nom | Rôle | Pouvoir | Intérêt | Statut |
|---|---|---|---|---|---|
| PP1 | Direction generale | Sponsor, arbitrage budgetaire | eleve | moyen | confirme |
| PP2 | Direction commerciale | Demandeur du devis en ligne | eleve | eleve | confirme |
| PP3 | Responsable service client | Beneficiaire de O1 | moyen | eleve | confirme |
| PP4 | Conseillers service client | Source de la donnee d'appels | faible | eleve | confirme |
| PP5 | Responsable IT | Garant de l'integration ERP | eleve | eleve | confirme |
| PP6 | Equipe IT | Realisation et recette internes | moyen | eleve | confirme |
| PP7 | Prestataire externe | Realisation | moyen | moyen | **a_contractualiser** |
| PP8 | Clients professionnels | Utilisateurs finaux | faible | eleve | confirme |
| PP9 | Clients pilotes | Validation iterative | faible | eleve | **a_constituer** |
| PP10 | DPO externe | Conformite RGPD | moyen | faible | confirme |
| PP11 | Direction administrative et financiere | Suivi budgetaire | eleve | faible | **a_confirmer** |
| PP12 | Chef de projet | Pilotage | moyen | eleve | **a_nommer** |

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
| R4 | PP4 | Consultes comme source de donnee, non responsables d'un livrable. Rattaches a PP3. |
| R4 | PP8 | Destinataires finaux, non responsables. Representes par PP9. |
| R4 | PP11 | Hors chaine de production des livrables ; intervient au suivi budgetaire, trace au plan de communication. |
