# SomNotiFy

Passerelle HTTP qui redirige des notifications recues via des requetes HTTP vers des services de push tiers comme [Pushover](https://pushover.net/).

## Fonctionnement

Le serveur recoit une requete GET et transmet la notification au service de push configure :

```
GET /http.php?email=x&pass=y&numero=z&message=txt
```

| Parametre | Description                          |
|-----------|--------------------------------------|
| `email`   | Email du compte du service de push   |
| `pass`    | Mot de passe du compte               |
| `numero`  | Numero de telephone du destinataire  |
| `message` | Contenu de la notification           |

## Services supportes

- [Pushover](https://pushover.net/)
- D'autres a venir...
