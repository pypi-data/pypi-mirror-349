# -*- coding: UTF-8 -*-
from Crypto.Cipher import ARC4
from typing import Union
class RC4Cryptor:
    """
    RC4 加解密工具类。
    输入输出均为字节格式（bytes）。
    """
    def __init__(self, key: bytes):
        """
        初始化 RC4 加解密工具
        :param key: 密钥，字节格式（1 到 256 字节）
        """
        if len(key) < 1 or len(key) > 256:
            raise ValueError("RC4 key must be between 1 and 256 bytes long")
        self.key = key
    def encrypt(self, plaintext: bytes) -> bytes:
        """
        对字节数据进行 RC4 加密
        :param plaintext: 明文数据，字节格式
        :return: 加密后的数据，字节格式
        """
        cipher = ARC4.new(self.key)
        ciphertext = cipher.encrypt(plaintext)
        return ciphertext
    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        对字节数据进行 RC4 解密
        :param ciphertext: 加密数据，字节格式
        :return: 解密后的数据，字节格式
        """
        cipher = ARC4.new(self.key)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext
# 测试代码
def test_rc4_cryptor():
    key = b'01234567'               # 8字节密钥
    plaintext = b"Hello, RC4!"      # 明文数据
    cryptor = RC4Cryptor(key)
    ciphertext = cryptor.encrypt(plaintext)
    print(f"Ciphertext: {ciphertext}")
    decrypted_text = cryptor.decrypt(ciphertext)
    print(f"Decrypted Text: {decrypted_text.decode()}")
    assert decrypted_text == plaintext, "Test failed!"
    print("Test passed!")
if __name__ == "__main__":
    test_rc4_cryptor()
