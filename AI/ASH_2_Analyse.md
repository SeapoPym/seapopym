# Étape 2 : Analyse

## Informations

- **Rôle** : Analyste
- **Étape précédente** : ASH_1_Initialization.md
- **Étape suivante** : ASH_3_Architecture.md
- **Validation utilisateur requise** : Non

## Objectif

Explorer et comprendre le répertoire de travail existant. Cette étape permet de cartographier la codebase, identifier les patterns utilisés et comprendre les standards en place avant de proposer des choix d'architecture.

## Obligations

- Explorer la structure des dossiers et fichiers du projet
- Identifier les technologies et frameworks utilisés
- Repérer les patterns de code récurrents (naming, organisation, etc.)
- Analyser les fichiers de configuration (package.json, tsconfig, .eslintrc, etc.)
- Identifier les dépendances externes et leurs versions
- Documenter les conventions de code existantes
- Noter les incohérences ou la dette technique apparente
- Rédiger un rapport d'analyse dans WORKFLOW_STATE.md

## Interdictions

- Ne pas modifier de fichiers existants
- Ne pas proposer de solutions techniques (réservé à l'étape Architecture)
- Ne pas ignorer des parties du projet même si elles semblent non pertinentes
- Ne pas faire d'hypothèses sur le code sans l'avoir lu

## Déroulement

1. **Structure globale** : Lister les dossiers principaux et comprendre l'organisation
2. **Technologies** : Identifier le langage, les frameworks, les outils de build
3. **Configuration** : Analyser les fichiers de config (linter, formatter, tests, CI/CD)
4. **Dépendances** : Examiner les packages/librairies utilisés
5. **Patterns** : Repérer les conventions de nommage, l'architecture des modules
6. **Points d'attention** : Noter les zones complexes, la dette technique, les risques
7. **Synthèse** : Rédiger le rapport d'analyse

## Critères de succès

Pour passer à l'étape suivante, tous ces critères doivent être remplis :

- [ ] La structure du projet est comprise et documentée
- [ ] Les technologies principales sont identifiées
- [ ] Les patterns et conventions existants sont listés
- [ ] Les points d'attention sont relevés
- [ ] Le rapport d'analyse est rédigé dans WORKFLOW_STATE.md

## Condition d'échec

- **Projet vide** : Si le répertoire est vide ou ne contient pas de code, noter "Projet greenfield" et passer directement à l'Architecture avec cette information.
- **Projet illisible** : Si le code est trop obfusqué ou incompréhensible, documenter le problème et demander des clarifications à l'utilisateur.

## Actions à effectuer dans WORKFLOW_STATE.md

À la fin de cette étape, ajouter une section et mettre à jour :

```markdown
## Informations générales

- **Étape courante** : 3. Architecture
- **Rôle actif** : Architecte
- **Dernière mise à jour** : [Date]

## Rapport d'analyse

### Structure du projet

[Description de l'organisation des dossiers]

### Technologies identifiées

- Langage : [...]
- Framework : [...]
- Build : [...]
- Tests : [...]

### Patterns et conventions

- Nommage : [camelCase, snake_case, etc.]
- Architecture : [MVC, composants, modules, etc.]
- Autres : [...]

### Points d'attention

- [Liste des zones à risque, dette technique, incohérences]

## Historique des transitions

| De | Vers | Raison | Date |
|----|------|--------|------|
| ... | ... | ... | ... |
| 2. Analyse | 3. Architecture | Analyse complétée | [Date] |
```

## Transition

Une fois les critères de succès validés :
→ Passer à **ASH_3_Architecture.md**
