# Installation

Ce guide vous accompagne pas à pas pour installer et configurer SomeNotify sur votre Raspberry Pi.

> **Étapes :**
> 1. Installation de SomeNotify
> 2. Configuration de SomeNotify
> 3. Configuration du DNS
> 4. Configuration de la centrale Somfy
> 5. Démarrage et vérification

## Prérequis

### Matériel

- Centrale Somfy Protexiom avec module IP installé
- Support du DNS personnalisé sur la centrale (vérifiez sur votre modèle — cette fonctionnalité n'est pas disponible sur les dernières versions)
- Raspberry Pi connecté en Ethernet au même réseau que la centrale

### Logiciel

- Distribution Linux avec systemd (ex. Raspberry Pi OS)
- Python 3, git et python3-venv
- dnsmasq
- Accès root

## Étape 1 — Installation de SomeNotify

Lancez le script d'installation :

```bash
curl -fsSL https://raw.githubusercontent.com/RP38/SomeNotify/main/scripts/install.sh | sudo bash
```

Le script effectue les actions suivantes :
- Clone le projet dans `/opt/somenotify`
- Crée un utilisateur système dédié `somenotify`
- Installe les dépendances Python dans un environnement virtuel isolé
- Configure un service systemd

## Étape 2 — Configuration de SomeNotify

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

## Étape 3 — Configuration du DNS

SomeNotify intercepte les requêtes de la centrale Somfy destinées au service `123-sms.net`. Pour cela, il faut configurer un serveur DNS local qui redirige ce domaine vers le Raspberry Pi.

Installez dnsmasq si ce n'est pas déjà fait :

```bash
sudo apt install dnsmasq
```

Créez un fichier de configuration dédié :

```bash
sudo nano /etc/dnsmasq.d/somenotify.conf
```

Ajoutez la ligne suivante :

```
address=/123-sms.net/127.0.0.1
```

Redémarrez dnsmasq pour appliquer la configuration :

```bash
sudo systemctl restart dnsmasq
```

Vérifiez que la résolution fonctionne :

```bash
dig @127.0.0.1 123-sms.net
```

La réponse doit indiquer `127.0.0.1` dans la section `ANSWER`.

## Étape 4 — Configuration de la centrale Somfy

Dans l'interface de configuration réseau de votre centrale, renseignez l'adresse IP du Raspberry Pi comme serveur DNS.

Consultez le [guide de configuration de la centrale](guide.md) pour les instructions détaillées.

## Étape 5 — Démarrage et vérification

Démarrez le service :

```bash
sudo systemctl start somenotify
```

Vérifiez que tout fonctionne :

```bash
sudo systemctl status somenotify
sudo journalctl -u somenotify -f
```

---

## Gestion du service

```bash
sudo systemctl start somenotify      # Démarrer
sudo systemctl stop somenotify       # Arrêter
sudo systemctl restart somenotify    # Redémarrer après un changement de config
sudo systemctl status somenotify     # Vérifier le statut
sudo journalctl -u somenotify -f     # Suivre les logs
```
