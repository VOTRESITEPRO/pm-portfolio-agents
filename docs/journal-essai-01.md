# Journal d'essai n°1 — premier run reel

Environnement : Windows, Python 3.14.2 (`py -3`), Claude Code v2.1.234, Sonnet 5.
Projet de test : `C:\Users\letra\test-pm`, vide.
Entree : « Refonte de l'intranet documentaire, environ 300 collaborateurs, budget evoque
autour de 80 k, pret l'an prochain. » — 3 lacunes bloquantes volontaires.

| # | Ce qui s'est passe | Attendu | Cause | Statut |
|---|---|---|---|---|
| E1 | Le hook `Stop` bloque avec « Aucun artefact dans pm-portfolio » | Ne rien faire tant que le portfolio est vide | `hook.py` traitait tout code de retour non nul comme un ecart. Or `validate.py` renvoie 1 pour « rien a valider » et 2 pour « ecart bloquant ». | **Corrige** — seul le code 2 bloque desormais |
| E2 | `pm-contexte-projet` est lance en **arriere-plan** par Claude Code | Premier plan : l'agent doit poser ses questions et attendre les arbitrages | Rien dans le skill ni le frontmatter n'interdit le backgrounding. | **Non bloquant** — l'agent a remonte ses questions malgre le mode arriere-plan |
| E3 | `Error: prompt is required when stop is not true` | — | Erreur du harness Claude Code, hors plugin | Sans objet |
| E4 | Le dossier `pm-portfolio/` a ete cree vide avant toute production | Acceptable | Consequence de E1, sans gravite propre | Resolu par E1 |

## Enseignement de E1

Un code de retour a trois valeurs distinctes (0 / 1 / 2) lu comme un booleen (0 / non-zero).
La porte qualite se declenchait donc sur une condition qui n'en est pas une.

C'est la meme famille d'erreur que celles trouvees jusqu'ici : **un controle qui verifie la
forme d'un signal plutot que son sens**. La porte de sortie qui validait « proprietaire
nomme » verifiait une chaine de caracteres, pas une personne ; ici le hook verifiait « le
script a echoue », pas « le portfolio est en ecart ».

## Resultat du test principal — REUSSI

`pm-contexte-projet` **s'est arrete et a pose ses questions** au lieu de produire un
contexte complet. Il a identifie **quatre** lacunes bloquantes la ou le cas de test n'en
comportait volontairement que trois : echeance, budget, criteres de succes — plus le
**perimetre**, que la conception du cas de test avait laisse passer.

C'est le seul comportement du systeme qu'aucun test unitaire ne pouvait couvrir, et le seul
qui justifie toute l'architecture. Un agent qui aurait rempli le budget, l'echeance et
l'objectif par plausibilite aurait produit un portfolio entierement credible et entierement
faux.

## E2 — a surveiller malgre tout

Le mode arriere-plan n'a pas empeche le dialogue cette fois. Rien ne garantit que ce soit
systematique : le comportement depend de l'orchestration de Claude Code, pas du plugin.

La mitigation robuste ne consiste pas a interdire le backgrounding — elle consiste a rendre
le controle **independant du mode d'execution** : une porte codee qui refuse tout
`contexte.yaml` comportant une lacune bloquante au statut `ouverte`, ou une lacune bloquante
`arbitree` sans texte d'arbitrage.

C'est l'une des sept portes mecaniques non encore codees
(voir `ECARTS-SPEC-IMPLEMENTATION.md`), et l'essai vient de montrer que c'est la plus
prioritaire des sept : elle protege le comportement le plus important du systeme, qui ne
repose aujourd'hui que sur la discipline d'un prompt.

## Suite du test — a observer

Reponses fournies : echeance 30/06/2027 ferme · budget 80 k EUR plafond vote · perimetre
consultation et recherche documentaire + migration, hors GED et hors mobile natif ·
succes 70 % des 300 collaborateurs en utilisateurs actifs mensuels a 3 mois.

Point d'observation suivant : la cible de 70 % est chiffree mais **sans base de depart
connue**. `pm-charte-objectifs` doit soit transformer la mesure initiale en tache du plan,
soit marquer la cible `seuil_propose`. S'il invente un taux d'usage actuel, la regle R9 doit
le rattraper.

---

# Apport terrain — a traiter apres le test (2026-08-31)

