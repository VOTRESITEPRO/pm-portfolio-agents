# Journal d'essai n°1 — premier run réel

Environnement : Windows, Python 3.14.2 (`py -3`), Claude Code v2.1.234, Sonnet 5. Projet de test : `C:\Users\letra\test-pm`, vide. Entrée : « Refonte de l'intranet documentaire, environ 300 collaborateurs, budget evoque autour de 80 k, prêt l'an prochain. » — 3 lacunes bloquantes volontaires.

| # | Ce qui s'est passe | Attendu | Cause | Statut |
|---|---|---|---|---|
| E1 | Le hook `Stop` bloque avec « Aucun artefact dans pm-portfolio » | Ne rien faire tant que le portfolio est vide | `hook.py` traitait tout code de retour non nul comme un écart. Or `validate.py` renvoie 1 pour « rien à valider » et 2 pour « écart bloquant ». | **Corrige** — seul le code 2 bloque désormais |
| E2 | `pm-contexte-projet` est lance en **arriere-plan** par Claude Code | Premier plan : l'agent doit poser ses questions et attendre les arbitrages | Rien dans le skill ni le frontmatter n'interdit le backgrounding. | **Non bloquant** — l'agent a remonté ses questions malgre le mode arriere-plan |
| E3 | `Error: prompt is required when stop is not true` | — | Erreur du harness Claude Code, hors plugin | Sans objet |
| E4 | Le dossier `pm-portfolio/` a été créé vide avant toute production | Acceptable | Conséquence de E1, sans gravite propre | Résolu par E1 |

## Enseignement de E1

Un code de retour à trois valeurs distinctes (0 / 1 / 2) lu comme un booleen (0 / non-zero). La porte qualité se declenchait donc sur une condition qui n'en est pas une.

C'est la même famille d'erreur que celles trouvees jusqu'ici : **un contrôle qui vérifie la forme d'un signal plutôt que son sens**. La porte de sortie qui validait « proprietaire nomme » verifiait une chaîne de caracteres, pas une personne ; ici le hook verifiait « le script a échoue », pas « le portfolio est en écart ».

## Résultat du test principal — Réussi

`pm-contexte-projet` **s'est arrête et a pose ses questions** au lieu de produire un contexte complet. Il a identifie **quatre** lacunes bloquantes là où le cas de test n'en comportait volontairement que trois : échéance, budget, critères de succès — plus le
**périmètre**, que la conception du cas de test avait laisse passer.

C'est le seul comportement du système qu'aucun test unitaire ne pouvait couvrir, et le seul qui justifie toute l'architecture. Un agent qui aurait rempli le budget, l'échéance et l'objectif par plausibilite aurait produit un portfolio entièrement crédible et entièrement faux.

## E2 — à surveiller malgre tout

Le mode arriere-plan n'a pas empeche le dialogue cette fois. Rien ne garantit que ce soit systématique : le comportement dépend de l'orchestration de Claude Code, pas du plugin.

La mitigation robuste ne consiste pas à interdire le backgrounding — elle consiste à rendre le contrôle **independant du mode d'exécution** : une porte codee qui refuse tout `contexte.yaml` comportant une lacune bloquante au statut `ouverte`, ou une lacune bloquante `arbitree` sans texte d'arbitrage.

C'est l'une des sept portes mecaniques non encore codees (voir `ECARTS-SPEC-IMPLEMENTATION.md`), et l'essai vient de montrer que c'est la plus prioritaire des sept : elle protégé le comportement le plus important du système, qui ne repose aujourd'hui que sur la discipline d'un prompt.

## Suite du test — à observer

Réponses fournies : échéance 30/06/2027 ferme · budget 80 k EUR plafond vote · périmètre consultation et recherche documentaire + migration, hors GED et hors mobile natif · succès 70 % des 300 collaborateurs en utilisateurs actifs mensuels à 3 mois.

Point d'observation suivant : la cible de 70 % est chiffrée mais **sans base de départ connue**. `pm-charte-objectifs` doit soit transformer la mesure initiale en tâche du plan, soit marquer la cible `seuil_propose`. S'il invente un taux d'usage actuel, la règle R9 doit le rattraper.

---

# Apport terrain — à traiter après le test (2026-08-31)

