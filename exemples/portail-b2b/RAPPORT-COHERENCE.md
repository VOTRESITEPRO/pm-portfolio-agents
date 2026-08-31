# Rapport de coherence inter-artefacts

Genere le 31/08/2026 a 10:36 par `validate.py` (controle deterministe, sans intervention d'un modele de langage).

**Artefacts presents** : charte, contexte, methodologie, parties-prenantes, plan, risques

**Tranche declaree** : charte, contexte, methodologie, parties-prenantes, plan, risques



## Verdict : **RETRAVAILLER**

9 ecart(s) bloquant(s) · 2 mineur(s) · 4 derogation(s) accordee(s)

## Execution des regles

| Regle | Libelle | Etat | Detail |
|---|---|---|---|
| R1 | Perimetre de la charte == somme des lots de la WBS | derogation |  |
| R2 | Somme des postes budgetaires == budget total annonce | non applicable | hors tranche declaree : pm-budget-achats |
| R3 | Reserve de contingence justifiee par des risques cotes | non applicable | hors tranche declaree : pm-budget-achats |
| R4 | Toute partie prenante presente dans le RACI et le plan de communication | non applicable | hors tranche declaree : pm-communications |
| R5 | Un seul Accountable par livrable dans le RACI | conforme |  |
| R6 | Chaque critere de succes couvert par un KPI et present en checklist de cloture | non applicable | hors tranche declaree : pm-qualite-suivi, pm-equipe-cloture |
| R7 | Chaque tache du chemin critique couverte par un risque analyse | conforme |  |
| R8 | Chaque livrable de la charte couvert par au moins une story | non applicable | hors tranche declaree : pm-backlog-stories — ATTENTION : methodologie.drapeau_agile == True, cet artefact est attendu des que la tranche s'elargit |
| R9 | Toute valeur chiffree appartient a une categorie de valeur declaree | conforme |  |
| R10 | Tout role proprietaire ou approbateur est pourvu au registre des parties prenantes | **ECART** | 6 ecart(s) |
| R11 | Tout total annonce est recalcule a partir de ses composants | **ECART** | 5 ecart(s) |

**6 regle(s) sur 11 executee(s).** Une regle non applicable l'est par condition declaree, jamais par absence constatee d'artefact.

## Ecarts bloquants

### [R10] Risque R-01 : proprietaire PP12 (Chef de projet) a le statut 'a_nommer' — role non pourvu

Derogation possible si le pourvoi est trace comme tache du plan ou comme risque

*Agent responsable de la correction : `pm-parties-prenantes`*

### [R10] Risque R-04 : proprietaire PP12 (Chef de projet) a le statut 'a_nommer' — role non pourvu

Derogation possible si le pourvoi est trace comme tache du plan ou comme risque

*Agent responsable de la correction : `pm-parties-prenantes`*

### [R10] Risque R-06 : proprietaire PP12 (Chef de projet) a le statut 'a_nommer' — role non pourvu

Derogation possible si le pourvoi est trace comme tache du plan ou comme risque

*Agent responsable de la correction : `pm-parties-prenantes`*

### [R10] Risque R-10 : proprietaire PP7 (Prestataire externe) a le statut 'a_contractualiser' — role non pourvu

Derogation possible si le pourvoi est trace comme tache du plan ou comme risque

*Agent responsable de la correction : `pm-parties-prenantes`*

### [R10] Risque R-12 : proprietaire PP12 (Chef de projet) a le statut 'a_nommer' — role non pourvu

Derogation possible si le pourvoi est trace comme tache du plan ou comme risque

*Agent responsable de la correction : `pm-parties-prenantes`*

### [R10] Risque R-14 : proprietaire PP7 (Prestataire externe) a le statut 'a_contractualiser' — role non pourvu

Derogation possible si le pourvoi est trace comme tache du plan ou comme risque

*Agent responsable de la correction : `pm-parties-prenantes`*

### [R11] Chemin critique, hypothese basse : 50 annonce, 52 recalcule

ecart de +2 semaines

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [R11] Chemin critique, hypothese haute : 67 annonce, 71 recalcule

ecart de +4 semaines

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [R11] Echeance intenable en hypothese haute : marge de -1.6 semaine(s)

fenetre 69.4 sem. (2026-09-01 -> 2027-12-31) contre un chemin critique de 71 sem. — un levier de reduction est un prealable, pas une precaution

*Agent responsable de la correction : `pm-planificateur-wbs`*

## Ecarts mineurs

### [R11] Lot 1 : sous-total 10-14 inferieur a son chemin interne 13-18

Le sous-total suppose un parallelisme que le chemin critique interdit

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [R11] Lot 4 : sous-total 9-13 inferieur a son chemin interne 11-16

Le sous-total suppose un parallelisme que le chemin critique interdit

*Agent responsable de la correction : `pm-planificateur-wbs`*

## Derogations accordees

Visibles et contestables — une derogation n'est jamais silencieuse.

| Regle | Element | Motif | Declaree dans |
|---|---|---|---|
| R1 | 1.1 | Lot de conduite de projet — cadrage | plan.yaml |
| R1 | 1.5 | Lot de conduite de projet — appel d'offres | plan.yaml |
| R1 | 1.6 | Lot de conduite de projet — contractualisation | plan.yaml |
| R1 | 5.1 | Lot de conduite de projet — support post-mise en service | plan.yaml |

## Renvoi aux agents

Les ecarts bloquants sont renvoyes a leur agent auteur :

- `pm-parties-prenantes`
- `pm-planificateur-wbs`
