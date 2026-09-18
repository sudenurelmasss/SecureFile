from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import base64
import hashlib
import os


def generate_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )

    return base64.urlsafe_b64encode(
        kdf.derive(password.encode("utf-8"))
    )


def encrypt_file(file_path: str, password: str) -> str:
    salt = os.urandom(16)

    key = generate_key(password, salt)
    fernet = Fernet(key)

    with open(file_path, "rb") as file:
        file_data = file.read()

    encrypted_data = fernet.encrypt(file_data)

    encrypted_file_path = file_path + ".secure"

    with open(encrypted_file_path, "wb") as encrypted_file:
        encrypted_file.write(
            salt + encrypted_data
        )

    return encrypted_file_path


def decrypt_file(file_path: str, password: str) -> str:
    if not file_path.endswith(".secure"):
        raise ValueError(
            "Lütfen .secure uzantılı şifreli bir dosya seçin."
        )

    with open(file_path, "rb") as file:
        data = file.read()

    if len(data) <= 16:
        raise ValueError(
            "Geçersiz veya bozuk şifreli dosya."
        )

    salt = data[:16]
    encrypted_data = data[16:]

    key = generate_key(
        password,
        salt
    )

    fernet = Fernet(key)

    try:
        decrypted_data = fernet.decrypt(
            encrypted_data
        )
    except InvalidToken:
        raise ValueError(
            "Parola yanlış veya dosya bozulmuş."
        )

    decrypted_file_path = file_path[:-7]

    if os.path.exists(decrypted_file_path):
        directory = os.path.dirname(
            decrypted_file_path
        )

        filename = os.path.basename(
            decrypted_file_path
        )

        name, extension = os.path.splitext(
            filename
        )

        counter = 1

        while True:
            new_path = os.path.join(
                directory,
                f"{name}_cozulmus_{counter}{extension}"
            )

            if not os.path.exists(new_path):
                decrypted_file_path = new_path
                break

            counter += 1

    with open(
        decrypted_file_path,
        "wb"
    ) as decrypted_file:
        decrypted_file.write(
            decrypted_data
        )

    return decrypted_file_path


def calculate_sha256(file_path: str) -> str:
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            data = file.read(4096)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()