# Agent `planificateur-wbs` — WBS, plan de projet, jalons et chemin critique

**Compétence Google PM Cert** : C3 — work breakdown structure, estimation de durée,
jalons, chemin critique
**Entrée** : charte (livrables D1-D8, périmètre), contexte (échéance, ressources)

> **Agent ajouté à la tranche verticale en cours de route.** Sa porte de sortie n'était pas
> prévue dans le périmètre initial ; l'agent `risques` s'est révélé non démarrable sans
> chemin critique. Voir `99-lecons-conception.md`, leçon n°1.

---

## 1. Work Breakdown Structure

| Lot | Intitulé | Livrable(s) couvert(s) | Durée estimée* |
|---|---|---|---|
| **1** | **Cadrage et contractualisation** | | **10-14 sem.** |
| 1.1 | Cadrage détaillé et validation du périmètre | — | 3-4 sem. |
| 1.2 | Analyse de la volumétrie et de la typologie des appels | D8 | 3-4 sem. |
| 1.3 | Étude d'exposition des données ERP (faisabilité, mode d'accès) | D6 | 4-5 sem. |
| 1.4 | Mesure de la base de départ (appels/jour, part d'usage mobile) | D8 | 2-3 sem. |
| 1.5 | Appel d'offres et sélection du prestataire | — | 6-8 sem. |
| 1.6 | Contractualisation | — | 3-5 sem. |
| **2** | **Conception** | | **8-11 sem.** |
| 2.1 | Identification des parcours auto-résolvables (à partir de 1.2) | D1-D4 | 3-4 sem. |
| 2.2 | Architecture d'information et parcours cibles | D1-D4 | 4-5 sem. |
| 2.3 | Design system responsive | D5 | 4-6 sem. |
| 2.4 | Architecture technique et conception de l'interface ERP | D6 | 4-5 sem. |
| **3** | **Réalisation itérative** (sprints de 2 semaines) | | **26-34 sem.** |
| 3.1 | Socle technique, authentification, performance | D5 | 6-8 sem. |
| 3.2 | Interface ERP en lecture | D6 | 6-8 sem. |
| 3.3 | Parcours consultation des devis | D1 | 4-5 sem. |
| 3.4 | Parcours consultation des commandes | D2 | 4-5 sem. |
| 3.5 | Parcours consultation des factures | D3 | 3-4 sem. |
| 3.6 | Parcours de commande sur catalogue | D4 | 8-11 sem. |
| 3.7 | Conformité responsive (transverse, critère d'acceptation de chaque sprint) | D5 | continu |
| **4** | **Reprise et bascule** | | **9-13 sem.** |
| 4.1 | Reprise des ~2 400 comptes clients | D7 | 4-6 sem. |
| 4.2 | Recette fonctionnelle et UAT | D1-D7 | 5-7 sem. |
| 4.3 | Validation de conformité RGPD (DPO) | D3, D7 | 2-3 sem. |
| 4.4 | Mise en service et bascule | D1-D7 | 2-3 sem. |
| **5** | **Post-mise en service** | | **12 sem.** |
| 5.1 | Support renforcé (hypercare) | — | 6 sem. |
| 5.2 | Mesure de O1 et O2 | D8 | 12 sem. |

\* **Fourchettes non empiriques.** Aucune donnée de vélocité ni d'historique projet n'a été
fournie. Ces durées sont un **support d'atelier d'estimation**, jamais un engagement. Elles
doivent être recalibrées avec l'équipe et le prestataire retenu.

## 2. Couverture des livrables de la charte

| Livrable | Lots couvrants | Statut |
|---|---|---|
| D1 Consultation devis | 2.1, 2.2, 3.3, 4.2 | Couvert |
| D2 Consultation commandes | 2.1, 2.2, 3.4, 4.2 | Couvert |
| D3 Consultation factures | 2.1, 2.2, 3.5, 4.2, 4.3 | Couvert |
| D4 Commande catalogue | 2.1, 2.2, 3.6, 4.2 | Couvert |
| D5 Socle responsive | 2.3, 3.1, 3.7 | Couvert |
| D6 Interface ERP | 1.3, 2.4, 3.2 | Couvert |
| D7 Reprise des comptes | 4.1, 4.2, 4.3 | Couvert |
| D8 Dispositif de mesure | 1.2, 1.4, 5.2 | Couvert |

**8/8 livrables couverts. Aucune tâche orpheline** (tout lot trace vers au moins un livrable,
hors 1.1, 1.5, 1.6, 5.1 qui sont des lots de conduite de projet identifiés comme tels).

## 3. Jalons

| Jalon | Intitulé | Cible | Nature |
|---|---|---|---|
| J1 | Périmètre validé et base de mesure établie | fin T4 2026 | Interne |
| J2 | Prestataire contractualisé | fin T1 2027 | **Contractuel** |
| J3 | Conception validée, architecture ERP arrêtée | fin T2 2027 | Contractuel |
| J4 | Parcours de consultation en production (D1-D3) | fin T3 2027 | Contractuel — KR1 |
| J5 | Parcours de commande en production (D4) | fin T4 2027 | Contractuel — KR2 |
| J6 | Mise en service complète | **31/12/2027** | **Contractuel, ferme** |
| J7 | Mesure des objectifs O1 et O2 | 31/03/2028 | Interne |

## 4. Chemin critique

```
1.3 ──▶ 1.5 ──▶ 1.6 ──▶ 2.4 ──▶ 3.1 ──▶ 3.2 ──▶ 3.3 ──▶ 3.6 ──▶ 4.1 ──▶ 4.2 ──▶ 4.4
Étude   Appel   Contrac  Archi   Socle   Inter   Parcours Commande Reprise Recette Bascule
ERP     d'offres -tualis. tech.          ERP     devis    catalogue comptes  UAT
```

**11 lots sur le chemin critique.** Durée cumulée : **50-67 semaines**.

### Constat structurant — marge nulle en hypothèse haute

Fenêtre disponible : du 01/09/2026 au 31/12/2027 ≈ **69 semaines**.

| Scénario | Durée du chemin critique | Marge |
|---|---|---|
| Hypothèse basse | 50 sem. | 19 sem. (~4,5 mois) |
| Hypothèse haute | 67 sem. | **2 sem.** |

**L'échéance du 31/12/2027 n'est pas tenable en hypothèse haute.** Ce n'est pas une alerte
de confort : le jalon J6 est adossé au pic commercial de janvier, donc non reportable.

**Trois leviers**, à arbitrer par le chef de projet — l'agent ne tranche pas :

1. **Paralléliser 1.3 avec 1.5** (étude ERP pendant l'appel d'offres) : gain estimé 4-5 sem.
   Contrepartie : l'appel d'offres part sur une hypothèse technique non consolidée.
2. **Réduire le périmètre de la v1** en décalant D4 (commande catalogue, lot 3.6, le plus
   lourd du chemin critique) après la mise en service. Gain : 8-11 sem. Contrepartie :
   KR2 non atteint au T4 2027.
3. **Renforcer le prestataire** sur 3.3-3.6. Contrepartie : pression sur le plafond de 400 k€.

## 5. Porte de sortie

| Critère DoD | Statut |
|---|---|
| Chaque livrable de la charte est couvert par ≥ 1 lot | OK — 8/8 |
| Aucune tâche orpheline | OK |
| Chemin critique identifié | OK — 11 lots |
| Cohérence avec l'échéance du contexte, **ou écart signalé explicitement** | **ÉCART SIGNALÉ** — marge de 2 semaines en hypothèse haute |

**Verdict : AVANCER avec écart signalé** → reprise humaine obligatoire.

## 6. Reprise humaine — VALIDATION OBLIGATOIRE

Les estimations de durée n'ont aucune base empirique sur cette équipe et ce prestataire.
Elles servent de point de départ d'atelier d'estimation. **Le choix du levier de réduction
du chemin critique appartient au chef de projet et au sponsor.**

---

### Ce que cette étape démontre

L'agent n'a pas produit un planning qui « rentre » dans l'échéance. Il a produit un chemin
critique, l'a confronté à la fenêtre réelle, et a signalé que l'échéance ne tenait pas en
hypothèse haute — en proposant trois leviers chiffrés sans en choisir aucun. C'est
exactement la ligne de partage revendiquée : l'IA calcule et alerte, le chef de projet
arbitre.
