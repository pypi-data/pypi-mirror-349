from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
from Crypto.Hash import MD2, MD5, SHA1, SHA224, SHA256, SHA384, SHA512
from typing import Tuple, Optional
class RSACryptor:

    KEY_SIZE = [512, 1024, 2048, 4096]
    KEY_FORMATS = ["PKCS#1", "PKCS#8"]
    PADDINGS = ["OAEP", "PKCS1", "NONE"]
    HASH_ALGOS = ["MD2", "MD5", "SHA1", "SHA224", "SHA256", "SHA384", "SHA512"]
    MGF_HASH_ALGOS = ["MD2", "MD5", "SHA1", "SHA224", "SHA256", "SHA384", "SHA512"]
    
    def __init__(self, private_key: Optional[str] = None, public_key: Optional[str] = None,
                 padding_mode: str = "OAEP", hash_algo: Optional[str] = "SHA256",
                 mgf_hash_algo: Optional[str] = "SHA256", passphrase: Optional[str] = None):
        """
        初始化 RSACryptor 类。
        :param private_key: PEM 格式的私钥字符串
        :param public_key: PEM 格式的公钥字符串
        :param padding_mode: RSA 填充模式，支持 "OAEP", "PKCS1", "NONE"
        :param hash_algo: Hash 算法，支持 "MD2", "MD5", "SHA1", "SHA224", "SHA256", "SHA384", "SHA512"
        :param mgf_hash_algo: MGF Hash 算法，支持 "MD2", "MD5", "SHA1", "SHA224", "SHA256", "SHA384", "SHA512"
        :param passphrase: 私钥的密码（如果私钥是加密的）
        """
        # 导入私钥（如果提供了密码）
        self.private_key = RSA.import_key(private_key, passphrase=passphrase) if private_key else None
        self.public_key = RSA.import_key(public_key) if public_key else None
        self.padding_mode = padding_mode
        # 设置 Hash 和 MGF Hash 算法
        if padding_mode == "OAEP":
            if not hash_algo or not mgf_hash_algo:
                raise ValueError("Hash and MGFHash algorithms are required for OAEP padding mode")
            self.hash_algo = self._get_hash_algo(hash_algo)
            self.mgf_hash_algo = self._get_hash_algo(mgf_hash_algo)
        else:
            self.hash_algo = None
            self.mgf_hash_algo = None
    def _get_hash_algo(self, algo_name: str):
        """
        根据算法名称返回对应的 Hash 算法对象。
        :param algo_name: Hash 算法名称
        :return: Hash 算法对象
        """
        hash_algo_map = {
            "MD2": MD2,
            "MD5": MD5,
            "SHA1": SHA1,
            "SHA224": SHA224,
            "SHA256": SHA256,
            "SHA384": SHA384,
            "SHA512": SHA512
        }
        if algo_name in hash_algo_map:
            return hash_algo_map[algo_name]
        else:
            raise ValueError(f"Unsupported hash algorithm: {algo_name}")
    def encrypt(self, plaintext: bytes) -> bytes:
        """
        使用公钥加密数据。
        :param plaintext: 明文数据（字节类型）
        :return: 加密后的数据（字节类型）
        """
        if not self.public_key:
            raise ValueError("Public key is not provided for encryption")
        if self.padding_mode == "OAEP":
            cipher = PKCS1_OAEP.new(self.public_key, hashAlgo=self.hash_algo,
                                    mgfunc=lambda x, y: PKCS1_OAEP.MGF1(x, y, self.mgf_hash_algo))
        elif self.padding_mode == "PKCS1":
            cipher = PKCS1_v1_5.new(self.public_key)
        elif self.padding_mode == "NONE":
            cipher = self.public_key
        else:
            raise ValueError(f"Unsupported padding mode: {self.padding_mode}")
        return cipher.encrypt(plaintext)
    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        使用私钥解密数据。
        :param ciphertext: 加密后的数据（字节类型）
        :return: 解密后的明文数据（字节类型）
        """
        if not self.private_key:
            raise ValueError("Private key is not provided for decryption")
        if self.padding_mode == "OAEP":
            cipher = PKCS1_OAEP.new(self.private_key, hashAlgo=self.hash_algo,
                                   mgfunc=lambda x, y: PKCS1_OAEP.MGF1(x, y, self.mgf_hash_algo))
        elif self.padding_mode == "PKCS1":
            cipher = PKCS1_v1_5.new(self.private_key)
        elif self.padding_mode == "NONE":
            cipher = self.private_key
        else:
            raise ValueError(f"Unsupported padding mode: {self.padding_mode}")
        return cipher.decrypt(ciphertext)
    @staticmethod
    def generate_key_pair(key_size: int = 2048, key_format: str = "PKCS#8", passphrase: Optional[str] = None) -> Tuple[str, str]:
        """
        生成 RSA 密钥对。
        :param key_size: 密钥长度，支持 512, 1024, 2048, 4096
        :param key_format: 密钥格式，支持 "PKCS#1" 和 "PKCS#8"
        :param passphrase: 用于加密私钥的密码（可选）
        :return: 生成的密钥对（私钥、公钥）
        """
        if key_size not in [512, 1024, 2048, 4096]:
            raise ValueError("Unsupported key size. Supported sizes: 512, 1024, 2048, 4096")
        if key_format not in ['PKCS#1', 'PKCS#8']:
            raise ValueError("Unsupported key format. Supported formats: 'PKCS#1', 'PKCS#8'")
        # 生成密钥对
        private_key = RSA.generate(key_size)
        public_key = private_key.publickey()
        # 根据格式导出密钥
        if key_format == 'PKCS#1':
            private_key_pem = private_key.export_key(format='PEM', passphrase=passphrase).decode()
            public_key_pem = public_key.export_key(format='PEM').decode()
        elif key_format == 'PKCS#8':
            private_key_pem = private_key.export_key(format='PEM', pkcs=8, passphrase=passphrase).decode()
            public_key_pem = public_key.export_key(format='PEM', pkcs=8).decode()
        return private_key_pem, public_key_pem
# 示例用法
if __name__ == "__main__":
    # 生成密钥对
    key_size = 2048
    key_format = "PKCS#8"
    passphrase = None  # 私钥密码
    private_key_pem, public_key_pem = RSACryptor.generate_key_pair(key_size, key_format, passphrase)
    # 打印生成的密钥
    print("Private Key:\n", private_key_pem)
    print("Public Key:\n", public_key_pem)
    # 初始化 RSACryptor
    rsa_cryptor = RSACryptor(private_key_pem, public_key_pem, padding_mode="OAEP", hash_algo="SHA256", mgf_hash_algo="SHA256", passphrase=passphrase)
    # 加密和解密
    plaintext = b"Hello, RSA!"  # 明文需要是字节类型
    encrypted = rsa_cryptor.encrypt(plaintext)
    print("Encrypted:", encrypted)
    decrypted = rsa_cryptor.decrypt(encrypted)
    print("Decrypted:", decrypted.decode())  # 将字节解码为字符串