**Source : Yannick, expérience P2R.** Budget evoque au départ : 80 k EUR. Coût final :
~370 k EUR. Facteur 4,6. Motif : le chiffré initial precedait le cadrage et ne tenait pas compte de ce qui devait réellement être fait.

## Le manque que cela révèle

`pm-contexte-projet` qualifie correctement un budget « evoque, non arbitre » en lacune bloquante. Mais dès que l'humain répond « 80 k, plafond vote », le système l'enregistre en `statut: source` et **construit tout le portfolio dessus**. Un arbitrage humain est traite comme une donnée definitive.

Or un budget arbitre AVANT le WBS n'est pas une donnée : c'est une hypothèse. Il ne devient une donnée qu'une fois confronte à une estimation ascendante.

Les trois catégories de valeur ne couvrent pas ce cas :

| Catégorie | Ce qu'elle capture | Ce qu'elle rate ici |
|---|---|---|
| `source` | traçable vers le contexte ou un arbitrage | un arbitrage peut être faux d'un facteur 4,6 |
| `seuil_propose` | proposition de pilotage à arbitrer | ce n'est pas un seuil, c'est un cadre |
| `a_sourcer` | donnée absente | la donnée n'est pas absente, elle est prématurée |

## Pistes de correction

1. **Quatrième statut** : `arbitre_avant_cadrage` — valeur fournie par l'humain, mais
   antérieure à toute estimation ascendante. Se comporte comme `source` pour la production, mais reste marquee comme non consolidee dans les artefacts.
2. **Règle de confrontation** (à implémenter dans `pm-budget-achats`, agent non encore
   ecrit) : comparer systématiquement le budget bottom-up issu de la WBS au budget cadre. Un écart majeur est un **écart bloquant remontant au sponsor**, pas une note de bas de page. C'est le moment où le cadre devient une donnée — ou est refute.
3. Applicable au-delà du budget : une échéance « evoquee » avant le chemin critique releve
   de la même catégorie. R11 fait déjà cette confrontation pour le calendrier (marge réelle vs fenêtre) ; l'équivalent budgétaire n'existe pas.

## Pourquoi ca compte

C'est un apport d'expérience terrain, pas de conception. Un système qui accepté sans broncher un budget d'avant-cadrage produit un portfolio cohérent avec une contrainte fausse — et perd sa crédibilité en mission au premier comité de pilotage.

---

# Observations en cours de chaîne

## Comportements CONFORMES vérifiés en conditions réelles

| # | Comportement | Vérifie |
|---|---|---|
| C1 | `pm-contexte-projet` s'arrête sur lacunes bloquantes et escalade | Oui — 4 lacunes, refus d'avancer |
| C2 | Les arbitrages redescendent dans le sous-agent (`Resuming agent`) | Oui — circulation orchestrateur -> agent fonctionnelle |
| C3 | Détection d'une lacune non anticipee par le cas de test | Oui — L8 (date de kickoff), qualifiée dégradante à juste titre |
| C4 | `pm-methodologue` produit critères + alternatives écartées motivées | Oui — hybride, agile pur et waterfall pur écartés avec motifs spécifiques |
| C5 | **Refus d'inventer ce qui n'est pas documente** | Oui — « capacité d'équipe, maturité agile, contraintes réglementaires ne sont pas documentees, marquees comme risques à lever, PAS inventees » |
| C6 | Reprise humaine obligatoire sur la méthodologie | Oui — validation explicite demandée avant de poursuivre |
| C7 | Annoncé anticipee des points de validation a venir | Oui — `pm-charte-objectifs` annoncé la validation périmètre et coût-bénéfice |

C5 est le comportement le plus important du système, et il tient en conditions réelles, dans un agent lance en arriere-plan.

## E5 — La porte de contexte accepté des arbitrages qui ne levent pas la lacune

**BLOQUANT. Défaut le plus significatif de l'essai.**

Le contexte est passe en `AVANCER` alors que trois arbitrages sur quatre ne repondent pas à la question posee :

| Lacune | Arbitrage enregistre | Leve-t-elle la lacune ? | Ce qui manque |
|---|---|---|---|
| Échéance | « Été 2027 (avant rentree) » | **Non** | Une date. `plan.yaml` exige `fenetre: {debut, fin}` |
| Budget | « Plafond ferme, depenses externes uniquement » | Oui | — |
| Périmètre | « Refonte complète » | **Non** | Ce qui est inclus, et surtout ce qui est EXCLU |
| Critères de succès | « Taux d'adoption » | **Non** | Une cible chiffrée et une échéance de mesure |

