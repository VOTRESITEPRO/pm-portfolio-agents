# Benchmark — dépôts d'agents/skills PO-PM pour Claude Code

Objectif : décider quoi RÉUTILISER plutôt que réinventer, pour concevoir une
équipe d'agents PO/BA. Vérification faite sur le contenu réel des dépôts
(août 2026), pas sur des descriptions de seconde main.

## Synthèse

| Dépôt | Licence | Maturité | Rôle retenu |
|---|---|---|---|
| alirezarezvani/claude-skills | MIT | Actif, large | Source de substance PO |
| slgoodrich/agents (AI PM Copilot) | PolyForm Noncommercial | Petit, structuré | Modèle d'orchestration |
| quitecommlt/product-manager-skill | MIT | Embryonnaire | Modèle de structure de skill |
| David-Martel/claude-agents (Conductor) | MIT | Fork peu suivi | Réserve (option exécutable) |

## Détail par dépôt

### 1. alirezarezvani/claude-skills — MIT, actif
- Dossier `product-team/` : Product Manager, Agile Product Owner, Product
  Strategist, UX Researcher, UI Designer, Discovery Specialist, Roadmap
  Communicator, Code-to-PRD, Analytics/Experiment Designer.
- Chaque skill = SKILL.md + outils Python (stdlib) + templates. Multi-plateforme.
- Licence MIT → réutilisable librement, y compris en contexte commercial.
- Le plus riche en couverture PO/PM : point de référence pour la substance
  (stories, backlog, PRD, discovery).
- Réserve : très large et généraliste — sélectionner, ne pas tout prendre.

### 2. slgoodrich/agents (AI PM Copilot) — Noncommercial
- 9 agents : `product-manager` (routeur) + 7 spécialistes (requirements-engineer,
  feature-prioritizer, market-analyst, research-ops, product-strategist,
  roadmap-builder, launch-planner) + context-scanner.
- Orchestration par routage : le routeur analyse la demande et délègue. C'est
  l'incarnation la plus propre du modèle "équipe d'agents" (proche d'Animus).
- Frameworks : RICE/ICE/Kano, JTBD, Continuous Discovery, Story Mapping,
  Shape Up, templates PRD (Lean, Amazon PR/FAQ…).
- LICENCE PolyForm Noncommercial 1.0.0 → usage NON commercial uniquement.
  OK apprentissage / portfolio perso ; PAS utilisable tel quel dans une mission
  ESN facturée. À signaler explicitement.
- Meilleur modèle d'orchestration à étudier ; contrainte de licence sur l'usage pro.

### 3. quitecommlt/product-manager-skill — MIT, embryonnaire
- Un seul skill : SKILL.md + templates + playbooks + examples (SaaS fictif
  "InvoiceFlow").
- Couvre discovery, PRD, RICE/MoSCoW/Impact-Effort, MVP, roadmap, métriques,
  communication parties prenantes. Opiniâtre (refuse d'inventer des données,
  exige métriques + risques).
- Licence MIT, mais maturité très faible (≈1 étoile, ≈1 commit) : à traiter comme
  un MODÈLE DE STRUCTURE d'un skill bien fait, pas comme une brique éprouvée.

### 4. David-Martel/claude-agents (Conductor) — MIT, fork
- Fork de wshobson/agents, volumineux (dizaines de plugins/agents).
- Conductor = flux Context → Specification → Implementation, contexte persistant,
  portes de vérification / TDD. C'est le pont PO ↔ développement.
- Licence MIT, mais 0 étoile, fork peu suivi → pour l'option "exécutable / lien
  dev" seulement ; regarder d'abord l'upstream wshobson/agents.

## Recommandation de curation (artefact "présentable")
- Modèle d'orchestration : s'inspirer de slgoodrich (routeur + spécialistes),
  SANS réutiliser son code en contexte commercial (licence).
- Substance PO (stories, backlog, PRD, discovery) : puiser dans
  alirezarezvani/claude-skills (MIT).
- Structure d'un skill (SKILL.md + templates + playbooks + examples) : calquer
  quitecommlt.
