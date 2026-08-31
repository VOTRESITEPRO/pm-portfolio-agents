# Écarts entre la spécification et l'implémentation

Ce fichier trace ce que `../cartographie-agents-pm.yaml` (v1.1) spécifie et que le code ne vérifie pas encore. Il existe parce que le principe du système — *le code vérifie, pas le modèle* — perd sa valeur dès qu'une porte qualité n'est déclarée que dans un prompt.

Mis à jour le 31/08/2026 · plugin v0.1.0

## 1. Portes de sortie déclarées dans un agent, non vérifiées par code

| Agent | Critère déclare | Vérifie ? | Conséquence |
|---|---|---|---|
| `pm-risques` | Plan d'atténuation et plan de secours pour toute criticité (p x i) >= 15 | **Non** | Un registre peut passer avec des plans vides |
| `pm-risques` | Chaque lacune `convertie_en_risque` existe dans le registre sous l'identifiant annoncé | **Non** | Une conversion peut être annoncée sans être faite |
| `pm-risques` | Chaque hypothèse de la charte portant un `risque_associe` est couverte | **Non** | Idem |
| `pm-charte-objectifs` | Les 5 critères SMART sont renseignes pour chaque objectif | **Non** | Un champ SMART vide passe |
| `pm-charte-objectifs` | Chaque livrable porte un critère de succès non vide | **Non** | — |
| `pm-methodologue` | Au moins 5 critères et 1 alternative écartée | **Non** | — |
| `pm-contexte-projet` | Aucune lacune bloquante au statut `ouverte` | **Non** | La chaîne peut avancer sur un contexte incomplet |

**Ces sept contrôles sont mecaniques et devraient l'être.** Ils ne dépendent d'aucun
jugement : ils comptent des champs et croisent des identifiants. Les laisser dans les prompts revient à faire confiance au modèle pour vérifier sa propre production — exactement ce que l'architecture refuse.

**A faire** : les implémenter comme règles de porte (`scripts/gates/`), distinctes des
règles de cohérence inter-artefacts (`scripts/rules/`). Une porte contrôle un artefact seul ; une règle de cohérence en croise plusieurs.

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

**25 tests**, tous passants (`python3 scripts/test_regles.py`).
