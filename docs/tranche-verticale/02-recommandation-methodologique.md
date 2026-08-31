# Agent `methodologue` — Recommandation de méthodologie

**Compétence Google PM Cert** : C1 — méthodologies de gestion de projet
**Entrée** : dossier de contexte validé
**Décision structurante** : positionne le drapeau d'activation de la branche agile

---

## 1. Analyse par critères

| # | Critère | Constat dans ce contexte | Pousse vers |
|---|---|---|---|
| C1 | Stabilité des exigences | Contrainte ERP ferme et non négociable ; parcours utilisateur cible inconnus (L5 non résolue) | **Mixte** : socle stable, surface instable |
| C2 | Échéance | 31/12/2027, ferme, adossée à un pic commercial | Waterfall (jalons contractuels) |
| C3 | Budget | 400 k€ plafond voté, non extensible | Waterfall (engagement au forfait) |
| C4 | Sourcing | Prestataire externe à contractualiser | Waterfall (périmètre contractualisable) |
| C5 | Capacité interne | 1,5 ETP seulement → arbitrages fréquents nécessaires | Agile (priorisation continue) |
| C6 | Découverte nécessaire | La cible « −40 % d'appels » suppose d'identifier ce qui est auto-résolvable — non spécifiable a priori | Agile (boucles de feedback) |
| C7 | Accès aux utilisateurs | 2 400 clients pros, service client interne disponible | Agile (validation itérative possible) |
| C8 | Maturité agile de l'organisation | Non documentée | **Risque** (voir R-06) |

## 2. Recommandation

### **HYBRIDE** — cadrage séquentiel, réalisation itérative

- **Phases 1 à 3 (initiation, planification, contractualisation) en waterfall.**
  Motif : un budget plafond voté et un contrat prestataire exigent un périmètre écrit,
  un budget ventilé et des jalons opposables. Ce sont des objets contractuels, pas des
  hypothèses à faire émerger.
- **Phase de réalisation en itératif, sprints de 2 semaines.**
  Motif : les parcours à auto-résoudre ne sont pas connus au démarrage. Les découvrir par
  spécification amont serait un pari ; les découvrir par livraisons successives et mesure
  du report d'appels est la seule approche qui adresse réellement C6.
- **Jalons de synchronisation contractuels** à chaque fin de trimestre : périmètre engagé
  vs périmètre livré, consommation budgétaire, décision de poursuite.

## 3. Alternatives écartées

| Alternative | Motif d'écartement |
|---|---|
| **Agile pur** | Incompatible avec C3 et C4 : on ne contractualise pas un prestataire externe sur une enveloppe plafond votée sans périmètre écrit. Le « nous verrons au fil des sprints » est ici un risque juridique et budgétaire, pas une posture méthodologique. |
| **Waterfall pur** | Incompatible avec C6 : spécifier en amont quelles fonctions réduiront les appels de 40 % revient à décider sans donnée (L5 non résolue). Le risque n'est pas le retard, c'est de livrer conforme et inutile. |
| **Composite (Lean/Six Sigma sur le flux d'appels)** | Pertinent sur le fond — la réduction d'appels est un problème de process autant que d'outil — mais hors capacité : 1,5 ETP interne ne permet pas de mener en parallèle une démarche d'amélioration continue structurée. À proposer en phase 2. |

## 4. Drapeau d'activation

```json
{ "drapeau_agile": true, "profil": "hybride", "cadence": "sprints de 2 semaines" }
```

→ Les agents `backlog-stories` et `sprint` sont activés dans la chaîne complète
(hors périmètre de cette tranche verticale).

## 5. Porte de sortie

| Critère DoD | Statut |
|---|---|
| Recommandation unique | OK — hybride |
| Argumentée sur ≥ 5 critères explicites | OK — 8 critères |
| Alternative écartée documentée | OK — 3 alternatives, motifs distincts |
| Drapeau agile positionné | OK |

**Verdict : AVANCER** → reprise humaine obligatoire avant la suite.

## 6. Reprise humaine — VALIDATION OBLIGATOIRE

Le choix de méthodologie engage le mode de contractualisation avec le prestataire et le
mode de collaboration interne. **L'IA propose, le chef de projet tranche.** Validation
réputée acquise pour la suite de la démonstration.

---

### Point d'honnêteté méthodologique

Le biais pro-agile est le risque documenté de cet agent (les corpus d'entraînement en sont
saturés). La grille de critères imposée est la mitigation : ici, quatre critères sur huit
poussaient vers le séquentiel, et c'est ce qui a produit une recommandation hybride plutôt
qu'un réflexe agile. Sans grille, la recommandation aurait probablement été « agile avec
quelques jalons ».
