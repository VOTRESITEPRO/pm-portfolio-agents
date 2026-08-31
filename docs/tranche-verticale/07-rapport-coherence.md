# Agent `verificateur-coherence` — Rapport de cohérence inter-artefacts

**Entrée** : tous les artefacts produits par la tranche verticale
**Principe** : ne réécrit rien. Émet un verdict et renvoie à l'agent auteur.

---

## 1. Exécution des règles de cohérence

| # | Règle | Applicable ? | Résultat |
|---|---|---|---|
| 1 | Périmètre de la charte == somme des lots de la WBS | Oui | **ÉCART E5** (mineur) |
| 2 | Somme des postes budgétaires == budget total | **Non** — `budget-achats` hors tranche | Non exécutée |
| 3 | Réserve de contingence justifiée par des risques cotés | **Non** — idem | Non exécutée |
| 4 | Toute partie prenante présente dans le RACI et le plan de communication | Partiel — `communications` hors tranche | **ÉCART E6** (mineur) |
| 5 | Un seul Accountable par livrable | Oui | Conforme — 8/8 |
| 6 | Chaque critère de succès couvert par un KPI et présent en checklist de clôture | **Non** — `qualite-suivi` et `equipe-cloture` hors tranche | Non exécutée |
| 7 | Chaque tâche du chemin critique couverte par un risque analysé | Oui | Conforme — 11/11 |
| 8 | Si branche agile active : chaque livrable couvert par ≥ 1 story | **Non** — `backlog-stories` hors tranche | Non exécutée |
| 9 | Aucune valeur chiffrée sans source tracée ou marquée [À SOURCER] | Oui | **ÉCART E3, E7** (bloquants) |

**5 règles sur 9 exécutées.** Voir leçon n°2.

---

## 2. Écarts bloquants

### E1 — Erreur de calcul du chemin critique *(agent responsable : `planificateur-wbs`)*

Le cumul des durées des 11 lots du chemin critique ne correspond pas au total annoncé.

| | Annoncé | Recalculé | Écart |
|---|---|---|---|
| Hypothèse basse | 50 sem. | **52 sem.** | +2 |
| Hypothèse haute | 67 sem. | **71 sem.** | +4 |

Détail du recalcul (hypothèse haute) : 1.3 (5) + 1.5 (8) + 1.6 (5) + 2.4 (5) + 3.1 (8) +
3.2 (8) + 3.3 (5) + 3.6 (11) + 4.1 (6) + 4.2 (7) + 4.4 (3) = **71 semaines**.

**Conséquence — la conclusion managériale est fausse.** Fenêtre disponible : ~69 semaines
(01/09/2026 → 31/12/2027).

| | Annoncé | Réel |
|---|---|---|
| Marge en hypothèse haute | 2 semaines | **−2 semaines** |

L'échéance du 31/12/2027 n'est pas « juste tenable » en hypothèse haute : elle est
**dépassée avant même le démarrage**. Le choix d'un levier de réduction du chemin critique
n'est pas une option de précaution, c'est un préalable.

**Effet en cascade** : le déclencheur de R-13 (« marge < 4 semaines au jalon J4 ») est déjà
atteint au T0. Le risque majeur du registre est en réalité un problème avéré, pas un risque.

> **Gravité : bloquante.** C'est l'écart le plus significatif du rapport, et le seul qui
> aurait été invisible à une relecture humaine rapide.

### E3 — Seuils chiffrés non sourcés dans le registre des risques *(agent : `risques`)*

Six déclencheurs reposent sur des seuils qui ne tracent ni vers le contexte, ni vers un arbitrage, et ne portent pas la mention [À SOURCER] :

