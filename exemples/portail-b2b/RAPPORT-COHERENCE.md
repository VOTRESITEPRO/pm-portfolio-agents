# Rapport de cohérence inter-artefacts

Généré le 02/09/2026 à 09:08 par `validate.py` (contrôle déterministe, sans intervention d'un modèle de langage).

**Artefacts présents** : charte, contexte, methodologie, parties-prenantes, plan, risques

**Tranche déclarée** : charte, contexte, methodologie, parties-prenantes, plan, risques



## Verdict : **RETRAVAILLER**

45 écart(s) bloquant(s) · 2 mineur(s) · 4 dérogation(s) accordée(s)

## Exécution des règles et portes

Origine : **standard** (référentiel nommé, non négociable) · **source** (comble un écart entre une spécification déjà écrite du projet et le code) · **choix_architecture** (décision de conception de ce système, pas une règle universelle) · **convention** (format technique).

| Règle | Libellé | État | Origine | Détail |
|---|---|---|---|---|
| R1 | Périmètre de la charte == somme des lots de la WBS | dérogation | standard |  |
| R2 | Somme des postes budgétaires == budget total annoncé | non applicable | standard | hors tranche déclarée : pm-budget-achats |
| R3 | Réserve de contingence justifiée par des risques cotés | non applicable | choix_architecture | hors tranche déclarée : pm-budget-achats |
| R4 | Toute partie prenante présente dans le RACI et le plan de communication | non applicable | standard | hors tranche déclarée : pm-communications |
| R5 | Un seul Accountable par livrable dans le RACI | conforme | standard |  |
| R6 | Chaque critère de succès couvert par un KPI et présent en checklist de clôture | non applicable | standard | hors tranche déclarée : pm-qualite-suivi, pm-equipe-cloture |
| R7 | Chaque tâche du chemin critique couverte par un risque analysé | conforme | standard |  |
| R8 | Chaque livrable de la charte couvert par au moins une story | non applicable | choix_architecture | hors tranche déclarée : pm-backlog-stories — ATTENTION : methodologie.drapeau_agile == True, cet artefact est attendu dès que la tranche s'élargit |
| R9 | Toute valeur chiffrée appartient à une catégorie de valeur déclarée | conforme | choix_architecture |  |
| R10 | Tout rôle propriétaire ou approbateur est pourvu au registre des parties prenantes | **ÉCART** | choix_architecture | 6 écart(s) |
| R11 | Tout total annoncé est recalculé à partir de ses composants | **ÉCART** | choix_architecture | 5 écart(s) |
| R12 | Lacune convertie_en_risque tracée dans le registre des risques | conforme | choix_architecture |  |
| R13 | Hypothèse de la charte couverte par le registre des risques | conforme | choix_architecture |  |
| R14 | Budget total recalculé confronté au budget cadre du contexte | non applicable | source | hors tranche déclarée : pm-budget-achats |
| R15 | Charge cumulée confrontée à la capacité de l'équipe interne | conforme | choix_architecture |  |
| G1 | Plans d'atténuation et de secours pour toute criticité (p × i) ≥ 15 | **ÉCART** | choix_architecture | 8 écart(s) |
| G2 | Les 5 critères SMART sont renseignés pour chaque objectif | conforme | standard |  |
| G3 | Chaque livrable porte un critère de succès non vide | conforme | standard |  |
| G4 | Au moins 5 critères motivés et 1 alternative écartée motivée | conforme | choix_architecture |  |
| G5 | Aucune lacune bloquante au statut ouverte | conforme | choix_architecture |  |
| G6 | Chaque lot portant une durée porte aussi une charge | **ÉCART** | source | 28 écart(s) |
| G7 | La prose d'un artefact contient des caractères accentués (pas de prose 100 % ASCII) | conforme | choix_architecture |  |
| G8 | projet.commanditaire et projet.secteur sont renseignés, ou leur absence est tracée | conforme | choix_architecture |  |

**17 règle(s) sur 23 exécutée(s).** Une règle non applicable l'est par condition déclarée, jamais par absence constatée d'artefact.

## Écarts bloquants

### [R10] Risque R-01 : propriétaire PP12 (Chef de projet) a le statut 'a_nommer' — rôle non pourvu

Dérogation possible si le pourvoi est tracé comme tâche du plan ou comme risque

*Agent responsable de la correction : `pm-parties-prenantes`*

### [R10] Risque R-04 : propriétaire PP12 (Chef de projet) a le statut 'a_nommer' — rôle non pourvu

Dérogation possible si le pourvoi est tracé comme tâche du plan ou comme risque

*Agent responsable de la correction : `pm-parties-prenantes`*

### [R10] Risque R-06 : propriétaire PP12 (Chef de projet) a le statut 'a_nommer' — rôle non pourvu

Dérogation possible si le pourvoi est tracé comme tâche du plan ou comme risque

*Agent responsable de la correction : `pm-parties-prenantes`*

### [R10] Risque R-10 : propriétaire PP7 (Prestataire externe) a le statut 'a_contractualiser' — rôle non pourvu

Dérogation possible si le pourvoi est tracé comme tâche du plan ou comme risque

*Agent responsable de la correction : `pm-parties-prenantes`*

### [R10] Risque R-12 : propriétaire PP12 (Chef de projet) a le statut 'a_nommer' — rôle non pourvu

Dérogation possible si le pourvoi est tracé comme tâche du plan ou comme risque

*Agent responsable de la correction : `pm-parties-prenantes`*

### [R10] Risque R-14 : propriétaire PP7 (Prestataire externe) a le statut 'a_contractualiser' — rôle non pourvu

Dérogation possible si le pourvoi est tracé comme tâche du plan ou comme risque

*Agent responsable de la correction : `pm-parties-prenantes`*

### [R11] Chemin critique, hypothèse basse : 50 annoncé, 52 recalculé

écart de +2 semaines

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [R11] Chemin critique, hypothèse haute : 67 annoncé, 71 recalculé

écart de +4 semaines

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [R11] Échéance intenable en hypothèse haute : marge de -1.6 semaine(s)

fenêtre 69.4 sem. (2026-09-01 -> 2027-12-31) contre un chemin critique de 71 sem. — un levier de réduction est un préalable, pas une précaution

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G1] Risque R-01 (criticité 16) : attenuation, plan_de_secours manquant(s)

