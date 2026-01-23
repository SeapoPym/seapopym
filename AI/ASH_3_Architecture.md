# Étape 3 : Architecture

## Informations

- **Rôle** : Architecte
- **Étape précédente** : ASH_2_Analyse.md
- **Étape suivante** : ASH_4_Planification.md
- **Validation utilisateur requise** : Oui

## Objectif

Définir les choix techniques et l'architecture de la solution avant de planifier les tâches. Cette étape produit un document d'architecture qui servira de référence pour tout le développement.

## Obligations

- Se baser sur le rapport d'analyse pour respecter les patterns existants
- Proposer des choix techniques justifiés (frameworks, librairies, patterns)
- Définir la structure des nouveaux composants/modules
- Spécifier les interfaces et contrats entre composants
- Produire des schémas si nécessaire (flux de données, modèles)
- Identifier les risques techniques et proposer des mitigations
- **Projet greenfield** : définir les conventions et standards du projet (voir section dédiée)
- Documenter les décisions dans WORKFLOW_STATE.md
- Présenter les choix à l'utilisateur pour validation

## Interdictions

- Ne pas ignorer les conventions existantes identifiées à l'étape Analyse
- Ne pas proposer des technologies incompatibles avec le projet existant
- Ne pas passer à l'étape suivante sans validation explicite de l'utilisateur
- Ne pas sur-architecturer : rester pragmatique et adapté au besoin

## Déroulement

1. **Revue du contexte** : Relire le besoin et le rapport d'analyse
2. **Choix techniques** : Sélectionner les technologies/librairies nécessaires
3. **Conventions** : Définir les standards (surtout si projet greenfield)
4. **Structure** : Définir l'organisation des fichiers/modules
5. **Interfaces** : Spécifier comment les composants communiquent
6. **Schémas** : Produire des diagrammes si la complexité le justifie
7. **Risques** : Identifier les points bloquants potentiels
8. **Présentation** : Soumettre l'architecture à l'utilisateur
9. **Validation** : Obtenir l'accord de l'utilisateur avant de continuer

## Cas particulier : Projet greenfield

Si le rapport d'analyse indique un projet vide ou nouveau, l'Architecte doit définir les conventions qui guideront tout le développement :

### Conventions à définir

| Domaine           | À définir                                                        |
| ----------------- | ---------------------------------------------------------------- |
| **Nommage**       | Variables (camelCase, snake_case), fichiers, classes, constantes |
| **Structure**     | Organisation des dossiers (src/, tests/, docs/, etc.)            |
| **Formatage**     | Outil (Prettier, Black), règles (indentation, quotes, etc.)      |
| **Linting**       | Outil (ESLint, Pylint), règles activées/désactivées              |
| **Typage**        | Strict ou non, outil (TypeScript, mypy)                          |
| **Tests**         | Framework (Jest, pytest), organisation, conventions de nommage   |
| **Documentation** | Style de commentaires, JSDoc/docstrings                          |
| **Git**           | Format des commits, stratégie de branches                        |

Ces conventions seront documentées dans WORKFLOW_STATE.md et serviront de référence pour les étapes Execution et Revue.

## Critères de succès

Pour passer à l'étape suivante, tous ces critères doivent être remplis :

- [ ] Les choix techniques sont documentés et justifiés
- [ ] La structure des composants est définie
- [ ] Les interfaces entre composants sont spécifiées
- [ ] Les risques techniques sont identifiés
- [ ] **Si greenfield** : les conventions sont définies
- [ ] L'utilisateur a validé explicitement l'architecture

## Condition d'échec

- **Incompatibilité technique** : Si une contrainte rend impossible l'implémentation, retourner à l'étape Initialisation pour rediscuter le besoin.
- **Refus utilisateur** : Si l'utilisateur rejette l'architecture, proposer des alternatives ou clarifier les contraintes.

## Actions à effectuer dans WORKFLOW_STATE.md

À la fin de cette étape, mettre à jour :

```markdown
## Informations générales

- **Étape courante** : 4. Planification
- **Rôle actif** : Planificateur
- **Dernière mise à jour** : [Date]

## Décisions d'architecture

### Choix techniques

| Domaine       | Choix | Justification |
| ------------- | ----- | ------------- |
| [Framework]   | [Nom] | [Raison]      |
| [Librairie X] | [Nom] | [Raison]      |
| [Pattern]     | [Nom] | [Raison]      |

### Conventions (si projet greenfield)

| Domaine           | Convention                   |
| ----------------- | ---------------------------- |
| Nommage variables | camelCase                    |
| Nommage fichiers  | kebab-case                   |
| Formatage         | Prettier (défaut)            |
| Linting           | ESLint (règles recommandées) |
| Typage            | TypeScript strict            |
| Tests             | Jest, fichiers \*.test.ts    |
| Commits           | Conventional Commits         |

### Structure proposée
```

src/
├── [nouveau_module]/
│ ├── [fichier1]
│ └── [fichier2]
└── ...

```

### Interfaces et contrats

[Description des interactions entre composants]

### Risques identifiés

| Risque | Impact | Mitigation |
|--------|--------|------------|
| [Description] | [Haut/Moyen/Bas] | [Solution proposée] |

## Historique des transitions

| De | Vers | Raison | Date |
|----|------|--------|------|
| ... | ... | ... | ... |
| 3. Architecture | 4. Planification | Architecture validée par l'utilisateur | [Date] |
```

## Transition

Une fois les critères de succès validés et l'utilisateur d'accord :
→ Passer à **ASH_4_Planification.md**
