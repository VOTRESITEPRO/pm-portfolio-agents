# Installation et premier essai

Objectif de cette page : faire tourner la chaine une premiere fois, pour de vrai. Le
systeme n'a jamais ete execute — seuls ses validateurs l'ont ete. Ce premier essai est un
test, pas une mise en service.

## Etape 0 — controle pre-vol

Depuis le dossier du plugin, sur la machine cible :

    python3 scripts/preflight.py
    # ou, si python3 n'existe pas :
    python scripts\preflight.py

Il verifie la version de Python, la presence de PyYAML, l'integrite du manifeste, des
7 agents et des 11 regles, et il execute le validateur sur l'exemple de reference. Il
n'installe rien.

**Il determine surtout quelle invocation Python fonctionne sur cette machine** — `py -3`,
`python3` ou `python` — et verifie que `hooks/hooks.json` utilise bien celle-la. C'est un
point critique et silencieux : un hook dont la commande echoue ne bloque rien, et les
portes qualite ne s'executent jamais sans que rien ne le signale.

Si l'invocation de `hooks.json` ne correspond pas :

    <invocation> scripts/preflight.py --fix-hooks

Sous Windows, `python.exe` et `python3.exe` sont souvent des alias vides du Microsoft Store
alors que le launcher `py` fonctionne. `hooks.json` est donc **specifique a la machine**
apres correction : a reajuster si le plugin change d'environnement.

Tant que le preflight ne dit pas « Pret pour l'installation », ne va pas plus loin.

## Claude Code

    cd <un projet de test, vide de preference>
    claude --plugin-dir "<chemin>/pm-portfolio-agents"

Verification prealable, si disponible :

    claude plugin validate "<chemin>/pm-portfolio-agents"

## Cowork

Le plugin s'installe depuis un marketplace : depot GitHub ou archive `.zip`. Il faut donc
d'abord versionner `pm-portfolio-agents/` dans un depot, puis l'ajouter comme marketplace.
Le `.gitignore` fourni exclut deja les caches et le fichier `.plugin-path`.

## Premier essai — 15 minutes

Prends un projet fictif court, pas un projet reel. Trois phrases suffisent, et **laisse-y
volontairement des trous** : c'est ce qui teste le comportement le plus important du systeme.

Exemple d'entree :

> « On veut refondre l'intranet documentaire de la societe. Environ 300 collaborateurs.
> Le budget evoque tourne autour de 80 k. Il faudrait que ce soit pret l'an prochain. »

Trois lacunes bloquantes y sont volontaires : budget non arbitre, echeance non datee, aucun
critere de succes.

    /pm-portfolio Refonte de l'intranet documentaire, environ 300 collaborateurs, budget evoque autour de 80 k, pret l'an prochain.

## Ce qu'il faut observer

| Attendu | Signification si absent |
|---|---|
| `pm-contexte-projet` **s'arrete** et pose 3 questions | La porte de sortie ne bloque pas — defaut majeur |
| Le registre des lacunes est ecrit dans `contexte.yaml` | L'agent n'a pas produit son second livrable |
| `pm-methodologue` demande une validation avant de continuer | La reprise humaine n'est pas respectee |
| `pm-portfolio/.plugin-path` apparait apres la premiere ecriture | Le hook ne s'execute pas |
| `RAPPORT-COHERENCE.md` se genere | Le validateur n'est pas atteint |
| Claude ne conclut pas son tour sur un ecart bloquant | Le hook `Stop` ne bloque pas |

## Journal d'essai

Note ce qui casse, sans le corriger a chaud. Le but du premier essai est l'inventaire, pas
la reparation : un defaut corrige immediatement est un defaut non compris. C'est la methode
qui a produit les six corrections de la version 1.1 de la cartographie.

| # | Ce qui s'est passe | Attendu | Hypothese de cause |
|---|---|---|---|
|   |                    |         |                    |

## Defauts deja anticipes

Ils ne sont pas des bugs a signaler, mais des points a confirmer :

1. `python3` absent sous Windows — utiliser `python`.
2. PyYAML absent — `pip install pyyaml`.
3. Hooks non executes dans Cowork — comportement non verifie a ce jour.
4. Les agents produisent du YAML non conforme au schema au premier essai. Le validateur le
   dira ; c'est son role.
5. Sept portes de sortie ne sont pas encore controlees par code — voir
   `ECARTS-SPEC-IMPLEMENTATION.md`. Un artefact incomplet peut donc passer.
