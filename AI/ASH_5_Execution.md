# Étape 5 : Execution

## Informations

- **Rôle** : Développeur
- **Étape précédente** : ASH_4_Planification.md
- **Étape suivante** : ASH_6_Revue.md
- **Validation utilisateur requise** : Non

## Objectif

Implémenter les tâches de la todo list une par une, dans l'ordre défini. Chaque tâche est traitée individuellement et son résultat est documenté.

## Obligations

- Exécuter les tâches dans l'ordre des dépendances
- Traiter une seule tâche à la fois
- Respecter les décisions d'architecture
- Respecter les patterns et conventions identifiés à l'étape Analyse
- Cocher la tâche et documenter la résolution dans WORKFLOW_STATE.md
- En cas d'échec, documenter la raison dans la colonne "Résolution"

## Interdictions

- Ne pas modifier des fichiers hors du scope de la tâche en cours
- Ne pas ignorer les dépendances (ne pas traiter T3 si T1 n'est pas fait)
- Ne pas créer de tests (réservé à l'étape Test)
- Ne pas sur-développer : implémenter uniquement ce qui est demandé
- Ne pas modifier l'architecture sans retourner à l'étape Architecture

## Déroulement

Pour chaque tâche de la todo list :

1. **Sélection** : Prendre la prochaine tâche non cochée dont les dépendances sont satisfaites
2. **Lecture** : Comprendre précisément ce qui est demandé
3. **Implémentation** : Écrire le code nécessaire
4. **Vérification** : S'assurer que le code compile/fonctionne
5. **Documentation** : Mettre à jour WORKFLOW_STATE.md (cocher + résolution)
6. **Répéter** : Passer à la tâche suivante

## Gestion des échecs

Un échec est acceptable si :
- La tâche est techniquement impossible
- Résoudre la tâche casserait le reste du projet
- Une dépendance externe est manquante

En cas d'échec :
1. Ne pas cocher la tâche
2. Documenter la raison dans la colonne "Résolution"
3. Continuer avec les tâches suivantes si possible
4. Les échecs seront analysés à l'étape Revue

## Critères de succès

Pour passer à l'étape suivante :

- [ ] Toutes les tâches ont été traitées (réussies ou échouées avec justification)
- [ ] Chaque tâche réussie est cochée avec sa résolution documentée
- [ ] Chaque tâche échouée a une explication claire
- [ ] Le code compile sans erreurs

## Condition d'échec

- **Trop d'échecs** : Si plus de 50% des tâches échouent, cela peut indiquer un problème d'architecture. Considérer un retour à l'étape Architecture.
- **Blocage total** : Si une tâche bloquante sans alternative échoue, documenter et passer à la Revue pour analyse.

## Actions à effectuer dans WORKFLOW_STATE.md

Pendant l'exécution, mettre à jour progressivement :

```markdown
## Todo List

| État | ID | Nom | Description | Dépendances | Résolution |
|------|-----|-----|-------------|-------------|------------|
| ☑ | T1 | Créer config | Créer `src/config.ts` | - | Fichier créé avec 3 constantes |
| ☑ | T2 | Créer validator | Créer `src/utils/validator.ts` | T1 | Implémenté avec 2 fonctions |
| ☐ | T3 | Créer UserService | Créer `src/services/user.ts` | T1, T2 | ÉCHEC: API externe indisponible |
| ☑ | T4 | Ajouter route | Ajouter `/api/users` | T3 | Implémenté sans UserService (stub) |
```

À la fin de l'étape :

```markdown
## Informations générales

- **Étape courante** : 6. Revue
- **Rôle actif** : Reviewer
- **Dernière mise à jour** : [Date]

## Historique des transitions

| De | Vers | Raison | Date |
|----|------|--------|------|
| ... | ... | ... | ... |
| 5. Execution | 6. Revue | Toutes les tâches traitées | [Date] |
```

## Transition

Une fois toutes les tâches traitées :
→ Passer à **ASH_6_Revue.md**
