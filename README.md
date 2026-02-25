# SomeNotify

Système de relais d'alertes conçu pour être utilisé comme extension des systèmes d'alarme Somfy. Il permet de recevoir les notifications d'alerte sur un serveur privé (tel qu'un Raspberry Pi) et de les rediriger vers un service de push tiers comme [Pushover](https://pushover.net/).

> **Avertissement** : ce projet est non officiel et n'est en aucun cas affilié, sponsorisé ou approuvé par Somfy. Tous les noms de marques et marques déposées appartiennent à leurs propriétaires respectifs.
>
> Ce logiciel est fourni « TEL QUEL », sans aucune garantie. Vous êtes seul responsable de son installation, de sa configuration et de son utilisation, y compris de la sécurisation de votre réseau et de vos systèmes. Utilisez-le uniquement sur des appareils qui vous appartiennent et des réseaux que vous administrez.

> **Compatibilité** : testé uniquement sur Somfy Protexiom.

Pour comprendre le fonctionnement en détail, voir [docs/explication.md](docs/explication.md).

## Prérequis

- Module IP installé sur la centrale Somfy
- Raspberry Pi connecté en Ethernet au même réseau que la centrale
- Distribution Linux avec systemd (ex. Raspberry Pi OS)
- Python 3, git et python3-venv installés
- Accès root (pour l'installation et l'écoute sur le port 80)

## Installation

Lancez le script d'installation sur votre serveur Linux :

```bash
curl -fsSL https://raw.githubusercontent.com/RP38/SomeNotify/main/scripts/install.sh | sudo bash
```

Le script effectue les actions suivantes :
- Clone le projet dans `/opt/somenotify`
- Crée un utilisateur système dédié `somenotify`
- Installe les dépendances Python dans un environnement virtuel isolé
- Configure un service systemd

## Configuration

Éditez le fichier de configuration :

```bash
sudo nano /opt/somenotify/.env
```

Renseignez votre backend et vos identifiants :

```ini
BACKEND=pushover
LISTEN_PORT=80

PUSHOVER_TOKEN=votre_token
PUSHOVER_USER_KEY=votre_clé_utilisateur
```

| Variable             | Description                              | Défaut    |
|----------------------|------------------------------------------|-----------|
| `BACKEND`            | Service de notification à utiliser       | `log`     |
| `LISTEN_HOST`        | Adresse d'écoute du serveur              | `0.0.0.0` |
| `LISTEN_PORT`        | Port d'écoute du serveur                 | `80`      |
| `PUSHOVER_TOKEN`     | Token de l'application Pushover          | —         |
| `PUSHOVER_USER_KEY`  | Clé utilisateur Pushover                 | —         |

## Gestion du service

```bash
sudo systemctl start somenotify      # Démarrer
sudo systemctl stop somenotify       # Arrêter
sudo systemctl restart somenotify    # Redémarrer après un changement de config
sudo systemctl status somenotify     # Vérifier le statut
sudo journalctl -u somenotify -f     # Suivre les logs
```

## Backends supportés

Un backend est un service tiers vers lequel SomeNotify redirige les alertes reçues. Backends disponibles :

- **log** — affiche les alertes sur stdout (par défaut, utile pour tester)
- **[Pushover](https://pushover.net/)** — envoie les alertes sous forme de notifications push sur vos appareils
- **[Free Mobile SMS](https://mobile.free.fr/account/mes-options/notifications-sms)** — envoie les alertes par SMS sur votre ligne Free via l'API de notification Free Mobile *(à venir)*

## Développement

Voir [docs/development.md](docs/development.md) pour la mise en place de l'environnement de développement et l'ajout de nouveaux backends.

Les pull requests ajoutant le support d'un nouveau backend sont les bienvenues. Vous pouvez également développer votre propre backend dans un fork du projet.

## Licence

[MIT](LICENSE)
