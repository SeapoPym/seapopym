# Orchestrator - ASH Method

Ce document décrit le fonctionnement du workflow **ASH Method** (Analyse-Solutioning-Handoff). Il doit être lu en premier par tout agent IA avant de commencer à travailler sur un projet.

## Principe général

La méthode ASH structure le développement en **9 étapes séquentielles**. Chaque étape est associée à un **rôle** (Analyste, Architecte, Développeur, etc.) avec des responsabilités et des règles précises.

L'état du projet est centralisé dans le fichier **WORKFLOW_STATE.md** qui sert de source de vérité partagée entre tous les rôles.

## Les 9 étapes

| # | Étape | Rôle | Fichier |
|---|-------|------|---------|
| 1 | Initialisation | Facilitateur | ASH_1_Initialization.md |
| 2 | Analyse | Analyste | ASH_2_Analyse.md |
| 3 | Architecture | Architecte | ASH_3_Architecture.md |
| 4 | Planification | Planificateur | ASH_4_Planification.md |
| 5 | Execution | Développeur | ASH_5_Execution.md |
| 6 | Revue | Reviewer | ASH_6_Revue.md |
| 7 | Resolution | Développeur | ASH_7_Resolution.md |
| 8 | Test | Testeur | ASH_8_Test.md |
| 9 | Finalisation | Facilitateur | ASH_9_Finalisation.md |

## Points de validation utilisateur

Certaines étapes requièrent une **validation explicite de l'utilisateur** avant de continuer :

- **Après Initialisation** : L'utilisateur valide que le besoin est bien compris
- **Après Architecture** : L'utilisateur valide les choix techniques
- **Avant Finalisation** : L'utilisateur valide le travail accompli avant commit/push

À ces points, l'agent doit **s'arrêter et demander confirmation** avant de passer à l'étape suivante.

## Structure de WORKFLOW_STATE.md

Le fichier WORKFLOW_STATE.md contient les sections suivantes :

```markdown
# Workflow State

## Informations générales

- **Projet** : [Nom du projet]
- **Étape courante** : [Numéro et nom de l'étape]
- **Rôle actif** : [Rôle en cours]
- **Dernière mise à jour** : [Date et heure]

## Résumé du besoin

[Description du besoin validé à l'étape Initialisation]

## Décisions d'architecture

[Choix techniques validés à l'étape Architecture]

## Todo List

| État | ID  | Nom | Description | Dépendances | Résolution |
| ---- | --- | --- | ----------- | ----------- | ---------- |
| ☐    | T1  | ... | ...         | -           |            |
| ☐    | T2  | ... | ...         | T1          |            |

## Historique des transitions

| De                | Vers       | Raison        | Date |
| ----------------- | ---------- | ------------- | ---- |
| 1. Initialisation | 2. Analyse | Besoin validé | ...  |
```

## Règles de transition

### Avancer à l'étape suivante

Pour passer à l'étape N+1, l'agent doit :

1. Vérifier que les **critères de succès** de l'étape N sont remplis (définis dans le fichier de l'étape)
2. Mettre à jour WORKFLOW_STATE.md :
   - Changer "Étape courante" et "Rôle actif"
   - Ajouter une ligne dans "Historique des transitions"
3. Si c'est un point de validation → demander confirmation à l'utilisateur
4. Lire le fichier de l'étape suivante et appliquer ses instructions

### Retourner à une étape précédente

Un retour en arrière est possible en cas d'échec ou de problème de conception. Pour revenir à l'étape N-x :

1. Documenter la raison dans "Historique des transitions"
2. Conserver les informations pertinentes dans WORKFLOW_STATE.md (ne pas effacer l'historique)
3. Mettre à jour "Étape courante" et "Rôle actif"
4. Reprendre depuis l'étape cible

Les retours typiques :

- **Revue → Analyse** : Problème de conception détecté
- **Test → Architecture** : Tests révèlent un défaut d'architecture
- **Execution → Planification** : Tâche impossible, besoin de re-planifier

## Règles générales pour les agents

### Obligations

- Toujours lire WORKFLOW_STATE.md avant de commencer
- Respecter le rôle assigné à l'étape courante
- Mettre à jour WORKFLOW_STATE.md après chaque action significative
- Documenter les décisions et les raisons des échecs
- S'arrêter aux points de validation utilisateur

### Interdictions

- Ne pas sauter d'étape
- Ne pas modifier le code sans être à l'étape Execution ou Resolution
- Ne pas créer de tests sans être à l'étape Test
- Ne pas commiter/pusher sans être à l'étape Finalisation
- Ne pas prendre de décision d'architecture sans être à l'étape Architecture

## Comment démarrer un nouveau projet

1. Créer un fichier WORKFLOW_STATE.md vide avec la structure ci-dessus
2. Définir "Étape courante" à "1. Initialisation"
3. Lire ASH_1_Initialization.md et suivre ses instructions
4. Avancer étape par étape jusqu'à la Finalisation

## Comment reprendre un projet en cours

1. Lire ce fichier (ASH_ORCHESTRATOR.md)
2. Lire WORKFLOW_STATE.md pour comprendre l'état actuel
3. Identifier l'étape courante
4. Lire le fichier de l'étape courante (BMAD*X*\*.md)
5. Continuer le travail
