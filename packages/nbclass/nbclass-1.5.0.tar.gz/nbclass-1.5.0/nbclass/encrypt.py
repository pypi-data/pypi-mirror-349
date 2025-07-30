# -*- coding: utf-8 -*-
"""
@ Created on 2024-09-04 15:44
---------
@summary: 
---------
@author: XiaoBai
"""
import base64
import binascii
import hashlib
import hmac

from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Util import Counter
from Crypto.Util.Padding import pad, unpad
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT

from nbclass.typeshed import StrBytes


def aes_encrypt_cbc(
        key: StrBytes, plaintext: StrBytes, iv: StrBytes,
        is_hex: bool = False
) -> str:
    """
    AES-CBC模式加密
    :param key: aes密钥
    :param plaintext: 明文
    :param iv: 初始化向量（字节串，长度为16字节，默认自动生成）
    :param is_hex: 是否返回Hex编码的密文（默认为Base64编码）
    :return: 密文
    """
    if isinstance(key, str):
        key = key.encode()
    if isinstance(iv, str):
        iv = iv.encode()
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    padded_text = pad(plaintext, AES.block_size)
    ciphertext = cipher.encrypt(padded_text)
    return bytes.hex(ciphertext) if is_hex else base64.b64encode(ciphertext).decode('utf-8')


def aes_decrypt_cbc(
        key: StrBytes, ciphertext: StrBytes, iv: StrBytes,
        is_hex: bool = False
) -> str:
    """
    AES-CBC模式解密
    :param key: aes密钥
    :param ciphertext: 密文
    :param iv: 初始化向量, 长度为8*N字节
    :param is_hex: 密文是否为Hex编码（默认为Base64编码）
    :return: 明文
    """
    if isinstance(key, str):
        key = key.encode()
    if isinstance(iv, str):
        iv = iv.encode()

    encrypted = ciphertext
    if isinstance(ciphertext, str):
        encrypted = bytes.fromhex(ciphertext) if is_hex is True else base64.b64decode(ciphertext)

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    padded_text = cipher.decrypt(encrypted)
    plaintext = unpad(padded_text, AES.block_size)
    return plaintext.decode('utf-8')


def aes_encrypt_cfb(
        key: StrBytes, plaintext: StrBytes, iv: StrBytes,
        segment_size: int = 8, is_hex: bool = False
) -> str:
    """
    AES-CFB模式加密
    :param key: aes密钥
    :param plaintext: 明文（字节串）
    :param iv: 初始化向量（长度为16字节）
    :param segment_size: 明文和密文被分割的**位数**, 它一定是8的倍数, 默认为8
    :param is_hex: 是否返回Hex编码的密文（默认为Base64编码）
    :return: 密文（字节串），IV（字节串）
    """
    if isinstance(key, str):
        key = key.encode()
    if isinstance(iv, str):
        iv = iv.encode()
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')

    cipher = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=segment_size)
    ciphertext = cipher.encrypt(plaintext)
    return bytes.hex(ciphertext) if is_hex else base64.b64encode(ciphertext).decode('utf-8')


def aes_decrypt_cfb(
        key: StrBytes, ciphertext: StrBytes, iv: StrBytes,
        segment_size: int = 8, is_hex: bool = False
) -> str:
    """
    AES-CFB模式解密
    :param key: aes密钥
    :param ciphertext: 密文
    :param iv: 初始化向量（长度为16字节）
    :param segment_size: 明文和密文被分割的**位数**, 它一定是8的倍数, 默认为8
    :param is_hex: 密文是否为Hex编码（默认为Base64编码）
    :return: 明文（字节串）
    """
    if isinstance(key, str):
        key = key.encode()
    if isinstance(iv, str):
        iv = iv.encode()

    encrypted = ciphertext
    if isinstance(ciphertext, str):
        encrypted = bytes.fromhex(ciphertext) if is_hex is True else base64.b64decode(ciphertext)

    cipher = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=segment_size)
    plaintext = cipher.decrypt(encrypted)
    return plaintext.decode()


