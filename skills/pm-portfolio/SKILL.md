---
name: pm-portfolio
description: Génère le portfolio d'artefacts de gestion de projet (charte, parties prenantes, RACI, WBS, jalons, chemin critique, registre des risques) à partir d'une description de projet, sous portes qualité vérifiées par code. A utiliser pour cadrer un projet, produire ou mettre à jour ses artefacts de pilotage, ou contrôler la cohérence d'un portfolio existant.
argument-hint: [description du projet ou chemin d'un fichier de contexte]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
---

# Portfolio d'artefacts de gestion de projet

Tu orchestres une chaîne d'agents specialises qui produisent les artefacts de pilotage d'un projet, chacun sous une porte qualité vérifiée par du code déterministe.

## Sobriété d'exécution

Chaque tour d'agent recharge tout son contexte : le coût d'un run tient au **nombre de
tours**, pas au volume produit. Trois règles :

- un agent écrit son artefact en **une seule écriture**, jamais par retouches successives ;
- ne relance le validateur qu'après une écriture complète, pas après chaque modification ;
- ne relis pas un artefact que tu viens d'écrire pour vérifier qu'il est correct — le
  validateur le fait, et lui ne coûte rien.

## Principe à ne pas perdre de vue

> Le LLM produit, analyse et qualifie. Le code vérifie, recalculé, compte et trace.

Aucune porte qualité ne repose sur le jugement d'un modèle sur sa propre production. Si tu te surprends à ecrire "j'ai vérifie que le total est correct", arrête-toi et lance le validateur : c'est lui qui vérifie.

## Séquence

    1. pm-contexte-projet      -> contexte.yaml      + registre des lacunes
       [reprise humaine : arbitrage des lacunes bloquantes]
    2. pm-methodologue         -> méthodologie.yaml  + drapeau agile
       [reprise humaine : VALIDATION OBLIGATOIRE]
    3. pm-charte-objectifs     -> charte.yaml
       [reprise humaine : périmètre et coût-bénéfice]
    4. pm-parties-prenantes    -> parties-prenantes.yaml
    5. pm-planificateur-wbs    -> plan.yaml
       [reprise humaine : VALIDATION OBLIGATOIRE des estimations]
    6. pm-risques              -> risques.yaml
    7. pm-vérificateur-cohérence -> RAPPORT-Cohérence.md

Les étapes 4 et 5 peuvent être menees en parallele : toutes deux ne dépendent que de la charte. L'étape 6 exige imperativement le chemin critique produit en 5.

## Règle de tranche

Une exécution partielle se déclare comme la **fermeture transitive** des dépendances des artefacts vises, jamais comme une sélection d'agents. Ecris `pm-portfolio/tranche.yaml` :

```yaml
artefacts: [risques, parties-prenantes]   # entraine plan, charte, methodologie, contexte
```

Sans ce fichier, la tranche est deduite des artefacts presents.

## Démarrage

1. Créé `pm-portfolio/` à la racine du projet.
2. Lance `pm-contexte-projet` avec la description fournie par l'utilisateur.
3. **Ne poursuis pas** tant qu'une lacune bloquante reste ouverte. Pose les questions, une
   par lacune, et attends les arbitrages. C'est le comportement attendu, pas un échec.

## Localiser les scripts

`${CLAUDE_PLUGIN_ROOT}` n'est PAS substitue dans le corps d'un skill ni d'un agent — la substitution ne fonctionne que dans les JSON de hooks (bug anthropics/claude-code#9354). Resous le chemin ainsi :

1. `pm-portfolio/.plugin-path` — dépose par le hook dès la première ecriture d'artefact ;
2. sinon, Glob sur `**/pm-portfolio-agents/scripts/validate.py` ;
3. sinon, demande le chemin à l'utilisateur. Ne devine pas.

Note `RACINE` le chemin obtenu et réutilise-le. Si `python3` échoue, essaie `python`.

## A chaque étape

Après qu'un agent a ecrit son artefact :

    python3 RACINE/scripts/validate.py pm-portfolio

Le rapport atterrit dans `pm-portfolio/RAPPORT-COHERENCE.md`. Un écart bloquant est renvoye à l'agent nomme dans le rapport, dans la limite de 3 itérations. Au-delà, remonté à l'utilisateur : l'écart vient probablement d'une lacune du contexte, pas d'un défaut de production.

## Rendu lisible

    python3 RACINE/scripts/render.py pm-portfolio

Génère les `.md` à partir des `.yaml`. **Le Markdown est une sortie, jamais la source** : toute correction se fait dans le YAML, puis on régénère.

## Les sept décisions que la chaîne ne prend jamais

Choix de méthodologie · ordonnancement du backlog · validation des chiffrés budgétaires · engagement de sprint · engagement vis-à-vis des parties prenantes · évaluation des personnes · cotation finale de l'impact des risques.

Présente-les à l'utilisateur au moment où elles se posent. Ne les tranche pas, même quand la réponse te parait evidente.

## Confidentialité

Tout s'exécute en local, les artefacts restent dans le dépôt du projet. En mission, ils contiennent des données client : traite-les comme tout livrable projet.
