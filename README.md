# PM Portfolio Agents

Une orchestration d'agents IA qui genere le portfolio d'artefacts d'un projet — charte,
parties prenantes, RACI, WBS, jalons, chemin critique, registre des risques — **sous des
portes qualite verifiees par du code, pas par un modele de langage**.

Plugin pour [Claude Code](https://code.claude.com) et Cowork.

---

## Le principe

> Le LLM produit, analyse et qualifie. Le code verifie, recalcule, compte et trace.

Aucune porte qualite ne depend du jugement d'un modele sur sa propre production. C'est la
seule regle non negociable du projet, et elle a une consequence sur le format : chaque
artefact est produit en **YAML structure**, puis rendu en Markdown lisible. Le Markdown est
une sortie, jamais la source — un tableau Markdown n'est pas verifiable mecaniquement.

Sur les 11 regles de coherence inter-artefacts, **9 sont du Python deterministe**. Les 2
restantes exigent un jugement semantique et sont confiees a un agent — c'est justement l'une
d'elles qui a rattrape le defaut le plus grave rencontre en test (voir plus bas).

## Ce que ca donne concretement

Deux exemples tires d'un run reel.

**Le code refuse une categorie inventee par le modele.** Contraint par trois categories de
valeur (`source`, `seuil_propose`, `a_sourcer`), un agent a invente une quatrieme —
`hypothese_illustrative` — pour exprimer quelque chose de legitime que le systeme ne lui
permettait pas de dire. Le nom etait raisonnable, l'intention honnete, le marquage correct.
La regle R9 l'a rejete parce qu'elle compare a une liste close. L'agent a corrige.

Un verificateur IA aurait tres probablement accepte.

**Le controle arithmetique inverse une conclusion managériale.** La regle R11 recalcule tout
total annonce a partir de ses composants :

```
[R11] Echeance intenable en hypothese haute : marge de -5.4 semaine(s)
      fenetre 34.6 sem. (2027-01-01 -> 2027-08-31) contre un chemin critique de 40 sem.
      — un levier de reduction est un prealable, pas une precaution
```

En phase de conception, une version de l'agent planificateur avait annonce un chemin
critique de 67 semaines la ou il en valait 71. La marge passait de +2 a -2 semaines :
l'echeance etait depassee avant le demarrage, et personne ne l'avait vu. **Ce defaut se
trouve en refaisant une addition, pas en relisant attentivement.**

## Ce que le systeme ne decide jamais

Sept decisions, listees et motivees dans la cartographie :

choix de methodologie · ordonnancement du backlog · validation des chiffres budgetaires ·
engagement de sprint · engagement vis-a-vis des parties prenantes · evaluation des
personnes · cotation finale de l'impact des risques.

Deux d'entre elles sont des regles du Scrum Guide, pas des preferences de conception.

## Demarche

Le depot contient autant la conception que le code, parce que la conception est le livrable.

| Etape | Document | Resultat |
|---|---|---|
| 1. Buy vs build | [`docs/benchmark-depots.md`](docs/benchmark-depots.md) | 4 depots inspectes sur leur contenu reel. Aucun ne produit d'artefact du referentiel PM : la reutilisation porte sur l'orchestration, pas sur la substance |
| 2. Conception | [`docs/cartographie-agents-pm.yaml`](docs/cartographie-agents-pm.yaml) | 15 agents en 4 couches, portes qualite, hand-offs, points de reprise humaine |
| 3. Test de conception | [`docs/tranche-verticale/`](docs/tranche-verticale/) | 7 agents joues a la main sur un cas neutre — **6 defauts de conception**, dont 5 introuvables en relisant le YAML |
| 4. Implementation | `agents/` `scripts/` `hooks/` | 7 agents, 11 regles, 25 tests de non-regression |
| 5. Run reel | [`docs/journal-essai-01.md`](docs/journal-essai-01.md) | Chaine complete en conditions reelles — **14 comportements conformes, 11 defauts, 3 familles** |
| 6. Limites | [`docs/ecarts-spec-implementation.md`](docs/ecarts-spec-implementation.md) | Ce que la specification exige et que le code ne verifie pas encore |
| 7. Raisonnement | [`docs/document-raisonnement.md`](docs/document-raisonnement.md) | Decisions de conception, alternatives ecartees, risques du systeme |

## Les trois familles de defauts

Le run reel n'a pas produit une liste de bugs disperses. Les 11 defauts se rangent en trois
familles, et **aucune ne concerne ce que le systeme produit** :

**1. Le controle verifie la FORME d'un signal, pas son SENS.**
« Proprietaire nomme » = chaine non vide, au lieu d'une personne pourvue. Un code de retour
a trois valeurs lu comme un booleen. « La lacune porte un arbitrage » = champ non vide, au
lieu d'un arbitrage qui repond a la question.

**2. Rien ne confronte une proposition AVAL aux contraintes AMONT.**
Exclure la conduite du changement alors que le critere de succes est le taux d'adoption.
Proposer un renfort alors que le plafond budgetaire est ferme. Proposer trois leviers de
reduction sans verifier qu'aucun ne ferme l'ecart. R11 est le seul controle de cette
famille, et il ne couvre que le calendrier.

**3. Le code valide ce que l'humain ne lit pas ; l'humain lit ce que le code ne valide pas.**
Un fichier YAML porte des champs structures — verifies, rarement lus — et de la prose —
jamais verifiee, mais c'est elle qui apparait dans le rendu Markdown. En test, des leviers
etaient marques `arbitre: false` dans les donnees et « deja choisis » dans les commentaires.
Un portfolio peut donc passer toutes ses regles en racontant l'inverse.

C'est la part LLM du verificateur qui a rattrape ce dernier cas. Aucun controle arithmetique
ne pouvait le voir.

## Installation

Voir [`INSTALLATION.md`](INSTALLATION.md). Controle pre-vol :

    python3 scripts/preflight.py        # ou : py scripts\preflight.py

Le preflight determine quelle invocation Python fonctionne sur la machine et verifie que
`hooks/hooks.json` utilise bien celle-la. **C'est un point critique et silencieux** : un hook
dont la commande echoue ne bloque rien, et les portes qualite ne s'executent jamais sans que
rien ne le signale. Le depot est livre avec `python3` ; sous Windows, ou le launcher `py`
est souvent le seul a fonctionner :

    py scripts\preflight.py --fix-hooks

Puis :

    claude --plugin-dir /chemin/vers/pm-portfolio-agents

## Commandes

    python3 scripts/validate.py ./pm-portfolio   # portes qualite, code retour 2 si ecart bloquant
    python3 scripts/render.py   ./pm-portfolio   # YAML -> Markdown lisible
    python3 scripts/test_regles.py               # 25 tests de non-regression
    python3 scripts/build_agents.py              # agents-src/ + _COMMUN.md -> agents/

## Etat

**v0.1.0 — increment 1** : 7 agents sur 15 conçus. Les 8 autres (budget, communications,
qualite, cloture, backlog, sprint, audit de tracabilite, orchestrateur) ne sont pas ecrits ;
les regles qui en dependent sont rapportees `non_applicable` avec leur condition, jamais
`echec`.

Ce qui n'est pas encore verifie par code est liste dans
[`docs/ecarts-spec-implementation.md`](docs/ecarts-spec-implementation.md). Sept portes de
sortie sont declarees dans les prompts d'agents sans etre controlees. Elles sont mecaniques
et devraient l'etre : les laisser dans les prompts reviendrait a faire confiance au modele
pour verifier sa propre production — precisement ce que l'architecture refuse.

## Portabilite

Le socle n'utilise que ce qui fonctionne dans Claude Code **et** dans Cowork : pas de
`${CLAUDE_PROJECT_DIR}`, pas d'injection shell dynamique, pas de reference `@fichier`.

`${CLAUDE_PLUGIN_ROOT}` n'est substitue que dans les JSON de hooks, jamais dans le corps
d'un agent ou d'un skill ([bug connu](https://github.com/anthropics/claude-code/issues/9354)) :
le hook depose donc la racine du plugin dans `pm-portfolio/.plugin-path`, que les agents
lisent, avec un repli par Glob.

## Confidentialite

Tout s'execute en local ; les artefacts restent dans le depot du projet. En mission, ils
contiennent des donnees client — les traiter comme tout livrable projet.

Le cas d'etude `exemples/portail-b2b` est **entierement fictif** : ses chiffres sont
inventes, et aucune donnee reelle d'un employeur n'a ete utilisee dans ce projet.

## Licence

MIT — voir [`LICENSE`](LICENSE).

Ce depot ne reutilise le code d'aucun autre projet. Les patterns d'architecture repris
(orchestration, memoire partagee, boucle de rework bornee) proviennent de
[sdi2200262/agentic-project-management](https://github.com/sdi2200262/agentic-project-management)
(MPL-2.0) et [kchia/project-management-agentic-workflow](https://github.com/kchia/project-management-agentic-workflow)
(MIT), etudies puis reecrits. Le detail figure dans
[`docs/benchmark-depots.md`](docs/benchmark-depots.md).
