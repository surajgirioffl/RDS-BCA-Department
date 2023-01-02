import bcrypt


def encryptPassword(password: str, rounds: int = 8):
    # rounds specifies the complexity of the hash. It is an integer that specifies the number of rounds of hashing to perform when generating the salt.
    salt = bcrypt.gensalt(rounds=rounds)
    hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash

