from Crypto.Cipher import AES
from typing import Union, Optional
import os

class AESCryptor:
    """
    AES 加解密工具类，支持多种填充模式和加密模式。
    输入输出均为字节格式（bytes）。
    """
    # AES支持的模式
    MODES = {
        'CBC': AES.MODE_CBC,
        'ECB': AES.MODE_ECB,
        'CFB': AES.MODE_CFB,
        'OFB': AES.MODE_OFB,
        'CTR': AES.MODE_CTR,
        'GCM': AES.MODE_GCM
    }
    # 填充方式
    PADDINGS = ['PKCS7', 'ISO7816', 'X923', 'ZeroPadding']
    LENGTHS = [16, 24, 32]  # 支持的密钥长度
    def __init__(self, key: bytes, mode: str, iv: Optional[bytes] = None, padding_mode: str = "PKCS7", key_length: int = 16):
        """
        初始化 AES 加解密工具
        :param key: 密钥，字节格式
        :param mode: 加密模式，支持 CBC, ECB, CFB, OFB, CTR, GCM
        :param iv: 初始化向量（IV），字节格式，CBC/CFB/OFB/GCM 模式需要
        :param padding_mode: 填充模式，支持 "PKCS7", "ZeroPadding", "ISO7816", "X923"
        :param key_length: 密钥长度，支持 16（128位）、24（192位）、32（256位）
        """
        self.key = key
        self.mode = self.MODES.get(mode)
        if self.mode is None:
            raise ValueError(f"Unsupported AES mode: {mode}")
        self.iv = iv if iv is not None else b''
        self.padding_mode = padding_mode
        if self.padding_mode not in self.PADDINGS:
            raise ValueError(f"Unsupported padding mode: {padding_mode}")
        if key_length not in self.LENGTHS:
            raise ValueError(f"Unsupported key length: {key_length}")
        self.key_length = key_length

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        对字节数据进行 AES 加密
        :param plaintext: 明文数据，字节格式
        :return: 加密后的数据，字节格式
        """
        if self.mode == AES.MODE_GCM:
            # GCM 模式不需要填充
            cipher = self._init_aes()
            ciphertext, tag = cipher.encrypt_and_digest(plaintext)
            return cipher.nonce + tag + ciphertext
        else:
            padded_data = self._pad(plaintext)
            cipher = self._init_aes()
            ciphertext = cipher.encrypt(padded_data)
            return ciphertext

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        对字节数据进行 AES 解密
        :param ciphertext: 加密数据，字节格式
        :return: 解密后的数据，字节格式
        """
        if self.mode == AES.MODE_GCM:
            # GCM 模式不需要填充
            nonce = ciphertext[:16]
            tag = ciphertext[16:32]
            ciphertext = ciphertext[32:]
            cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            return plaintext
        else:
            cipher = self._init_aes()
            padded_plaintext = cipher.decrypt(ciphertext)
            plaintext = self._unpad(padded_plaintext)
            return plaintext

    def _init_aes(self) -> AES:
        """
        初始化 AES 对象
        :return: AES 对象
        """
        if self.mode in (AES.MODE_CBC, AES.MODE_CFB, AES.MODE_OFB):
            return AES.new(self.key, self.mode, self.iv)
        elif self.mode == AES.MODE_ECB:
            return AES.new(self.key, self.mode)
        elif self.mode == AES.MODE_CTR:
            return AES.new(self.key, self.mode, nonce=self.iv[:8])
        elif self.mode == AES.MODE_GCM:
            return AES.new(self.key, self.mode, nonce=self.iv)
        else:
            raise ValueError(f"Unsupported AES mode: {self.mode}")

    def _pad(self, data: bytes) -> bytes:
        """
        填充数据
        :param data: 原始数据，字节格式
        :return: 填充后的数据，字节格式
        """
        block_size = self.key_length
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
def test_aes_cryptor():
    key = b'0123456789abcdef'  # 16字节密钥
    iv = b'1234567890abcdef'   # 16字节IV
    plaintext = b"Hello, AES!"  # 明文数据
    for mode in AESCryptor.MODES:
        for padding_mode in AESCryptor.PADDINGS:
            try:
                cryptor = AESCryptor(key, mode, iv, padding_mode)
                ciphertext = cryptor.encrypt(plaintext)
                decrypted_text = cryptor.decrypt(ciphertext)
                assert decrypted_text == plaintext, f'{mode}/{padding_mode} test failed'
            except Exception as e:
                print(f'{mode}/{padding_mode} test failed with error: {e}')
    print("All tests passed!")

if __name__ == "__main__":
    test_aes_cryptor()
