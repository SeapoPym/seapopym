# Étape 4 : Planification

## Informations

- **Rôle** : Planificateur
- **Étape précédente** : ASH_3_Architecture.md
- **Étape suivante** : ASH_5_Execution.md
- **Validation utilisateur requise** : Non

## Objectif

Décomposer l'architecture validée en tâches unitaires et actionables. Chaque tâche doit être atomique : un fichier, une idée, une action. Cette étape produit la todo list qui guidera le développement.

## Obligations

- Se baser sur les décisions d'architecture pour définir les tâches
- Créer des tâches atomiques (1 tâche = 1 fichier = 1 idée)
- Attribuer un identifiant unique à chaque tâche (T1, T2, etc.)
- Définir les dépendances entre tâches
- Ordonner les tâches de manière logique (dépendances respectées)
- Rédiger des descriptions claires et non ambiguës
- Documenter la todo list dans WORKFLOW_STATE.md

## Interdictions

- Ne pas créer de tâches qui touchent plusieurs fichiers à la fois
- Ne pas créer de tâches vagues ou mal définies
- Ne pas oublier de spécifier les dépendances
- Ne pas commencer à coder (réservé à l'étape Execution)

## Déroulement

1. **Revue de l'architecture** : Relire les décisions d'architecture et la structure proposée
2. **Identification des composants** : Lister tous les fichiers/modules à créer ou modifier
3. **Décomposition** : Pour chaque composant, définir les tâches unitaires
4. **Dépendances** : Identifier quelles tâches dépendent d'autres
5. **Ordonnancement** : Organiser les tâches dans un ordre logique d'exécution
6. **Rédaction** : Écrire la todo list complète dans WORKFLOW_STATE.md

## Règles de décomposition

### Une bonne tâche

- ✅ "Créer le fichier `src/utils/validator.ts` avec la fonction `validateEmail`"
- ✅ "Ajouter la route `/api/users` dans `src/routes/index.ts`"
- ✅ "Modifier `src/config.ts` pour ajouter la variable `API_TIMEOUT`"

### Une mauvaise tâche

- ❌ "Implémenter l'authentification" (trop vague, plusieurs fichiers)
- ❌ "Créer les composants" (pas atomique)
- ❌ "Faire le backend" (beaucoup trop large)

## Critères de succès

Pour passer à l'étape suivante, tous ces critères doivent être remplis :

- [ ] Toutes les tâches sont atomiques (1 fichier, 1 idée)
- [ ] Chaque tâche a un ID unique
- [ ] Les dépendances sont spécifiées
- [ ] L'ordre d'exécution respecte les dépendances
- [ ] Les descriptions sont claires et non ambiguës

## Condition d'échec

- **Architecture insuffisante** : Si l'architecture ne permet pas de définir des tâches claires, retourner à l'étape Architecture pour plus de détails.

## Actions à effectuer dans WORKFLOW_STATE.md

À la fin de cette étape, mettre à jour :

```markdown
## Informations générales

- **Étape courante** : 5. Execution
- **Rôle actif** : Développeur
- **Dernière mise à jour** : [Date]

## Todo List

| État | ID  | Nom                 | Description                                     | Dépendances | Résolution |
| ---- | --- | ------------------- | ----------------------------------------------- | ----------- | ---------- |
| ☐    | T1  | Créer config        | Créer `src/config.ts` avec les constantes       | -           |            |
| ☐    | T2  | Créer validator     | Créer `src/utils/validator.ts`                  | T1          |            |
| ☐    | T3  | Créer UserService   | Créer `src/services/user.ts`                    | T1, T2      |            |
| ☐    | T4  | Ajouter route users | Ajouter `/api/users` dans `src/routes/index.ts` | T3          |            |

## Historique des transitions

| De               | Vers         | Raison              | Date   |
| ---------------- | ------------ | ------------------- | ------ |
| ...              | ...          | ...                 | ...    |
| 4. Planification | 5. Execution | Todo list complétée | [Date] |
```

## Transition

Une fois les critères de succès validés :
→ Passer à **ASH_5_Execution.md**