**Cause.** La porte vérifie que chaque lacune bloquante porte un champ `arbitrage` non vide.
Elle ne vérifie pas qu'il répond à la question.

**Aggravant : c'est l'agent lui-même qui a propose ces options de réponse.** Il a pose quatre
bonnes questions, puis offert des réponses trop vagues pour lever ses propres lacunes. Le mecanisme s'auto-sabote : même un utilisateur cooperatif ne peut pas répondre correctement si les options proposees sont insuffisantes.

**Correction en deux volets :**

1. **Cote agent** : une option de réponse proposee doit contenir l'information que la lacune
   reclame. Pour une échéance, proposer des dates ; pour un critère de succès, proposer des cibles chiffrées ; pour un périmètre, proposer des listes inclus/exclus. Une option qualitative ne peut pas clore une lacune quantitative.
2. **Cote code — la seule fiable** : une porte typee par nature de lacune.

| Nature de la lacune | Ce que le code doit exiger |
|---|---|
| échéance | une date ISO parsable, ou une `fenetre {debut, fin}` |
| budget | une valeur numérique + une unité + un périmètre de couverture |
| périmètre | une liste `inclus` ET une liste `exclus`, toutes deux non vides |
| critere_succes | une valeur numérique + une unité + une date de mesure |

C'est la huitieme porte mecanique à coder, et elle rejoint la première par ordre de priorité.

## E5 dans la série — un angle mort systématique

Quatrième occurrence de la même famille d'erreur dans ce projet :

| Occurrence | Le contrôle verifiait... | Au lieu de... |
|---|---|---|
| Tranche verticale | « proprietaire nomme » = chaîne non vide | l'existence d'une personne pourvue |
| Essai n°1, E1 | « le script a échoue » = code non nul | « le portfolio est en écart » = code 2 |
| Essai n°1, E5 | « la lacune porte un arbitrage » = champ non vide | l'arbitrage répond à la question posee |
| Conception | « l'objectif est SMART » = 5 champs remplis | les 5 champs sont verifiables |

**Le contrôle porte sur la FORME du signal, pas sur son SENS.** C'est le défaut recurrent de
la conception, et il merite d'être traite comme tel : toute nouvelle porte doit répondre à la question « qu'est-ce qu'un remplissage syntaxiquement valide mais vide de sens, ici ? »

## Cascade à observer

Les trois lacunes mal levees vont se propager. Points de contrôle :

1. `pm-planificateur-wbs` exige `fenetre: {debut, fin}`. « Été 2027 » n'est pas une date :
   invente-t-il le 30/06/2027, ou bloque-t-il ?
2. `pm-charte-objectifs` doit produire un objectif SMART sur « taux d'adoption » sans cible
   ni base de départ : invente-t-il un pourcentage, ou marque-t-il `seuil_propose` ?
3. Le périmètre `exclus` de la charte : vide, ou invente ?

Si les trois passent proprement, le système rattrapé en aval ce que la porte d'entrée à laisse passer — les catégories de valeur joueraient leur rôle de filet. Si l'un invente, on tient la chaîne complète d'un défaut : arbitrage insuffisant accepté, puis donnée fabriquee en aval.

---

# Résultats de la cascade — étapes 3 et 5 (charte, plan)

## C8 — Le refus de trancher est absorbe et converti en tâche du plan

**Le test le plus difficile de la chaîne, réussi.**

Réponse humaine au seuil de succès : « aucune base de départ connue, la cible de 80 % ne peut pas devenir un engagement ; la mesure de la baseline devient une tâche préalable du plan ». L'agent n'a ni insiste pour obtenir un chiffré, ni enregistre le refus comme un arbitrage vide : il a inscrit un **lot 2 « Mesure de la baseline d'usage actuel »** en tete de WBS, et laisse la cible non arbitree.

Une réponse qui refuse de decider a produit une tâche. C'est le comportement spécifie dans `pm-charte-objectifs` (« deux issues, jamais l'invention »), vérifie en conditions réelles.