| Risque | Seuil non sourcé |
|---|---|
| R-03 | « consommation > 70 % au jalon J4 » |
| R-05 | « retard > 5 j. ouvrés sur deux sprints consécutifs » |
| R-07 | « part auto-résolvable < 45 % » |
| R-08 | « taux d'anomalies > 5 % » |
| R-10 | « > 2 s en recette » *(hérite de E7)* |
| R-12 | « délai moyen d'approbation > 5 j. ouvrés » |

Cas le plus problématique : **R-07**. L'objectif O1 vise −40 % d'appels. Un seuil de déclenchement fixé à 45 % de part auto-résolvable est arbitraire — le seuil mathématiquement signifiant est 40 %, en deçà duquel l'objectif devient inatteignable par construction.

### E4 — Propriétaire de risque non pourvu *(agents : `risques` et `charte-objectifs`)*

Quatre risques (R-01, R-04, R-06, R-12) ont pour propriétaire le « chef de projet ». Or la charte indique **« chef de projet : à nommer »**. Un quart du registre est donc sans propriétaire réel, alors que la porte de sortie de `risques` a validé « propriétaire nommé : 14/14 ». La porte a vérifié la présence d'un libellé, pas l'existence de la personne.

### E7 — Exigence de performance non sourcée *(agent : `charte-objectifs`)*

Le critère de succès de D1 fixe un temps de chargement « < 2 s ». Le contexte mentionne seulement que le portail est « jugé lent ». Le seuil de 2 secondes est une valeur générée. Il se propage ensuite dans R-10 et dans les critères d'acceptation à venir.

---

## 3. Écarts mineurs

### E2 — Sous-totaux de la WBS incohérents *(agent : `planificateur-wbs`)*

| Lot | Sous-total annoncé | Chemin interne minimal | Constat |
|---|---|---|---|
| Lot 1 | 10-14 sem. | 1.3 → 1.5 → 1.6 = **13-18 sem.** | Sous-total inférieur au chemin interne |
| Lot 4 | 9-13 sem. | 4.1 → 4.2 → 4.4 = **11-16 sem.** | Idem |

Les sous-totaux supposent un parallélisme que la séquence du chemin critique interdit.

### E5 — Lots sans livrable rattaché *(règle 1)*

Les lots 1.1, 1.5, 1.6 et 5.1 ne tracent vers aucun livrable D1-D8. `planificateur-wbs` les à déclarés « lots de conduite de projet », ce qui est méthodologiquement correct — mais la règle 1 ne prévoit pas cette catégorie. **L'écart est dans la règle, pas dans l'artefact.**

### E6 — Parties prenantes hors RACI *(règle 4)*

PP4, PP8 et PP11 sont absentes de la matrice, avec une justification explicite. La règle 4 exige une présence, sans prévoir de dérogation motivée. **L'écart est à nouveau dans la règle.**

---

## 4. Verdict

**RETRAVAILLER** — 4 écarts bloquants (E1, E3, E4, E7).

| Agent | Écarts à traiter |
|---|---|
| `planificateur-wbs` | E1 (bloquant), E2 |
| `risques` | E3 (bloquant), E4 |
| `charte-objectifs` | E7 (bloquant), E4 |

Écarts E5 et E6 : **non renvoyés aux agents**. Ils relèvent d'une correction des règles de cohérence elles-mêmes — escaladés à la conception (voir `99-lecons-conception.md`).

---

### Ce que cette étape démontre

Le vérificateur a fait ce qu'aucune porte de sortie individuelle n'avait fait : additionner. Chaque agent avait validé sa propre porte — `planificateur-wbs` avait même correctement signalé un écart d'échéance — mais aucun n'avait recalculé le total, et la conclusion managériale annoncée (« marge de 2 semaines ») était inversée (marge négative).

C'est l'argument central de l'architecture à deux niveaux : **une porte de sortie vérifie la conformité d'un artefact à son propre format ; elle ne vérifie pas sa vérité.** Il faut un contrôle qui traverse les artefacts, et il faut qu'il soit mécanique — E1 se trouve en refaisant une addition, pas en relisant attentivement.
