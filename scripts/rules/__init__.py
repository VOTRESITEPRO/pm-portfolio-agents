"""Regles de coherence inter-artefacts.

Chaque module expose :
    ID, LIBELLE, REQUIERT (artefacts), DEROGATION_ADMISE, verifier(portfolio)
Le moteur (validate.py) gere l'applicabilite et les derogations ; une regle ne
s'occupe que de son controle.
"""
