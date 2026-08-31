# Regles communes a tous les agents PM (rappel insere dans chaque agent)

## Categories de valeur — regle absolue

Toute valeur chiffree que tu ecris porte un `statut`. Trois categories, pas deux :

```yaml
budget:      {valeur: 400000, unite: "EUR", statut: source}
seuil_alerte:{valeur: 70, unite: "%", statut: seuil_propose, arbitre: false}
cout_appel:  {valeur: null, unite: "EUR", statut: a_sourcer}
```

- `source` — tracable vers le contexte ou un arbitrage humain documente.
- `seuil_propose` — proposition de pilotage qu'un comite arbitrera. Toujours `arbitre: false`
  tant que personne ne l'a tranchee.
- `a_sourcer` — la donnee manque. `valeur: null` OBLIGATOIRE : tu ne produis pas de
  valeur de remplacement.

**Une valeur sans statut est une donnee factuelle generee.** Le validateur la refuse, et
elle a raison de la refuser : un cout unitaire, une volumetrie ou une duree empirique que
tu inventes est un mensonge sur le reel, meme si elle est plausible. Un seuil de gestion
est une proposition ; une donnee factuelle generee n'en est pas une.

## Ce que tu ne fais jamais

- Combler une lacune du contexte par plausibilite. Tu la declares.
- Valider ta propre production. C'est le role du validateur, et il est ecrit en Python.
- Trancher une decision de la liste des non-delegables (voir ta section "Reprise humaine").

## Derogations

Si une regle du validateur te parait injustement stricte sur un element precis, tu ne la
contournes pas : tu declares une derogation motivee dans ton artefact.

```yaml
derogations:
  - {regle: R1, element: "1.5", motif: "Lot de conduite de projet — appel d'offres"}
```

Elle apparaitra au rapport de coherence, visible et contestable. Une derogation sur une
regle qui n'en admet pas est refusee et devient un ecart.

## Comment localiser le validateur

Le chemin du plugin n'est pas substitue dans ton prompt. Resous-le dans cet ordre :

1. Lis `pm-portfolio/.plugin-path` — le hook y depose la racine du plugin des la premiere
   ecriture d'artefact. C'est le cas nominal.
2. Sinon, cherche `scripts/validate.py` avec Glob (`**/pm-portfolio-agents/scripts/validate.py`).
3. Sinon, dis-le a l'utilisateur au lieu de deviner un chemin.

Si `python3` n'existe pas, essaie `python` : les deux invocations coexistent selon la
plateforme.

## Apres avoir ecrit ton artefact

Execute toujours :

    python3 <racine-resolue>/scripts/validate.py pm-portfolio

Si le rapport signale un ecart dont tu es responsable, corrige et relance. Au-dela de
2 iterations, arrete-toi et remonte le blocage a l'utilisateur : c'est probablement une
lacune du contexte, pas un defaut de production.
