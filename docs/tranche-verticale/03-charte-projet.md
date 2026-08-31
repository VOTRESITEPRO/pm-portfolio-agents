# Agent `charte-objectifs` — Charte de projet

**Compétence Google PM Cert** : C2 — documentation d'initiation, buts SMART, OKR,
périmètre et scope creep, analyse coût-bénéfice
**Entrée** : dossier de contexte validé + recommandation méthodologique validée

---

## 1. CHARTE DE PROJET

### Identification

| | |
|---|---|
| **Projet** | Refonte du portail client B2B |
| **Sponsor** | Direction générale |
| **Chef de projet** | À nommer — *décision organisationnelle, hors périmètre de l'IA* |
| **Méthodologie** | Hybride (cadrage séquentiel, réalisation itérative) |
| **Échéance** | 31/12/2027, ferme |
| **Budget** | 400 k€, plafond voté non extensible |

### Justification business

Le portail actuel (2016) ne permet pas aux clients professionnels de résoudre seuls leurs
demandes courantes. Le service client absorbe ~60 appels/jour, dont une part significative
relève de consultations que le portail devrait servir. L'absence d'usage mobile exploitable
écarte une partie des utilisateurs terrain. La refonte vise à transférer au portail la
charge de service auto-résolvable et à rendre l'outil utilisable en mobilité.

### Analyse coût-bénéfice (premier niveau)

| Élément | Valeur | Source |
|---|---|---|
| Coût projet | 400 k€ | plafond voté |
| Volume d'appels actuel | 60/jour | contexte |
| Cible de réduction | −40 %, soit 24 appels/jour évités | arbitrage commanditaire |
| Coût unitaire d'un appel | **[À SOURCER]** | *non fourni — l'agent ne l'estime pas* |
| Gain annuel chiffré | **Non calculable en l'état** | dépend du coût unitaire |
| Bénéfices non monétisés | Usage mobile, satisfaction client, capacité du service client redéployée | contexte |

> **L'analyse coût-bénéfice est volontairement incomplète.** Le coût de traitement d'un
> appel n'a pas été fourni ; le générer aurait produit un ROI crédible et infondé. Il est
> marqué à sourcer, et le retour sur investissement reste à établir avec la DAF.

---

## 2. OBJECTIFS SMART

### O1 — Réduction de la charge de service client

> **Réduire de 40 % le volume d'appels entrants auto-résolvables au service client, en le
> ramenant de 60 à 36 appels/jour en moyenne mensuelle, mesuré sur les trois mois suivant
> la mise en service, soit au 31/03/2028.**

| Critère | Vérification |
|---|---|
| **S**pécifique | Volume d'appels entrants au service client — périmètre nommé |
| **M**esurable | 60 → 36 appels/jour, moyenne mensuelle (source : outil de téléphonie) |
| **A**tteignable | Sous réserve de R-07 : la part réellement auto-résolvable des 60 appels n'est pas établie |
| **R**éaliste | Cohérent avec le budget et l'échéance |
| **T**emporel | Mesuré au 31/03/2028, 3 mois après mise en service |

### O2 — Usage mobile

> **Atteindre 30 % de sessions sur terminal mobile ou tablette sur le portail refondu, au
> 31/03/2028, contre une base actuelle à établir avant démarrage.**

| Critère | Vérification |
|---|---|
| **S**pécifique | Part de sessions mobile/tablette |
| **M**esurable | 30 % des sessions (source : analytics) — **base de départ [À ÉTABLIR]** |
| **A**tteignable | Non vérifiable sans la base de départ |
| **R**éaliste | À confirmer après mesure initiale |
| **T**emporel | 31/03/2028 |

### O3 — Mise en service

> **Mettre en service le portail refondu au plus tard le 31/12/2027, avec les parcours
> consultation (devis, commandes, factures) et commande sur catalogue opérationnels et
> alimentés par l'ERP.**

| Critère | Vérification |
|---|---|
| **S**pécifique | Parcours nommés, source de données nommée |
| **M**esurable | Parcours en production, oui/non |
| **A**tteignable | Sous réserve des estimations de charge (non empiriques) |
| **R**éaliste | Sous réserve du budget plafond |
| **T**emporel | 31/12/2027 |

---

## 3. OKR (déclinaison trimestrielle, année 2027)

**Objectif — Rendre le portail client autonome et utilisable en mobilité.**

