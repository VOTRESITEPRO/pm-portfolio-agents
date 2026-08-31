# Ecarts entre la specification et l'implementation

Ce fichier trace ce que `../cartographie-agents-pm.yaml` (v1.1) specifie et que le code
ne verifie pas encore. Il existe parce que le principe du systeme — *le code verifie, pas
le modele* — perd sa valeur des qu'une porte qualite n'est declaree que dans un prompt.

Mis a jour le 31/08/2026 · plugin v0.1.0

## 1. Portes de sortie declarees dans un agent, non verifiees par code

| Agent | Critere declare | Verifie ? | Consequence |
|---|---|---|---|
| `pm-risques` | Plan d'attenuation et plan de secours pour toute criticite (p x i) >= 15 | **Non** | Un registre peut passer avec des plans vides |
| `pm-risques` | Chaque lacune `convertie_en_risque` existe dans le registre sous l'identifiant annonce | **Non** | Une conversion peut etre annoncee sans etre faite |
| `pm-risques` | Chaque hypothese de la charte portant un `risque_associe` est couverte | **Non** | Idem |
| `pm-charte-objectifs` | Les 5 criteres SMART sont renseignes pour chaque objectif | **Non** | Un champ SMART vide passe |
| `pm-charte-objectifs` | Chaque livrable porte un critere de succes non vide | **Non** | — |
| `pm-methodologue` | Au moins 5 criteres et 1 alternative ecartee | **Non** | — |
| `pm-contexte-projet` | Aucune lacune bloquante au statut `ouverte` | **Non** | La chaine peut avancer sur un contexte incomplet |

**Ces sept controles sont mecaniques et devraient l'etre.** Ils ne dependent d'aucun
jugement : ils comptent des champs et croisent des identifiants. Les laisser dans les
prompts revient a faire confiance au modele pour verifier sa propre production — exactement
ce que l'architecture refuse.

**A faire** : les implementer comme regles de porte (`scripts/gates/`), distinctes des
regles de coherence inter-artefacts (`scripts/rules/`). Une porte controle un artefact seul ;
une regle de coherence en croise plusieurs.

## 2. Regles de coherence implementees mais non testables en l'etat

| Regle | Statut | Motif |
|---|---|---|
| R2, R3 | Implementees, jamais executees | `pm-budget-achats` n'existe pas encore |
| R4 | Implementee, jamais executee | `pm-communications` n'existe pas encore |
| R6 | Implementee, jamais executee | `pm-qualite-suivi` et `pm-equipe-cloture` n'existent pas |
| R8 | Implementee, executee a vide | `pm-backlog-stories` n'existe pas encore |

Le code de ces regles est ecrit et lisible, mais **aucun test ne le couvre** faute de
donnees realistes. Il est donc a considerer comme non eprouve.

## 3. Elements de la cartographie sans equivalent dans le code

| Element specifie | Etat |
|---|---|
| `max_rework` par agent (2 ou 3 selon l'agent) | Enonce dans les prompts, **non compte** par le systeme |
| Verdict `escalader` apres epuisement des boucles | Repose sur la discipline de l'agent |
| Agents `orchestrateur-pm` et `auditeur-curriculum` | Non implementes — le skill `pm-portfolio` tient lieu d'orchestration |
| Matrice de tracabilite competence Google PM Cert -> artefact | Non implementee (role de `auditeur-curriculum`) |
| Categorie de valeur : jugement sur un statut usurpe | Non automatisable — confie a `pm-verificateur-coherence` |

## 4. Portabilite non verifiee

| Point | Etat |
|---|---|
| Execution des hooks dans Cowork | **Non verifie** — la doc indique le meme schema, sans confirmation pratique |
| Invocation `python3` sous Windows | **Non verifie** — `python` peut etre requis. A tester a l'installation |
| Absence de `${CLAUDE_PROJECT_DIR}`, d'injection dynamique et de reference `@fichier` | Verifie par construction (build des agents) |

## 5. Ce qui EST verifie par code, et teste

| Regle | Controle | Tests |
|---|---|---|
| R1 | Couverture livrable -> lot, lots de conduite, derogations | 3 |
| R5 | Un seul Accountable, au moins un Responsible | 3 |
| R7 | Chaque lot du chemin critique couvert par un risque | 1 |
| R9 | Categories de valeur, statuts, `a_sourcer` sans valeur | 4 |
| R10 | Proprietaire pourvu, reference et non libelle libre | 3 |
| R11 | Recalcul des totaux, sous-totaux, marge calendaire, lots inexistants | 4 |
| R8 / C1 | Applicabilite conditionnelle, tranche, fermeture transitive | 5 |
| C2 | Distinction non-applicable / ecart | 1 |
| C6 | Derogation refusee sur une regle qui n'en admet pas | 1 |

**25 tests**, tous passants (`python3 scripts/test_regles.py`).