**Source : Yannick, experience P2R.** Budget evoque au depart : 80 k EUR. Cout final :
~370 k EUR. Facteur 4,6. Motif : le chiffre initial precedait le cadrage et ne tenait pas
compte de ce qui devait reellement etre fait.

## Le manque que cela revele

`pm-contexte-projet` qualifie correctement un budget « evoque, non arbitre » en lacune
bloquante. Mais des que l'humain repond « 80 k, plafond vote », le systeme l'enregistre en
`statut: source` et **construit tout le portfolio dessus**. Un arbitrage humain est traite
comme une donnee definitive.

Or un budget arbitre AVANT le WBS n'est pas une donnee : c'est une hypothese. Il ne devient
une donnee qu'une fois confronte a une estimation ascendante.

Les trois categories de valeur ne couvrent pas ce cas :

| Categorie | Ce qu'elle capture | Ce qu'elle rate ici |
|---|---|---|
| `source` | tracable vers le contexte ou un arbitrage | un arbitrage peut etre faux d'un facteur 4,6 |
| `seuil_propose` | proposition de pilotage a arbitrer | ce n'est pas un seuil, c'est un cadre |
| `a_sourcer` | donnee absente | la donnee n'est pas absente, elle est prematuree |

## Pistes de correction

1. **Quatrieme statut** : `arbitre_avant_cadrage` — valeur fournie par l'humain, mais
   antérieure a toute estimation ascendante. Se comporte comme `source` pour la production,
   mais reste marquee comme non consolidee dans les artefacts.
2. **Regle de confrontation** (a implementer dans `pm-budget-achats`, agent non encore
   ecrit) : comparer systematiquement le budget bottom-up issu de la WBS au budget cadre.
   Un ecart majeur est un **ecart bloquant remontant au sponsor**, pas une note de bas de
   page. C'est le moment ou le cadre devient une donnee — ou est refute.
3. Applicable au-dela du budget : une echeance « evoquee » avant le chemin critique releve
   de la meme categorie. R11 fait deja cette confrontation pour le calendrier (marge reelle
   vs fenetre) ; l'equivalent budgetaire n'existe pas.

## Pourquoi ca compte

C'est un apport d'experience terrain, pas de conception. Un systeme qui accepte sans
broncher un budget d'avant-cadrage produit un portfolio coherent avec une contrainte fausse
— et perd sa credibilite en mission au premier comite de pilotage.

---

# Observations en cours de chaine

## Comportements CONFORMES verifies en conditions reelles

| # | Comportement | Verifie |
|---|---|---|
| C1 | `pm-contexte-projet` s'arrete sur lacunes bloquantes et escalade | Oui — 4 lacunes, refus d'avancer |
| C2 | Les arbitrages redescendent dans le sous-agent (`Resuming agent`) | Oui — circulation orchestrateur -> agent fonctionnelle |
| C3 | Detection d'une lacune non anticipee par le cas de test | Oui — L8 (date de kickoff), qualifiee degradante a juste titre |
| C4 | `pm-methodologue` produit criteres + alternatives ecartees motivees | Oui — hybride, agile pur et waterfall pur ecartes avec motifs specifiques |
| C5 | **Refus d'inventer ce qui n'est pas documente** | Oui — « capacite d'equipe, maturite agile, contraintes reglementaires ne sont pas documentees, marquees comme risques a lever, PAS inventees » |
| C6 | Reprise humaine obligatoire sur la methodologie | Oui — validation explicite demandee avant de poursuivre |
| C7 | Annonce anticipee des points de validation a venir | Oui — `pm-charte-objectifs` annonce la validation perimetre et cout-benefice |

C5 est le comportement le plus important du systeme, et il tient en conditions reelles, dans
un agent lance en arriere-plan.

## E5 — La porte de contexte accepte des arbitrages qui ne levent pas la lacune

**BLOQUANT. Defaut le plus significatif de l'essai.**

Le contexte est passe en `AVANCER` alors que trois arbitrages sur quatre ne repondent pas a
la question posee :

