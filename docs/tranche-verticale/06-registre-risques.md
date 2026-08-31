# Agent `risques` — Registre des risques, matrice et plans d'atténuation

**Compétence Google PM Cert** : C3 — identification des risques, registre, matrice
probabilité/impact, plans d'atténuation
**Entrée** : plan de projet et chemin critique, contexte, registre des lacunes

---

## 1. Registre des risques

Cotation : P = probabilité (1 faible → 5 élevée), I = impact (1 → 5), **C = criticité (P×I)** Réponse : É = éviter · R = réduire · T = transférer · A = accepter

| # | Risque | Catégorie | Lot critique couvert | P | I | C | Rép. | Propriétaire | Déclencheur observable |
|---|---|---|---|---|---|---|---|---|---|
| R-01 | Le devis en ligne, exclu de la v1, est réintroduit en cours de projet par la direction commerciale | Périmètre | — | 4 | 4 | **16** | É | Chef de projet | Toute demande d'évolution mentionnant le devis en comité de pilotage |
| R-02 | L'ERP n'expose pas les données nécessaires en lecture, ou exige un développement non prévu | Technique | **1.3, 2.4, 3.2** | 3 | 5 | **15** | R | Responsable IT (PP5) | Rapport d'étude 1.3 concluant à l'absence d'interface exploitable |
| R-03 | Le plafond de 400 k€ est atteint avant la mise en service | Budget | — | 3 | 5 | **15** | R | Sponsor (PP1) | Consommation > 70 % au jalon J4 |
| R-04 | L'appel d'offres et la contractualisation dépassent le délai prévu | Délai | **1.5, 1.6** | 3 | 5 | **15** | R | Chef de projet | Absence de candidat retenu à J2 − 4 semaines |
| R-05 | 1,5 ETP interne insuffisant pour l'encadrement et la recette | Ressources | **4.2** | 4 | 4 | **16** | R | Responsable IT (PP5) | Retard de validation > 5 j. ouvrés sur deux sprints consécutifs |
| R-06 | L'organisation n'a pas la maturité agile supposée par la cadence de sprints | Organisation | — | 3 | 3 | 9 | R | Chef de projet | Deux revues de sprint sans participation métier |
| R-07 | La part réellement auto-résolvable des 60 appels/jour est trop faible pour atteindre −40 % | Métier | — | 3 | 5 | **15** | R | Resp. service client (PP3) | Résultat du lot 1.2 : part auto-résolvable < 45 % |
| R-08 | La qualité des données des ~2 400 comptes empêche une reprise propre | Données | **4.1** | 3 | 4 | 12 | R | Responsable IT (PP5) | Taux d'anomalies > 5 % sur un échantillon de contrôle |
| R-09 | La validation RGPD intervient trop tard et bloque la mise en service | Conformité | **4.4** | 2 | 5 | 10 | É | DPO (PP10) | DPO non saisi avant le jalon J4 |
| R-10 | L'exigence de performance (< 2 s) n'est pas tenue par le socle technique | Technique | **3.1** | 3 | 4 | 12 | R | Prestataire (PP7) | Mesure > 2 s en recette de sprint sur le socle |
| R-11 | Le panel de clients pilotes ne se constitue pas ou se démobilise | Externe | — | 4 | 3 | 12 | R | Dir. commerciale (PP2) | Moins de 5 pilotes actifs après deux sprints |
| R-12 | La concentration des approbations sur le responsable IT (A sur 6 livrables/8) crée un goulot | Organisation | — | 3 | 4 | 12 | R | Chef de projet | Délai moyen d'approbation > 5 j. ouvrés |
| R-13 | L'échéance du 31/12/2027, adossée au pic commercial, ne dispose d'aucune fenêtre de report | Délai | **4.4** | 4 | 5 | **20** | R | Sponsor (PP1) | Marge du chemin critique < 4 semaines à J4 |
| R-14 | La complexité fonctionnelle du catalogue et des règles de commande B2B est sous-estimée | Technique | **3.3, 3.6** | 4 | 4 | **16** | R | Prestataire (PP7) | Dépassement > 30 % de l'estimation sur le lot 3.3 |

## 2. Matrice probabilité / impact

```
        ^ IMPACT
      5 |        R-09          R-02 R-03    R-13
        |                      R-04 R-07
      4 |                      R-08 R-10    R-01 R-05
        |                      R-12          R-14
      3 |                      R-06          R-11
        |
      2 |
      1 |
        +--------------------------------------------> PROBABILITÉ
             1      2      3           4        5
```

