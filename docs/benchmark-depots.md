# Benchmark — dépôts d'agents/skills PO-PM pour Claude Code

Objectif : décider quoi RÉUTILISER plutôt que réinventer, pour concevoir une équipe d'agents PO/BA. Vérification faite sur le contenu réel des dépôts (août 2026), pas sur des descriptions de seconde main.

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
  Strategist, UX Researcher, UI Designer, Discovery Specialist, Roadmap Communicator, Code-to-PRD, Analytics/Experiment Designer.
- Chaque skill = SKILL.md + outils Python (stdlib) + templates. Multi-plateforme.
- Licence MIT → réutilisable librement, y compris en contexte commercial.
- Le plus riche en couverture PO/PM : point de référence pour la substance
  (stories, backlog, PRD, discovery).
- Réserve : très large et généraliste — sélectionner, ne pas tout prendre.

### 2. slgoodrich/agents (AI PM Copilot) — Noncommercial
- 9 agents : `product-manager` (routeur) + 7 spécialistes (requirements-engineer,
  feature-prioritizer, market-analyst, research-ops, product-strategist, roadmap-builder, launch-planner) + context-scanner.
- Orchestration par routage : le routeur analyse la demande et délègue. C'est
  l'incarnation la plus propre du modèle "équipe d'agents" (proche d'Animus).
- Frameworks : RICE/ICE/Kano, JTBD, Continuous Discovery, Story Mapping,
  Shape Up, templates PRD (Lean, Amazon PR/FAQ…).
- LICENCE PolyForm Noncommercial 1.0.0 → usage NON commercial uniquement.
  OK apprentissage / portfolio perso ; PAS utilisable tel quel dans une mission ESN facturée. À signaler explicitement.
- Meilleur modèle d'orchestration à étudier ; contrainte de licence sur l'usage pro.

### 3. quitecommlt/product-manager-skill — MIT, embryonnaire
- Un seul skill : SKILL.md + templates + playbooks + examples (SaaS fictif
  "InvoiceFlow").
- Couvre discovery, PRD, RICE/MoSCoW/Impact-Effort, MVP, roadmap, métriques,
  communication parties prenantes. Opiniâtre (refuse d'inventer des données, exige métriques + risques).
- Licence MIT, mais maturité très faible (≈1 étoile, ≈1 commit) : à traiter comme
  un MODÈLE DE STRUCTURE d'un skill bien fait, pas comme une brique éprouvée.

### 4. David-Martel/claude-agents (Conductor) — MIT, fork
- Fork de wshobson/agents, volumineux (dizaines de plugins/agents).
- Conductor = flux Context → Spécification → Implémentation, contexte persistant,
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
  fonctionnel / ERP / gestion d'affaires / recette — exactement la cible d'emploi. C'est là que se construit l'apport original (analyste fonctionnel, spécifications / cahier des charges, cadrage d'ateliers, recette), le reste étant réutilisé.

## Ce que ça prouve (recruteur)
Un raisonnement buy-vs-build documenté, avec due diligence sur licences et maturité, et une architecture combinant réutilisation de l'existant + apport ciblé. C'est un livrable PO en soi.

## Réserve de fiabilité
Certains chiffrés publics (étoiles, nombre d'outils) n'ont pas été revérifiés un à un ; les points structurants utilisés ici (rôles, orchestration, licences, maturité relative) proviennent de l'inspection des dépôts. Revérifier la licence exacte avant tout usage commercial.


---

# Benchmark — dépôts cites par les instructions revisees (vérifie le 2026-08-31)

Ces deux dépôts sont les références d'orchestration des instructions projet revisees. Ils n'etaient pas couverts par le benchmark ci-dessus.

| Dépôt | Licence | Maturité | Produit des artefacts PM Cert ? |
|---|---|---|---|
| sdi2200262/agentic-project-management | MPL-2.0 | 2,4k stars, 479 commits, v1.0.0 | **Non** |
| kchia/project-management-agentic-workflow | MIT | 1 star, 4 commits | **Non** |

## sdi2200262/agentic-project-management — MPL-2.0, mature

- Trois rôles : **Planner** (decouverte structuree -> Spec / Plan / Rules),
  **Manager** (assignation, revue, maintien de l'état), **Workers** (exécution
  par domaine, avec Task Prompt autonome).
- Artefacts : Spec, Plan, Rules, Task Prompts, Memory (logs de tâches cumulatifs).
- Flux pilote par commandes (`/apm-1-initiate-planner`, `/apm-2-initiate-manager`),
  chaque échange inter-agents **mediee par l'utilisateur** : validation humaine obligatoire entre chaque étape.
- **Licence MPL-2.0 : usage commercial autorisé**, y compris en mission ESN.
  Copyleft de fichier — toute modification d'un fichier source reste sous MPL-2.0. C'est un avantage décisif sur AI PM Copilot (PolyForm Noncommercial).
- **Ce qui est repris** : modèle d'orchestration, memoire partagee persistante,
  principe de validation humaine systématique. Pas de substance PM.

## kchia/project-management-agentic-workflow — MIT, exercice pedagogique

- Sept types d'agents generiques : DirectPrompt, AugmentedPrompt,
  KnowledgeAugmentedPrompt, RAGKnowledgePrompt, **Évaluation** (rework itératif, max 10 interactions), **Routing** (par similarite d'embeddings),
  **ActionPlanning** (décomposition objectif -> étapes).
- Trois équipes : Product Manager (user stories), Program Manager (groupes de
  fonctionnalites), Development Engineer (tâches avec critères d'acceptation, effort, dépendances).
- Maturité très faible (1 star, 4 commits) : à traiter comme une **collection de
  patterns**, pas comme une brique reutilisable. L'auteur documente lui-même ses limites (dépendance séquentielle, communication inter-agents limitee, critères d'évaluation rigides).
- **Ce qui est repris** : boucle de rework bornée par un plafond d'itérations,
  routage, décomposition séquentielle. Pas de code.

## Conclusion structurante

**Aucun des deux dépôts ne génère d'artefact du Google PM Certificate** : ni
charte, ni RACI, ni registre des risques, ni budget, ni plan de communication, ni artefacts de clôture. La réutilisation porte exclusivement sur la couche orchestration et gouvernance ; les onze agents producteurs d'artefacts sont construits en propre.

Conséquence sur la cartographie : 5 agents "adapte", 10 agents "créé",
**0 agent "réutilise" tel quel**.

## Ce que ca prouve (recruteur)

Due diligence licence et maturité faite sur le contenu réel des dépôts, pas sur leur README : un dépôt à 2,4k stars a été retenu pour son modèle mais écarté pour sa substance, un dépôt à 1 star a été conserve pour trois patterns précis. La décision buy-vs-build est tracée agent par agent dans `cartographie-agents-pm.yaml`.
