# SomeNotify

Système de relais d'alertes conçu pour être utilisé comme extension des systèmes d'alarme Somfy. Il permet de recevoir les notifications d'alerte sur un serveur privé (tel qu'un Raspberry Pi) et de les rediriger vers un service de push tiers comme [Pushover](https://pushover.net/).

> **Avertissement** : ce projet est non officiel et n'est en aucun cas affilié, sponsorisé ou approuvé par Somfy. Tous les noms de marques et marques déposées appartiennent à leurs propriétaires respectifs.
>
> Ce logiciel est fourni « TEL QUEL », sans aucune garantie. Vous êtes seul responsable de son installation, de sa configuration et de son utilisation, y compris de la sécurisation de votre réseau et de vos systèmes. Utilisez-le uniquement sur des appareils qui vous appartiennent et des réseaux que vous administrez.

> **Compatibilité** : testé uniquement sur Somfy Protexiom.

## Motivation

Les centrales Somfy Protexiom permettent d'envoyer des alertes par SMS grâce à un module GSM utilisant le réseau 2G (EDGE). Avec l'extinction progressive du réseau 2G prévue courant 2026, ce module ne fonctionnera plus.

SomeNotify offre une alternative : en passant par le module IP de la centrale et un Raspberry Pi sur le réseau local, les alertes sont redirigées vers un service de notification push. Cela permet de continuer à recevoir les alertes sur son téléphone sans avoir à remplacer l'ensemble du système d'alarme.

## Documentation

| Document | Description |
|----------|-------------|
| [Guide de configuration de la centrale](docs/guide.md) | Configuration réseau de la centrale Somfy pour rediriger les alertes |
| [Installation et configuration](docs/installation.md) | Prérequis, installation et configuration du service SomeNotify |
| [Fonctionnement](docs/explication.md) | Explication détaillée du fonctionnement et format des requêtes |
| [Développement](docs/development.md) | Environnement de développement et ajout de nouveaux backends |

## Backends supportés

Un backend est un service tiers vers lequel SomeNotify redirige les alertes reçues. Backends disponibles :

- **log** — affiche les alertes sur stdout (par défaut, utile pour tester)
- **[Pushover](https://pushover.net/)** — envoie les alertes sous forme de notifications push sur vos appareils
- **[Free Mobile SMS](https://mobile.free.fr/account/mes-options/notifications-sms)** — envoie les alertes par SMS sur votre ligne Free via l'API de notification Free Mobile *(à venir)*

## Contribuer

Les pull requests ajoutant le support d'un nouveau backend sont les bienvenues. Vous pouvez également développer votre propre backend dans un fork du projet.

Voir [docs/development.md](docs/development.md) pour la mise en place de l'environnement de développement.

## Licence

[MIT](LICENSE)