**Risque majeur : R-13** (criticité 20). L'échéance est ferme, non reportable, et le chemin
critique n'offre que 2 semaines de marge en hypothèse haute (voir 05-wbs-plan-projet.md). Ce n'est pas un risque parmi d'autres : c'est celui qui conditionne les trois leviers d'arbitrage identifiés par le planificateur.

## 3. Plans d'atténuation — risques de criticité ≥ 15

| # | Plan d'atténuation | Plan de secours (si déclencheur atteint) |
|---|---|---|
| **R-13** | Point de marge formel à chaque jalon ; décision de réduction de périmètre déclenchée dès que la marge passe sous 4 semaines | Activation du levier 2 : décalage de D4 (commande catalogue) après mise en service |
| **R-01** | Périmètre exclu inscrit au contrat prestataire ; toute demande de devis en ligne passe en demande d'évolution chiffrée avec impact délai/budget explicite | Escalade au sponsor ; arbitrage périmètre vs échéance en comité |
| **R-05** | Recette planifiée sprint par sprint, pas en fin de projet ; charge de recette estimée dès la conception | Externalisation partielle de la recette (impact budget, arbitrage R-03) |
| **R-14** | Lot 3.3 traité en premier comme lot pilote d'étalonnage de la complexité réelle | Recalibrage de l'ensemble des estimations 3.x après 3.3 ; arbitrage de périmètre |
| **R-02** | Étude 1.3 lancée en tout premier, avant l'appel d'offres ; le mode d'accès aux données conditionne le cahier des charges | Passage par une couche d'intégration intermédiaire (impact budget et délai) |
| **R-03** | Suivi de consommation mensuel ; jalons de décision de poursuite trimestriels | Réduction de périmètre — le plafond n'est pas extensible, seul le périmètre l'est |
| **R-04** | Rédaction du cahier des charges anticipée pendant le cadrage ; sourcing préalable de candidats | Parallélisation de 1.3 avec 1.5 (levier 1), avec la contrepartie assumée |
| **R-07** | Lot 1.2 (analyse des appels) traité avant toute conception de parcours | Renégociation de la cible O1 avec le sponsor sur la base de la part réellement mesurée |

## 4. Traçabilité des lacunes converties en risques

| Lacune | Devenue | Vérification |
|---|---|---|
| L5 — typologie et volumétrie des appels non disponibles | **R-07** | OK |
| Hypothèse H1 (part auto-résolvable) | **R-07** | OK |
| Hypothèse H2 (ERP expose les données) | **R-02** | OK |
| Hypothèse H3 (prestataire contractualisable) | **R-04** | OK |
| Hypothèse H4 (1,5 ETP suffisant) | **R-05** | OK |
| Maturité agile non documentée (`methodologue`, critère C8) | **R-06** | OK |
| Goulot d'approbation PP5 (`parties-prenantes`, reprise humaine n°2) | **R-12** | OK |
| Disponibilité du panel pilote PP9 (`parties-prenantes`, reprise humaine n°3) | **R-11** | OK |

## 5. Porte de sortie

| Critère DoD | Statut |
|---|---|
| Chaque lot du chemin critique couvert par ≥ 1 risque analysé | OK — 11/11 (voir colonne « lot critique couvert ») |
| Chaque risque porte un propriétaire nommé | OK — 14/14 |
| Chaque risque porte une stratégie de réponse | OK — 14/14 |
| Chaque risque porte un déclencheur observable | OK — 14/14 |
| Chaque lacune bloquante convertie en risque | OK — L5 → R-07 |

**Verdict : Avancer**

## 6. Reprise humaine

La cotation d'impact dépend de la tolérance au risque de l'organisation, non déductible du contexte. Les cotations à 5 (R-02, R-03, R-04, R-07, R-09, R-13) engagent des décisions de poursuite : elles doivent être revues en comité de pilotage.

---

### Ce que cette étape démontre

Chaque risque est **ancré** : soit sur un lot nommé du chemin critique, soit sur une lacune du registre d'information, soit sur un point de vigilance remonté par un agent amont. Aucun risque générique du type « résistance au changement » ou « manque de communication ». C'est la porte de sortie qui l'impose — et c'est ce qui distingue un registre exploitable d'une liste de précautions oratoires.
