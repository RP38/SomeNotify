# SomeNotify

Système de relais d'alertes conçu pour être utilisé comme extension des systèmes d'alarme Somfy. Il permet de recevoir les notifications d'alerte sur un serveur privé (tel qu'un Raspberry Pi) et de les rediriger vers un service de push tiers comme [Pushover](https://pushover.net/).

> **Avertissement** : ce projet est non officiel et n'est en aucun cas affilié, sponsorisé ou approuvé par Somfy. Tous les noms de marques et marques déposées appartiennent à leurs propriétaires respectifs.
>
> Ce logiciel est fourni « TEL QUEL », sans aucune garantie. Vous êtes seul responsable de son installation, de sa configuration et de son utilisation, y compris de la sécurisation de votre réseau et de vos systèmes. Utilisez-le uniquement sur des appareils qui vous appartiennent et des réseaux que vous administrez.

> **Compatibilité** : testé uniquement sur Somfy Protexiom.

Pour comprendre le fonctionnement en détail, voir [docs/explication.md](docs/explication.md).

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

- **log** — affiche les alertes sur stdout (par défaut, utile pour tester)
- **[Pushover](https://pushover.net/)** — envoie les alertes sur vos appareils

## Développement

Voir [docs/development.md](docs/development.md) pour la mise en place de l'environnement de developpement et l'ajout de nouveaux backends.

## Licence

[MIT](LICENSE)
