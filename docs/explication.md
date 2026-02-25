# Fonctionnement

SomeNotify reçoit des alertes sous forme de requêtes HTTP GET et les retransmet au backend de notification configuré.

## Format de la requête

```
GET /http.php?email=x&pass=y&numero=z&message=hello
```

| Paramètre | Description                          | Requis |
|-----------|--------------------------------------|--------|
| `message` | Contenu de l'alerte                  | oui    |
| `numero`  | Numéro de téléphone du destinataire  | non    |
| `email`   | Email du compte                     | non    |
| `pass`    | Mot de passe du compte              | non    |
