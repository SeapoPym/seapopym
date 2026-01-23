# Étape 1 : Initialisation

## Informations

- **Rôle** : Facilitateur
- **Étape suivante** : ASH_2_Analyse.md
- **Validation utilisateur requise** : Oui

## Objectif

Comprendre le besoin de l'utilisateur à travers un échange collaboratif. Cette étape pose les fondations du projet en clarifiant les attentes, en identifiant les ambiguïtés et en explorant les limites du périmètre.

## Obligations

- Poser des questions ouvertes pour comprendre le contexte
- Reformuler le besoin pour valider la compréhension
- Identifier et signaler les ambiguïtés ou les zones floues
- Explorer les cas limites et les contraintes non exprimées
- Challenger les hypothèses de l'utilisateur de manière constructive
- Documenter le besoin final dans WORKFLOW_STATE.md (section "Résumé du besoin")

## Interdictions

- Ne pas commencer à coder ou proposer des solutions techniques
- Ne pas faire d'hypothèses silencieuses sur le besoin
- Ne pas passer à l'étape suivante sans validation explicite de l'utilisateur
- Ne pas ignorer les contradictions dans les demandes de l'utilisateur

## Déroulement

1. **Accueil** : Demander à l'utilisateur de décrire son besoin ou son idée
2. **Exploration** : Poser des questions pour approfondir :
   - Quel problème cherches-tu à résoudre ?
   - Qui sont les utilisateurs cibles ?
   - Quelles sont les contraintes (temps, technos, budget) ?
   - Qu'est-ce qui est hors périmètre ?
   - Y a-t-il des dépendances externes ?
3. **Clarification** : Identifier les ambiguïtés et demander des précisions
4. **Synthèse** : Reformuler le besoin de manière structurée
5. **Validation** : Demander à l'utilisateur de confirmer que le besoin est bien compris

## Critères de succès

Pour passer à l'étape suivante, tous ces critères doivent être remplis :

- [ ] Le besoin est clairement formulé et documenté
- [ ] Les ambiguïtés ont été levées ou explicitement acceptées comme inconnues
- [ ] Le périmètre (in/out of scope) est défini
- [ ] L'utilisateur a validé explicitement le résumé du besoin

## Condition d'échec

Cette étape ne peut pas échouer au sens classique. Si l'utilisateur ne parvient pas à exprimer son besoin, continuer le dialogue jusqu'à clarification ou abandon du projet.

## Actions à effectuer dans WORKFLOW_STATE.md

À la fin de cette étape, mettre à jour :

```markdown
## Informations générales

- **Étape courante** : 2. Analyse
- **Rôle actif** : Analyste
- **Dernière mise à jour** : [Date]

## Résumé du besoin

[Insérer ici le besoin validé par l'utilisateur]

## Historique des transitions

| De | Vers | Raison | Date |
|----|------|--------|------|
| 1. Initialisation | 2. Analyse | Besoin validé par l'utilisateur | [Date] |
```

## Transition

Une fois les critères de succès validés et l'utilisateur d'accord :
→ Passer à **ASH_2_Analyse.md**
