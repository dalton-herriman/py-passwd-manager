from argon2 import PasswordHasher

'''
Everything related to encryption, 
decryption and key management
'''

def generate_salt():
    salt_phrase = os.urandom(16).hex()
    return salt_phrase

def apply_salt(input_string):
    salt = generate_salt()
    return f"{salt}:{input_string}"

def apply_hash_argon2(input_string):
    ph = PasswordHasher()
    return ph.hash(input_string)