def aes_encrypt_ctr(
        key: StrBytes, plaintext: StrBytes, nonce: StrBytes,
        initial_value=0, is_hex: bool = False
) -> str:
    """
    AES-CTR模式加密
    :param key: aes密钥（字节串or字符串）
                AES-CTR-128模式, key长度16字节
                AES-CTR-192模式, key长度24字节
                AES-CTR-256模式, key长度32字节
    :param plaintext: 明文（字节串or字符串）
    :param nonce: 随机数（长度通常为8字节, [CTR-128、CTR-192、CTR-256]模式，nonce长度固定为16字节）
    :param initial_value: 初始计数器值（整数，默认为0）
    :param is_hex: 是否返回Hex编码的密文（默认为Base64编码）
    :return: 密文（字节串），nonce（字节串）
    """

    if isinstance(key, str):
        key = key.encode()
    if isinstance(nonce, str):
        nonce = nonce.encode()
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')

    if len(nonce) == 16:
        counter = Counter.new(nbits=128, initial_value=int.from_bytes(nonce, byteorder='big'))
        cipher = AES.new(key, AES.MODE_CTR, counter=counter)
    else:
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce, initial_value=initial_value)

    ciphertext = cipher.encrypt(plaintext)
    return bytes.hex(ciphertext) if is_hex else base64.b64encode(ciphertext).decode('utf-8')


def aes_decrypt_ctr(
        key: StrBytes, ciphertext: StrBytes, nonce,
        initial_value=0, is_hex: bool = False
) -> str:
    """
    AES-CTR模式解密
    :param key: aes密钥（字节串or字符串）
                AES-CTR-128模式, key长度16字节
                AES-CTR-192模式, key长度24字节
                AES-CTR-256模式, key长度32字节
    :param ciphertext: 密文（字节串or字符串）
    :param nonce: 随机数（长度通常为8字节, [CTR-128、CTR-192、CTR-256]模式，nonce长度固定为16字节）
    :param initial_value: 初始计数器值（整数，默认为0）
    :param is_hex: 密文是否为Hex编码（默认为Base64编码）
    :return: 明文（字节串）
    """
    if isinstance(key, str):
        key = key.encode()
    if isinstance(nonce, str):
        nonce = nonce.encode()

    if len(nonce) == 16:
        counter = Counter.new(nbits=128, initial_value=int.from_bytes(nonce, byteorder='big'))
        cipher = AES.new(key, AES.MODE_CTR, counter=counter)
    else:
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce, initial_value=initial_value)

    encrypted = ciphertext
    if isinstance(ciphertext, str):
        encrypted = bytes.fromhex(ciphertext) if is_hex is True else base64.b64decode(ciphertext)
    plaintext = cipher.decrypt(encrypted)
    return plaintext.decode()


def aes_encrypt_ecb(key: StrBytes, plaintext: StrBytes, is_hex: bool = False) -> str:
    """
    AES-ECB模式加密
    :param key: aes密钥
    :param plaintext: 待加密明文
    :param is_hex: 是否返回Hex编码的密文（默认为Base64编码）
    :return:
    """
    if isinstance(key, str):
        key = key.encode('utf-8')
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')

    cipher = AES.new(key=key, mode=AES.MODE_ECB)
    padded_plaintext = pad(plaintext, AES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)

    return bytes.hex(ciphertext) if is_hex else base64.b64encode(ciphertext).decode('utf-8')


def aes_decrypt_ecb(key: StrBytes, ciphertext: StrBytes, is_hex: bool = False) -> str:
    """
    AES-ECB模式解密
    :param key: aes密钥
    :param ciphertext: 密文
    :param is_hex: 密文是否为Hex编码（默认为Base64编码）
    :return:
    """
    if isinstance(key, str):
        key = key.encode()

    encrypted = ciphertext
    if isinstance(ciphertext, str):
        encrypted = bytes.fromhex(ciphertext) if is_hex is True else base64.b64decode(ciphertext)

    cipher = AES.new(key=key, mode=AES.MODE_ECB)
    decrypted = cipher.decrypt(encrypted)
    de_plaintext = unpad(decrypted, AES.block_size)

    return de_plaintext.decode('utf-8')


