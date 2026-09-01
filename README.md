# PM Portfolio Agents

Une orchestration d'agents IA qui génère le portfolio d'artefacts d'un projet — charte, parties prenantes, RACI, WBS, jalons, chemin critique, registre des risques — **sous des portes qualité vérifiées par du code, pas par un modèle de langage**.

Plugin pour [Claude Code](https://code.claude.com) et Cowork.

---

## En clair

On décrit un projet en quelques phrases — objectif, parties prenantes, budget, échéance.
Une chaîne d'agents IA spécialisés se passe ensuite le dossier : chacun rédige un document
(charte, cartographie des parties prenantes, calendrier, registre des risques...) à partir
de ce que les précédents ont écrit, comme une équipe qui se transmettrait le dossier.

Une fois les documents produits, un programme classique — pas un modèle de langage — les
relit et vérifie mécaniquement ce qui est vérifiable : il recalcule les totaux au lieu de
croire ceux annoncés, il vérifie que toute personne citée comme responsable existe bien
dans la liste des parties prenantes, que le budget ne dépasse pas le plafond fixé au
départ. Un écart repart vers l'agent responsable, avec une limite d'allers-retours pour
que ça ne boucle pas indéfiniment.

## Le principe

> Le LLM produit, analyse et qualifie. Le code vérifie, recalcule, compte et trace.

Aucune porte qualité ne dépend du jugement d'un modèle sur sa propre production. C'est la seule règle non négociable du projet, et elle a une conséquence sur le format : chaque artefact est produit en **YAML structuré**, puis rendu en Markdown lisible. Le Markdown est une sortie, jamais la source — un tableau Markdown n'est pas vérifiable mécaniquement.

Les 15 règles de cohérence inter-artefacts et les 6 portes de sortie par artefact sont **entièrement du Python déterministe** — voir [`docs/ecarts-spec-implementation.md`](docs/ecarts-spec-implementation.md) pour le détail. Une part reste hors de portée du calcul et confiée au jugement sémantique de l'agent vérificateur : c'est elle qui a rattrapé le défaut le plus grave rencontré en test (voir plus bas).

## Ce que ça donne concrètement

Deux exemples tirés d'un run réel.

**Le code refuse une catégorie inventée par le modèle.** Contraint par trois catégories de
valeur (`source`, `seuil_propose`, `a_sourcer`), un agent a inventé une quatrième — `hypothese_illustrative` — pour exprimer quelque chose de légitime que le système ne lui permettait pas de dire. Le nom était raisonnable, l'intention honnête, le marquage correct. La règle R9 l'a rejeté parce qu'elle compare à une liste close. L'agent a corrigé.

Un vérificateur IA aurait très probablement accepté.

**Le contrôle arithmétique inverse une conclusion managériale.** La règle R11 recalcule tout
total annoncé à partir de ses composants :

```
[R11] Echeance intenable en hypothese haute : marge de -5.4 semaine(s)
      fenetre 34.6 sem. (2027-01-01 -> 2027-08-31) contre un chemin critique de 40 sem.
      — un levier de reduction est un prealable, pas une precaution
```

En phase de conception, une version de l'agent planificateur avait annoncé un chemin critique de 67 semaines là où il en valait 71. La marge passait de +2 à −2 semaines : l'échéance était dépassée avant le démarrage, et personne ne l'avait vu. **Ce défaut se trouve en refaisant une addition, pas en relisant attentivement.**

## Ce que le système ne décide jamais

Sept décisions, listées et motivées dans la cartographie :

choix de méthodologie · ordonnancement du backlog · validation des chiffres budgétaires · engagement de sprint · engagement vis-à-vis des parties prenantes · évaluation des personnes · cotation finale de l'impact des risques.

Deux d'entre elles sont des règles du Scrum Guide, pas des préférences de conception.

## Démarche

Le dépôt contient autant la conception que le code, parce que la conception est le livrable.

| Étape | Document | Résultat |
|---|---|---|
| 1. Buy vs build | [`docs/benchmark-depots.md`](docs/benchmark-depots.md) | 4 dépôts inspectés sur leur contenu réel. Aucun ne produit d'artefact du référentiel PM : la réutilisation porte sur l'orchestration, pas sur la substance |
| 2. Conception | [`docs/cartographie-agents-pm.yaml`](docs/cartographie-agents-pm.yaml) | 15 agents en 4 couches, portes qualité, hand-offs, points de reprise humaine |
| 3. Test de conception | [`docs/tranche-verticale/`](docs/tranche-verticale/) | 7 agents joués à la main sur un cas neutre — **6 défauts de conception**, dont 5 introuvables en relisant le YAML |
| 4. Implémentation | `agents/` `scripts/` `hooks/` | 7 agents, 15 règles + 6 portes de sortie, 51 tests de non-régression |
| 5. Run réel | [`docs/journal-essai-01.md`](docs/journal-essai-01.md) | Chaîne complète en conditions réelles — **14 comportements conformes, 11 défauts, 3 familles** |
| 6. Limites | [`docs/ecarts-spec-implementation.md`](docs/ecarts-spec-implementation.md) | Ce que la spécification exige et que le code ne vérifie pas encore |
| 7. Raisonnement | [`docs/document-raisonnement.md`](docs/document-raisonnement.md) | Décisions de conception, alternatives écartées, risques du système |

## Les trois familles de défauts

Le run réel n'a pas produit une liste de bugs dispersés. Les 11 défauts se rangent en trois familles, et **aucune ne concerne ce que le système produit** :

**1. Le contrôle vérifie la FORME d'un signal, pas son SENS.**
« Propriétaire nommé » = chaîne non vide, au lieu d'une personne pourvue. Un code de retour à trois valeurs lu comme un booléen. « La lacune porte un arbitrage » = champ non vide, au lieu d'un arbitrage qui répond à la question.

**2. Rien ne confronte une proposition AVAL aux contraintes AMONT.**
Exclure la conduite du changement alors que le critère de succès est le taux d'adoption. Proposer un renfort alors que le plafond budgétaire est ferme. Proposer trois leviers de réduction sans vérifier qu'aucun ne ferme l'écart. R11 est le seul contrôle de cette famille, et il ne couvre que le calendrier.

**3. Le code valide ce que l'humain ne lit pas ; l'humain lit ce que le code ne valide pas.**
Un fichier YAML porte des champs structurés — vérifiés, rarement lus — et de la prose — jamais vérifiée, mais c'est elle qui apparaît dans le rendu Markdown. En test, des leviers étaient marqués `arbitre: false` dans les données et « déjà choisis » dans les commentaires. Un portfolio peut donc passer toutes ses règles en racontant l'inverse.

C'est la part LLM du vérificateur qui a rattrapé ce dernier cas. Aucun contrôle arithmétique ne pouvait le voir.

## Installation

Voir [`INSTALLATION.md`](INSTALLATION.md). Contrôle pré-vol :

    python3 scripts/preflight.py        # ou : py scripts\preflight.py

Le preflight détermine quelle invocation Python fonctionne sur la machine et vérifie que `hooks/hooks.json` utilise bien celle-là. **C'est un point critique et silencieux** : un hook dont la commande échoue ne bloque rien, et les portes qualité ne s'exécutent jamais sans que rien ne le signale. Le dépôt est livré avec `python3` ; sous Windows, où le launcher `py` est souvent le seul à fonctionner :

    py scripts\preflight.py --fix-hooks

Puis :

    claude --plugin-dir /chemin/vers/pm-portfolio-agents

## Commandes

    python3 scripts/validate.py ./pm-portfolio   # portes qualité, code retour 2 si écart bloquant
    python3 scripts/render.py   ./pm-portfolio   # YAML -> Markdown lisible
    python3 scripts/test_regles.py               # 51 tests de non-régression
    python3 scripts/build_agents.py              # agents-src/ + _COMMUN.md -> agents/

## État

**v0.1.0 — incrément 1** : 7 agents sur 15 conçus. Les 8 autres (budget, communications,
qualité, clôture, backlog, sprint, audit de traçabilité, orchestrateur) ne sont pas écrits ; les règles qui en dépendent sont rapportées `non_applicable` avec leur condition, jamais `echec`.

Ce qui reste à faire est listé dans [`docs/ecarts-spec-implementation.md`](docs/ecarts-spec-implementation.md) : les règles dépendant des 8 agents non encore écrits, et le suivi de portabilité (hooks Cowork, invocation Python selon l'OS). Les sept portes de sortie qui n'étaient déclarées que dans un prompt d'agent, sans contrôle code, sont désormais implémentées (`scripts/gates/`, `scripts/rules/R12`-`R13`) — les laisser dans les prompts seuls aurait revenu à faire confiance au modèle pour vérifier sa propre production, précisément ce que l'architecture refuse.

## Portabilité

Le socle n'utilise que ce qui fonctionne dans Claude Code **et** dans Cowork : pas de `${CLAUDE_PROJECT_DIR}`, pas d'injection shell dynamique, pas de référence `@fichier`.

`${CLAUDE_PLUGIN_ROOT}` n'est substitué que dans les JSON de hooks, jamais dans le corps d'un agent ou d'un skill ([bug connu](https://github.com/anthropics/claude-code/issues/9354)) : le hook dépose donc la racine du plugin dans `pm-portfolio/.plugin-path`, que les agents lisent, avec un repli par Glob.

## Confidentialité

Tout s'exécute en local ; les artefacts restent dans le dépôt du projet. En mission, ils contiennent des données client — les traiter comme tout livrable projet.

Le cas d'étude `exemples/portail-b2b` est **entièrement fictif** : ses chiffres sont inventés, et aucune donnée réelle d'un employeur n'a été utilisée dans ce projet.

## Licence

MIT — voir [`LICENSE`](LICENSE).

Ce dépôt ne réutilise le code d'aucun autre projet. Les patterns d'architecture repris (orchestration, mémoire partagée, boucle de rework bornée) proviennent de [sdi2200262/agentic-project-management](https://github.com/sdi2200262/agentic-project-management) (MPL-2.0) et [kchia/project-management-agentic-workflow](https://github.com/kchia/project-management-agentic-workflow) (MIT), étudiés puis réécrits. Le détail figure dans [`docs/benchmark-depots.md`](docs/benchmark-depots.md).
