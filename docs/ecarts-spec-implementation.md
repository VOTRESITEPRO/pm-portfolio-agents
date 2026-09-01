# Écarts entre la spécification et l'implémentation

Ce fichier trace ce que `../cartographie-agents-pm.yaml` (v1.1) spécifie et que le code ne vérifie pas encore. Il existe parce que le principe du système — *le code vérifie, pas le modèle* — perd sa valeur dès qu'une porte qualité n'est déclarée que dans un prompt.

Mis à jour le 01/09/2026 (chantier C) · plugin v0.1.0

## 0. Chantier C — généralisation du patron R11 (01/09/2026)

R11 recalcule un total aval (durée du chemin critique) et le confronte à une contrainte
amont fixée indépendamment dans `contexte.yaml` (la fenêtre calendaire). Seul le calendrier
était couvert. État après investigation, par cible :

| Cible | Verdict | Implémenté en |
|---|---|---|
| Budget | Gap réel contre la v1.1 : `budget-achats.porte_qualite.coherence_arithmetique` spécifiait déjà « écart au budget cadre == budget total − budget cadre, recalculé », jamais codé. R2 recalculait le total, sans jamais le confronter au plafond amont (`contexte.contraintes.budget_plafond`). | `rules/R14` |
| Ressources | Absent de la v1.1 — aucune règle, aucun champ. `plan.yaml` ne portait qu'une `duree` calendaire, rien qui mesure l'effort. Extension de schéma décidée cette session : un champ `charge` (personne-semaines) par lot, distinct de `duree`. | `agents-src/pm-planificateur-wbs.md` (schéma + porte de sortie), `gates/G6` (charge déclarée si durée déclarée), `rules/R15` (charge cumulée ≤ etp_interne × fenêtre) |
| Périmètre | Nature différente : `charte.perimetre.exclus` n'est pas un plafond numérique à confronter à un total recalculé, mais une liste à ne pas voir réapparaître en aval. Pas une généralisation du patron R11 — non traité dans ce chantier. | — |

`docs/cartographie-agents-pm.yaml` mis à jour en conséquence (R12-R15 ajoutés à
`regles_de_coherence`, contrôle de charge ajouté à `planificateur-wbs`).

**Gain révélé** : faire tourner `validate.py` sur `exemples/portail-b2b` après G6 fait
passer les écarts bloquants de 17 à 45 — les 28 lots de la WBS de cet exemple n'ont jamais
porté de charge. R15 reste `conforme` sur cet exemple tant que G6 n'est pas corrigé (rien à
confronter sans charge déclarée) ; R14 reste `non_applicable` (`pm-budget-achats` n'existe
pas). Exemple non corrigé, pour la même raison qu'en chantier B : il documente un manque réel.

## 1. Portes de sortie déclarées dans un agent — résolu

Les sept contrôles ci-dessous n'étaient déclarés que dans un prompt. Ils sont maintenant
vérifiés par code, répartis selon le nombre d'artefacts qu'ils lisent :

| Agent | Critère déclaré | Implémenté en |
|---|---|---|
| `pm-risques` | Plan d'atténuation et plan de secours pour toute criticité (p x i) >= 15 | `gates/G1` |
| `pm-charte-objectifs` | Les 5 critères SMART sont renseignés pour chaque objectif | `gates/G2` |
| `pm-charte-objectifs` | Chaque livrable porte un critère de succès non vide | `gates/G3` |
| `pm-methodologue` | Au moins 5 critères et 1 alternative écartée | `gates/G4` |
| `pm-contexte-projet` | Aucune lacune bloquante au statut `ouverte` | `gates/G5` |
| `pm-risques` | Chaque lacune `convertie_en_risque` existe dans le registre sous l'identifiant annoncé | `rules/R12` |
| `pm-risques` | Chaque hypothèse de la charte portant un `risque_associe` est couverte | `rules/R13` |

**Reclassement note** : la doc initiale rangeait les sept comme « portes », au motif que le
code vérifie ce qu'un prompt se contentait de déclarer. Mais G1-G5 lisent un seul artefact
(`risques` seul, `charte` seule, `methodologie` seule, `contexte` seul) alors que les deux
derniers croisent deux artefacts (`contexte`+`risques`, `charte`+`risques`) : ce sont des
règles de cohérence par construction (`rules/`), pas des portes (`gates/`), au sens même où
ce fichier définissait la distinction. D'où R12/R13 plutôt que G6/G7.