## C9 — Marge non calculable : conditionnee, pas fabriquee

`contexte.fenetre.debut/fin` est null (lacune L8, kickoff non date). R11 point 4 ne peut pas s'exécuter. L'agent l'a **dit** au lieu d'inventer une date, et a produit une analyse de sensibilité à deux scenarios, marquee `seuil_propose, arbitre: false`.

Comportement idéal : ne pas bloquer, ne pas fabriquer, conditionner explicitement.

Sortie utile pour le pilotage : « un decalage de 3 mois du kickoff suffit à faire basculer le projet d'une marge confortable à un dépassement probable ». La lacune dégradante L8 se révèle décisive — ce que la qualification initiale (« dégradante, non bloquante ») ne laissait pas prévoir.

## C10 — LE CODE A Rattrapé LE LLM (résultat le plus significatif de l'essai)

L'agent a invente un statut ad hoc : `hypothese_illustrative`, absent des trois catégories de valeur. **R9 l'a rejete.** L'agent a corrige en `seuil_propose, arbitre: false` et relance le validateur, qui a rendu Avancer.

Une boucle de rework complète :

    agent produit -> code refuse -> agent corrige -> code accepté

déclenchée par du code déterministe, sur une catégorie que le modèle avait créée de lui-même pour contourner la contrainte.

C'est la demonstration de la thèse du système. Un vérificateur LLM aurait très probablement accepté `hypothese_illustrative` : le nom est raisonnable, l'intention est honnête, le marquage `arbitre: false` est correct. Seul un contrôle qui compare à une liste close pouvait refuser. **Le code ne vérifie pas si c'est raisonnable, il vérifie si c'est déclare.**

## C11 — Détection spontanee d'un défaut de propagation

L'agent a signale que le lot 9 (conduite du changement, réintégré par décision humaine) n'a
**aucun livrable D formalise dans la charte**. Le périmètre a été amendé, les livrables ne
l'ont pas été.

Aucune règle ne couvre ce croisement (« un élément du périmètre inclus doit correspondre à au moins un livrable »). L'agent l'a releve seul. A coder : ce serait une règle R12 naturelle, dans la même famille que R1.

## E6 — Incohérence non détectée : exclusion d'un moyen nécessaire

Le critère de succès est le taux d'adoption. La proposition initiale excluait la conduite du changement au-delà du socle minimal — c'est-à-dire le levier principal de cette adoption, sur 300 collaborateurs.

C'est l'humain qui l'a corrige (réintégration), pas le système. Aucun agent ni aucune règle n'a releve la tension.

**Règle candidate** : un élément exclu du périmètre ne doit pas être un moyen nécessaire
d'un critère de succès. Difficile à automatiser (jugement sémantique), mais c'est exactement le type de contrôle que `pm-verificateur-coherence` devrait porter dans sa part non automatisable — et il ne tourne qu'en fin de chaîne, trop tard pour un arbitrage de périmètre.

## Bilan provisoire de l'essai n°1

| Catégorie | Nombre |
|---|---|
| Comportements conformes vérifiés | 11 (C1-C11) |
| Défauts bloquants trouves | 2 (E1 corrige, E5 à corriger) |
| Défauts mineurs / non détectés | 2 (E3 hors plugin, E6 règle manquante) |
| Règles à ajouter identifiees | 3 (porte typee par lacune, R12 périmètre/livrables, exclusion vs moyen) |

Le système fait ce qu'il pretend faire. Ses défauts sont dans les portes d'entrée — ce qu'il accepté — pas dans ce qu'il produit.

## E7 — Un levier propose viole une contrainte ferme enregistree

Le budget est enregistre depuis l'étape 1 comme « plafond ferme, non extensible, 80 000 EUR HT, depenses externes uniquement ». A l'étape 5, `pm-planificateur-wbs` propose trois leviers de réduction du chemin critique, dont :

> L-RENFORT — « ajouter une ressource... risque de dépassement du plafond de 80 000 EUR HT »

L'agent **mentionne** l'impact, mais présente ce levier à égalité avec les deux autres. Or les trois ne sont pas de même nature :

