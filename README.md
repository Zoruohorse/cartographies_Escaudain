# Cartographie des acteurs — Escaudain

Projet statique prêt pour GitHub Pages, basé sur le moteur visuel, les cartes, les filtres, la physique du réseau et les deux onglets complémentaires du livrable Dunkerque, lui-même adapté de Fouju.

## Vues

- `apps/network/` : réseau interactif, même simulation physique, tailles, liens courbes, zoom, déplacement, sélection, panneaux, couleurs de Fouju (catégories complémentaires ajoutées).
- `apps/cards/` : cartes acteurs, filtres, preuves documentaires, relations et trois onglets (cartographie, synthèse des oppositions, points de vigilance & sources).
- `data/` et `config/` : référentiel JSON partagé, sans serveur ni service tiers.

## Données intégrées

- **45 nœuds / 80 liens** provenant du réseau Escaudain fourni.
- **55 nœuds / 90 liens au total** : ajout de 10 fiches acteurs absentes du nuage initial, et 10 relations de rattachement/mention **explicitement signalées comme contextuelles**. Aucun partenariat n'a été déduit du seul voisinage visuel.
- **32 fiches**, avec leurs résumés de positionnement et de preuve conservés.
- **7 thèmes de synthèse**, **6 points de vigilance** et **15 références**.

**Important :** les preuves issues des fiches sont des formulations fournies, non des citations littérales vérifiées. Les sources citées n'ont pas de liens article-à-article dans le corpus ; les URLs sont donc volontairement nulles. La validité externe des affirmations et des chiffres n'a pas été vérifiée indépendamment.

**Doublon d'origine :** les formes `SoftBank`, `Softbank` et `SoftBank (Masayoshi Son)` sont conservées en tant que mentions distinctes pour préserver les 32 fiches. Deux liens `alias_of` précisent qu'il ne s'agit pas de trois entreprises indépendantes. Dans une révision éditoriale, elles pourront être fusionnées sans perdre les positions associées.

## Publication GitHub Pages

1. Décompresser l'archive ; transférer **son contenu** à la racine de ton dépôt GitHub (pas l'archive ZIP elle-même).
2. Dans `Settings → Pages`, choisir `Deploy from a branch`, branche `main`, dossier `/ (root)`.
3. Utiliser les chemins `apps/cards/` et `apps/network/`.

## Validation / test local

```bash
python3 validate.py
python3 -m http.server 8000
```

Puis ouvrir `http://localhost:8000`. Le chargement JSON via `fetch` nécessite un serveur HTTP (ou GitHub Pages), pas l'ouverture directe de `index.html` en `file://`.


## Extension du 9 novembre 2026 : cinq onglets

La vue en cartes comporte désormais : **Cartographie des acteurs**, **Synthèse des oppositions**, **Points de vigilance et sources**, **Chronologie**, **Évolution des acteurs**.

- **Oppositions et interrogations :** huit thèmes présentés comme enjeux, non imputés à des opposants faute de preuve. Chaque fiche pointe vers ses sources et propose d'ouvrir les preuves. Aucun opposant local formel n'est établi dans le corpus actuel, sans que cela présume d'un consensus.
- **Chronologie :** douze jalons du premier communiqué de décembre 2025 à l'horizon de première mise en service 2030. Les événements prévus, en particulier l'enquête publique PLUi du 10 novembre au 10 décembre 2026, sont distingués des événements réalisés.
- **Évolution :** 17 acteurs datables, 10 autres non datables, et 4 fiches génériques ou insuffisamment qualifiées exclues. Deux périmètres : projet local (13 acteurs datables) et contexte étendu (4 acteurs datables supplémentaires).
- **Trois variantes du graphique :** « Nouveaux » et « Cumulés », ventilées par catégorie, et « Par position », cumulée selon les classes **favorables, opposés, prudents / institutionnels, non établis**. Ce classement repose sur les positions actuelles du référentiel, **pas sur un historique de bascules politiques**. Zéro opposant documenté sur le dossier, sans interprétation sur l'opinion générale.

Les acteurs, leurs positions, les relations et les références sources historiques sont inchangés. Nouvelle traçabilité dans `data/timeline.json`, `data/content.json`, `data/synthesis.json` et `data/evolution-audit-20261109.json`. Contrôles : `python validate.py`.