| Lacune | Arbitrage enregistre | Leve-t-elle la lacune ? | Ce qui manque |
|---|---|---|---|
| Echeance | « Ete 2027 (avant rentree) » | **Non** | Une date. `plan.yaml` exige `fenetre: {debut, fin}` |
| Budget | « Plafond ferme, depenses externes uniquement » | Oui | — |
| Perimetre | « Refonte complete » | **Non** | Ce qui est inclus, et surtout ce qui est EXCLU |
| Criteres de succes | « Taux d'adoption » | **Non** | Une cible chiffree et une echeance de mesure |

**Cause.** La porte verifie que chaque lacune bloquante porte un champ `arbitrage` non vide.
Elle ne verifie pas qu'il repond a la question.

**Aggravant : c'est l'agent lui-meme qui a propose ces options de reponse.** Il a pose quatre
bonnes questions, puis offert des reponses trop vagues pour lever ses propres lacunes. Le
mecanisme s'auto-sabote : meme un utilisateur cooperatif ne peut pas repondre correctement
si les options proposees sont insuffisantes.

**Correction en deux volets :**

1. **Cote agent** : une option de reponse proposee doit contenir l'information que la lacune
   reclame. Pour une echeance, proposer des dates ; pour un critere de succes, proposer des
   cibles chiffrees ; pour un perimetre, proposer des listes inclus/exclus. Une option
   qualitative ne peut pas clore une lacune quantitative.
2. **Cote code — la seule fiable** : une porte typee par nature de lacune.

| Nature de la lacune | Ce que le code doit exiger |
|---|---|
| echeance | une date ISO parsable, ou une `fenetre {debut, fin}` |
| budget | une valeur numerique + une unite + un perimetre de couverture |
| perimetre | une liste `inclus` ET une liste `exclus`, toutes deux non vides |
| critere_succes | une valeur numerique + une unite + une date de mesure |

C'est la huitieme porte mecanique a coder, et elle rejoint la premiere par ordre de priorite.

## E5 dans la serie — un angle mort systematique

Quatrieme occurrence de la meme famille d'erreur dans ce projet :

| Occurrence | Le controle verifiait... | Au lieu de... |
|---|---|---|
| Tranche verticale | « proprietaire nomme » = chaine non vide | l'existence d'une personne pourvue |
| Essai n°1, E1 | « le script a echoue » = code non nul | « le portfolio est en ecart » = code 2 |
| Essai n°1, E5 | « la lacune porte un arbitrage » = champ non vide | l'arbitrage repond a la question posee |
| Conception | « l'objectif est SMART » = 5 champs remplis | les 5 champs sont verifiables |

**Le controle porte sur la FORME du signal, pas sur son SENS.** C'est le defaut recurrent de
la conception, et il merite d'etre traite comme tel : toute nouvelle porte doit repondre a la
question « qu'est-ce qu'un remplissage syntaxiquement valide mais vide de sens, ici ? »

## Cascade a observer

Les trois lacunes mal levees vont se propager. Points de controle :

1. `pm-planificateur-wbs` exige `fenetre: {debut, fin}`. « Ete 2027 » n'est pas une date :
   invente-t-il le 30/06/2027, ou bloque-t-il ?
2. `pm-charte-objectifs` doit produire un objectif SMART sur « taux d'adoption » sans cible
   ni base de depart : invente-t-il un pourcentage, ou marque-t-il `seuil_propose` ?
3. Le perimetre `exclus` de la charte : vide, ou invente ?

Si les trois passent proprement, le systeme rattrape en aval ce que la porte d'entree a
laisse passer — les categories de valeur joueraient leur role de filet. Si l'un invente, on
tient la chaine complete d'un defaut : arbitrage insuffisant accepte, puis donnee fabriquee
en aval.

---

# Resultats de la cascade — etapes 3 et 5 (charte, plan)

## C8 — Le refus de trancher est absorbe et converti en tache du plan

**Le test le plus difficile de la chaine, reussi.**

Reponse humaine au seuil de succes : « aucune base de depart connue, la cible de 80 % ne
peut pas devenir un engagement ; la mesure de la baseline devient une tache prealable du
plan ». L'agent n'a ni insiste pour obtenir un chiffre, ni enregistre le refus comme un
arbitrage vide : il a inscrit un **lot 2 « Mesure de la baseline d'usage actuel »** en tete
de WBS, et laisse la cible non arbitree.

