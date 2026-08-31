"""R11 — Tout total annonce est recalcule a partir de ses composants (correction C3).

Origine : le chemin critique annonce 50-67 semaines valait en realite 52-71. La
conclusion managériale en etait inversee : marge annoncee +2 semaines, marge reelle
-2 semaines. C'est la seule categorie d'erreur que la relecture ne detecte pas et
que le recalcul detecte toujours.
"""
from datetime import date

from pmlib import Ecart, liste, somme_bornes, valeur_de

ID = "R11"
LIBELLE = "Tout total annonce est recalcule a partir de ses composants"
REQUIERT = ["plan"]
DEROGATION_ADMISE = False


def _lots_par_id(plan):
    return {str(l.get("id")): l for l in liste(plan.get("lots"))}


def verifier(pf):
    ecarts = []
    plan = pf.get("plan")
    lots = _lots_par_id(plan)
    critique = [str(x) for x in liste(plan.get("chemin_critique"))]
    totaux = plan.get("totaux_annonces") or {}

    # 1. Le chemin critique ne reference que des lots existants
    inconnus = [c for c in critique if c not in lots]
    for c in inconnus:
        ecarts.append(Ecart(ID, "bloquant", "pm-planificateur-wbs",
                            f"Chemin critique : lot {c} inexistant dans la WBS"))
    critique = [c for c in critique if c in lots]

    # 2. Recalcul de la duree du chemin critique
    mn, mx = somme_bornes([lots[c] for c in critique])
    annonce = (totaux.get("chemin_critique") or {})
    a_mn, a_mx = valeur_de(annonce.get("min")), valeur_de(annonce.get("max"))
    if a_mn is not None and float(a_mn) != mn:
        ecarts.append(Ecart(ID, "bloquant", "pm-planificateur-wbs",
                            f"Chemin critique, hypothese basse : {a_mn} annonce, {mn:g} recalcule",
                            f"ecart de {mn - float(a_mn):+g} semaines"))
    if a_mx is not None and float(a_mx) != mx:
        ecarts.append(Ecart(ID, "bloquant", "pm-planificateur-wbs",
                            f"Chemin critique, hypothese haute : {a_mx} annonce, {mx:g} recalcule",
                            f"ecart de {mx - float(a_mx):+g} semaines"))

    # 3. Un sous-total de lot parent ne peut pas etre inferieur a son chemin interne
    for lot in liste(plan.get("lots")):
        enfants = [l for l in liste(plan.get("lots")) if str(l.get("parent")) == str(lot.get("id"))]
        if not enfants or not lot.get("duree"):
            continue
        crit_int = [e for e in enfants if str(e.get("id")) in critique]
        if crit_int:
            i_mn, i_mx = somme_bornes(crit_int)
            l_mn = float((lot.get("duree") or {}).get("min") or 0)
            l_mx = float((lot.get("duree") or {}).get("max") or 0)
            if l_mn < i_mn or l_mx < i_mx:
                ecarts.append(Ecart(ID, "mineur", "pm-planificateur-wbs",
                                    f"Lot {lot.get('id')} : sous-total {l_mn:g}-{l_mx:g} inferieur a son "
                                    f"chemin interne {i_mn:g}-{i_mx:g}",
                                    "Le sous-total suppose un parallelisme que le chemin critique interdit"))

    # 4. Marge = fenetre calendaire reelle - duree du chemin critique
    fen = (pf.get("contexte").get("fenetre") or {}) if "contexte" in pf else {}
    d, f = fen.get("debut"), fen.get("fin")
    if d and f:
        d = d if isinstance(d, date) else date.fromisoformat(str(d))
        f = f if isinstance(f, date) else date.fromisoformat(str(f))
        semaines = (f - d).days / 7
        marge_haute = semaines - mx
        if marge_haute < 0:
            ecarts.append(Ecart(ID, "bloquant", "pm-planificateur-wbs",
                                f"Echeance intenable en hypothese haute : marge de {marge_haute:+.1f} semaine(s)",
                                f"fenetre {semaines:.1f} sem. ({d} -> {f}) contre un chemin critique de {mx:g} sem. "
                                f"— un levier de reduction est un prealable, pas une precaution"))
    return ecarts
