# Leçons de conception issues de la tranche verticale

> Ce document est le vrai produit de l'exercice. La tranche verticale n'avait pas pour but
> de produire de beaux artefacts : elle avait pour but de **casser la conception** avant
> qu'un recruteur ne le fasse.

**Tranche exécutée** : 7 agents sur 15 — `contexte-projet`, `methodologue`,
`charte-objectifs`, `parties-prenantes`, `planificateur-wbs`, `risques`, `verificateur-coherence`.

---

## Leçon n°1 — `risques` n'est pas démarrable sans `planificateur-wbs`

**Constat.** La tranche était prévue à 6 agents. La porte d'entrée (DoR) de `risques` exige
« plan de projet produit ; chemin critique identifié », et sa porte de sortie exige que chaque tâche du chemin critique soit couverte. Sans WBS, l'agent ne démarre pas.

**Nature.** Ce n'est pas un défaut : c'est une dépendance correctement spécifiée, découverte
par l'usage. Le YAML la déclarait déjà (`risques.depends_on: [planificateur-wbs]`) — c'est le découpage de la tranche qui était faux, pas la cartographie.

**Correction.** Aucune sur le YAML. Note ajoutée : toute tranche d'exécution doit être
définie comme une **fermeture transitive des dépendances**, pas comme un choix d'agents.

---

## Leçon n°2 — Le vérificateur ne peut exécuter que 5 règles sur 9 en tranche partielle

**Constat.** Quatre règles de cohérence portent sur des artefacts absents de la tranche
(budget, KPI, checklist de clôture, backlog). Le vérificateur les à déclarées non exécutées.

**Le vrai problème.** Le YAML ne distingue pas « règle non applicable car l'agent est hors
périmètre » de « règle en échec car l'artefact manque ». Sur une chaîne complète où la branche agile serait désactivée, la règle 8 devrait être ignorée ; sur une chaîne où `backlog-stories` a échoué, elle devrait bloquer. **Le YAML actuel produirait le même résultat dans les deux cas.**

**Correction à apporter.** Ajouter à chaque règle de `verificateur-coherence` un champ
`condition_applicabilite` référençant les agents requis, et distinguer trois états de sortie : `conforme` / `ecart` / `non_applicable`, ce dernier étant justifié par une condition, jamais par une absence constatée.

---

## Leçon n°3 — Une porte de sortie vérifie un format, pas une vérité *(la plus importante)*

**Constat.** `planificateur-wbs` a validé sa porte de sortie et signalé un écart d'échéance
— comportement correct. Mais son calcul de chemin critique était faux (67 au lieu de 71 semaines), et la conclusion managériale s'en trouvait inversée : marge annoncée de 2 semaines, marge réelle de **−2 semaines**.

Aucune porte de sortie individuelle ne pouvait le voir : la porte vérifiait « chemin critique identifié », pas « chemin critique correctement additionné ».

**Ce que ça valide.** L'architecture à deux niveaux de contrôle est justifiée, et par un
argument plus fort que prévu : le second niveau ne sert pas à relire, il sert à **recalculer**.

**Correction à apporter.** Ajouter aux portes de sortie des agents produisant du chiffré
(`planificateur-wbs`, `budget-achats`, `sprint`) un critère de **cohérence arithmétique interne** : tout total annoncé est recalculé à partir de ses composants, et l'écart est rejeté. C'est mécanique, donc fiable — contrairement à une relecture.

---

## Leçon n°4 — La règle « aucune valeur non sourcée » est incompatible avec l'exigence de déclencheur observable

**Constat.** La porte de sortie de `risques` exige un déclencheur observable pour chaque
risque. Un déclencheur observable exige un seuil. Or aucun seuil de gestion n'existe dans le contexte d'entrée. Résultat : **6 des 14 déclencheurs reposent sur des seuils générés** (E3), et le registre à franchi sa porte de sortie sans que rien ne le détecte.

**Nature.** C'est une contradiction entre deux règles de la cartographie, pas une erreur
d'exécution. La règle 9 interdit la valeur non sourcée ; la porte de `risques` en exige une.

