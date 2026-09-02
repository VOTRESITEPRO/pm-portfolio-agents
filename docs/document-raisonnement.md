# Document de raisonnement

**Projet** : orchestration d'agents IA pour la génération d'un portfolio d'artefacts de
gestion de projet, aligné sur le Google Project Management Certificate (Cours 1-6).
**Version** : 1.3 — 01/09/2026 (ajout §1.3 : schéma de l'architecture effectivement implémentée)
**Objet** : justifier les décisions de conception, pas décrire le système. La description
est dans `cartographie-agents-pm.yaml` ; la démonstration est dans `portfolio-demo/`.

---

## Convention de lecture

Ce document distingue systématiquement trois natures d'affirmation :

| Marque | Nature |
|---|---|
| **[FAIT]** | Vérifié sur la source primaire, à la date indiquée |
| **[HYP]** | Hypothèse de travail, non vérifiée, explicitement assumée |
| **[BP]** | Bonne pratique de la discipline, appliquée par choix et non par contrainte |

---

# 1. Problème posé

Un chef de projet produit, sur chaque projet, une vingtaine d'artefacts dont la structure est largement invariante : charte, analyse des parties prenantes, RACI, WBS, registre des risques, budget, plan de communication, dispositif qualité, artefacts de clôture, et — en contexte agile — backlog, stories, cadence de sprint.

Deux constats orientent la conception.

**Ces artefacts ne sont pas indépendants.** Le RACI dépend des livrables de la charte ; la
contingence budgétaire dépend des risques cotés ; les risques dépendent du chemin critique. Une IA qui génère chaque artefact isolément produit un portfolio qui *paraît* cohérent sans l'être. **[BP]** — c'est le principe d'intégration du management de projet, appliqué ici comme contrainte d'architecture.

**La partie automatisable n'est pas la partie qui a de la valeur.** La structure d'une
charte est automatisable. L'arbitrage de périmètre qu'elle contient ne l'est pas. Un système qui ne pose pas cette frontière explicitement produit des documents qui usurpent l'autorité d'une décision.

**Ce que le système vise** : produire la structure exhaustive et vérifier sa cohérence.
**Ce qu'il ne vise pas** : décider à la place du chef de projet.

## 1.1 Ce que le système garantit, ce qu'il ne garantit pas

**[BP]** — à formuler sans ambiguïté, parce que la profusion de règles et de portes (15
règles, 10 portes, 93 tests) peut donner l'illusion inverse.

Le système contrôle une **cohérence** : structurelle (tout champ requis présent), logique
(un artefact aval retrouve bien ce que l'artefact amont a posé), arithmétique (un total
recalculé à partir de ses composants correspond au total annoncé). Il peut vérifier que le
budget total est la somme des postes ; il ne peut pas déterminer si 400 000 € est un
budget réaliste pour ce projet. Il peut vérifier qu'un risque coté ≥ 15 porte un plan
d'atténuation ; il ne peut pas juger si ce plan est le bon. Il peut vérifier qu'un RACI a
exactement un Accountable par livrable ; il ne peut pas juger si c'est la bonne personne.

> Le système garantit une **cohérence structurelle, logique et arithmétique**.
> Il ne garantit pas la **vérité métier** ni la **qualité** du contenu.

Cette frontière n'est pas un défaut à corriger : c'est la limite de ce qu'un contrôle
mécanique peut faire, et la raison pour laquelle la reprise humaine (D8) reste centrale.

## 1.2 Ce que produit le LLM, ce que vérifie le code

```
        LLM                          Code                         Humain
   ────────────                 ─────────────                ──────────────
   interprète                   calcule                      arbitre
   raisonne                     vérifie                       décide
   propose                      compare                       engage
   rédige                       impose (exit 2)

        │                            │                             │
        ▼                            ▼                             ▼
   artefacts YAML  ───────►  validation déterministe  ───────►  rapport d'écarts
                              (règles + portes)                 → rework ou
                                                                    reprise humaine
```

**[FAIT]** Décision d'architecture centrale du projet, appliquée depuis la première version :
aucune porte qualité ne dépend du jugement d'un modèle sur sa propre production. Voir D6.

## 1.3 Architecture effectivement implémentée (état au 01/09/2026)

**[FAIT]** — le schéma ci-dessus (§1.2) est le principe général. Celui-ci est
l'instanciation réelle, à distinguer explicitement de l'architecture théorique de
`docs/cartographie-agents-pm.yaml` : `pm-orchestrateur-pm` y est spécifié comme un agent
séparé, mais **n'existe pas encore** (incrément 2, non commencé). L'orchestration réelle est
portée par le skill `pm-portfolio` — décision D11 assumée, pas un oubli (voir
`docs/ecarts-spec-implementation.md` §3).

```
                              UTILISATEUR
                                   │
                                   ▼
                    skill pm-portfolio  [LLM — orchestrateur réel]
                    (pm-orchestrateur-pm séparé : pas encore construit)
                                   │
                 ┌─────────────────┴─────────────────┐
                 ▼                                    ▼
     scripts/tranche.py  [CODE]                 Agents PM  [LLM]
     fermeture transitive                       contexte-projet, méthodologue,
     + ordre d'exécution (D11)                  charte-objectifs, parties-prenantes,
                 │                               planificateur-wbs, risques
                 ▼                               (7 sur 15 construits, incrément 1)
     tranche.yaml — copié tel quel,                    │
     jamais recomposé de mémoire                       │
                 └─────────────────┬────────────────────┘
                                   ▼
                     artefacts YAML (pm-portfolio/*.yaml)
                                   │
                    hook PostToolUse / Stop  [CODE — automatique]
                                   ▼
                       scripts/validate.py  [CODE]
                    15 règles + 10 portes, chacune avec son ORIGINE
                                   │
                        RAPPORT-COHERENCE.md
                                   │
                       ┌───────────┴───────────┐
                       ▼                       ▼
                   conforme                  écart
                       │                       │
                       ▼                       ▼
                   AVANCER          pm-verificateur-coherence  [LLM]
                                     renvoie à l'agent auteur
                                     (max_rework, puis ESCALADER — D7)
```

**Ce que ce schéma montre, que celui de §1.2 ne montre pas** : que l'orchestration
elle-même est aujourd'hui un skill, pas un agent dédié ; que la fermeture transitive passe
par un script appelé, jamais recalculée en prose ; et que la validation se déclenche deux
fois — automatiquement par les hooks à chaque écriture, et explicitement dans la boucle de
rework portée par `pm-verificateur-coherence`.

---

# 2. Buy vs build

## 2.1 Méthode

Inspection du contenu réel des dépôts, pas de leur README ni de descriptions de seconde main. Trois critères : **licence** (usage commercial possible en ESN ?), **maturité** (éprouvé ou exercice ?), **adéquation** (produit-il les artefacts visés ?).

## 2.2 Dépôts inspectés

**[FAIT — vérifié le 31/08/2026]**

| Dépôt | Licence | Maturité | Produit des artefacts PM Cert ? |
|---|---|---|---|
| sdi2200262/agentic-project-management | **MPL-2.0** | 2,4k stars, 479 commits, v1.0.0 | **Non** |
| kchia/project-management-agentic-workflow | MIT | 1 star, 4 commits | **Non** |
| alirezarezvani/claude-skills | MIT | Actif, large | Non (substance PO) |
| slgoodrich/agents (AI PM Copilot) | **PolyForm Noncommercial** | Petit, structuré | Non |

## 2.3 Le constat qui structure tout

**Aucun dépôt inspecté ne génère d'artefact du référentiel PM.** Ni charte, ni RACI, ni
registre des risques, ni budget, ni plan de communication, ni artefacts de clôture.

- `sdi2200262` produit Spec / Plan / Rules / Task Prompts / Memory — du **spec-driven pour
  du développement logiciel**.
- `kchia` produit des user stories, des groupes de fonctionnalités et des tâches
  d'ingénierie — et se décrit lui-même comme exploratoire, avec ses limites documentées par son auteur.

**Conséquence** : la réutilisation porte sur la **couche orchestration et gouvernance**.
La couche de génération d'artefacts est intégralement construite en propre. Répartition finale : **5 agents « adapté », 10 « créé », 0 « réutilisé » tel quel.**

## 2.4 Ce qui est repris, et sous quelle forme

| Ce qui est repris | Origine | Forme de la reprise |
|---|---|---|
| Orchestration Planner / Manager / Workers | sdi2200262 — MPL-2.0 | Principe transposé au séquençage d'artefacts |
| Mémoire partagée persistante | sdi2200262 — MPL-2.0 | Devient le « contexte partagé », source unique de vérité |
| Validation humaine entre chaque étape | sdi2200262 — MPL-2.0 | Durcie : certaines décisions ne sont pas *validées* par l'humain, elles lui **appartiennent** |
| Boucle de rework bornée par un plafond | kchia — MIT | Devient `max_rework` + verdict `escalader` |
| Routage selon la nature de la demande | kchia — MIT | Devient le branchement conditionnel agile |
| Décomposition objectif → étapes | kchia — MIT | Principe du `planificateur-wbs` |

**Aucun code n'est repris.** Ce sont des patterns d'architecture. **[FAIT]** — les licences
MIT et MPL-2.0 l'autoriseraient pourtant ; la raison n'est pas juridique mais fonctionnelle, aucun de ces codes ne faisant ce que le système doit faire.

## 2.5 Le point de licence qui compte en mission

**[FAIT]** MPL-2.0 (sdi2200262) autorisé l'usage commercial, avec un copyleft de fichier :
toute modification d'un fichier source reste sous MPL-2.0. **Utilisable en mission ESN facturée.**

**[FAIT]** PolyForm Noncommercial (AI PM Copilot) **interdit l'usage commercial**. Ce dépôt
est le mieux structuré des quatre sur le plan de l'orchestration produit — et c'est précisément celui qu'on ne peut pas embarquer chez un client. Il a été étudié comme concept, jamais copié.

> C'est le type de vérification qui distingue une veille d'une due diligence. Un dépôt à
> 2,4k étoiles a été retenu pour son modèle et écarté pour sa substance ; un dépôt à
> 1 étoile a été conservé pour trois patterns précis ; le mieux conçu a été écarté pour sa
> licence.

---

# 3. Décisions de conception

## D1 — Un orchestrateur unique, pas un catalogue d'agents

**Décision.** L'utilisateur décrit son projet ; il ne choisit pas quel agent invoquer.

**Motif.** Un catalogue reporte sur l'utilisateur la connaissance de la séquence et des
dépendances — c'est-à-dire l'essentiel de la compétence de gestion de projet. Un système qui exige de savoir qu'il faut le WBS avant les risques n'apporte rien à qui le sait déjà, et induit en erreur qui ne le sait pas.

**Alternative écartée.** Bibliothèque de prompts spécialisés. Plus simple à construire, mais
ce n'est plus une orchestration : c'est un presse-papier.

## D2 — Quinze agents : arbitrage de granularité

**Décision.** 15 agents — 2 orchestration, 11 production, 2 contrôle.

**Motif.** La granularité suit le **découpage des compétences du curriculum**, pas une
intuition d'équilibre. Un agent = un bloc de compétences nommées, cohérent en entrée et en sortie.

| Alternative | Écartée parce que |
|---|---|
| ~5 agents (un par phase) | L'agent « planification » cumulerait WBS, risques, budget et communication : quatre logiques d'entrée-sortie incompatibles, et une porte de sortie qui ne peut plus être mécanique |
| ~30 agents (un par artefact) | Multiplication des hand-offs sans gain de contrôle ; le coût de coordination dépasse le bénéfice de spécialisation |

**[HYP]** L'optimum est probablement entre 12 et 18. Aucune mesure ne l'établit — c'est un
arbitrage de conception, pas un résultat.

## D3 — Le registre des lacunes est un livrable, pas une note interne

**Décision.** `contexte-projet` produit deux sorties : le dossier de contexte **et** le
registre des lacunes qualifiées (bloquante / dégradante / mineure). Une lacune bloquante arrête la chaîne.

**Motif.** C'est la mitigation principale du risque d'hallucination, et elle est
structurelle plutôt que déclarative. Une consigne « n'invente pas » dans un prompt système est une intention ; un livrable qui liste ce qui manque est un contrôle.

**Vérifié en pratique.** Sur le cas de test, 4 lacunes bloquantes sur 7 ont arrêté la
chaîne : échéance non datée, budget non arbitré, périmètre indéterminé, aucun critère de succès chiffré. Un système non gouverné aurait produit un portfolio entièrement plausible et entièrement faux.

## D4 — Branchement conditionnel, pas deux chaînes séparées

**Décision.** Une seule chaîne. `methodologue` produit un drapeau qui active ou non la
branche agile.

**Motif.** Les postes visés couvrent les deux registres, et **la plupart des contextes réels
sont hybrides**. Deux chaînes séparées obligeraient à choisir un camp au démarrage — exactement l'erreur que la recommandation méthodologique doit éviter.

**Effet secondaire assumé.** La chaîne waterfall pure produit quand même une WBS et un
chemin critique allégés ; la chaîne agile pure aussi. C'est voulu : un projet agile à besoin d'un budget et de jalons contractuels dès qu'un prestataire est engagé.

## D5 — Deux agents de contrôle, pas un

**Décision.** `verificateur-coherence` (cohérence interne) et `auditeur-curriculum`
(conformité au référentiel), séquentiels.

**Motif.** Ils ne vérifient pas la même chose. Un portfolio peut être parfaitement cohérent
et ne couvrir que trois compétences sur vingt-deux ; il peut couvrir toutes les compétences et se contredire d'un artefact à l'autre. Fusionner les deux produirait une porte de sortie qui mélange deux échelles de jugement — et une porte qui mélange ne peut plus être mécanique.

**Ordre.** Cohérence d'abord. Auditer la conformité d'un portfolio incohérent n'a pas de sens.

**[BP]** Le second contrôle est ce qu'aucun dépôt du benchmark ne fait : l'audit de
traçabilité vis-à-vis d'un référentiel de compétences. C'est la brique la plus différenciante du système.

## D6 — Portes qualité mécaniques, pas qualitatives

**Décision.** Chaque porte est une liste de contrôles vérifiables sans jugement : « un seul
Accountable par livrable », « chaque tâche du chemin critique couverte par un risque », « tout total recalculé à partir de ses composants ».

**Motif.** Une porte qualitative (« l'artefact est-il de bonne qualité ? ») demande à un
modèle de langage d'évaluer sa propre production. **[BP]** C'est le point de complaisance connu de ces systèmes : ils valident ce qu'ils viennent d'écrire.

**Validé par le test, et plus fortement que prévu.** Le seul défaut qui inversait une
conclusion managériale (chemin critique mal additionné) s'est trouvé par **recalcul**, pas par relecture. Une relecture attentive ne l'aurait pas vu ; une addition le voit toujours.

## D7 — Boucle de rework bornée, puis escalade

**Décision.** Verdict `retravailler` → retour à l'agent auteur, dans la limite de
`max_rework` (2 ou 3 selon l'agent). Au-delà : `escalader` vers l'humain.

**Motif.** Sans plafond, deux agents peuvent se renvoyer indéfiniment un écart qu'aucun
n'est en mesure de résoudre — typiquement quand l'écart vient d'une lacune du contexte, pas d'un défaut de production. Le plafond convertit l'impasse en décision humaine.

## D8 — La reprise humaine est spécifiée, pas invoquée

**Décision.** Chaque agent déclare ce qu'il ne décide jamais. Sept décisions sont listées
comme non délégables au niveau du système.

**Motif.** « L'humain garde le contrôle » est une formule. Ce qui a de la valeur, c'est la
liste précise, et surtout **le motif de chaque entrée** :

| Décision | Motif du non-délégable |
|---|---|
| Choix de méthodologie | Engagé la contractualisation et le mode de collaboration |
| Ordonnancement du backlog | Prérogative du Product Owner — **[FAIT]** Scrum Guide 2020 ; la valeur n'est pas calculable |
| Validation des chiffrés budgétaires | Risque de crédibilité le plus élevé du portfolio |
| Engagement de sprint | **[FAIT]** Une équipe s'engagé elle-même — Scrum Guide |
| Engagement vis-à-vis des parties prenantes | La parole donnée engagé une personne |
| Évaluation des personnes | Hors périmètre, quelle que soit la qualité des données |
| Cotation finale de l'impact des risques | Dépend de la tolérance au risque de l'organisation |

**[BP]** Deux de ces entrées sont des règles de référentiel, pas des préférences : le Scrum
Guide les impose. Les autres sont des arbitrages de conception assumés.

## D9 — Trois catégories de valeur, pas deux

**Décision.** Donnée sourcée (autorisée) · seuil de gestion proposé (autorisé **si marqué**)
· donnée factuelle générée (interdite).

**Motif — cette décision est née d'une contradiction découverte au test.** La porte de
l'agent `risques` exige un déclencheur observable, donc un seuil ; la règle initiale interdisait toute valeur non sourcée ; et aucun seuil de gestion n'existe jamais dans un contexte d'entrée. Résultat : **6 déclencheurs sur 14 reposaient sur des seuils inventés, et le registre à franchi sa porte sans alerte.**

La distinction qui résout la contradiction :

> Un seuil de gestion est une **proposition de pilotage** qu'un comité arbitre.
> Une donnée factuelle générée est un **mensonge sur le réel**.

Les confondre conduit soit à interdire les déclencheurs — registre inexploitable — soit à laisser passer des chiffrés inventés — registre trompeur.

## D10 — Deux agents pour l'agile, un pour le budget et les achats

**Décision.** `backlog-stories` et `sprint` séparés ; `budget-achats` séparé de
`planificateur-wbs`.

**Motif.** Le double registre est un impératif du projet, et l'agile en est la moitié : un
agent unique l'affaiblirait. L'approvisionnement (appel d'offres, sélection fournisseurs, contractualisation, éthique) est **[FAIT]** une compétence nommée distincte du curriculum C3 — la fusionner dans la planification la ferait disparaître.

## D11 — Le graphe de dépendances se calcule par du code, jamais par le jugement du LLM

**Décision.** La fermeture transitive d'une tranche d'exécution (quels artefacts, donc
quels agents, une demande partielle entraîne) est calculée par `scripts/tranche.py`, qui
appelle `pmlib.fermeture_transitive()`. Le skill `pm-portfolio` (et tout agent qui en
tiendra lieu par la suite) copie la sortie du script telle quelle dans `tranche.yaml` ; il
ne la recompose jamais de mémoire.

**Motif — cohérence avec D6.** `orchestrateur-pm` n'existe pas encore comme agent séparé :
c'est le skill `pm-portfolio` qui tient lieu d'orchestration (voir
`docs/ecarts-spec-implementation.md` §3). Avant cette décision, son seul calcul mécanique —
« quels artefacts amont une tranche partielle entraîne » — était laissé au raisonnement du
skill, alors que le code pour le faire exactement (`fermeture_transitive`) existait déjà,
non appelé. C'est la même famille d'erreur que celle qui a produit R11 : un calcul
énumérable, laissé à un modèle qui peut en oublier une branche sur un graphe à 12 noeuds.

**Ce qui reste au jugement du LLM.** Interpréter la demande de l'utilisateur pour en tirer
la *cible* (quels artefacts sont visés) reste une tâche d'interprétation, donc légitimement
confiée au modèle. Ce qui en découle mécaniquement — la fermeture, l'ordre, la liste des
agents — ne l'est plus.

**Portée volontairement limitée.** Cette décision ne construit pas l'agent
`orchestrateur-pm` séparé que décrit la cartographie : le skill actuel est déjà testé en
conditions réelles (verdict AVANCER, voir §5) ; le remplacer par un agent neuf non testé
aurait été un risque non justifié par le gain. Seul le point de jugement identifié comme
réellement délégué à tort a été corrigé.

## D12 — L'orthographe accentuée est une porte mécanique (G7), pas une consigne de prompt

**Décision.** Ajout de la porte `G7` (`scripts/gates/g7_orthographe_accents.py`) : sur un
artefact dont la prose cumule au moins 150 lettres, l'absence totale de caractère accentué
est un écart mineur (dérogation admise). Consigne miroir ajoutée dans
`agents-src/_COMMUN.md` (« Orthographe ») pour tous les agents.

**Motif — même famille que D6.** Au run palier 4 (01/09/2026, mêmes données que l'essai
01), `pm-contexte-projet` et `pm-charte-objectifs` ont produit une prose entièrement sans
accents ("Perimetre", "depassable", "concernes"), tandis que `pm-planificateur-wbs` et
`pm-risques` écrivaient un français correct sur le même run. Aucune règle ni porte ne le
détectait — un défaut de forme pur, jusqu'ici laissé à la seule discipline du prompt, alors
que la présence d'accents dans un volume de texte donné est un signal aussi mécaniquement
vérifiable que ceux déjà couverts par D6.

**Portée volontairement limitée.** Sévérité `mineur`, pas `bloquant` : la perte d'accents
dégrade la qualité de forme d'un livrable, pas la validité d'une décision de gestion de
projet — elle ne doit pas bloquer un verdict AVANCER. Dérogation admise pour ne pas
pénaliser un artefact légitimement non accentué (vocabulaire technique anglophone).

## D13 — La fermeture aval d'une modification se calcule par du code, symétrique de D11

**Décision.** Ajout de `scripts/impact.py` et `pmlib.fermeture_transitive_aval()` : donné
un artefact déjà produit dont une information a changé, calcule mécaniquement tout ce qui
en dépend en aval, sur le même graphe `DEPENDANCES` que `tranche.py`, parcouru dans l'autre
sens. Le skill `pm-portfolio` l'invoque désormais (« Modifier une information déjà
arbitrée », SKILL.md) avant de relancer quoi que ce soit.

**Motif.** Discussion avec l'utilisateur (02/09/2026) sur le palier 4 : que se passe-t-il
si une échéance connue après coup diffère de celle déjà posée ? Réponse honnête à
l'époque — le mécanisme d'édition existe (un agent relancé réécrit son YAML), mais rien ne
calcule ce qui, en aval, devient potentiellement obsolète. Éditer `contexte.yaml` seul
laisserait `plan.yaml`/`risques.yaml` silencieusement périmés, sans qu'aucune règle ne s'en
plaigne nécessairement (une échéance repoussée *augmente* une marge, ce qu'aucune règle ne
sanctionne). Même famille que D11 : un calcul énumérable sur un graphe explicite ne doit
jamais être laissé au raisonnement du skill.

**Portée volontairement limitée — la limite qui compte.** `impact.py` ne fait que
*détecter*. Il ne relance rien, ne réécrit rien. Chaque agent en aval, une fois relancé,
repasse par ses propres points de validation obligatoire (méthodologie, estimations,
cotations…) déjà existants dans la chaîne. Une automatisation qui réécrirait silencieusement
une durée ou une cotation déjà validée par l'utilisateur violerait directement la liste des
« sept décisions que la chaîne ne prend jamais » (SKILL.md) — ce n'est pas un oubli, c'est
un choix délibéré : détecter par le code, reconfirmer par l'humain, jamais l'inverse.

## D14 — Les champs utiles non bloquants se demandent en une passe groupée, tracée par une porte

**Décision.** Ajout de la porte `G8` (`scripts/gates/g8_champs_utiles_renseignes.py`) :
`projet.commanditaire` et `projet.secteur` vides sont un écart mineur (dérogation admise).
`pm-contexte-projet` pose désormais, une fois les lacunes bloquantes résolues, une seule
question groupée pour ces champs plutôt que de les laisser silencieusement vides.

**Motif.** Seules 4 lacunes (échéance, budget, périmètre, critère de succès) sont
qualifiées « bloquantes » et déclenchent une question — un choix délibéré pour ne pas
sursolliciter l'humain (voir agents-src/pm-contexte-projet.md). Mais ce choix avait un
effet de bord non voulu : un champ utile non bloquant laissé vide était indiscernable d'un
champ explicitement décliné. G8 rend cette différence traçable sans rendre le champ
bloquant.

**Portée volontairement limitée.** Sévérité `mineur`. N'étend pas la liste des lacunes
bloquantes — un commanditaire non nommé ne doit pas empêcher de produire une charte
honnête ; il doit seulement être visible et, si décliné, tracé par dérogation plutôt que
silencieusement absent.

## D15 — Un document source fourni par l'utilisateur s'exploite, avec provenance tracée

**Décision.** `pm-contexte-projet` lit désormais tout document que l'utilisateur mentionne
ou fournit, avant de poser ses questions, et en extrait ce qui répond au schéma de
`contexte.yaml`. Une valeur ainsi extraite porte `statut: source` **et** un champ
`provenance` (document + section), convention ajoutée à `agents-src/_COMMUN.md`.

**Motif.** Jusqu'ici, seule une description orale en entrée était prévue. Un utilisateur
disposant déjà d'un cahier des charges ou d'un brief devait retaper l'essentiel à la main.

**Ce qui reste au jugement du LLM, et sa limite honnête.** Lire un document ne supprime
pas le risque d'erreur de lecture ou d'extraction — ça le déplace, ça ne l'élimine pas.
Aucun contrôle de code ne vérifie aujourd'hui qu'une valeur `provenance` correspond
réellement au document cité : c'est une discipline de prompt, pas encore une porte
mécanique. Contrairement à D12/D13/D14, cette décision n'ajoute aucun contrôle vérifiable
par du code — à noter comme limite explicite, pas comme un oubli.

## D16 — Le texte de substitution résiduel est une porte mécanique (G9), pas une consigne de prompt

**Décision.** Ajout de la porte `G9` (`scripts/gates/g9_texte_substitution.py`) : la
détection d'un résidu de génération (`TODO`, `TBD`, `PLACEHOLDER`, `[INSERT]`...) dans la
prose d'un artefact est un écart mineur (dérogation admise), sur tous les artefacts
indifféremment.

**Motif.** Analyse du 02/09/2026 de docforge-ai (Venkatesh188, benchmark GitHub) : ce dépôt
fait passer chaque document généré par un filtre déterministe équivalent avant toute
vérification de fond. Même famille que D12/D14 : un signal de forme se vérifie par du code,
jamais par la seule discipline d'un prompt — et rien ne le détectait jusqu'ici sur ce
portfolio, faute d'un run réel ayant produit ce défaut précis.

**Portée volontairement limitée.** Sévérité `mineur`, comme G7 : un résidu de génération
dégrade la qualité de forme, pas la validité d'une décision de gestion de projet.
Dérogation admise pour un terme métier légitime qui coïnciderait avec un motif surveillé.

## D17 — La plausibilité lexicale de l'énoncé SMART est une porte mécanique (G10), distincte de la présence des champs (G2)

**Décision.** Ajout de la porte `G10` (`scripts/gates/g10_smart_contenu_plausible.py`) :
l'énoncé (`enonce`) de chaque objectif SMART doit contenir une grandeur chiffrée détectable
ET une échéance détectable, sous peine d'écart mineur (dérogation admise).

**Motif.** Analyse du 02/09/2026 de ConversationProjectInitiator (useffj, benchmark
GitHub) : ce dépôt applique une heuristique lexicale équivalente
(`utils/validators.py::check_smart`) en complément, jamais en remplacement, de la
validation qualitative par LLM. `G2` vérifie que les 5 champs `smart` (s/m/a/r/t) sont
renseignés — pas que leur contenu est plausible. Un objectif dont `smart.m` vaut « sera
mesuré au fil de l'eau » passe `G2` sans jamais être questionné.

**Piège évité — cibler le bon champ.** Une première version ciblait `smart.m`/`smart.t`
directement, par calque trop littéral de ConversationProjectInitiator. Testée contre
`exemples/portail-b2b`, elle a produit un faux positif systématique : dans ce schéma,
`smart.m` documente la **source/méthode de mesure** (ex : « source : outil de
téléphonie »), pas la grandeur cible elle-même — celle-ci vit dans `enonce` et dans
`cible.valeur` (déjà gouverné par `R9`). La porte cible donc `enonce`, seul champ qui
combine mesure et échéance en une phrase lisible. Reproductible : relancer
`validate.py exemples/portail-b2b` après avoir pointé `G10` sur `smart.m`/`smart.t`
fait réapparaître le faux positif sur les trois objectifs de l'exemple.

**Portée volontairement limitée.** Même principe que ConversationProjectInitiator : les
critères Spécifique/Atteignable/Pertinent ne sont pas fiablement vérifiables par
expression régulière sur un texte libre, et restent hors périmètre de cette porte. Un
objectif-jalon binaire (mise en service à une date, sans grandeur chiffrée) est un cas
légitime couvert par la dérogation, pas une exception à coder — `G10` le signale
effectivement sur l'objectif O3 de `portail-b2b` (mise en service du portail), qui est bien
un jalon binaire et non un défaut de l'exemple.

## D18 — La formulation Cause-Événement-Impact d'un risque reste une consigne de prompt, sans porte mécanique

**Décision.** `agents-src/pm-risques.md` exige désormais que `libelle` suive la structure
Cause-Événement-Impact (« En raison de [cause], [événement] peut survenir, entraînant
[impact]. »), cinquième exigence contrôlée aux côtés de l'ancrage, du propriétaire pourvu,
des seuils marqués et de l'indépendance.

**Motif.** Analyse du 02/09/2026 de ConversationProjectInitiator (useffj) : ce dépôt impose
ce même format par prompt pour chaque risque généré — un standard de rédaction des risques
qui améliore la traçabilité cause → conséquence sans coût d'implémentation.

**Pourquoi aucune porte, contrairement à D16/D17 — la limite qui compte, même famille que
D15.** Une structure Cause-Événement-Impact valide s'exprime en français de trop de façons
différentes pour être fiablement détectée par une expression régulière, contrairement à un
résidu de génération (`G9`, motifs fermés) ou une grandeur chiffrée (`G10`, motifs
numériques bornés). Coder un contrôle friable dessus produirait plus de faux négatifs et de
faux positifs qu'il n'apporterait de garantie réelle — à noter comme limite explicite, pas
comme un oubli.

---

# 4. Risques du système et mitigations

## 4.1 Risques de production

| # | Risque | Mitigation | Statut |
|---|---|---|---|
| S-01 | **Hallucination de données factuelles** (coûts unitaires, volumétries, durées empiriques) | Catégories de valeur (D9) + registre des lacunes livrable (D3) + règle R9 bloquante | Testé — 3 refus de fabriquer observés sur le cas |
| S-02 | **Plausibilité structurelle** : un portfolio cohérent et creux | Ancrage obligatoire de chaque élément sur le contexte ou un artefact amont ; le vérificateur rejette le générique | Testé — registre des risques 14/14 ancrés |
| S-03 | **Fausse précision des estimations** (durées au jour près sans base) | Sorties en fourchettes + mention explicite du caractère non empirique + reprise humaine obligatoire | Testé |
| S-04 | **Biais pro-agile** du `methodologue` (les corpus en sont saturés) | Grille de critères imposée + obligation de documenter l'alternative écartée | Testé — 4 critères sur 8 poussaient au séquentiel, recommandation hybride obtenue |
| S-05 | **Erreur arithmétique invisible** | Cohérence arithmétique obligatoire (C3) : tout total recalculé, tout écart bloquant | **Découvert au test**, corrigé en v1.1, non re-testé |

## 4.2 Risques de contrôle

| # | Risque | Mitigation | Statut |
|---|---|---|---|
| S-06 | **Complaisance du vérificateur** : valider ce qui vient d'être produit | Règles mécaniques, jamais d'appréciation globale (D6) | Testé |
| S-07 | **Faux positifs** décrédibilisant le contrôle et poussant à désactiver la règle | Mécanisme de dérogation motivée (C6) : visible, listée au rapport, contestable | **Découvert au test** — 2 écarts sur 6 étaient des défauts de règle, pas d'artefact |
| S-08 | **Porte validant un champ vide de sens** (rôle « à nommer » accepté comme propriétaire) | Règle R10 : tout rôle propriétaire doit être **pourvu** au registre des parties prenantes | **Découvert au test**, corrigé en v1.1 |
| S-09 | **Confusion « non applicable » / « en échec »** sur chaîne partielle | `condition_applicabilite` par règle + 4 états de sortie (C2) | **Découvert au test**, corrigé en v1.1 |

## 4.3 Risques d'usage

| # | Risque | Mitigation |
|---|---|---|
| S-10 | **Substitution du jugement** : le portfolio est pris pour une décision | Liste des 7 décisions non délégables (D8), inscrite dans chaque artefact concerné |
| S-11 | **Dérive de licence** : réutilisation d'un composant non commercial en mission | Traçabilité licence par agent dans le YAML ; MPL-2.0 et MIT seuls retenus |
| S-12 | **Malentendu sur le statut** : croire que la chaîne s'exécute | Statut « PRÉSENTABLE — conception documentée » affiché en tête du YAML et du portfolio |
| S-13 | **Recette humaine escamotée** : un portfolio bien formé donne l'illusion d'être validé | Le rapport de cohérence et les points de reprise humaine sont des livrables du portfolio, pas des annexes |

## 4.4 Où l'IA aide, où elle est risquée

**[BP]** — la frontière est la même dans les deux sens, et c'est ce qui la rend défendable.

| L'IA apporte le plus | L'IA est risquée |
|---|---|
| Exhaustivité structurelle : aucune rubrique oubliée | Toute valeur chiffrée absente du contexte d'entrée |
| Cohérence croisée, vérifiable mécaniquement | Estimation de durée ou de vélocité sans historique |
| Traçabilité à un référentiel | Cartographie politique d'une organisation |
| Première version comme support d'atelier | Appréciation qualitative déguisée en calcul |

---

# 5. Ce que la validation a produit

**Méthode.** Tranche verticale de 7 agents sur 15, exécutée manuellement selon les
spécifications, sur un cas neutre (refonte d'un portail client B2B). Dossier `portfolio-demo/`.

**Résultat : 6 défauts de conception, dont 5 introuvables en relisant la cartographie.**

Le plus significatif : `planificateur-wbs` a validé sa propre porte de sortie avec un chemin critique mal additionné — 67 semaines annoncées, 71 réelles. La conclusion managériale en était inversée : marge annoncée de +2 semaines sur l'échéance, marge réelle de **−2 semaines**. L'échéance était dépassée avant le démarrage.

**Ce que ce défaut enseigne, et qui vaut au-delà de ce projet :**

> Une porte de sortie vérifie un **format**, pas une **vérité**.
> Le second niveau de contrôle ne sert pas à relire : il sert à **recalculer**.

C'est l'argument qui justifie l'architecture à deux niveaux — et il est plus fort que celui qui avait présidé à sa conception.

---

# 6. Limites assumées

**[FAIT]** — état au 31/08/2026 :

- La chaîne n'a **jamais été exécutée automatiquement**. La tranche verticale a été jouée
  manuellement selon les spécifications. Aucune mesure de la qualité réelle des sorties d'un agent réellement instancié.
- **8 agents sur 15 restent non testés** : budget-achats, communications, qualité-suivi,
  équipe-cloture, backlog-stories, sprint, auditeur-curriculum, orchestrateur-pm.
- Les corrections **C1 à C6 sont spécifiées mais n'ont pas été re-testées** par une nouvelle
  tranche.
- Les libellés exacts des compétences du curriculum n'ont pas été recoupés module par module
  avec les dépôts pédagogiques de référence.
- Les portes qualité sont spécifiées ; leur implémentation reste à écrire.

**[HYP]** L'exécution réelle révélera d'autres défauts, probablement du même ordre que ceux
trouvés : des contradictions entre règles, et des portes qui valident la forme d'un champ plutôt que son sens.

---

# 7. Transférabilité

La méthode ne dépend ni d'un secteur, ni d'un employeur, ni d'un outil :

- Le **référentiel** est interchangeable — Google PM Cert ici, PMBOK, PRINCE2 ou un
  référentiel interne d'ESN ailleurs. Seule la matrice de traçabilité change.
- Le **cas d'étude** est fictif et générique.
- Les **patterns de gouvernance** — portes mécaniques, contrôle par recalcul, catégories de
  valeur, dérogation motivée, reprise humaine spécifiée — sont indépendants du domaine.

Ce qui se transfère n'est pas le système : c'est la façon de le gouverner.