`scripts/gates/` est un nouveau paquet, même interface que `scripts/rules/` (`ID`,
`LIBELLE`, `REQUIERT`, `DEROGATION_ADMISE`, `verifier(pf)`). `validate.py` charge et évalue
les deux via `charger_regles() + charger_portes()` — aucun changement à `hook.py`.

**Gain révélé** : faire tourner `validate.py` sur `exemples/portail-b2b` après l'ajout de
G1 fait apparaître 8 écarts bloquants qui n'existaient pas avant — les risques de criticité
≥ 15 de cet exemple n'ont jamais porté `attenuation`/`plan_de_secours`. Le registre passait
depuis le début sans ces plans ; seule l'absence de porte le masquait. L'exemple de
référence n'a pas été corrigé : il documente maintenant un vrai manque, pas un défaut
volontaire.

## 2. Règles de cohérence implémentées mais non testables en l'état

| Règle | Statut | Motif |
|---|---|---|
| R2, R3 | Implémentées, jamais exécutées | `pm-budget-achats` n'existe pas encore |
| R4 | Implémentée, jamais exécutée | `pm-communications` n'existe pas encore |
| R6 | Implémentée, jamais exécutée | `pm-qualite-suivi` et `pm-equipe-cloture` n'existent pas |
| R8 | Implémentée, exécutée à vide | `pm-backlog-stories` n'existe pas encore |

Le code de ces règles est ecrit et lisible, mais **aucun test ne le couvre** faute de données réalistes. Il est donc à considérer comme non éprouvé.

## 3. Éléments de la cartographie sans équivalent dans le code

| Élément spécifie | État |
|---|---|
| `max_rework` par agent (2 ou 3 selon l'agent) | Énoncé dans les prompts, **non compte** par le système |
| Verdict `escalader` après épuisement des boucles | Repose sur la discipline de l'agent |
| Agents `orchestrateur-pm` et `auditeur-curriculum` | Non implémentés — le skill `pm-portfolio` tient lieu d'orchestration |
| Matrice de traçabilité compétence Google PM Cert -> artefact | Non implémentée (rôle de `auditeur-curriculum`) |
| Catégorie de valeur : jugement sur un statut usurpé | Non automatisable — confie à `pm-verificateur-coherence` |

## 4. Portabilité non vérifiée

| Point | État |
|---|---|
| Exécution des hooks dans Cowork | **Non vérifie** — la doc indique le même schéma, sans confirmation pratique |
| Invocation `python3` sous Windows | **Non vérifie** — `python` peut être requis. A tester à l'installation |
| Absence de `${CLAUDE_PROJECT_DIR}`, d'injection dynamique et de référence `@fichier` | Vérifie par construction (build des agents) |

## 5. Ce qui EST vérifie par code, et teste

| Règle | Contrôle | Tests |
|---|---|---|
| R1 | Couverture livrable -> lot, lots de conduite, dérogations | 3 |
| R5 | Un seul Accountable, au moins un Responsible | 3 |
| R7 | Chaque lot du chemin critique couvert par un risque | 1 |
| R9 | Catégories de valeur, statuts, `a_sourcer` sans valeur | 4 |
| R10 | Proprietaire pourvu, référence et non libellé libre | 3 |
| R11 | Recalcul des totaux, sous-totaux, marge calendaire, lots inexistants | 4 |
| R8 / C1 | Applicabilité conditionnelle, tranche, fermeture transitive | 5 |
| C2 | Distinction non-applicable / écart | 1 |
| C6 | Dérogation refusée sur une règle qui n'en admet pas | 1 |
| R12 | Lacune `convertie_en_risque` tracée dans le registre des risques | 2 |
| R13 | Hypothèse de la charte couverte par le registre des risques | 2 |
| R14 | Budget total recalculé confronté au budget cadre du contexte | 3 |
| R15 | Charge cumulée confrontée à la capacité de l'équipe interne | 3 |
| G1 | Plans d'atténuation/de secours pour criticité ≥ 15 | 3 |
| G2 | Cinq critères SMART renseignés | 2 |
| G3 | Critère de succès non vide par livrable | 2 |
| G4 | ≥ 5 critères motivés et ≥ 1 alternative écartée motivée | 3 |
| G5 | Aucune lacune bloquante au statut `ouverte` | 3 |
| G6 | Chaque lot déclarant une durée déclare aussi une charge | 3 |

**51 tests**, tous passants (`python3 scripts/test_regles.py`). 15 règles + 6 portes chargées
(`python3 scripts/preflight.py`).