**Correction à apporter.** Introduire une **troisième catégorie de valeur**, entre la donnée
sourcée et la valeur interdite :

| Catégorie | Statut | Exemple |
|---|---|---|
| Donnée sourcée | Autorisée | « 60 appels/jour » (contexte) |
| **Seuil de gestion proposé** | **Autorisée si marquée `[SEUIL PROPOSÉ — À ARBITRER]`** | « consommation > 70 % au jalon J4 » |
| Donnée factuelle générée | **Interdite** | « coût unitaire d'un appel : 12 € » |

La distinction est nette : un seuil de gestion est une **proposition de pilotage** qu'un comité arbitre ; une donnée factuelle générée est un **mensonge sur le réel**. Les confondre conduit soit à interdire les déclencheurs (registre inexploitable), soit à laisser passer des chiffrés inventés (registre trompeur).

---

## Leçon n°5 — Une porte de sortie peut valider un champ vide de sens

**Constat.** `risques` a validé « propriétaire nommé : 14/14 ». Quatre de ces propriétaires
sont « le chef de projet », rôle que la charte déclare **à nommer** (E4). La porte a vérifié la présence d'une chaîne de caractères, pas l'existence d'une personne.

**Correction à apporter.** Toute porte exigeant un propriétaire, un responsable ou un
approbateur doit vérifier que le rôle cité est **pourvu dans le registre des parties prenantes**, et non seulement renseigné. C'est une règle de cohérence croisée (`risques` × `parties-prenantes` × `charte-objectifs`), à ajouter au vérificateur.

---

## Leçon n°6 — Deux écarts sur six étaient des défauts de règle, pas d'artefact

**Constat.** E5 (lots de conduite de projet sans livrable) et E6 (parties prenantes hors
RACI avec justification) ont été signalés comme écarts alors que les artefacts étaient méthodologiquement corrects. Les règles 1 et 4 étaient trop strictes.

**Ce que ça révèle.** Un vérificateur mécanique produit des faux positifs. Sans traitement,
ils décrédibilisent le contrôle — et, en usage réel, poussent à désactiver la règle.

**Correction à apporter.** Prévoir dans `verificateur-coherence` un mécanisme de
**dérogation motivée** : un agent peut déclarer une exception explicite et justifiée, que le
vérificateur enregistre au lieu de la rejeter. Les dérogations sont listées dans le rapport, donc visibles et contestables — plutôt que silencieuses.

---

## Synthèse des corrections à porter au YAML

| # | Correction | Cible dans `cartographie-agents-pm.yaml` |
|---|---|---|
| C1 | Fermeture transitive des dépendances pour toute tranche d'exécution | `flux` — note d'usage |
| C2 | Champ `condition_applicabilite` par règle + 3 états de sortie | `verificateur-coherence.regles_de_coherence` |
| C3 | Critère de cohérence arithmétique interne | portes de sortie de `planificateur-wbs`, `budget-achats`, `sprint` |
| C4 | Catégorie « seuil de gestion proposé » | règle 9 + porte de sortie de `risques` |
| C5 | Vérification que tout rôle propriétaire est pourvu | nouvelle règle de cohérence croisée |
| C6 | Mécanisme de dérogation motivée | `verificateur-coherence` |

**Bilan : 6 corrections issues d'une seule tranche verticale de 7 agents sur 15.** Cinq
n'auraient pas été trouvées en relisant la cartographie — elles ne se révèlent qu'en produisant.

---

## Ce que cet exercice permet de dire en entretien

> « J'ai conçu l'architecture, puis je l'ai testée sur un cas avant de la présenter. Le test
> a trouvé six défauts, dont une contradiction entre deux de mes propres règles et une
> erreur de calcul qui inversait la conclusion sur la tenue de l'échéance. C'est
> précisément pour ça que le système a deux niveaux de contrôle, et c'est pour ça que je ne
> présente pas une IA qui produit des livrables, mais une IA qui produit des livrables
> **contrôlables**. »

C'est un discours de gouvernance, pas de démonstration technique — et c'est ce qui distingue un chef de projet qui a compris l'IA d'un utilisateur d'IA.
