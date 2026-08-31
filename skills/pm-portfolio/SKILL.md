---
name: pm-portfolio
description: Genere le portfolio d'artefacts de gestion de projet (charte, parties prenantes, RACI, WBS, jalons, chemin critique, registre des risques) a partir d'une description de projet, sous portes qualite verifiees par code. A utiliser pour cadrer un projet, produire ou mettre a jour ses artefacts de pilotage, ou controler la coherence d'un portfolio existant.
argument-hint: [description du projet ou chemin d'un fichier de contexte]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
---

# Portfolio d'artefacts de gestion de projet

Tu orchestres une chaine d'agents specialises qui produisent les artefacts de pilotage d'un
projet, chacun sous une porte qualite verifiee par du code deterministe.

## Principe a ne pas perdre de vue

> Le LLM produit, analyse et qualifie. Le code verifie, recalcule, compte et trace.

Aucune porte qualite ne repose sur le jugement d'un modele sur sa propre production. Si tu
te surprends a ecrire "j'ai verifie que le total est correct", arrete-toi et lance le
validateur : c'est lui qui verifie.

## Sequence

    1. pm-contexte-projet      -> contexte.yaml      + registre des lacunes
       [reprise humaine : arbitrage des lacunes bloquantes]
    2. pm-methodologue         -> methodologie.yaml  + drapeau agile
       [reprise humaine : VALIDATION OBLIGATOIRE]
    3. pm-charte-objectifs     -> charte.yaml
       [reprise humaine : perimetre et cout-benefice]
    4. pm-parties-prenantes    -> parties-prenantes.yaml
    5. pm-planificateur-wbs    -> plan.yaml
       [reprise humaine : VALIDATION OBLIGATOIRE des estimations]
    6. pm-risques              -> risques.yaml
    7. pm-verificateur-coherence -> RAPPORT-COHERENCE.md

Les etapes 4 et 5 peuvent etre menees en parallele : toutes deux ne dependent que de la
charte. L'etape 6 exige imperativement le chemin critique produit en 5.

## Regle de tranche

Une execution partielle se declare comme la **fermeture transitive** des dependances des
artefacts vises, jamais comme une selection d'agents. Ecris `pm-portfolio/tranche.yaml` :

```yaml
artefacts: [risques, parties-prenantes]   # entraine plan, charte, methodologie, contexte
```

Sans ce fichier, la tranche est deduite des artefacts presents.

## Demarrage

1. Cree `pm-portfolio/` a la racine du projet.
2. Lance `pm-contexte-projet` avec la description fournie par l'utilisateur.
3. **Ne poursuis pas** tant qu'une lacune bloquante reste ouverte. Pose les questions, une
   par lacune, et attends les arbitrages. C'est le comportement attendu, pas un echec.

## Localiser les scripts

`${CLAUDE_PLUGIN_ROOT}` n'est PAS substitue dans le corps d'un skill ni d'un agent — la
substitution ne fonctionne que dans les JSON de hooks
(bug anthropics/claude-code#9354). Resous le chemin ainsi :

1. `pm-portfolio/.plugin-path` — depose par le hook des la premiere ecriture d'artefact ;
2. sinon, Glob sur `**/pm-portfolio-agents/scripts/validate.py` ;
3. sinon, demande le chemin a l'utilisateur. Ne devine pas.

Note `RACINE` le chemin obtenu et reutilise-le. Si `python3` echoue, essaie `python`.

## A chaque etape

Apres qu'un agent a ecrit son artefact :

    python3 RACINE/scripts/validate.py pm-portfolio

Le rapport atterrit dans `pm-portfolio/RAPPORT-COHERENCE.md`. Un ecart bloquant est renvoye
a l'agent nomme dans le rapport, dans la limite de 3 iterations. Au-dela, remonte a
l'utilisateur : l'ecart vient probablement d'une lacune du contexte, pas d'un defaut de
production.

## Rendu lisible

    python3 RACINE/scripts/render.py pm-portfolio

Genere les `.md` a partir des `.yaml`. **Le Markdown est une sortie, jamais la source** :
toute correction se fait dans le YAML, puis on regenere.

## Les sept decisions que la chaine ne prend jamais

Choix de methodologie · ordonnancement du backlog · validation des chiffres budgetaires ·
engagement de sprint · engagement vis-a-vis des parties prenantes · evaluation des
personnes · cotation finale de l'impact des risques.

Presente-les a l'utilisateur au moment ou elles se posent. Ne les tranche pas, meme quand
la reponse te parait evidente.

## Confidentialite

Tout s'execute en local, les artefacts restent dans le depot du projet. En mission, ils
contiennent des donnees client : traite-les comme tout livrable projet.
