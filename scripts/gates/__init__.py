"""Portes qualite mecaniques, un artefact a la fois.

Chaque module expose :
    ID, LIBELLE, REQUIERT (artefacts), DEROGATION_ADMISE, verifier(portfolio)
Meme interface que scripts/rules/ ; la difference est de perimetre, pas de
mecanique : une porte controle un artefact seul, une regle en croise plusieurs
(voir docs/ecarts-spec-implementation.md). Le moteur (validate.py) les evalue
ensemble via charger_regles() + charger_portes().
"""