Une reponse qui refuse de decider a produit une tache. C'est le comportement specifie dans
`pm-charte-objectifs` (« deux issues, jamais l'invention »), verifie en conditions reelles.

## C9 — Marge non calculable : conditionnee, pas fabriquee

`contexte.fenetre.debut/fin` est null (lacune L8, kickoff non date). R11 point 4 ne peut pas
s'executer. L'agent l'a **dit** au lieu d'inventer une date, et a produit une analyse de
sensibilite a deux scenarios, marquee `seuil_propose, arbitre: false`.

Comportement ideal : ne pas bloquer, ne pas fabriquer, conditionner explicitement.

Sortie utile pour le pilotage : « un decalage de 3 mois du kickoff suffit a faire basculer
le projet d'une marge confortable a un depassement probable ». La lacune degradante L8 se
revele decisive — ce que la qualification initiale (« degradante, non bloquante ») ne
laissait pas prevoir.

## C10 — LE CODE A RATTRAPE LE LLM (resultat le plus significatif de l'essai)

L'agent a invente un statut ad hoc : `hypothese_illustrative`, absent des trois categories
de valeur. **R9 l'a rejete.** L'agent a corrige en `seuil_propose, arbitre: false` et
relance le validateur, qui a rendu AVANCER.

Une boucle de rework complete :

    agent produit -> code refuse -> agent corrige -> code accepte

declenchee par du code deterministe, sur une categorie que le modele avait creee de
lui-meme pour contourner la contrainte.

C'est la demonstration de la these du systeme. Un verificateur LLM aurait tres
probablement accepte `hypothese_illustrative` : le nom est raisonnable, l'intention est
honnete, le marquage `arbitre: false` est correct. Seul un controle qui compare a une liste
close pouvait refuser. **Le code ne verifie pas si c'est raisonnable, il verifie si c'est
declare.**

## C11 — Detection spontanee d'un defaut de propagation

L'agent a signale que le lot 9 (conduite du changement, reintegre par decision humaine) n'a
**aucun livrable D formalise dans la charte**. Le perimetre a ete amende, les livrables ne
l'ont pas ete.

Aucune regle ne couvre ce croisement (« un element du perimetre inclus doit correspondre a
au moins un livrable »). L'agent l'a releve seul. A coder : ce serait une regle R12
naturelle, dans la meme famille que R1.

## E6 — Incoherence non detectee : exclusion d'un moyen necessaire

Le critere de succes est le taux d'adoption. La proposition initiale excluait la conduite du
changement au-dela du socle minimal — c'est-a-dire le levier principal de cette adoption,
sur 300 collaborateurs.

C'est l'humain qui l'a corrige (reintegration), pas le systeme. Aucun agent ni aucune regle
n'a releve la tension.

**Regle candidate** : un element exclu du perimetre ne doit pas etre un moyen necessaire
d'un critere de succes. Difficile a automatiser (jugement semantique), mais c'est
exactement le type de controle que `pm-verificateur-coherence` devrait porter dans sa part
non automatisable — et il ne tourne qu'en fin de chaine, trop tard pour un arbitrage de
perimetre.

## Bilan provisoire de l'essai n°1

| Categorie | Nombre |
|---|---|
| Comportements conformes verifies | 11 (C1-C11) |
| Defauts bloquants trouves | 2 (E1 corrige, E5 a corriger) |
| Defauts mineurs / non detectes | 2 (E3 hors plugin, E6 regle manquante) |
| Regles a ajouter identifiees | 3 (porte typee par lacune, R12 perimetre/livrables, exclusion vs moyen) |

Le systeme fait ce qu'il pretend faire. Ses defauts sont dans les portes d'entree — ce qu'il
accepte — pas dans ce qu'il produit.

## E7 — Un levier propose viole une contrainte ferme enregistree

Le budget est enregistre depuis l'etape 1 comme « plafond ferme, non extensible,
80 000 EUR HT, depenses externes uniquement ». A l'etape 5, `pm-planificateur-wbs` propose
trois leviers de reduction du chemin critique, dont :

> L-RENFORT — « ajouter une ressource... risque de depassement du plafond de 80 000 EUR HT »

L'agent **mentionne** l'impact, mais presente ce levier a egalite avec les deux autres. Or
les trois ne sont pas de meme nature :

| Levier | Ce qu'il coute reellement |
|---|---|
| L-PARALLEL | Depend d'une capacite d'equipe **non documentee** (risque C5) — c'est un pari |
| L-PERIMETRE | Requalifie le livrable D4 — arbitrage necessaire, mais **ne depend d'aucune ressource incertaine** |
| L-RENFORT | **Contredit une contrainte dure deja enregistree** |

Un levier qui casse une contrainte ferme n'est pas un levier : c'est une renegociation de
contrainte, et cela se presente comme tel au sponsor. Dans le cadre pose, seul L-PERIMETRE
est reellement actionnable.

**Regle candidate** : une action proposee ne doit pas violer une contrainte enregistree sans
etre explicitement qualifiee de « renegociation de contrainte » et adressee au detenteur de
cette contrainte.

Meme famille que E6 : le systeme enregistre correctement une contrainte, puis propose plus
loin une action qui la contredit, sans que rien ne releve la contradiction. Les deux
relevent du meme manque — **aucun controle ne confronte une proposition aval aux contraintes
amont**. R11 le fait pour le calendrier (marge vs fenetre) ; rien ne le fait pour le budget,
le perimetre ou les ressources.

C'est le manque structurel le plus large identifie par cet essai, et il rejoint l'apport
terrain sur le budget d'avant-cadrage : dans les deux cas il s'agit de **confronter ce qui
est propose a ce qui a ete pose**.

---

# C12 — L'agent refuse de contourner un blocage qu'il pourrait effacer

**Resultat le plus important de l'essai, avec C10.**

Sequence observee :

1. L'agent ecrit la date de kickoff dans **`contexte.yaml`** (`fenetre.debut/fin`), c'est-a-dire
   la ou R11 la cherche — et non dans son seul artefact. La circulation inter-artefacts
   fonctionne.
2. Il annote les dates : « hypothese de planification arbitree (coordinateur, 2026-08-31),
   pas une date contractuelle ». Origine et auteur traces.
3. L8 passe de `ouverte` a `arbitree`.
4. R11 s'execute enfin : fenetre 34,6 sem. contre chemin critique de 40 sem. en hypothese
   haute -> **marge -5,4 semaines -> ECART BLOQUANT -> verdict RETRAVAILLER**.
5. L'agent ecrit : « Je ne derogerai pas dessus (R11 n'admet pas de derogation, et ce serait
   contraire a l'esprit de la regle) » et « je n'ai pas cherche a le faire disparaitre en
   modifiant les chiffres deja valides par l'humain ».
6. Il cree une section `risque_amont_menace_echeance` destinee a `pm-risques`, avec les trois
   leviers presentes comme options non tranchees.

**Il avait les moyens de contourner et il a refuse.** Rallonger la fenetre, raboter deux
estimations, declarer une derogation : tout etait a sa portee. Il a transmis le signal tel
quel, en le qualifiant de « signal a transmettre, pas un defaut a corriger en douce ».

C'est le comportement decisif pour ce type de systeme. Un outil qui maquille un resultat
defavorable est pire qu'aucun outil : il produit de la fausse assurance.

## E8 — L'agent propose une option que le code refusera

Au moment de debloquer, l'agent propose : « Accepter le risque formellement et continuer —
documenter une derogation explicite ».

Or R11 porte `DEROGATION_ADMISE = False`, et le moteur transforme toute derogation declaree
sur une telle regle en **ecart supplementaire**. L'option 1 ne debloquerait rien : elle
produirait deux ecarts au lieu d'un.

L'agent le savait — il venait de l'ecrire deux lignes plus haut. Il connait la contrainte,
l'enonce correctement, puis propose une action qui la viole.

**Meme famille que E7** : l'agent enonce une contrainte, puis propose une action qui la
contredit, sans que rien ne releve la contradiction.

## E9 — Des leviers proposes sans verifier qu'ils atteignent l'objectif

L'ecart a combler est de 5,4 semaines. Les trois leviers proposes :

| Levier | Gain annonce | Suffit ? |
|---|---|---|
| L-PARALLEL | 3 a 5 sem. | Non — et depend d'une capacite non documentee (C5) |
| L-PERIMETRE | 2 a 4 sem. | Non |
| L-RENFORT | 4 a 6 sem. | Limite, et viole le plafond ferme (cf. E7) |

**Aucun levier seul ne ferme l'ecart.** L'agent propose de « trancher entre » trois options
dont aucune n'atteint l'objectif, sans avoir confronte leurs gains a l'ecart a combler. Une
combinaison est necessaire (L-PERIMETRE + L-PARALLEL = 5 a 9 sem.).

**Regle candidate** : lorsqu'un ecart chiffre est identifie, tout levier propose porte son
gain estime ET le verdict de suffisance (ferme / ne ferme pas / combinaison necessaire).
C'est mecanique : comparer une somme a un ecart.

---

# BILAN DE L'ESSAI N°1

## Verdict

**Le systeme fait ce qu'il pretend faire.** Il a traverse cinq etapes de chaine en
conditions reelles, refuse d'inventer a chaque point ou il aurait pu, absorbe deux
amendements humains, et bloque sur une echeance intenable sans chercher a maquiller le
resultat.

## Comportements conformes verifies (12)

| # | Comportement |
|---|---|
| C1 | Arret et escalade sur lacunes bloquantes |
| C2 | Circulation des arbitrages orchestrateur -> sous-agent |
| C3 | Detection d'une lacune non anticipee par le cas de test (L8) |
| C4 | Criteres et alternatives ecartees motives (methodologie) |
| C5 | Refus d'inventer ce qui n'est pas documente |
| C6 | Reprise humaine obligatoire respectee a chaque point specifie |
| C7 | Annonce anticipee des points de validation a venir |
| C8 | Un refus humain de trancher converti en tache du plan |
| C9 | Marge non calculable : conditionnee, jamais fabriquee |
| C10 | **Le code rattrape le LLM** (statut invente rejete par R9, agent corrige) |
| C11 | Detection spontanee d'un defaut de propagation perimetre -> livrables |
| C12 | **Refus de contourner un blocage qu'il pouvait effacer** |

## Defauts trouves (9)

| # | Gravite | Etat |
|---|---|---|
| E1 | Bloquant — hook Stop declenche sur portfolio vide | **Corrige** |
| E5 | Bloquant — porte acceptant des arbitrages qui ne levent pas la lacune | A corriger (priorite 1) |
| E6 | Regle manquante — exclusion d'un moyen necessaire a un critere de succes | A concevoir |
| E7 | Regle manquante — levier violant une contrainte ferme enregistree | A concevoir |
| E8 | Agent proposant une option que le code refusera | A corriger |
| E9 | Leviers proposes sans verdict de suffisance | A coder (mecanique) |
| E2 | Backgrounding des agents — non bloquant en pratique | A surveiller |
| E3 | `prompt is required` — harness Claude Code | Hors plugin |
| E4 | Dossier pm-portfolio cree vide | Resolu par E1 |

## L'enseignement structurant

Les defauts ne sont pas disperses. Ils se rangent en **deux familles**, et aucune ne concerne
ce que le systeme produit :

**Famille 1 — le controle verifie la FORME d'un signal, pas son SENS.**
Proprietaire « nomme » = chaine non vide · code de retour lu comme booleen · arbitrage
« present » = champ non vide · objectif « SMART » = cinq champs remplis.

**Famille 2 — rien ne confronte une proposition AVAL aux contraintes AMONT.**
Exclure la conduite du changement alors que le succes est l'adoption (E6) · proposer un
renfort alors que le plafond est ferme (E7) · proposer des leviers sans verifier qu'ils
ferment l'ecart (E9) · accepter un plafond qui exclut le cout interne (apport terrain).

R11 est le seul controle de la famille 2 aujourd'hui, et il ne couvre que le calendrier.
C'est lui qui a produit le resultat le plus utile de tout l'essai. **Generaliser ce patron —
confronter ce qui est propose a ce qui a ete pose — est le chantier de conception le plus
rentable devant nous.**

## Ce qui reste non teste

`pm-risques` et le rapport de coherence final n'ont pas ete atteints (limite de session).
R7 et R10 restent couverts par les tests unitaires et par `exemples/portail-b2b`. Ce n'est
pas le test critique : celui-ci est passe.

---

# C13 — Cycle complet blocage -> levier -> re-validation

**La boucle de rework sur un ecart bloquant, bouclee de bout en bout.**

1. R11 bloque : marge -5,4 semaines en hypothese haute, verdict RETRAVAILLER.
2. L'humain tranche : combinaison de leviers, dont la scission du lot migration.
3. L'agent applique : lot 8 (corpus coeur) / lot 12 (archives, phase 2), chemin critique
   recalcule a **18-31 semaines**.
4. Marge recalculee : **+3,6 semaines** en hypothese haute.
5. Validateur relance : **AVANCER**.

Le controle le plus important du systeme a fait exactement son travail : detecter, bloquer,
laisser l'humain arbitrer, verifier que la correction ferme reellement l'ecart. Sans jamais
que l'agent tente de contourner (cf. C12).

C'est la demonstration complete de l'architecture, sur le cas le plus difficile.

## E10 — Inflation de cotation et double comptage des risques

`pm-risques` produit 8 risques, dont **3 cotes a la criticite maximale (4x5 = 20/25)** :

| Risque | Libelle |
|---|---|
| R-01 | Commanditaire/sponsor non nomme |
| R-03 | Menace sur l'echeance ete 2027 |
| R-05 | Escalade sponsor sur scission du perimetre migration (D4) |

**Deux problemes distincts.**

**1. Inflation.** Trois risques sur huit au plafond absolu. Un registre dont un quart des
entrees est au maximum ne priorise plus rien — c'est le defaut classique du registre produit
pour se couvrir plutot que pour piloter.

**2. Double comptage — le plus grave.** R-05 n'est pas independant de R-01. L'escalade
sponsor sur la scission de D4 ne peut pas *echouer* si le sponsor n'est pas nomme : elle ne
peut pas *avoir lieu*. **R-05 est une consequence de R-01**, pas un risque parallele. Les
coter tous deux a 20 compte deux fois le meme probleme et gonfle artificiellement le profil
de risque du projet.

**Consequence en aval, non encore visible** : R3 (reserve de contingence justifiee par les
risques cotes) additionne les expositions des risques retenus. Un double comptage a la
source produirait une contingence surevaluee, elle-meme presentee comme « justifiee par des
risques cotes ». Le defaut se propagerait avec l'apparence de la rigueur.

**Regle candidate — mecanisable** : un risque porte un champ optionnel `depend_de: R-xx`.
Le validateur verifie qu'aucun risque dependant n'est cote independamment dans les calculs
d'exposition, et signale deux risques de meme criticite maximale dont l'un conditionne
l'autre.

Relevant de la **famille 2** : rien ne confronte les elements produits entre eux au-dela des
regles de couverture. Ici il ne s'agit meme pas d'amont/aval mais de coherence interne d'un
seul artefact — variante a ajouter a la famille.

---

# C14 — Boucle de rework multi-agents distribuee

Le verificateur final a trouve **une incoherence narrative bloquante, non detectable par le
controle arithmetique** — precisement la part non automatisable qui lui etait assignee.

Sequence observee :

1. `pm-verificateur-coherence` : 1 ecart bloquant + 2 mineurs, renvoyes a leurs agents
   producteurs (planificateur, contexte). Iteration 1/3 annoncee.
2. `pm-contexte-projet`, en corrigeant, **decouvre une contradiction plus profonde** dans
   `plan.yaml` et la remonte.
3. L'orchestrateur transmet la precision au planificateur, deja en train de traiter deux
   ecarts : les trois points sont traites **en une seule passe consolidee**.
4. Re-verification : AVANCER.
5. Nettoyage d'un dernier point mineur, puis generation du rendu Markdown.

La boucle rediteur -> relecteur -> rediteur fonctionne entre agents distincts, avec
plafond d'iterations respecte et remontee d'un defaut decouvert en cours de correction.

# E11 — DIVERGENCE ENTRE DONNEES STRUCTUREES ET PROSE (defaut d'architecture)

**La decouverte la plus importante de l'essai.**

Contradiction trouvee par le verificateur :

> « les champs structures marquent les leviers comme `arbitre: false` / "a arbitrer", alors
> que les commentaires des lots les traitent comme deja choisis »

## Pourquoi c'est un defaut d'architecture et non un bug

Le principe fondateur du systeme est : *donnees structurees -> verifiables par code*. Mais
un fichier `.yaml` porte deux choses :

| Contenu | Verifie par | Lu par l'humain |
|---|---|---|
| Champs structures (`arbitre: false`, `valeur`, `statut`) | **le code** | rarement |
| Commentaires et champs de prose (`commentaire`, `libelle`, `motif`) | **personne** | **c'est ce qu'il lit dans le rendu .md** |

**Le code valide ce que l'humain ne lit pas, et l'humain lit ce que le code ne valide pas.**

Un portfolio peut donc etre `AVANCER` sur toutes ses regles tout en racontant, dans sa
prose, l'inverse de ce que ses donnees declarent. C'est le pire cas possible : la rigueur
mecanique certifie un document dont le sens lisible est faux.

Ici, la divergence portait sur un point decisif — un levier « a arbitrer » selon les donnees,
« deja choisi » selon les commentaires. Un comite lisant le `.md` aurait cru la decision
prise.

## Ce qui l'a rattrape, et ce que ca coute

C'est `pm-verificateur-coherence` — la part LLM du controle — qui l'a vu. C'est la
justification retrospective de son maintien : je l'avais decrit comme « presque plus un
agent, 9 regles sur 11 automatisables ». **Les 2 regles restantes viennent de rattraper le
defaut le plus grave du portfolio.**

Mais c'est fragile : rien ne garantit qu'il le voie la prochaine fois.

## Pistes

1. **Reduire la prose non verifiee.** Tout champ de prose qui affirme un etat (« deja
   choisi », « valide », « arrete ») duplique une information portee par un champ structure.
   Interdire ces affirmations dans la prose : la prose explique, elle ne declare pas.
2. **Regle mecanisable partielle** : detecter dans les champs de prose un vocabulaire d'etat
   (`choisi`, `retenu`, `valide`, `arbitre`, `decide`) et exiger qu'il soit coherent avec le
   champ `arbitre` / `statut` du meme bloc. Imparfait mais couvre le cas rencontre.
3. **Renforcer le rendu** : `render.py` affiche deja « seuil propose, **a arbitrer** ». Le
   rendu devrait faire foi sur l'etat et ignorer toute affirmation contraire en prose.

---

# BILAN FINAL DE L'ESSAI N°1 — CHAINE COMPLETE

**Verdict : AVANCER — 0 ecart bloquant, 0 mineur, 12 derogations motivees.**

Six artefacts produits (contexte, methodologie, charte, parties prenantes, plan, risques),
en `.yaml` source et `.md` rendu. Chaine complete parcourue, du texte brut au portfolio
verifie.

## Ce que le systeme a demontre

| # | Comportement decisif |
|---|---|
| C5 | Refus d'inventer ce qui n'est pas documente |
| C8 | Un refus humain de trancher converti en tache du plan |
| C10 | **Le code rattrape le LLM** — statut invente rejete par R9 |
| C12 | **Refus de contourner un blocage qu'il pouvait effacer** |
| C13 | Cycle complet blocage -> levier -> re-validation -> AVANCER |
| C14 | Boucle de rework distribuee entre agents, avec remontee de defaut |

## Ce que l'humain a apporte, que le systeme n'aurait pas trouve

| Apport | Nature |
|---|---|
| Reintegration de la conduite du changement | Coherence moyen / objectif (E6) |
| Impact R-03 ramene de 5 a 3 | Absence de consequence documentee |
| Restructuration du registre en chaine causale | Trois risques a 20 = un seul probleme (E10) |
| Budget d'avant-cadrage (retour P2R) | Un arbitrage humain n'est pas une donnee consolidee |

**Ces quatre apports relevent tous de la meme chose : confronter ce qui est produit a ce qui
a ete pose.** C'est la famille 2, et c'est ce que le systeme ne sait pas faire.

## Defauts : 11 trouves, 1 corrige

Familles inchangees, plus une decouverte :

- **Famille 1** — le controle verifie la FORME d'un signal, pas son SENS (4 occurrences)
- **Famille 2** — rien ne confronte une proposition AVAL aux contraintes AMONT (5 occurrences)
- **Famille 3 (nouvelle, E11)** — le code valide ce que l'humain ne lit pas, l'humain lit ce
  que le code ne valide pas

## Conclusion

Le systeme fait ce qu'il pretend faire. Ses defauts ne sont pas dans sa production mais dans
ses controles — ce qu'il accepte, ce qu'il propose, et ce qu'il ne confronte pas.

Le chantier prioritaire n'est pas d'ecrire les huit agents restants : c'est de generaliser le
patron de R11 — **confronter ce qui est propose a ce qui a ete pose** — et de traiter la
divergence donnees/prose.