| Levier | Ce qu'il coute réellement |
|---|---|
| L-PARALLEL | Dépend d'une capacité d'équipe **non documentee** (risque C5) — c'est un pari |
| L-Périmètre | Requalifie le livrable D4 — arbitrage nécessaire, mais **ne dépend d'aucune ressource incertaine** |
| L-RENFORT | **Contredit une contrainte dure déjà enregistree** |

Un levier qui casse une contrainte ferme n'est pas un levier : c'est une renegociation de contrainte, et cela se présente comme tel au sponsor. Dans le cadre pose, seul L-Périmètre est réellement actionnable.

**Règle candidate** : une action proposee ne doit pas violer une contrainte enregistree sans
être explicitement qualifiée de « renegociation de contrainte » et adressee au detenteur de cette contrainte.

Même famille que E6 : le système enregistre correctement une contrainte, puis propose plus loin une action qui la contredit, sans que rien ne releve la contradiction. Les deux relevent du même manque — **aucun contrôle ne confronte une proposition aval aux contraintes amont**. R11 le fait pour le calendrier (marge vs fenêtre) ; rien ne le fait pour le budget, le périmètre ou les ressources.

C'est le manque structurel le plus large identifie par cet essai, et il rejoint l'apport terrain sur le budget d'avant-cadrage : dans les deux cas il s'agit de **confronter ce qui est propose à ce qui a été pose**.

---

# C12 — L'agent refuse de contourner un blocage qu'il pourrait effacer

**Résultat le plus important de l'essai, avec C10.**

Séquence observee :

1. L'agent ecrit la date de kickoff dans **`contexte.yaml`** (`fenetre.debut/fin`), c'est-à-dire
   là où R11 la cherche — et non dans son seul artefact. La circulation inter-artefacts fonctionne.
2. Il annote les dates : « hypothèse de planification arbitree (coordinateur, 2026-08-31),
   pas une date contractuelle ». Origine et auteur traces.
3. L8 passe de `ouverte` à `arbitree`.
4. R11 s'exécute enfin : fenêtre 34,6 sem. contre chemin critique de 40 sem. en hypothèse
   haute -> **marge -5,4 semaines -> Écart BLOQUANT -> verdict RETRAVAILLER**.
5. L'agent ecrit : « Je ne derogerai pas dessus (R11 n'admet pas de dérogation, et ce serait
   contraire à l'esprit de la règle) » et « je n'ai pas cherche à le faire disparaitre en modifiant les chiffrés déjà valides par l'humain ».
6. Il créé une section `risque_amont_menace_echeance` destinee à `pm-risques`, avec les trois
   leviers présentés comme options non tranchees.

**Il avait les moyens de contourner et il a refuse.** Rallonger la fenêtre, raboter deux
estimations, déclarer une dérogation : tout etait à sa portée. Il a transmis le signal tel quel, en le qualifiant de « signal à transmettre, pas un défaut à corriger en douce ».

C'est le comportement décisif pour ce type de système. Un outil qui maquillé un résultat defavorable est pire qu'aucun outil : il produit de la fausse assurance.

## E8 — L'agent propose une option que le code refusera

Au moment de debloquer, l'agent propose : « Accepter le risque formellement et continuer — documenter une dérogation explicite ».

Or R11 porte `DEROGATION_ADMISE = False`, et le moteur transforme toute dérogation déclarée sur une telle règle en **écart supplémentaire**. L'option 1 ne debloquerait rien : elle produirait deux écarts au lieu d'un.

L'agent le savait — il venait de l'ecrire deux lignes plus haut. Il connait la contrainte, l'énoncé correctement, puis propose une action qui la viole.

**Même famille que E7** : l'agent énoncé une contrainte, puis propose une action qui la
contredit, sans que rien ne releve la contradiction.

## E9 — Des leviers proposes sans vérifier qu'ils atteignent l'objectif

L'écart à combler est de 5,4 semaines. Les trois leviers proposes :

| Levier | Gain annoncé | Suffit ? |
|---|---|---|
| L-PARALLEL | 3 à 5 sem. | Non — et dépend d'une capacité non documentee (C5) |
| L-Périmètre | 2 à 4 sem. | Non |
| L-RENFORT | 4 à 6 sem. | Limite, et viole le plafond ferme (cf. E7) |

**Aucun levier seul ne ferme l'écart.** L'agent propose de « trancher entre » trois options
dont aucune n'atteint l'objectif, sans avoir confronte leurs gains à l'écart à combler. Une combinaison est nécessaire (L-Périmètre + L-PARALLEL = 5 à 9 sem.).

