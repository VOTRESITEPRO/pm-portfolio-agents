# Agent `contexte-projet` — Dossier de contexte et registre des lacunes

**Entrée** : demande brute (00-cas-etude.md)
**Porte de sortie (DoD)** : tous les champs renseignés ou déclarés en lacune qualifiée ;
aucune lacune bloquante non résolue.

---

## 1. Dossier de contexte (extrait lisible du JSON)

| Champ | Valeur | Source |
|---|---|---|
| Nom du projet | Refonte du portail client B2B | demande |
| Commanditaire | Direction générale | demande |
| Secteur | Distribution de matériel industriel | demande |
| Effectif | 180 salariés | demande |
| Base clients | ~2 400 clients professionnels | demande |
| Problème | Portail de 2016 : lenteur, inutilisable sur mobile, faible autonomie client | demande |
| Signal quantifié | ~60 appels/jour au service client | demande |
| Contrainte technique | L'ERP interne reste source de vérité (stocks, facturation) — non négociable | demande |
| Ressource interne | Équipe IT = 4 personnes | demande |
| Sourcing | Recours à un prestataire envisagé | demande |
| Budget évoqué | ~400 k€ | demande (non arbitré) |
| Échéance évoquée | Fin de l'exercice suivant | demande (non datée) |

## 2. Registre des lacunes d'information

| # | Lacune | Gravité | Effet si non résolue |
|---|---|---|---|
| L1 | « Fin de l'exercice suivant » : exercice fiscal non défini, aucune date | **Bloquante** | Aucun jalon ni chemin critique calculable |
| L2 | « Autour de 400 k€ » : enveloppe évoquée en comité, non votée. Plafond ou cible ? | **Bloquante** | Budget non opposable ; arbitrages de périmètre impossibles |
| L3 | Espace de devis en ligne : dans le périmètre ou non ? Non chiffré | **Bloquante** | Périmètre indéterminé ; charte non rédigeable |
| L4 | Part des 4 personnes IT réellement allouée au projet | Dégradante | Estimations de charge sans base |
| L5 | Typologie et volumétrie détaillées des 60 appels/jour | Dégradante | Impossible de cibler ce qui est réellement auto-résolvable |
| L6 | Cadre RGPD / traitement des données clients : DPO identifié ? | Mineure | Risque de conformité non instruit |
| L7 | Aucun critère de succès chiffré fourni par le commanditaire | **Bloquante** | Objectifs SMART non formulables (le M manque) |

## 3. Verdict de la porte de sortie

**Escalader** — 4 lacunes bloquantes (L1, L2, L3, L7).
La chaîne s'arrête. L'agent ne produit aucune valeur de substitution.

> C'est le comportement attendu, pas un échec. Un système qui aurait « estimé » un budget
> de 400 k€ ferme, une échéance au 31/12 et un objectif de −30 % d'appels aurait produit un
> portfolio entièrement plausible et entièrement faux.

## 4. Reprise humaine — arbitrages du commanditaire

Réponses obtenues (simulées pour la démonstration) :

| # | Arbitrage rendu |
|---|---|
| L1 | Exercice = année civile. **Échéance ferme : 31/12/2027.** Mise en service avant le pic commercial de janvier. |
| L2 | **400 k€ = plafond voté, non extensible.** Tout dépassement passe en comité. |
| L3 | **Devis en ligne HORS périmètre v1**, inscrit en évolution post-mise en service. |
| L7 | Critère principal : **réduire de 40 % le volume d'appels** auto-résolvables, soit une cible de 36 appels/jour. Critère secondaire : usage mobile mesurable. |
| L4 | **1,5 ETP interne** alloué au projet sur la durée. |
| L5 | Non disponible — **converti en risque** (voir 05-registre-risques.md, R-07). |
| L6 | DPO externe mandaté, à associer au cadrage. |

## 5. Verdict après reprise humaine

**Avancer** — 0 lacune bloquante résiduelle. L5 tracée en risque, L6 en partie prenante.

---

### Ce que cette étape démontre

Le registre des lacunes est un **livrable**, pas une note de travail. En entretien, c'est l'artefact qui prouve que le système est gouverné : il sait ce qu'il ne sait pas, et il refuse d'avancer sans arbitrage humain sur les quatre points qui engagent l'organisation.
