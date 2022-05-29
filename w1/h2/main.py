from __future__ import annotations
from typing import AnyStr, NoReturn, Type, Any

import os
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography import exceptions


class Hash:
    def __init__(self, algorithm: Type[hashes.HashAlgorithm]) -> NoReturn:
        self.algorithm = algorithm

    def __repr__(self) -> str:
        return f'{type(self).__name__}<{self.algorithm.__name__}>'

    def __call__(self, data: AnyStr) -> str:
        if isinstance(data, str):
            data = data.encode()
        digest = hashes.Hash(self.algorithm())
        digest.update(data)
        return digest.finalize().hex()

    def debug(self, data: AnyStr) -> bool:
        print(self)
        print('Hashed:', f"{self.__call__(data)}")
        return True


class Symmetric:
    def __init__(self,
                 algorithm: Type[algorithms.CipherAlgorithm],
                 key_length: int,
                 mode: modes.Mode,
                 padding_algorithm: Type[Any] = padding.PKCS7) -> NoReturn:
        self.algorithm = algorithm
        self.key_length = key_length
        self.mode = mode
        self.padding_algorithm = padding_algorithm

        self.key = os.urandom(key_length // 8)
        # noinspection PyArgumentList
        self.cipher = Cipher(algorithm(self.key), mode)

    def __repr__(self) -> str:
        return (
            f'{type(self).__name__}<'
            f'{self.algorithm.__name__}-{self.key_length}-{type(self.mode).__name__}-{self.padding_algorithm.__name__}'
            '>'
        )

    def encrypt(self, data: AnyStr) -> str:
        if isinstance(data, str):
            data = data.encode()
        encryptor = self.cipher.encryptor()
        padder = self.padding_algorithm(self.key_length).padder()
        data = padder.update(data) + padder.finalize()
        return b64encode(encryptor.update(data) + encryptor.finalize()).decode()

    def decrypt(self, data: AnyStr) -> AnyStr:
        if isinstance(data, str):
            data = b64decode(data)
        decryptor = self.cipher.decryptor()
        unpadder = self.padding_algorithm(self.key_length).unpadder()
        decrypted = decryptor.update(data) + decryptor.finalize()
        decrypted = unpadder.update(decrypted) + unpadder.finalize()
        try:
            return decrypted.decode()
        except UnicodeDecodeError:
            return decrypted

    def debug(self, data: AnyStr) -> bool:
        print(self)
        print('Key:', self.key.hex())
        encrypted = self.encrypt(data)
        print('Encrypted:', encrypted)
        decrypted = self.decrypt(encrypted)
        print('Decrypted:', decrypted)
        ok = data == decrypted
        print('OK:', ok)
        return ok


class ECDSASignature:
    def __init__(self,
                 algorithm: Type[ec.EllipticCurveSignatureAlgorithm] = ec.ECDSA,
                 hash_algorithm: Type[hashes.HashAlgorithm] = hashes.SHA256,
                 private_key: ec.EllipticCurvePrivateKey = None) -> NoReturn:
        self.algorithm = algorithm
        self.hash_algorithm = hash_algorithm
        self.private_key = private_key or ec.generate_private_key(ec.SECP384R1())
        self.public_key = self.private_key.public_key()

    def __repr__(self) -> str:
        return f'{type(self).__name__}<{self.algorithm.__name__}-{self.hash_algorithm.__name__}>'

    def sign(self, data: AnyStr) -> str:
        if isinstance(data, str):
            data = data.encode()
        # noinspection PyArgumentList
        signature = self.private_key.sign(data, self.algorithm(self.hash_algorithm()))
        return b64encode(signature).decode()

    def verify(self, data: AnyStr, signature: AnyStr) -> bool:
        if isinstance(data, str):
            data = data.encode()
        if isinstance(signature, str):
            signature = b64decode(signature)
        try:
            # noinspection PyArgumentList
            self.public_key.verify(signature, data, self.algorithm(self.hash_algorithm()))
            return True
        except (exceptions.InvalidSignature, exceptions.UnsupportedAlgorithm, ValueError):
            return False

    def debug(self, data: AnyStr) -> bool:
        print(self)
        print('Private key:', self.private_key.private_numbers().private_value)
        print('Public key:', self.public_key.public_numbers().x, '(x),', self.public_key.public_numbers().y, '(y)')
        signature = self.sign(data)
        print('Signature:', signature)
        ok = self.verify(data, signature)
        print('Verification:', 'valid' if ok else 'invalid')
        print('OK:', ok)
        return ok


if __name__ == '__main__':
    input_data = input('Input data: ')
    print()

    Hash(hashes.SHA256).debug(input_data)
    print()
    Hash(hashes.SM3).debug(input_data)
    print()

    Symmetric(algorithms.AES, 256, modes.CBC(os.urandom(16)), padding.ANSIX923).debug(input_data)
    print()
    Symmetric(algorithms.AES, 256, modes.CBC(os.urandom(16)), padding.PKCS7).debug(input_data)
    print()
    Symmetric(algorithms.SM4, 128, modes.CBC(os.urandom(16)), padding.ANSIX923).debug(input_data)
    print()
    Symmetric(algorithms.SM4, 128, modes.CBC(os.urandom(16)), padding.PKCS7).debug(input_data)
    print()

    ECDSASignature(ec.ECDSA, hashes.SHA256, ec.generate_private_key(ec.SECP384R1())).debug(input_data)
