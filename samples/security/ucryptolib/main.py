"Exercise ucryptolib.aes with NIST SP 800-38A test vectors"
from binascii import unhexlify
import ucryptolib

VECTORS = {
    "F.5.1-2": {  # AES 128 CTR
        "key": unhexlify(b"2b7e151628aed2a6abf7158809cf4f3c"),
        "mode": ucryptolib.MODE_CTR,
        "initial": unhexlify(b"f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff"),
        "blocks": (
            (unhexlify(b"6bc1bee22e409f96e93d7e117393172a"),
             unhexlify(b"874d6191b620e3261bef6864990db6ce")),

            (unhexlify(b"ae2d8a571e03ac9c9eb76fac45af8e51"),
             unhexlify(b"9806f66b7970fdff8617187bb9fffdff")),

            (unhexlify(b"30c81c46a35ce411e5fbc1191a0a52ef"),
             unhexlify(b"5ae4df3edbd5d35e5b4f09020db03eab")),

            (unhexlify(b"f69f2445df4f9b17ad2b417be66c3710"),
             unhexlify(b"1e031dda2fbe03d1792170a0f3009cee")),
        )
    },
    "F.5.5-6": {  # AES 256 CTR
        "key": unhexlify(b"603deb1015ca71be2b73aef0857d7781"
                         b"1f352c073b6108d72d9810a30914dff4"),
        "mode": ucryptolib.MODE_CTR,
        "initial": unhexlify(b"f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff"),
        "blocks": (
            (unhexlify(b"6bc1bee22e409f96e93d7e117393172a"),
             unhexlify(b"601ec313775789a5b7a7f504bbf3d228")),

            (unhexlify(b"ae2d8a571e03ac9c9eb76fac45af8e51"),
             unhexlify(b"f443e3ca4d62b59aca84e990cacaf5c5")),

            (unhexlify(b"30c81c46a35ce411e5fbc1191a0a52ef"),
             unhexlify(b"2b0930daa23de94ce87017ba2d84988d")),

            (unhexlify(b"f69f2445df4f9b17ad2b417be66c3710"),
             unhexlify(b"dfc9c58db67aada613c2dd08457941a6")),
        )
    },

    "F.2.1-2": {  # AES 128 CBC
        "key": unhexlify(b"2b7e151628aed2a6abf7158809cf4f3c"),
        "mode": ucryptolib.MODE_CBC,
        "initial": unhexlify(b"000102030405060708090a0b0c0d0e0f"),
        "blocks": (
            (unhexlify(b"6bc1bee22e409f96e93d7e117393172a"),
             unhexlify(b"7649abac8119b246cee98e9b12e9197d")),

            (unhexlify(b"ae2d8a571e03ac9c9eb76fac45af8e51"),
             unhexlify(b"5086cb9b507219ee95db113a917678b2")),

            (unhexlify(b"30c81c46a35ce411e5fbc1191a0a52ef"),
             unhexlify(b"73bed6b8e3c1743b7116e69e22229516")),

            (unhexlify(b"f69f2445df4f9b17ad2b417be66c3710"),
             unhexlify(b"3ff1caa1681fac09120eca307586e1a7")),
        )
    },
    "F.2.5-6": {  # AES 256 CBC
        "key": unhexlify(b"603deb1015ca71be2b73aef0857d7781"
                         b"1f352c073b6108d72d9810a30914dff4"),
        "mode": ucryptolib.MODE_CBC,
        "initial": unhexlify(b"000102030405060708090a0b0c0d0e0f"),
        "blocks": (
            (unhexlify(b"6bc1bee22e409f96e93d7e117393172a"),
             unhexlify(b"f58c4c04d6e5f1ba779eabfb5f7bfbd6")),

            (unhexlify(b"ae2d8a571e03ac9c9eb76fac45af8e51"),
             unhexlify(b"9cfc4e967edb808d679f777bc6702c7d")),

            (unhexlify(b"30c81c46a35ce411e5fbc1191a0a52ef"),
             unhexlify(b"39f23369a9d9bacfa530e26304231461")),

            (unhexlify(b"f69f2445df4f9b17ad2b417be66c3710"),
             unhexlify(b"b2eb05e2c39be9fcda6c19078c6a9d1b")),
        )
    },
}


def test(vector):
    "Run the test block by block and compare to expected results"
    key = VECTORS[vector]["key"]
    mode = VECTORS[vector]["mode"]
    initial = VECTORS[vector]["initial"]
    blocks = VECTORS[vector]["blocks"]

    # Encrypt direction
    eng = ucryptolib.aes(key, mode, initial)
    for block in blocks:
        ciphertext = eng.encrypt(block[0])
        assert ciphertext == block[1]

    # Get a new object for decrypting.
    # (Each aes object can be used for either encrypting or decrypting,
    # but not both.)
    eng = ucryptolib.aes(key, mode, initial)
    for block in blocks:
        plaintext = eng.decrypt(block[1])
        assert plaintext == block[0]

    print("Pass")


def main():
    "Run all the vectors"
    for vector in VECTORS:
        print("Running {}".format(vector))
        test(vector)


if __name__ == "__main__":
    main()
