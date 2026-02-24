# SomeNotify

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

## Installation

```bash
pip install -r requirements.txt
cp .env.example .env
```

Ouvrez `.env` et renseignez vos identifiants (token Pushover, etc.) puis lancez le serveur :

```bash
python3 server.py
```

## Configuration

Toute la configuration se fait dans le fichier `.env` :

| Variable           | Description                                | Defaut      |
|--------------------|--------------------------------------------|-------------|
| `BACKEND`          | Service de notification a utiliser         | `log`       |
| `LISTEN_HOST`      | Adresse d'ecoute du serveur                | `0.0.0.0`   |
| `LISTEN_PORT`      | Port d'ecoute du serveur                   | `80`        |
| `PUSHOVER_TOKEN`   | Token de l'application Pushover            | —           |
| `PUSHOVER_USER_KEY`| Cle utilisateur Pushover                   | —           |

## Services supportes

- [Pushover](https://pushover.net/)
- D'autres a venir...
