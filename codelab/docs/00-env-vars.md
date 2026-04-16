# 00 - Variables d'environnement (Cloud Shell)

Utilisez cette page comme source unique de vérité pour les variables de l'atelier.

## Pourquoi on utilise ces variables

Dans l'atelier, plusieurs commandes ont besoin des mêmes valeurs (ID projet et région).

Au lieu de réécrire ces valeurs à chaque commande, on les stocke dans des variables:

- `PROJECT_ID` évite les erreurs de frappe sur l'identifiant du projet
- `REGION` garantit que tous les services sont déployés dans la même région

Résultat: commandes plus courtes, plus lisibles, et moins d'erreurs.

Pour cette session, nous définissons uniquement 2 variables:

- `PROJECT_ID`
- `REGION`

La région choisie pour l'atelier est: `europe-west1`.

## 1. Définir `PROJECT_ID` (ligne par ligne)

Exécutez cette commande:

```bash
export PROJECT_ID="votre-id-projet-gcp"
```

Testez immédiatement:

```bash
echo "$PROJECT_ID"
```

Résultat attendu: votre ID projet s'affiche (exemple: `ladycraft1-4ee09`).

## 2. Définir `REGION` (ligne par ligne)

Exécutez cette commande:

```bash
export REGION="europe-west1"
```

Testez immédiatement:

```bash
echo "$REGION"
```

Résultat attendu: `europe-west1`.

## 3. Vérifier les 2 variables ensemble

Exécutez:

```bash
echo "PROJECT_ID=$PROJECT_ID"
```

```bash
echo "REGION=$REGION"
```

Si les deux lignes s'affichent correctement, vous pouvez passer à l'étape suivante.

## 4. Rappel important

- N'utilisez pas `africa-south1` pour cet atelier.
- Nous utilisons `europe-west1`.
- Les autres variables (URLs de services, etc.) seront définies plus tard, étape par étape.

## 5. Important: ces variables sont temporaires

Ces variables existent seulement dans la session terminal en cours.

Si vous fermez Cloud Shell, rechargez la page, ou ouvrez une nouvelle session, elles peuvent disparaître.

Si une commande échoue avec une variable vide, redéfinissez simplement:

```bash
export PROJECT_ID="votre-id-projet-gcp"
```

```bash
export REGION="europe-west1"
```

Test rapide:

```bash
echo "$PROJECT_ID"
```

```bash
echo "$REGION"
```
