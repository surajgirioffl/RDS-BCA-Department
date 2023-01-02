import bcrypt


def encryptPassword(password: str, rounds: int = 12):
    # rounds specifies the complexity of the hash. It is an integer that specifies the number of rounds of hashing to perform when generating the salt.
    salt = bcrypt.gensalt(rounds=rounds)
    hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash


def checkPassword(password: str, hash: str) -> bool:
    if not isinstance(hash, bytes):
        hash = hash.encode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'), hash)


if __name__ == "__main__":
    hash = encryptPassword('Suraj Giri')
    print(hash)
    print(checkPassword("Suraj Giri", hash))
