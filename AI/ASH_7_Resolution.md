# Étape 7 : Resolution

## Informations

- **Rôle** : Développeur
- **Étape précédente** : ASH_6_Revue.md
- **Étape suivante** : ASH_8_Test.md
- **Validation utilisateur requise** : Non

## Objectif

Corriger les issues identifiées lors de la Revue. Chaque issue est traitée individuellement et son statut est mis à jour.

## Obligations

- Traiter les issues par ordre de sévérité (Critique → Majeure → Mineure)
- Corriger une issue à la fois
- Respecter les décisions d'architecture existantes
- Documenter chaque correction dans WORKFLOW_STATE.md
- Relancer les vérifications automatiques après corrections

## Interdictions

- Ne pas ignorer les issues critiques
- Ne pas introduire de nouvelles fonctionnalités
- Ne pas modifier l'architecture sans retourner à l'étape Architecture
- Ne pas créer de tests (réservé à l'étape suivante)

## Déroulement

Pour chaque issue de la liste :

1. **Sélection** : Prendre l'issue non résolue de plus haute sévérité
2. **Analyse** : Comprendre la cause du problème
3. **Correction** : Appliquer le fix approprié
4. **Vérification** : S'assurer que l'issue est résolue
5. **Documentation** : Mettre à jour le statut dans WORKFLOW_STATE.md
6. **Répéter** : Passer à l'issue suivante

Après toutes les corrections :

7. **Validation globale** : Relancer les vérifications automatiques (lint, typecheck)
8. **Confirmation** : Vérifier qu'aucune nouvelle issue n'a été introduite

## Critères de succès

Pour passer à l'étape suivante :

- [ ] Toutes les issues critiques sont résolues
- [ ] Toutes les issues majeures sont résolues
- [ ] Les issues mineures sont résolues ou explicitement reportées
- [ ] Les vérifications automatiques passent
- [ ] Aucune nouvelle issue n'a été introduite

## Condition d'échec

- **Issue non résolvable** : Si une issue critique ne peut pas être corrigée sans changer l'architecture, documenter et retourner à l'étape Architecture.
- **Régression** : Si corriger une issue en crée d'autres, analyser la cause racine.

## Actions à effectuer dans WORKFLOW_STATE.md

Pendant la résolution, mettre à jour les issues :

```markdown
## Rapport de revue

### Issues identifiées

| ID  | Sévérité | Description           | Fichier         | Statut     |
| --- | -------- | --------------------- | --------------- | ---------- |
| I1  | Critique | Variable non typée    | src/utils.ts:42 | ✅ Corrigé |
| I2  | Mineure  | Nommage incohérent    | src/api.ts:15   | ✅ Corrigé |
| I3  | Info     | Améliorer commentaire | src/index.ts:5  | ⏭ Reporté |

### Vérifications post-correction

| Outil      | Résultat     |
| ---------- | ------------ |
| ESLint     | ✅ 0 erreurs |
| TypeScript | ✅ 0 erreurs |
```

À la fin de l'étape :

```markdown
## Informations générales

- **Étape courante** : 8. Test
- **Rôle actif** : Testeur
- **Dernière mise à jour** : [Date]

## Historique des transitions

| De            | Vers    | Raison          | Date   |
| ------------- | ------- | --------------- | ------ |
| ...           | ...     | ...             | ...    |
| 7. Resolution | 8. Test | Issues résolues | [Date] |
```

## Transition

Une fois les critères de succès validés :
→ Passer à **ASH_8_Test.md**
