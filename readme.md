📦 RHash – Outil de chiffrement / déchiffrement sécurisé

RHash est un programme Python permettant de chiffrer et déchiffrer des messages en utilisant :

🔐 Argon2id pour la dérivation de clé (KDF)

🔒 AES-256 en mode GCM pour le chiffrement authentifié

🛡 HMAC-SHA256 pour l’intégrité

📦 Compression Zlib avant chiffrement

🎨 Interface console colorée avec colorama

Ce programme est pensé pour être simple, sûr et robuste, tout en restant facile à utiliser en CLI.

✨ Fonctionnalités

Entrée d’un message + mot de passe

Double hash SHA-256 du mot de passe

Dérivation Argon2id (sécurisée, résistante GPU)

Chiffrement AES-GCM avec tag d’authentification

HMAC supplémentaire pour l’intégrité

Affichage lisible et coloré

Décompression + déchiffrement avec vérification du mot de passe

📥 Installation
1. Cloner ou télécharger le projet
git clone 
cd rhash

2. Installer les dépendances

Tu peux installer tous les packages avec :

pip install -r requirements.txt


Ou manuellement (voir liste ci-dessous).

📦 Dépendances Python

Voici tous les modules nécessaires :

pycryptodome
argon2-cffi
colorama


Installation individuelle :

pip install pycryptodome argon2-cffi colorama

▶️ Exécution

Exécuter le script :

python3 rhash.py


Tu verras alors un menu :

=== RHash - Encrypt Decrypt ===

1. Chiffrer
2. Déchiffrer
3. Quitter

🔐 Exemple d’utilisation
➤ Chiffrement

Tu entres un message et un mot de passe.
Le programme retourne :

Le message chiffré en Base64

Le hash du mot de passe (à conserver pour déchiffrer)

➤ Déchiffrement

Tu colles :

Le message chiffré (Base64)

Le hash du mot de passe

Si tout est correct → le message apparaît.

📝 Notes de sécurité

Le mot de passe n’est jamais stocké, seule sa double empreinte SHA-256 est utilisée.

Le sel Argon2id est généré aléatoirement à chaque chiffrement.

AES-GCM assure confidentialité + intégrité.

HMAC-SHA256 ajoute une couche d’intégrité supplémentaire.

Cette structure offre un modèle proche d’un format AEAD renforcé.