def aes_encrypt_gcm(
        key: StrBytes, plaintext: StrBytes, nonce: StrBytes,
        is_tag: bool = True, is_hex: bool = False
) -> tuple:
    """
    AES-GCM模式加密
    :param key: aes密钥
    :param plaintext: 明文（字节串）
    :param nonce: 随机数或IV，长度通常为12字节
    :param is_tag: 是否需要验证（默认为True）
    :param is_hex: 是否返回Hex编码的密文（默认为Base64编码）
    :return: 密文（字节串），IV（字节串）
    """
    if isinstance(key, str):
        key = key.encode()
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    if is_tag is True:
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    else:
        tag = ''
        ciphertext = cipher.encrypt(plaintext)
    return bytes.hex(ciphertext) if is_hex else base64.b64encode(ciphertext).decode('utf-8'), tag


def aes_decrypt_gcm(
        key: StrBytes, ciphertext: StrBytes, nonce: StrBytes,
        tag: str = None, is_hex: bool = False
) -> str:
    """
    AES-CFB模式解密
    :param key: aes密钥
    :param ciphertext: 密文
    :param nonce: 随机数或IV
    :param tag: 认证Tag
    :param is_hex: 密文是否为Hex编码（默认为Base64编码）
    :return: 明文（字节串）
    """
    if isinstance(key, str):
        key = key.encode()

    encrypted = ciphertext
    if isinstance(ciphertext, str):
        encrypted = bytes.fromhex(ciphertext) if is_hex is True else base64.b64decode(ciphertext)

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    if tag:
        if isinstance(tag, str):
            tag = tag.encode()
        plaintext = cipher.decrypt_and_verify(encrypted, tag)
        return plaintext.decode()
    else:
        plaintext = cipher.decrypt(encrypted)
        return plaintext.decode()


def aes_encrypt_ofb(
        key: StrBytes, plaintext: StrBytes, iv: StrBytes,
        is_hex: bool = False
) -> str:
    """
    AES-OFB模式加密
    :param key: aes密钥
    :param plaintext: 明文（字节串）
    :param iv: 初始化向量（字节串，长度为16字节，默认自动生成）
    :param is_hex: 是否返回Hex编码的密文（默认为Base64编码）
    :return: 密文（字节串），IV（字节串）
    """
    if isinstance(key, str):
        key = key.encode()
    if isinstance(iv, str):
        iv = iv.encode()
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')

    cipher = AES.new(key, AES.MODE_OFB, iv=iv)
    ciphertext = cipher.encrypt(plaintext)
    return bytes.hex(ciphertext) if is_hex else base64.b64encode(ciphertext).decode('utf-8')


def aes_decrypt_ofb(
        key: StrBytes, ciphertext: StrBytes, iv: StrBytes,
        is_hex: bool = False
) -> str:
    """
    AES-OFB模式解密
    :param key: aes密钥
    :param ciphertext: 密文（字节串）
    :param iv: 初始化向量（字节串，长度为16字节）
    :param is_hex: 密文是否为Hex编码（默认为Base64编码）
    :return: 明文（字节串）
    """
    if isinstance(key, str):
        key = key.encode()
    if isinstance(iv, str):
        iv = iv.encode()

    encrypted = ciphertext
    if isinstance(ciphertext, str):
        encrypted = bytes.fromhex(ciphertext) if is_hex is True else base64.b64decode(ciphertext)

    cipher = AES.new(key, AES.MODE_OFB, iv=iv)
    plaintext = cipher.decrypt(encrypted)
    return plaintext.decode()


def get_md5(*args):
    """
    @summary: 获取唯一的32位md5
    ---------
    @param args: 参与联合去重的值
    ---------
    @result: 7c8684bcbdfcea6697650aa53d7b1405
    """

    m = hashlib.md5()
    for arg in args:
        m.update(str(arg).encode())

    return m.hexdigest()