p=4, i=4

*Agent responsable de la correction : `pm-risques`*

### [G1] Risque R-02 (criticité 15) : attenuation, plan_de_secours manquant(s)

p=3, i=5

*Agent responsable de la correction : `pm-risques`*

### [G1] Risque R-03 (criticité 15) : attenuation, plan_de_secours manquant(s)

p=3, i=5

*Agent responsable de la correction : `pm-risques`*

### [G1] Risque R-04 (criticité 15) : attenuation, plan_de_secours manquant(s)

p=3, i=5

*Agent responsable de la correction : `pm-risques`*

### [G1] Risque R-05 (criticité 16) : attenuation, plan_de_secours manquant(s)

p=4, i=4

*Agent responsable de la correction : `pm-risques`*

### [G1] Risque R-07 (criticité 15) : attenuation, plan_de_secours manquant(s)

p=3, i=5

*Agent responsable de la correction : `pm-risques`*

### [G1] Risque R-13 (criticité 20) : attenuation, plan_de_secours manquant(s)

p=4, i=5

*Agent responsable de la correction : `pm-risques`*

### [G1] Risque R-14 (criticité 16) : attenuation, plan_de_secours manquant(s)

p=4, i=4

*Agent responsable de la correction : `pm-risques`*

### [G6] Lot 1 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 1.1 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 1.2 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 1.3 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 1.4 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 1.5 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 1.6 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 2 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 2.1 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 2.2 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 2.3 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 2.4 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 3 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 3.1 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 3.2 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 3.3 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 3.4 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 3.5 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 3.6 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 3.7 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 4 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 4.1 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 4.2 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 4.3 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 4.4 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 5 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 5.1 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [G6] Lot 5.2 : durée déclarée sans charge

sans charge, R15 ne peut pas confronter la charge cumulée à la capacité de l'équipe interne

*Agent responsable de la correction : `pm-planificateur-wbs`*

## Écarts mineurs

### [R11] Lot 1 : sous-total 10-14 inférieur à son chemin interne 13-18

Le sous-total suppose un parallélisme que le chemin critique interdit

*Agent responsable de la correction : `pm-planificateur-wbs`*

### [R11] Lot 4 : sous-total 9-13 inférieur à son chemin interne 11-16

Le sous-total suppose un parallélisme que le chemin critique interdit

*Agent responsable de la correction : `pm-planificateur-wbs`*

## Dérogations accordées

Visibles et contestables — une dérogation n'est jamais silencieuse.

| Règle | Élément | Motif | Déclarée dans |
|---|---|---|---|
| R1 | 1.1 | Lot de conduite de projet — cadrage | plan.yaml |
| R1 | 1.5 | Lot de conduite de projet — appel d'offres | plan.yaml |
| R1 | 1.6 | Lot de conduite de projet — contractualisation | plan.yaml |
| R1 | 5.1 | Lot de conduite de projet — support post-mise en service | plan.yaml |

## Renvoi aux agents

Les écarts bloquants sont renvoyés à leur agent auteur :

- `pm-parties-prenantes`
- `pm-planificateur-wbs`
- `pm-risques`
