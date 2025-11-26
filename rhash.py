from Crypto.Cipher import AES
from Crypto.Hash import SHA256, HMAC
from Crypto.Random import get_random_bytes
from argon2.low_level import hash_secret_raw, Type
import base64
import zlib
import sys
from colorama import init, Fore, Style

init(autoreset=True)

def print_header():
    print(Fore.CYAN + Style.BRIGHT + "\n=== RHash - Encrypt Decrypt ===\n" + Style.RESET_ALL)

def double_hash(mdp):
    h1 = SHA256.new(mdp.encode()).digest()
    h2 = SHA256.new(h1).digest()
    return h2

def derive_key_argon2id(mdp_hash, salt):
    return hash_secret_raw(
        secret=mdp_hash,
        salt=salt,
        time_cost=3,
        memory_cost=64 * 1024,  # 64 MB
        parallelism=4,
        hash_len=32,
        type=Type.ID
    )

def chiffrer(message, motdepasse):
    salt = get_random_bytes(16)
    mdp_hash = double_hash(motdepasse)
    key = derive_key_argon2id(mdp_hash, salt)

    compressed = zlib.compress(message.encode())

    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(compressed)

    package = salt + cipher.nonce + tag + ciphertext
    hmac = HMAC.new(key, package, digestmod=SHA256)
    final = package + hmac.digest()

    return base64.b64encode(final).decode(), base64.b64encode(mdp_hash).decode()

def dechiffrer(data_b64, mdp_hash_b64):
    try:
        data = base64.b64decode(data_b64)
        mdp_hash = base64.b64decode(mdp_hash_b64)

        salt = data[:16]
        nonce = data[16:32]
        tag = data[32:48]
        hmac_received = data[-32:]
        ciphertext = data[48:-32]

        key = derive_key_argon2id(mdp_hash, salt)
        hmac = HMAC.new(key, data[:-32], digestmod=SHA256)
        hmac.verify(hmac_received)

        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        compressed = cipher.decrypt_and_verify(ciphertext, tag)
        message = zlib.decompress(compressed)

        return Fore.GREEN + "[OK]" + Style.RESET_ALL + " Message :\n" + message.decode()

    except Exception as e:
        return Fore.RED + "[Échec]" + Style.RESET_ALL + " Mot de passe ou intégrité incorrecte."

def main():
    print_header()
    while True:
        print(Fore.YELLOW + "\n1. Chiffrer\n2. Déchiffrer\n3. Quitter")
        choix = input(Fore.CYAN + "Choix : " + Style.RESET_ALL).strip()

        if choix == '1':
            msg = input(Fore.CYAN + "Message : " + Style.RESET_ALL)
            mdp = input(Fore.CYAN + "Mot de passe : " + Style.RESET_ALL)
            data, hash_mdp = chiffrer(msg, mdp)
            print(Fore.MAGENTA + "\n==> Message chiffré :\n" + data)
            print(Fore.MAGENTA + "\n==> Hash du mot de passe :\n" + hash_mdp)

        elif choix == '2':
            data = input(Fore.CYAN + "Message chiffré : " + Style.RESET_ALL)
            mdp_hash = input(Fore.CYAN + "Hash du mot de passe : " + Style.RESET_ALL)
            print("\n" + dechiffrer(data, mdp_hash))

        elif choix == '3':
            print(Fore.CYAN + "Fermeture. Merci d’avoir utilisé RHash.")
            sys.exit()
        else:
            print(Fore.RED + "Choix invalide." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