def get_sha1(*args):
    """
    @summary: 获取唯一的sha1
    ---------
    @result: 356a192b7913b04c54574d18c28d46e6395428ab
    """
    m = hashlib.sha1()
    for arg in args:
        m.update(str(arg).encode())

    return m.hexdigest()


def get_sha256(*args):
    """
    @summary: 获取唯一的64位sha256值
    ---------
    @result:
    """
    m = hashlib.sha256()
    for arg in args:
        m.update(str(arg).encode())

    return m.hexdigest()


def get_sha512(*args):
    """
    @summary: 获取sha512
    ---------
    @result:
    """
    m = hashlib.sha512()
    for arg in args:
        m.update(str(arg).encode())

    return m.hexdigest()


def get_hmac_md5(key: StrBytes, message: StrBytes):
    """
    @summary: 获取hmac_md5
    :param key: 密钥
    :param message: 明文
    ---------
    @result:
    """
    if isinstance(key, str):
        key = key.encode()
    if isinstance(message, str):
        message = message.encode()

    m = hmac.new(key, message, hashlib.md5)

    return m.hexdigest()


def get_hmac_sha1(key: StrBytes, message: StrBytes):
    """
    @summary: 获取hmac_sha1
    :param key: 密钥
    :param message: 明文
    ---------
    @result:
    """
    if isinstance(key, str):
        key = key.encode()
    if isinstance(message, str):
        message = message.encode()

    m = hmac.new(key, message, hashlib.sha1)

    return m.hexdigest()


def get_hmac_sha256(key: StrBytes, message: StrBytes):
    """
    @summary: 获取hmac_sha256
    :param key: 密钥
    :param message: 明文
    ---------
    @result:
    """
    if isinstance(key, str):
        key = key.encode()
    if isinstance(message, str):
        message = message.encode()

    m = hmac.new(key, message, hashlib.sha256)

    return m.hexdigest()


def get_hmac_sha512(key: StrBytes, message: StrBytes):
    """
    @summary: 获取hmac_sha512
    :param key: 密钥
    :param message: 明文
    ---------
    @result:
    """
    if isinstance(key, str):
        key = key.encode()
    if isinstance(message, str):
        message = message.encode()

    m = hmac.new(key, message, hashlib.sha512)

    return m.hexdigest()


def rsa_encrypt(key: str, data: str):
    public_key = RSA.import_key(base64.b64decode(key))
    rsa = PKCS1_v1_5.new(public_key)
    encrypt_msg = rsa.encrypt(data.encode('utf-8'))
    return base64.b64encode(encrypt_msg).decode()


class SM4Encrypt:
    """
    国密sm4加解密
    """

    def __init__(self, secret_key):
        self.secret_key = secret_key  # 需要加密和解密的key
        self.crypt_sm4 = CryptSM4()

    @staticmethod
    def str_to_hex(hex_str):
        """
        字符串转hex
        :param hex_str: 字符串
        :return: hex
        """
        hex_data = hex_str.encode('utf-8')
        str_bin = binascii.unhexlify(hex_data)
        return str_bin.decode('utf-8')

    def encrypt(self, value, salt):
        """
        国密sm4加密
        :param value: 待加密的字符串
        :param salt: 盐
        :return: sm4加密后的hex值
        """
        crypt_sm4 = self.crypt_sm4
        crypt_sm4.set_key(self.secret_key.encode(), SM4_ENCRYPT)
        value = value + salt
        encrypt_value = crypt_sm4.crypt_ecb(value.encode())  # bytes类型
        return encrypt_value.hex()

    def decrypt(self, encrypt_value):
        """
        国密sm4解密
        :param encrypt_value: 待解密的hex值
        :return: 原字符串
        """
        crypt_sm4 = self.crypt_sm4
        crypt_sm4.set_key(self.secret_key.encode(), SM4_DECRYPT)
        decrypt_value = crypt_sm4.crypt_ecb(bytes.fromhex(encrypt_value))  # bytes类型
        return self.str_to_hex(decrypt_value.hex())
