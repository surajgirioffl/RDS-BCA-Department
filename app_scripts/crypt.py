"""
    @file: crypt.py
    @author: Suraj Kumar Giri
    @init-date: 2nd Jan 2023
    @last-modified: 15th Feb 2024

    @description:
        * Module to encrypt and check encrypted password using bcrypt.
"""

import bcrypt


def encryptPassword(password: str, rounds: int = 12) -> bytes:
    """
        Description:
            - Function to encrypt password using bcrypt.

        Args:
            * password (str):
                - Password to be encrypted.
            * rounds (int, optional):
                - It specifies the number of rounds of hashing to perform when generating the salt.
                - Defaults to 12.

        Returns:
            * hash (bytes):
                - Hashed password.
    """
    # rounds specifies the complexity of the hash. It is an integer that specifies the number of rounds of hashing to perform when generating the salt.
    salt = bcrypt.gensalt(rounds=rounds)
    hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash


def checkPassword(password: str, hash: str) -> bool:
    """
        Description:
            - Function to check if the password is correct or not.

        Args:
            * password (str):
                - Password to check.
            * hash (str):
                - Hashed password.

        Returns:
            * True:
                - If password is correct.
            * False:
                - If password is incorrect.

    """
    if not isinstance(hash, bytes):
        hash = hash.encode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'), hash)


if __name__ == "__main__":
    while True:
        password = input("Write password to get hash (enter to exit): ")
        if not password:
            exit(0)

        hash = encryptPassword(password)
        print("Hash:", hash.decode())

        password, hash = input(
            "Write password and hash to check (comma separated): ").split(',')
        print(checkPassword(password.strip(), hash.strip()))
        print('-----next------')
