# Agent `parties-prenantes` — Analyse des parties prenantes et matrice RACI

**Compétence Google PM Cert** : C2 — analyse des parties prenantes, grille pouvoir/intérêt,
matrice RACI, rôles et responsabilités
**Entrée** : dossier de contexte + charte (livrables D1 à D8)

---

## 1. Registre des parties prenantes

| # | Partie prenante | Rôle projet | Pouvoir | Intérêt | Source | Statut |
|---|---|---|---|---|---|---|
| PP1 | Direction générale | Sponsor, arbitrage budgétaire | Élevé | Moyen | contexte | Confirmé |
| PP2 | Direction commerciale | Demandeur du devis en ligne (exclu v1) | Élevé | Élevé | contexte | Confirmé |
| PP3 | Responsable service client | Bénéficiaire principal de O1 | Moyen | Élevé | contexte | Confirmé |
| PP4 | Conseillers service client | Utilisateurs indirects, source de la donnée d'appels | Faible | Élevé | contexte | Confirmé |
| PP5 | Responsable IT | Garant de l'intégration ERP | Élevé | Élevé | contexte | Confirmé |
| PP6 | Équipe IT (4 pers., 1,5 ETP alloué) | Réalisation et recette internes | Moyen | Élevé | contexte + arbitrage L4 | Confirmé |
| PP7 | Prestataire externe | Réalisation | Moyen | Moyen | contexte | **À contractualiser** |
| PP8 | Clients professionnels (~2 400) | Utilisateurs finaux | Faible | Élevé | contexte | Confirmé |
| PP9 | Clients pilotes | Validation itérative des parcours | Faible | Élevé | *déduit de la méthodologie hybride* | **À constituer** |
| PP10 | DPO externe | Conformité RGPD | Moyen | Faible | arbitrage L6 | Confirmé |
| PP11 | Direction administrative et financière | Suivi budgétaire, coût unitaire d'un appel | Élevé | Faible | *déduit du besoin de sourcer le ROI* | **À confirmer** |

> Les entrées PP9 et PP11 ne figurent pas dans la demande initiale : elles sont marquées
> « à confirmer / à constituer », pas présentées comme acquises. C'est la règle de
> traçabilité — chaque partie prenante trace vers le contexte, ou porte la mention.

## 2. Grille pouvoir / intérêt et stratégie d'engagement

```
        ^  POUVOIR
        |
 ÉLEVÉ  |  Satisfaire                 |  Gérer étroitement
        |  PP11 (DAF)                 |  PP1 (DG)
        |                             |  PP2 (Dir. commerciale)
        |                             |  PP5 (Responsable IT)
        |-----------------------------+-----------------------------
        |  Surveiller                 |  Tenir informé
 FAIBLE |  PP10 (DPO)*                |  PP3, PP4, PP6, PP7, PP8, PP9
        |
        +-------------------------------------------------> INTÉRÊT
                    FAIBLE                      ÉLEVÉ
```
\* PP10 est à pouvoir moyen : positionné en surveillance rapprochée, avec veto de conformité.

| Quadrant | Parties prenantes | Stratégie |
|---|---|---|
| **Gérer étroitement** | PP1, PP2, PP5 | Comité de pilotage mensuel, arbitrages formalisés. **PP2 est la vigilance n°1** : demandeur du devis en ligne exclu du périmètre, c'est la source de scope creep la plus probable. |
| **Satisfaire** | PP11 | Reporting budgétaire trimestriel ; sollicitée pour sourcer le coût unitaire d'un appel |
| **Tenir informé** | PP3, PP4, PP6, PP7, PP8, PP9 | Démonstrations de fin de sprint, communication de mise en service |
| **Surveiller** | PP10 | Consultation au cadrage, validation avant mise en service |

## 3. Matrice RACI

**R** = Réalise · **A** = Approuve (un seul par livrable) · **C** = Consulté · **I** = Informé

| Livrable | PP1 DG | PP2 Comm. | PP3 SC | PP5 IT | PP6 Éq. IT | PP7 Presta. | PP9 Pilotes | PP10 DPO |
|---|---|---|---|---|---|---|---|---|
| D1 Consultation devis | I | C | C | **A** | R | R | C | I |
| D2 Consultation commandes | I | C | C | **A** | R | R | C | I |
| D3 Consultation factures | I | I | C | **A** | R | R | C | C |
| D4 Commande sur catalogue | I | **A** | C | C | R | R | C | I |
| D5 Socle responsive | I | I | I | **A** | C | R | C | I |
| D6 Interface ERP | I | I | I | **A** | R | C | I | C |
| D7 Reprise des comptes clients | I | I | C | **A** | R | C | I | **C** |
| D8 Dispositif de mesure | **A** | C | R | C | R | C | I | C |

### Contrôles de la porte de sortie

| Contrôle | Résultat |
|---|---|
| Un seul A par livrable | OK — 8/8 |
| Au moins un R par livrable | OK — 8/8 |
| Toute partie prenante du registre apparaît dans la matrice, ou son absence est justifiée | **PARTIEL** |

**Parties prenantes absentes de la matrice** — justifications :
- **PP4 (conseillers)** : consultés en tant que source de donnée, pas responsables d'un livrable. Rattachés à PP3.
- **PP8 (clients)** : destinataires finaux, non responsables. Représentés par PP9.
- **PP11 (DAF)** : hors chaîne de production des livrables ; intervient sur le suivi budgétaire, tracé au plan de communication.

**Verdict : Avancer**

## 4. Reprise humaine

La cartographie politique réelle n'est pas déductible d'un texte. Trois points appellent explicitement une validation humaine :

1. **PP2 en A sur D4** : la direction commerciale approuve le parcours de commande. Est-ce
   le rapport de force réel, ou le responsable IT approuve-t-il tout ? L'agent a fait un choix fonctionnel ; il peut être faux politiquement.
2. **PP5 en A sur 6 livrables sur 8** : forte concentration. Soutenable si le responsable IT
   est réellement le référent technique unique ; risque de goulot sinon.
3. **Existence et disponibilité de PP9** : un panel de clients pilotes se constitue, il ne
   se décrète pas. La méthodologie hybride en dépend.

---

### Ce que cette étape démontre

Le RACI est mécaniquement vérifiable (un seul A, au moins un R, couverture du registre) — c'est ce qui rend la porte qualité exécutable plutôt que déclarative. Mais la démonstration utile en entretien est la section 4 : l'agent produit une matrice cohérente **et signale lui-même les trois points où sa cohérence pourrait être politiquement fausse.**