| KR | Formulation | Échéance |
|---|---|---|
| KR1 | Les 3 parcours de consultation sont en production et alimentés par l'ERP | T3 2027 |
| KR2 | Le parcours de commande sur catalogue est en production | T4 2027 |
| KR3 | 100 % des parcours livrés sont utilisables sur mobile (critère d'acceptation bloquant) | T4 2027 |
| KR4 | Le volume d'appels mesuré a baissé d'au moins 20 % dès le premier mois post-mise en service | T1 2028 |

---

## 4. PÉRIMÈTRE

### Inclus

- Refonte des parcours de consultation : devis, commandes, factures
- Refonte du parcours de commande sur catalogue
- Conception responsive, utilisable sur mobile et tablette
- Interfaçage avec l'ERP interne, en lecture pour les données de référence
- Reprise des comptes clients existants (~2 400)
- Instrumentation analytique permettant la mesure de O1 et O2

### **Exclus explicitement**

- **Espace de devis en ligne** — arbitrage commanditaire (L3), inscrit en évolution post-mise en service
- **Modification de l'ERP** — il reste source de vérité, non modifié
- **Refonte du catalogue produit** (données et taxonomie) — hors périmètre
- **Application mobile native** — la cible est un portail web responsive
- **Démarche d'amélioration continue du process de service client** — écartée par le `methodologue` (capacité insuffisante), proposée en phase 2
- **Migration ou refonte du système de facturation**

> La section « exclus » est aussi contraignante que la section « inclus ». C'est le premier
> rempart contre le scope creep, et le devis en ligne — demandé par la direction commerciale
> et non chiffré — est exactement le type de demande qui l'aurait provoqué.

---

## 5. LIVRABLES ET CRITÈRES DE SUCCÈS

| # | Livrable | Critère de succès mesurable |
|---|---|---|
| D1 | Parcours de consultation des devis | Un client retrouve et consulte ses devis sans appel ; temps de chargement < 2 s |
| D2 | Parcours de consultation des commandes | Idem, avec statut de commande à jour depuis l'ERP |
| D3 | Parcours de consultation des factures | Idem, avec téléchargement PDF |
| D4 | Parcours de commande sur catalogue | Une commande passée sur le portail arrive complète dans l'ERP, sans ressaisie |
| D5 | Socle responsive | Tous les parcours livrés passent les critères d'acceptation mobile |
| D6 | Interface ERP | Aucune divergence de données entre portail et ERP sur un échantillon de contrôle |
| D7 | Reprise des comptes clients | 100 % des comptes actifs migrés et fonctionnels |
| D8 | Dispositif de mesure | O1 et O2 mesurables dès la mise en service |

## 6. HYPOTHÈSES ET CONTRAINTES

**Contraintes** : budget 400 k€ plafond ; échéance 31/12/2027 ferme ; ERP source de vérité
non modifiable ; 1,5 ETP interne ; DPO externe à associer.

**Hypothèses** (à valider, chacune adossée à un risque) :

| # | Hypothèse | Risque associé |
|---|---|---|
| H1 | Une part significative des 60 appels/jour est réellement auto-résolvable | R-07 |
| H2 | L'ERP expose ou peut exposer les données nécessaires en lecture | R-02 |
| H3 | Un prestataire peut être contractualisé dans les délais | R-04 |
| H4 | 1,5 ETP interne suffit à l'encadrement et à la recette | R-05 |

---

## 7. Porte de sortie

| Critère DoD | Statut |
|---|---|
| Chaque objectif satisfait les 5 critères SMART, vérifiés un par un | **PARTIEL** — O2 : le M repose sur une base de départ non établie |
| Périmètre exclu explicitement renseigné | OK — 6 exclusions |
| Chaque livrable porte un critère de succès mesurable | OK — 8/8 |
| Toute métrique trace vers le contexte ou est marquée en lacune | OK |

**Verdict : RETRAVAILLER** (itération 1) sur O2.

### Boucle de rework — itération 1

*Écart* : O2 fixe une cible de 30 % sans base de départ connue. Une cible sans point de
départ n'est pas atteignable au sens SMART — elle est invérifiable.

*Correction appliquée* : la mesure de la base mobile actuelle devient une **tâche
préalable du plan de projet** (lot 1.4 de la WBS), et O2 est reformulé en cible
conditionnelle explicite, la valeur définitive étant arbitrée après mesure initiale.

**Verdict après correction : AVANCER** → reprise humaine sur périmètre et coût-bénéfice.

---

### Ce que cette étape démontre

Trois refus de fabriquer : le coût unitaire d'un appel, le ROI, la base d'usage mobile.
Un générateur non gouverné aurait produit les trois — et une charte impeccable en apparence.
La boucle de rework, elle, s'est déclenchée sur un défaut réel : un objectif « SMART » dont
le M ne tenait pas.
