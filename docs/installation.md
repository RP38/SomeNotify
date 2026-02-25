# Installation et configuration

## Prérequis

- Centrale Somfy Protexiom avec support du DNS personnalisé (vérifiez sur votre modèle avant de commencer — cette fonctionnalité semble non disponible sur les dernières versions. Une version compatible avec les centrales sans DNS personnalisé est prévue.)
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
