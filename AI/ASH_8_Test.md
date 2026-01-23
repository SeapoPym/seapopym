# Étape 8 : Test

## Informations

- **Rôle** : Testeur
- **Étape précédente** : ASH_7_Resolution.md (ou ASH_6_Revue.md si pas d'issues)
- **Étape suivante** : ASH_9_Finalisation.md
- **Validation utilisateur requise** : Non

## Objectif

Créer et exécuter les tests pour le code développé. Cette étape valide que le code fonctionne comme attendu ou identifie les problèmes à corriger.

## Obligations

- Créer des tests pour chaque fonctionnalité implémentée
- Couvrir les cas nominaux (happy path)
- Couvrir les cas d'erreur et cas limites
- Suivre les conventions de test du projet existant
- Utiliser le framework de test déjà en place (ou en proposer un si absent)
- Exécuter tous les tests créés
- Documenter les résultats (passés, échoués, ignorés)
- Analyser chaque test échoué pour identifier la cause
- Mettre à jour WORKFLOW_STATE.md avec les tests et résultats

## Interdictions

- Ne pas modifier le code source (seulement les fichiers de test)
- Ne pas ignorer les cas d'erreur
- Ne pas créer des tests qui dépendent de l'environnement externe sans mock
- Ne pas ignorer les tests échoués sans analyse
- Ne pas supprimer des tests pour faire "passer" la suite

## Types de tests à créer

Selon le contexte du projet :

| Type        | Quand                        | Exemple                              |
| ----------- | ---------------------------- | ------------------------------------ |
| Unitaire    | Fonctions/méthodes isolées   | Tester `validateEmail()`             |
| Intégration | Interactions entre modules   | Tester `UserService` avec `Database` |
| E2E         | Parcours utilisateur complet | Tester le flow de login              |

Prioriser les tests unitaires, puis intégration si pertinent.

## Déroulement

### Phase 1 : Création des tests

1. **Inventaire** : Lister les fonctionnalités à tester depuis la todo list
2. **Stratégie** : Définir quels types de tests pour chaque fonctionnalité
3. **Cas de test** : Pour chaque fonctionnalité, identifier :
   - Cas nominal (entrée valide → résultat attendu)
   - Cas limites (entrées aux bornes)
   - Cas d'erreur (entrées invalides)
4. **Implémentation** : Écrire les fichiers de test

### Phase 2 : Exécution des tests

5. **Exécution** : Lancer la suite de tests complète
6. **Collecte** : Noter les résultats (passés/échoués/ignorés)
7. **Analyse** : Pour chaque test échoué, identifier la cause
8. **Documentation** : Mettre à jour WORKFLOW_STATE.md

## Structure des tests

Suivre le pattern AAA (Arrange, Act, Assert) :

```
test("description du comportement attendu", () => {
  // Arrange : préparer les données
  // Act : exécuter la fonction
  // Assert : vérifier le résultat
})
```

Nommer les tests de manière descriptive :

- ✅ "should return true for valid email"
- ✅ "should throw error when user not found"
- ❌ "test1"
- ❌ "email test"

## Analyse des échecs

Pour chaque test échoué, classifier la cause :

| Cause               | Description                                            | Action                           |
| ------------------- | ------------------------------------------------------ | -------------------------------- |
| Test incorrect      | Le test est mal écrit ou teste le mauvais comportement | Corriger le test et relancer     |
| Bug code            | Le code ne fait pas ce qu'il devrait                   | Retourner à l'étape Execution    |
| Problème conception | L'architecture ne permet pas le comportement attendu   | Retourner à l'étape Architecture |

## Critères de succès

Pour passer à l'étape suivante :

- [ ] Chaque fonctionnalité a au moins un test
- [ ] Les cas nominaux sont couverts
- [ ] Les principaux cas d'erreur sont couverts
- [ ] Les tests suivent les conventions du projet
- [ ] Tous les tests ont été exécutés
- [ ] Tous les tests passent (ou les échecs sont analysés avec décision)

## Condition d'échec

- **Code non testable** : Si le code est structuré de manière non testable (couplage fort, effets de bord), documenter le problème. Peut nécessiter un retour à l'Architecture.

- **Bug dans le code** → Retourner à **ASH_5_Execution.md**
  - Ajouter une tâche de correction dans la todo list
  - Repasser par Execution → Revue → Resolution → Test

- **Problème de conception** → Retourner à **ASH_3_Architecture.md**
  - Revoir l'architecture
  - Reprendre le workflow depuis là

## Actions à effectuer dans WORKFLOW_STATE.md

À la fin de cette étape, ajouter :

```markdown
## Tests

### Tests créés

| Fichier                   | Fonctionnalité testée        | Nb tests | Types       |
| ------------------------- | ---------------------------- | -------- | ----------- |
| tests/validator.test.ts   | validateEmail, validatePhone | 8        | Unitaire    |
| tests/userService.test.ts | createUser, getUser          | 5        | Unitaire    |
| tests/api.test.ts         | POST /users, GET /users      | 4        | Intégration |

### Résultats d'exécution

- **Date** : [Date]
- **Commande** : `npm test` / `pytest` / etc.

| Statut     | Nombre |
| ---------- | ------ |
| ✅ Passés  | [N]    |
| ❌ Échoués | [N]    |
| ⏭ Ignorés | [N]    |
| **Total**  | [N]    |

### Tests échoués (si applicable)

| Test                  | Fichier           | Cause    | Action           |
| --------------------- | ----------------- | -------- | ---------------- |
| should validate email | validator.test.ts | Bug code | Retour Execution |

## Informations générales

- **Étape courante** : 9. Finalisation
- **Rôle actif** : Facilitateur
- **Dernière mise à jour** : [Date]

## Historique des transitions

| De      | Vers            | Raison                 | Date   |
| ------- | --------------- | ---------------------- | ------ |
| ...     | ...             | ...                    | ...    |
| 8. Test | 9. Finalisation | Tous les tests passent | [Date] |
```

## Transition

Selon les résultats :

- **Tous les tests passent** → Passer à **ASH_9_Finalisation.md**
- **Bugs dans le code** → Retourner à **ASH_5_Execution.md**
- **Problème de conception** → Retourner à **ASH_3_Architecture.md**