- Conductor : réserve pour l'option exécutable / lien avec le dev.
- VALEUR AJOUTÉE PROPRE : aucun dépôt ne traite sérieusement le versant BA
  fonctionnel / ERP / gestion d'affaires / recette — exactement la cible d'emploi.
  C'est là que se construit l'apport original (analyste fonctionnel,
  spécifications / cahier des charges, cadrage d'ateliers, recette), le reste
  étant réutilisé.

## Ce que ça prouve (recruteur)
Un raisonnement buy-vs-build documenté, avec due diligence sur licences et
maturité, et une architecture combinant réutilisation de l'existant + apport
ciblé. C'est un livrable PO en soi.

## Réserve de fiabilité
Certains chiffres publics (étoiles, nombre d'outils) n'ont pas été revérifiés un
à un ; les points structurants utilisés ici (rôles, orchestration, licences,
maturité relative) proviennent de l'inspection des dépôts. Revérifier la licence
exacte avant tout usage commercial.


---

# Benchmark — depots cites par les instructions revisees (verifie le 2026-08-31)

Ces deux depots sont les references d'orchestration des instructions projet
revisees. Ils n'etaient pas couverts par le benchmark ci-dessus.

| Depot | Licence | Maturite | Produit des artefacts PM Cert ? |
|---|---|---|---|
| sdi2200262/agentic-project-management | MPL-2.0 | 2,4k stars, 479 commits, v1.0.0 | **Non** |
| kchia/project-management-agentic-workflow | MIT | 1 star, 4 commits | **Non** |

## sdi2200262/agentic-project-management — MPL-2.0, mature

- Trois roles : **Planner** (decouverte structuree -> Spec / Plan / Rules),
  **Manager** (assignation, revue, maintien de l'etat), **Workers** (execution
  par domaine, avec Task Prompt autonome).
- Artefacts : Spec, Plan, Rules, Task Prompts, Memory (logs de taches cumulatifs).
- Flux pilote par commandes (`/apm-1-initiate-planner`, `/apm-2-initiate-manager`),
  chaque echange inter-agents **mediee par l'utilisateur** : validation humaine
  obligatoire entre chaque etape.
- **Licence MPL-2.0 : usage commercial autorise**, y compris en mission ESN.
  Copyleft de fichier — toute modification d'un fichier source reste sous MPL-2.0.
  C'est un avantage decisif sur AI PM Copilot (PolyForm Noncommercial).
- **Ce qui est repris** : modele d'orchestration, memoire partagee persistante,
  principe de validation humaine systematique. Pas de substance PM.

## kchia/project-management-agentic-workflow — MIT, exercice pedagogique

- Sept types d'agents generiques : DirectPrompt, AugmentedPrompt,
  KnowledgeAugmentedPrompt, RAGKnowledgePrompt, **Evaluation** (rework iteratif,
  max 10 interactions), **Routing** (par similarite d'embeddings),
  **ActionPlanning** (decomposition objectif -> etapes).
- Trois equipes : Product Manager (user stories), Program Manager (groupes de
  fonctionnalites), Development Engineer (taches avec criteres d'acceptation,
  effort, dependances).
- Maturite tres faible (1 star, 4 commits) : a traiter comme une **collection de
  patterns**, pas comme une brique reutilisable. L'auteur documente lui-meme ses
  limites (dependance sequentielle, communication inter-agents limitee, criteres
  d'evaluation rigides).
- **Ce qui est repris** : boucle de rework bornee par un plafond d'iterations,
  routage, decomposition sequentielle. Pas de code.

## Conclusion structurante

**Aucun des deux depots ne genere d'artefact du Google PM Certificate** : ni
charte, ni RACI, ni registre des risques, ni budget, ni plan de communication, ni
artefacts de cloture. La reutilisation porte exclusivement sur la couche
orchestration et gouvernance ; les onze agents producteurs d'artefacts sont
construits en propre.

Consequence sur la cartographie : 5 agents "adapte", 10 agents "cree",
**0 agent "reutilise" tel quel**.

## Ce que ca prouve (recruteur)

Due diligence licence et maturite faite sur le contenu reel des depots, pas sur
leur README : un depot a 2,4k stars a ete retenu pour son modele mais ecarte pour
sa substance, un depot a 1 star a ete conserve pour trois patterns precis. La
decision buy-vs-build est tracee agent par agent dans
`cartographie-agents-pm.yaml`.
