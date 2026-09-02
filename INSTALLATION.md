# Installation et premier essai

Objectif de cette page : faire tourner la chaîne une première fois, pour de vrai. Le système n'a jamais été exécute — seuls ses validateurs l'ont été. Ce premier essai est un test, pas une mise en service.

## Étape 0 — contrôle pré-vol

Depuis le dossier du plugin, sur la machine cible :

    python3 scripts/preflight.py
    # ou, si python3 n'existe pas :
    python scripts\preflight.py

Il vérifie la version de Python, la presence de PyYAML, l'integrite du manifeste, des 7 agents, des 15 règles et des 8 portes, et il exécute le validateur sur l'exemple de référence. Il n'installé rien.

**Il determine surtout quelle invocation Python fonctionne sur cette machine** — `py -3`,
`python3` ou `python` — et vérifie que `hooks/hooks.json` utilise bien celle-là. C'est un point critique et silencieux : un hook dont la commande échoue ne bloque rien, et les portes qualité ne s'executent jamais sans que rien ne le signale.

Si l'invocation de `hooks.json` ne correspond pas :

    <invocation> scripts/preflight.py --fix-hooks

Sous Windows, `python.exe` et `python3.exe` sont souvent des alias vides du Microsoft Store alors que le launcher `py` fonctionne. `hooks.json` est donc **spécifique à la machine** après correction : à reajuster si le plugin change d'environnement.

Tant que le preflight ne dit pas « Prêt pour l'installation », ne va pas plus loin.

## Claude Code

    cd <un projet de test, vide de préférence>
    claude --plugin-dir "<chemin>/pm-portfolio-agents"

Vérification préalable, si disponible :

    claude plugin validate "<chemin>/pm-portfolio-agents"

## Cowork

Le plugin s'installé depuis un marketplace : dépôt GitHub ou archive `.zip`. Il faut donc d'abord versionner `pm-portfolio-agents/` dans un dépôt, puis l'ajouter comme marketplace. Le `.gitignore` fourni exclut déjà les caches et le fichier `.plugin-path`.

## Premier essai — 15 minutes

Prends un projet fictif court, pas un projet réel. Trois phrases suffisent, et **laisse-y volontairement des trous** : c'est ce qui teste le comportement le plus important du système.

Exemple d'entrée :

> « On veut refondre l'intranet documentaire de la société. Environ 300 collaborateurs.
> Le budget evoque tourne autour de 80 k. Il faudrait que ce soit prêt l'an prochain. »

Trois lacunes bloquantes y sont volontaires : budget non arbitre, échéance non datee, aucun critère de succès.

    /pm-portfolio Refonte de l'intranet documentaire, environ 300 collaborateurs, budget evoque autour de 80 k, prêt l'an prochain.

## Ce qu'il faut observer

| Attendu | Signification si absent |
|---|---|
| `pm-contexte-projet` **s'arrête** et pose 3 questions | La porte de sortie ne bloque pas — défaut majeur |
| Le registre des lacunes est ecrit dans `contexte.yaml` | L'agent n'a pas produit son second livrable |
| `pm-methodologue` demande une validation avant de continuer | La reprise humaine n'est pas respectee |
| `pm-portfolio/.plugin-path` apparait après la première ecriture | Le hook ne s'exécute pas |
| `RAPPORT-COHERENCE.md` se génère | Le validateur n'est pas atteint |
| Claude ne conclut pas son tour sur un écart bloquant | Le hook `Stop` ne bloque pas |

## Journal d'essai

Note ce qui casse, sans le corriger à chaud. Le but du premier essai est l'inventaire, pas la réparation : un défaut corrige immédiatement est un défaut non compris. C'est la méthode qui a produit les six corrections de la version 1.1 de la cartographie.

| # | Ce qui s'est passe | Attendu | Hypothèse de cause |
|---|---|---|---|
|   |                    |         |                    |

## Défauts déjà anticipes

Ils ne sont pas des bugs à signaler, mais des points à confirmer :

1. `python3` absent sous Windows — utiliser `python`.
2. PyYAML absent — `pip install pyyaml`.
3. Hooks non exécutés dans Cowork — comportement non vérifié à ce jour.
4. Les agents produisent du YAML non conforme au schéma au premier essai. Le validateur le
   dira ; c'est son rôle.
5. Les règles dépendant d'un agent non encore écrit (budget, communications, qualité,
   clôture, backlog, sprint) sortent `non_applicable`, jamais `échec` — voir
   `docs/ecarts-spec-implementation.md`.
