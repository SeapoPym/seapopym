# Étape 6 : Revue

## Informations

- **Rôle** : Reviewer
- **Étape précédente** : ASH_5_Execution.md
- **Étape suivante** : ASH_7_Resolution.md (si issues) ou ASH_8_Test.md (si OK)
- **Validation utilisateur requise** : Non

## Objectif

Valider et examiner la qualité du travail réalisé. Cette étape combine les vérifications automatiques (lint, typecheck) et l'examen manuel de la qualité du code.

## Obligations

- Exécuter toutes les vérifications automatiques
- Examiner la cohérence avec les patterns existants
- Analyser les tâches échouées pour comprendre les causes
- Documenter toutes les issues trouvées
- Décider de la suite : Resolution, retour Architecture, ou Test

## Interdictions

- Ne pas modifier le code (réservé à l'étape Resolution)
- Ne pas ignorer les issues trouvées
- Ne pas passer aux tests si des issues critiques sont présentes

## Sous-tâches

### 1. Vérification automatique

Exécuter les outils de qualité configurés dans le projet :

- **Linter** (ESLint, Pylint, etc.) : vérifier les règles de style
- **Typecheck** (TypeScript, mypy, etc.) : vérifier les types
- **Formatage** (Prettier, Black, etc.) : vérifier le formatage

Documenter les erreurs et warnings trouvés.

### 2. Cohérence avec la codebase

Vérifier manuellement :

- Les conventions de nommage sont respectées
- L'organisation des fichiers suit les patterns existants
- Le style de code est cohérent avec le reste du projet
- Pas de duplication de code

### 3. Qualité du code

Examiner :

- Lisibilité : le code est compréhensible
- Maintenabilité : le code sera facile à modifier
- Absence de code mort ou commenté
- Gestion des erreurs appropriée

### 4. Analyse des échecs

Pour chaque tâche échouée à l'étape Execution :

- Comprendre la cause de l'échec
- Déterminer si c'est un problème de conception ou d'implémentation
- Décider de l'action : corriger, re-architecturer, ou accepter

## Critères de succès

Pour passer à l'étape suivante :

- [ ] Toutes les vérifications automatiques ont été exécutées
- [ ] Les issues sont documentées avec leur sévérité
- [ ] Les tâches échouées ont été analysées
- [ ] Une décision est prise pour chaque issue

## Classification des issues

| Sévérité | Description | Action |
|----------|-------------|--------|
| Critique | Bloque le fonctionnement | Doit être corrigé |
| Majeure | Impact significatif | Devrait être corrigé |
| Mineure | Impact limité | Peut être corrigé |
| Info | Suggestion d'amélioration | Optionnel |

## Condition d'échec

- **Problème de conception** : Si les échecs ou issues révèlent un défaut d'architecture, retourner à l'étape Analyse ou Architecture.

## Actions à effectuer dans WORKFLOW_STATE.md

À la fin de cette étape, ajouter :

```markdown
## Rapport de revue

### Vérifications automatiques

| Outil | Résultat | Erreurs | Warnings |
|-------|----------|---------|----------|
| ESLint | ✅/❌ | [N] | [N] |
| TypeScript | ✅/❌ | [N] | [N] |
| Prettier | ✅/❌ | [N] | - |

### Issues identifiées

| ID | Sévérité | Description | Fichier | Action |
|----|----------|-------------|---------|--------|
| I1 | Critique | Variable non typée | src/utils.ts:42 | Corriger |
| I2 | Mineure | Nommage incohérent | src/api.ts:15 | Corriger |

### Analyse des tâches échouées

| Tâche | Cause | Recommandation |
|-------|-------|----------------|
| T3 | API externe indisponible | Créer un mock, corriger plus tard |

### Décision

[X issues à corriger → Passer à Resolution]
ou
[0 issues → Passer directement à Test]
ou
[Problème de conception → Retour à Architecture]
```

Mettre à jour les informations générales :

```markdown
## Informations générales

- **Étape courante** : 7. Resolution (ou 8. Test si pas d'issues)
- **Rôle actif** : Développeur (ou Testeur)
- **Dernière mise à jour** : [Date]

## Historique des transitions

| De | Vers | Raison | Date |
|----|------|--------|------|
| ... | ... | ... | ... |
| 6. Revue | 7. Resolution | X issues à corriger | [Date] |
```

## Transition

Selon le résultat de la revue :
- **Issues à corriger** → Passer à **ASH_7_Resolution.md**
- **Aucune issue** → Passer directement à **ASH_8_Test.md**
- **Problème de conception** → Retourner à **ASH_2_Analyse.md** ou **ASH_3_Architecture.md**