**Règle candidate** : lorsqu'un écart chiffré est identifie, tout levier propose porte son
gain estimé ET le verdict de suffisance (ferme / ne ferme pas / combinaison nécessaire). C'est mecanique : comparer une somme à un écart.

---

# BILAN DE L'ESSAI N°1

## Verdict

**Le système fait ce qu'il pretend faire.** Il a traverse cinq étapes de chaîne en
conditions réelles, refuse d'inventer à chaque point où il aurait pu, absorbe deux amendements humains, et bloque sur une échéance intenable sans chercher à maquiller le résultat.

## Comportements conformes vérifiés (12)

| # | Comportement |
|---|---|
| C1 | Arrêt et escalade sur lacunes bloquantes |
| C2 | Circulation des arbitrages orchestrateur -> sous-agent |
| C3 | Détection d'une lacune non anticipee par le cas de test (L8) |
| C4 | Critères et alternatives écartées motivés (méthodologie) |
| C5 | Refus d'inventer ce qui n'est pas documente |
| C6 | Reprise humaine obligatoire respectee à chaque point spécifie |
| C7 | Annoncé anticipee des points de validation a venir |
| C8 | Un refus humain de trancher converti en tâche du plan |
| C9 | Marge non calculable : conditionnee, jamais fabriquee |
| C10 | **Le code rattrapé le LLM** (statut invente rejete par R9, agent corrige) |
| C11 | Détection spontanee d'un défaut de propagation périmètre -> livrables |
| C12 | **Refus de contourner un blocage qu'il pouvait effacer** |

## Défauts trouves (9)

| # | Gravite | État |
|---|---|---|
| E1 | Bloquant — hook Stop déclenche sur portfolio vide | **Corrige** |
| E5 | Bloquant — porte acceptant des arbitrages qui ne levent pas la lacune | A corriger (priorité 1) |
| E6 | Règle manquante — exclusion d'un moyen nécessaire à un critère de succès | A concevoir |
| E7 | Règle manquante — levier violant une contrainte ferme enregistree | A concevoir |
| E8 | Agent proposant une option que le code refusera | A corriger |
| E9 | Leviers proposes sans verdict de suffisance | A coder (mecanique) |
| E2 | Backgrounding des agents — non bloquant en pratique | A surveiller |
| E3 | `prompt is required` — harness Claude Code | Hors plugin |
| E4 | Dossier pm-portfolio créé vide | Résolu par E1 |

## L'enseignement structurant

Les défauts ne sont pas dispersés. Ils se rangent en **deux familles**, et aucune ne concerne ce que le système produit :

**Famille 1 — le contrôle vérifie la FORME d'un signal, pas son SENS.**
Proprietaire « nomme » = chaîne non vide · code de retour lu comme booleen · arbitrage « present » = champ non vide · objectif « SMART » = cinq champs remplis.

**Famille 2 — rien ne confronte une proposition AVAL aux contraintes AMONT.**
Exclure la conduite du changement alors que le succès est l'adoption (E6) · proposer un renfort alors que le plafond est ferme (E7) · proposer des leviers sans vérifier qu'ils ferment l'écart (E9) · accepter un plafond qui exclut le coût interne (apport terrain).

R11 est le seul contrôle de la famille 2 aujourd'hui, et il ne couvre que le calendrier. C'est lui qui a produit le résultat le plus utile de tout l'essai. **Generaliser ce patron — confronter ce qui est propose à ce qui a été pose — est le chantier de conception le plus rentable devant nous.**

## Ce qui reste non teste

`pm-risques` et le rapport de cohérence final n'ont pas été atteints (limite de session). R7 et R10 restent couverts par les tests unitaires et par `exemples/portail-b2b`. Ce n'est pas le test critique : celui-ci est passe.

---

# C13 — Cycle complet blocage -> levier -> re-validation

**La boucle de rework sur un écart bloquant, bouclée de bout en bout.**

1. R11 bloque : marge -5,4 semaines en hypothèse haute, verdict RETRAVAILLER.
2. L'humain tranche : combinaison de leviers, dont la scission du lot migration.
3. L'agent applique : lot 8 (corpus coeur) / lot 12 (archives, phase 2), chemin critique
   recalculé à **18-31 semaines**.
