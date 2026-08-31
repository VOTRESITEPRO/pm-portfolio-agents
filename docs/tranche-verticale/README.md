# Portfolio démonstratif — tranche verticale

Démonstration de bout en bout de la chaîne d'agents décrite dans
`../cartographie-agents-pm.yaml`, sur un cas d'étude neutre.

**7 agents sur 15**, toutes les couches représentées (orchestration, production, contrôle).

## Ordre de lecture

| # | Fichier | Agent | Compétence Google PM Cert |
|---|---|---|---|
| 00 | `00-cas-etude.md` | — | Entrée du système |
| 01 | `01-contexte-projet.md` | `contexte-projet` | C2 — définition du projet |
| 02 | `02-recommandation-methodologique.md` | `methodologue` | C1 — méthodologies |
| 03 | `03-charte-projet.md` | `charte-objectifs` | C2 — charte, SMART, OKR, périmètre |
| 04 | `04-parties-prenantes-raci.md` | `parties-prenantes` | C2 — stakeholders, RACI |
| 05 | `05-wbs-plan-projet.md` | `planificateur-wbs` | C3 — WBS, jalons, chemin critique |
| 06 | `06-registre-risques.md` | `risques` | C3 — registre, matrice, atténuation |
| 07 | `07-rapport-coherence.md` | `verificateur-coherence` | C6 — intégration et cohérence |
| 99 | `99-lecons-conception.md` | — | **Résultat de l'exercice** |

## Si vous ne lisez que deux fichiers

`07-rapport-coherence.md` et `99-lecons-conception.md`. Le reste est la matière ; ces deux-là
sont la démonstration.

## Points de reprise humaine rencontrés

4 lacunes bloquantes arbitrées au cadrage · validation obligatoire de la méthodologie ·
validation du périmètre et du coût-bénéfice · validation des estimations de durée et choix
du levier de réduction du chemin critique · revue des cotations de risque en comité.

## Statut

Conception documentée, exécutée manuellement selon les spécifications du YAML. Aucun agent
n'est branché ni exécuté automatiquement.
