# -*- coding: UTF-8 -*-
from gmssl import sm4
from typing import Optional


class SM4Cryptor:
    """
    SM4 加解密工具类，基于 gmssl 模块实现，支持多种填充模式和加密模式。
    输入输出均为字节格式（bytes）。
    """
    MODES = ['ECB', 'CBC']   # 加密模式
    # 填充方式
    PADDINGS = ['PKCS7', 'ZeroPadding']

    def __init__(self, key: bytes, mode: str = 'CBC', iv: Optional[bytes] = None, padding_mode: str = "PKCS7"):
        """
        初始化 SM4 加解密工具
        :param key: 密钥，字节格式（16字节，128位）
        :param mode: 加密模式，支持 ECB, CBC
        :param iv: 初始化向量（IV），字节格式，CBC 模式需要
        :param padding_mode: 填充模式，支持 "PKCS7", "ZeroPadding"
        """
        if len(key) != 16:
            raise ValueError("SM4 key must be 16 bytes long (128 bits)")
        self.key = key
        self.mode = mode.upper()
        if self.mode not in self.MODES:
            raise ValueError(f"Unsupported SM4 mode: {mode}")
        self.iv = iv if iv is not None else b''
        if self.mode == 'CBC' and len(self.iv) != 16:
            raise ValueError("IV must be 16 bytes long for CBC mode")
        self.padding_mode = padding_mode

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        对字节数据进行 SM4 加密
        :param plaintext: 明文数据，字节格式
        :return: 加密后的数据，字节格式
        """
        padded_data = self._pad(plaintext)
        cipher = sm4.CryptSM4()
        cipher.set_key(self.key, sm4.SM4_ENCRYPT)
        if self.mode == 'CBC':
            ciphertext = cipher.crypt_cbc(self.iv, padded_data)
        else:  # ECB模式
            ciphertext = cipher.crypt_ecb(padded_data)
        return ciphertext

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        对字节数据进行 SM4 解密
        :param ciphertext: 加密数据，字节格式
        :return: 解密后的数据，字节格式
        """
        cipher = sm4.CryptSM4()
        cipher.set_key(self.key, sm4.SM4_DECRYPT)
        if self.mode == 'CBC':
            padded_plaintext = cipher.crypt_cbc(self.iv, ciphertext)
        else:  # ECB模式
            padded_plaintext = cipher.crypt_ecb(ciphertext)
        plaintext = self._unpad(padded_plaintext)
        return plaintext

    def _pad(self, data: bytes) -> bytes:
        """
        填充数据
        :param data: 原始数据，字节格式
        :return: 填充后的数据，字节格式
        """
        block_size = 16  # SM4的分组长度为16字节
        padding_length = block_size - (len(data) % block_size)
        if self.padding_mode == "PKCS7":
            return data + bytes([padding_length] * padding_length)
        elif self.padding_mode == "ZeroPadding":
            return data + bytes([0] * padding_length)
        else:
            raise ValueError(f"Unsupported padding mode: {self.padding_mode}")

    def _unpad(self, data: bytes) -> bytes:
        """
        去除填充
        :param data: 填充后的数据，字节格式
        :return: 去除填充后的数据，字节格式
        """
        if self.padding_mode == "PKCS7":
            padding_length = data[-1]
            return data[:-padding_length]
        elif self.padding_mode == "ZeroPadding":
            return data.rstrip(b'\x00')
        else:
            raise ValueError(f"Unsupported padding mode: {self.padding_mode}")


# 测试代码
def test_sm4_cryptor():
    key = b'0123456789abcdef'  # 16字节密钥
    iv = b'1234567890abcdef'   # 16字节IV
    plaintext = b"Hello, SM4!"  # 明文数据

    # 测试 CBC 模式
    cryptor = SM4Cryptor(key, 'CBC', iv, padding_mode='PKCS7')
    ciphertext = cryptor.encrypt(plaintext)
    decrypted_text = cryptor.decrypt(ciphertext)
    assert decrypted_text == plaintext, "CBC mode test failed"

    # 测试 ECB 模式
    cryptor = SM4Cryptor(key, 'ECB', padding_mode='PKCS7')
    ciphertext = cryptor.encrypt(plaintext)
    decrypted_text = cryptor.decrypt(ciphertext)
    assert decrypted_text == plaintext, "ECB mode test failed"

    # 测试 ZeroPadding 填充
    cryptor = SM4Cryptor(key, 'CBC', iv, padding_mode='ZeroPadding')
    ciphertext = cryptor.encrypt(plaintext)
    decrypted_text = cryptor.decrypt(ciphertext)
    assert decrypted_text == plaintext, "ZeroPadding test failed"

    print("All tests passed!")


if __name__ == "__main__":
    # pip install gmssl
    test_sm4_cryptor()