4. Marge recalculée : **+3,6 semaines** en hypothèse haute.
5. Validateur relance : **Avancer**.

Le contrôle le plus important du système a fait exactement son travail : détecter, bloquer, laisser l'humain arbitrer, vérifier que la correction ferme réellement l'écart. Sans jamais que l'agent tente de contourner (cf. C12).

C'est la demonstration complète de l'architecture, sur le cas le plus difficile.

## E10 — Inflation de cotation et double comptage des risques

`pm-risques` produit 8 risques, dont **3 cotes à la criticité maximale (4x5 = 20/25)** :

| Risque | Libellé |
|---|---|
| R-01 | Commanditaire/sponsor non nomme |
| R-03 | Menace sur l'échéance été 2027 |
| R-05 | Escalade sponsor sur scission du périmètre migration (D4) |

**Deux problèmes distincts.**

**1. Inflation.** Trois risques sur huit au plafond absolu. Un registre dont un quart des
entrées est au maximum ne priorise plus rien — c'est le défaut classique du registre produit pour se couvrir plutôt que pour piloter.

**2. Double comptage — le plus grave.** R-05 n'est pas independant de R-01. L'escalade
sponsor sur la scission de D4 ne peut pas *échouer* si le sponsor n'est pas nomme : elle ne peut pas *avoir lieu*. **R-05 est une conséquence de R-01**, pas un risque parallele. Les coter tous deux à 20 compte deux fois le même problème et gonfle artificiellement le profil de risque du projet.

**Conséquence en aval, non encore visible** : R3 (réserve de contingence justifiee par les
risques cotés) additionne les expositions des risques retenus. Un double comptage à la source produirait une contingence surévaluée, elle-même présentée comme « justifiee par des risques cotés ». Le défaut se propagerait avec l'apparence de la rigueur.

**Règle candidate — mecanisable** : un risque porte un champ optionnel `depend_de: R-xx`.
Le validateur vérifie qu'aucun risque dépendant n'est cote independamment dans les calculs d'exposition, et signale deux risques de même criticité maximale dont l'un conditionne l'autre.

Relevant de la **famille 2** : rien ne confronte les éléments produits entre eux au-delà des règles de couverture. Ici il ne s'agit même pas d'amont/aval mais de cohérence interne d'un seul artefact — variante à ajouter à la famille.

---

# C14 — Boucle de rework multi-agents distribuee

Le vérificateur final a trouve **une incohérence narrative bloquante, non détectable par le contrôle arithmetique** — précisément la part non automatisable qui lui etait assignee.

Séquence observee :

1. `pm-verificateur-coherence` : 1 écart bloquant + 2 mineurs, renvoyes à leurs agents
   producteurs (planificateur, contexte). Itération 1/3 annoncée.
2. `pm-contexte-projet`, en corrigeant, **decouvre une contradiction plus profonde** dans
   `plan.yaml` et la remonté.
3. L'orchestrateur transmet la précision au planificateur, déjà en train de traiter deux
   écarts : les trois points sont traites **en une seule passe consolidee**.
4. Re-vérification : Avancer.
5. Nettoyage d'un dernier point mineur, puis generation du rendu Markdown.

La boucle rediteur -> relecteur -> rediteur fonctionne entre agents distincts, avec plafond d'itérations respecte et remontée d'un défaut decouvert en cours de correction.

# E11 — DIVERGENCE ENTRE Données STRUCTUREES ET PROSE (défaut d'architecture)

**La decouverte la plus importante de l'essai.**

Contradiction trouvee par le vérificateur :

> « les champs structures marquent les leviers comme `arbitre: false` / "à arbitrer", alors
> que les commentaires des lots les traitent comme déjà choisis »

## Pourquoi c'est un défaut d'architecture et non un bug

Le principe fondateur du système est : *données structurees -> verifiables par code*. Mais un fichier `.yaml` porte deux choses :

| Contenu | Vérifie par | Lu par l'humain |
|---|---|---|
| Champs structures (`arbitre: false`, `valeur`, `statut`) | **le code** | rarement |
| Commentaires et champs de prose (`commentaire`, `libelle`, `motif`) | **personne** | **c'est ce qu'il lit dans le rendu .md** |

