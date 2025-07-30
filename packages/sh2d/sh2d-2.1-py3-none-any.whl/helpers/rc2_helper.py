# -*- coding: UTF-8 -*-
from Crypto.Cipher import ARC2
from typing import Union, Optional

class RC2Cryptor:
    """
    RC2 加解密工具类，支持多种填充模式和加密模式。
    输入输出均为字节格式（bytes）。
    """
    # RC2支持的模式
    MODES = {
        'CBC': ARC2.MODE_CBC,
        'ECB': ARC2.MODE_ECB,
        'CFB': ARC2.MODE_CFB,
        'OFB': ARC2.MODE_OFB,
    }
    # 填充方式
    PADDINGS = ['PKCS7', 'ISO7816', 'X923', 'ZeroPadding']

    def __init__(self, key: bytes, mode: str, iv: Optional[bytes] = None, padding_mode: str = "PKCS7", effective_keylen: Optional[int] = None):
        """
        初始化 RC2 加解密工具
        :param key: 密钥，字节格式（1 到 128 字节）
        :param mode: 加密模式，支持 CBC, ECB, CFB, OFB
        :param iv: 初始化向量（IV），字节格式，CBC/CFB/OFB 模式需要
        :param padding_mode: 填充模式，支持 "PKCS7", "ZeroPadding", "ISO7816", "X923"
        :param effective_keylen: 有效密钥长度（位），可选，默认为密钥长度
        """
        if len(key) < 1 or len(key) > 128:
            raise ValueError("RC2 key must be between 1 and 128 bytes long")
        self.key = key
        self.mode = self.MODES.get(mode)
        if self.mode is None:
            raise ValueError(f"Unsupported RC2 mode: {mode}")
        self.iv = iv if iv is not None else b''
        self.padding_mode = padding_mode
        self.effective_keylen = effective_keylen if effective_keylen is not None else len(key) * 8

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        对字节数据进行 RC2 加密
        :param plaintext: 明文数据，字节格式
        :return: 加密后的数据，字节格式
        """
        padded_data = self._pad(plaintext)
        cipher = self._init_rc2()
        ciphertext = cipher.encrypt(padded_data)
        return ciphertext

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        对字节数据进行 RC2 解密
        :param ciphertext: 加密数据，字节格式
        :return: 解密后的数据，字节格式
        """
        cipher = self._init_rc2()
        padded_plaintext = cipher.decrypt(ciphertext)
        plaintext = self._unpad(padded_plaintext)
        return plaintext

    def _init_rc2(self) -> ARC2:
        """
        初始化 RC2 对象
        :return: RC2 对象
        """
        if self.mode in (ARC2.MODE_CBC, ARC2.MODE_CFB, ARC2.MODE_OFB):
            return ARC2.new(self.key, self.mode, self.iv, effective_keylen=self.effective_keylen)
        elif self.mode == ARC2.MODE_ECB:
            return ARC2.new(self.key, self.mode, effective_keylen=self.effective_keylen)
        else:
            raise ValueError(f"Unsupported RC2 mode: {self.mode}")

    def _pad(self, data: bytes) -> bytes:
        """
        填充数据
        :param data: 原始数据，字节格式
        :return: 填充后的数据，字节格式
        """
        block_size = 8  # RC2的块大小是8字节
        padding_length = block_size - (len(data) % block_size)
        if self.padding_mode == "PKCS7":
            return data + bytes([padding_length] * padding_length)
        elif self.padding_mode == "ZeroPadding":
            return data + bytes([0] * padding_length)
        elif self.padding_mode == "ISO7816":
            return data + bytes([0x80]) + bytes([0x00] * (padding_length - 1))
        elif self.padding_mode == "X923":
            return data + bytes([0x00] * (padding_length - 1)) + bytes([padding_length])
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
        elif self.padding_mode == "ISO7816":
            return data.rstrip(b'\x00')[:-1]
        elif self.padding_mode == "X923":
            padding_length = data[-1]
            return data[:-padding_length]
        else:
            raise ValueError(f"Unsupported padding mode: {self.padding_mode}")

# 测试代码
def test_rc2_cryptor():
    key = b'01234567'               # 8字节密钥
    iv = b'12345678'                # 8字节IV
    plaintext = b"Hello, RC2!"      # 明文数据
    for mode in RC2Cryptor.MODES:
        for padding_mode in RC2Cryptor.PADDINGS:
            try:
                cryptor = RC2Cryptor(key, mode, iv, padding_mode)
                ciphertext = cryptor.encrypt(plaintext)
                decrypted_text = cryptor.decrypt(ciphertext)
                assert decrypted_text == plaintext, f'{mode}/{padding_mode} test failed'
            except Exception as e:
                print(f'{mode}/{padding_mode} test failed with error: {e}')
    print("All tests passed!")

if __name__ == "__main__":
    test_rc2_cryptor()