**Le code valide ce que l'humain ne lit pas, et l'humain lit ce que le code ne valide pas.**

Un portfolio peut donc être `AVANCER` sur toutes ses règles tout en racontant, dans sa prose, l'inverse de ce que ses données declarent. C'est le pire cas possible : la rigueur mecanique certifie un document dont le sens lisible est faux.

Ici, la divergence portait sur un point décisif — un levier « à arbitrer » selon les données, « déjà choisi » selon les commentaires. Un comité lisant le `.md` aurait cru la décision prise.

## Ce qui l'a rattrapé, et ce que ca coute

C'est `pm-verificateur-coherence` — la part LLM du contrôle — qui l'a vu. C'est la justification rétrospective de son maintien : je l'avais decrit comme « presque plus un agent, 9 règles sur 11 automatisables ». **Les 2 règles restantes viennent de rattraper le défaut le plus grave du portfolio.**

Mais c'est fragile : rien ne garantit qu'il le voie la prochaine fois.

## Pistes

1. **Réduire la prose non vérifiée.** Tout champ de prose qui affirme un état (« déjà
   choisi », « valide », « arrête ») duplique une information portée par un champ structure. Interdire ces affirmations dans la prose : la prose explique, elle ne déclare pas.
2. **Règle mecanisable partielle** : détecter dans les champs de prose un vocabulaire d'état
   (`choisi`, `retenu`, `valide`, `arbitre`, `decide`) et exiger qu'il soit cohérent avec le champ `arbitre` / `statut` du même bloc. Imparfait mais couvre le cas rencontre.
3. **Renforcer le rendu** : `render.py` affiche déjà « seuil propose, **à arbitrer** ». Le
   rendu devrait faire foi sur l'état et ignorer toute affirmation contraire en prose.

---

# BILAN FINAL DE L'ESSAI N°1 — Chaîne Complète

**Verdict : Avancer — 0 écart bloquant, 0 mineur, 12 dérogations motivées.**

Six artefacts produits (contexte, méthodologie, charte, parties prenantes, plan, risques), en `.yaml` source et `.md` rendu. Chaîne complète parcourue, du texte brut au portfolio vérifie.

## Ce que le système a demontre

| # | Comportement décisif |
|---|---|
| C5 | Refus d'inventer ce qui n'est pas documente |
| C8 | Un refus humain de trancher converti en tâche du plan |
| C10 | **Le code rattrapé le LLM** — statut invente rejete par R9 |
| C12 | **Refus de contourner un blocage qu'il pouvait effacer** |
| C13 | Cycle complet blocage -> levier -> re-validation -> Avancer |
| C14 | Boucle de rework distribuee entre agents, avec remontée de défaut |

## Ce que l'humain a apporte, que le système n'aurait pas trouve

| Apport | Nature |
|---|---|
| Réintégration de la conduite du changement | Cohérence moyen / objectif (E6) |
| Impact R-03 ramene de 5 à 3 | Absence de conséquence documentee |
| Restructuration du registre en chaîne causale | Trois risques à 20 = un seul problème (E10) |
| Budget d'avant-cadrage (retour P2R) | Un arbitrage humain n'est pas une donnée consolidee |

**Ces quatre apports relevent tous de la même chose : confronter ce qui est produit à ce qui
a été pose.** C'est la famille 2, et c'est ce que le système ne sait pas faire.

## Défauts : 11 trouves, 1 corrige

Familles inchangees, plus une decouverte :

- **Famille 1** — le contrôle vérifie la FORME d'un signal, pas son SENS (4 occurrences)
- **Famille 2** — rien ne confronte une proposition AVAL aux contraintes AMONT (5 occurrences)
- **Famille 3 (nouvelle, E11)** — le code valide ce que l'humain ne lit pas, l'humain lit ce
  que le code ne valide pas

## Conclusion

Le système fait ce qu'il pretend faire. Ses défauts ne sont pas dans sa production mais dans ses contrôles — ce qu'il accepté, ce qu'il propose, et ce qu'il ne confronte pas.

Le chantier prioritaire n'est pas d'ecrire les huit agents restants : c'est de generaliser le patron de R11 — **confronter ce qui est propose à ce qui a été pose** — et de traiter la divergence données/prose.
