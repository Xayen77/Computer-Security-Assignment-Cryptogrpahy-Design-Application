# ---------------------------------------------------------------
#  DeMorganBlock Cipher 
#  Custom cipher using De Morgan's Law + Feistel structure
#  Now with improved round key generation for more variation.
# ---------------------------------------------------------------

from typing import List

BLOCK_SIZE = 8
ROUNDS = 4


# ===============================================================
# Utility functions
# ===============================================================
def bytes_to_u32_pair(b: bytes):
    assert len(b) == 8
    left = int.from_bytes(b[:4], 'big')
    right = int.from_bytes(b[4:], 'big')
    return left, right


def u32_pair_to_bytes(l: int, r: int) -> bytes:
    return l.to_bytes(4, 'big') + r.to_bytes(4, 'big')


def rotl32(x: int, n: int) -> int:
    n %= 32
    return ((x << n) & 0xFFFFFFFF) | (x >> (32 - n))


def pad_pkcs7(data: bytes, block_size: int = BLOCK_SIZE) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    if pad_len == 0:
        pad_len = block_size
    return data + bytes([pad_len] * pad_len)


def unpad_pkcs7(data: bytes) -> bytes:
    if not data:
        return data
    pad_len = data[-1]
    if pad_len < 1 or pad_len > BLOCK_SIZE:
        raise ValueError("Invalid padding length")
    if data[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Bad PKCS#7 padding")
    return data[:-pad_len]


# ===============================================================
# Enhanced Key Schedule
# ===============================================================
def key_schedule(master_key: bytes, rounds: int = ROUNDS) -> List[int]:
    """
    Generate round keys by rotating, mixing, and XORing the master key.
    Produces more variation than the basic version.
    """
    if len(master_key) != 8:
        raise ValueError("Key must be exactly 8 bytes (8 characters)")

    k64 = int.from_bytes(master_key, 'big') & 0xFFFFFFFFFFFFFFFF
    round_keys = []

    for i in range(rounds):
        # 1. Rotate key by 8*i bits
        rot = ((k64 << (8 * i)) & 0xFFFFFFFFFFFFFFFF) | (k64 >> (64 - 8 * i))
        # 2. Nonlinear mixing
        mixed = ((rot ^ (rot >> 17)) + (rot << 5)) & 0xFFFFFFFFFFFFFFFF
        # 3. XOR with round number and mask to 32 bits
        rk = (mixed ^ (0x9E3779B1 * (i + 1))) & 0xFFFFFFFF
        round_keys.append(rk)

    return round_keys


# ===============================================================
# Round function using De Morgan's Law
# ===============================================================
def F_demorgan(r32: int, round_key32: int, round_no: int) -> int:
    a = r32 ^ round_key32
    b = (a * 0x9E3779B1) & 0xFFFFFFFF

    ab_direct = a & b
    ab_demorgan = (~((~a) | (~b))) & 0xFFFFFFFF  # same as a & b
    or_direct = a | b
    or_demorgan = (~((~a) & (~b))) & 0xFFFFFFFF  # same as a | b

    t1 = rotl32(ab_direct ^ b, (round_no * 3 + 5) % 32)
    t2 = rotl32(ab_demorgan ^ a, (round_no * 5 + 11) % 32)
    res = (t1 ^ t2) + (or_direct ^ or_demorgan)
    res &= 0xFFFFFFFF

    res = rotl32(res, ((round_key32 & 0xF) + round_no) % 32)
    res ^= ((res << 3) & 0xFFFFFFFF) ^ (round_key32 >> (round_no % 8))
    return res & 0xFFFFFFFF


# ===============================================================
# Feistel Network
# ===============================================================
def encrypt_block(block8: bytes, round_keys: List[int]) -> bytes:
    L, R = bytes_to_u32_pair(block8)
    for i, rk in enumerate(round_keys, start=1):
        Fout = F_demorgan(R, rk, i)
        L, R = R, L ^ Fout
    return u32_pair_to_bytes(L, R)


def decrypt_block(block8: bytes, round_keys: List[int]) -> bytes:
    L, R = bytes_to_u32_pair(block8)
    for i, rk in reversed(list(enumerate(round_keys, start=1))):
        Fout = F_demorgan(L, rk, i)
        L, R = R ^ Fout, L
    return u32_pair_to_bytes(L, R)


# ===============================================================
# Encrypt/decrypt full message
# ===============================================================
def encrypt_message(plaintext: bytes, master_key: bytes) -> bytes:
    rk = key_schedule(master_key, rounds=ROUNDS)
    padded = pad_pkcs7(plaintext, BLOCK_SIZE)
    ciphertext = bytearray()
    for i in range(0, len(padded), BLOCK_SIZE):
        ciphertext += encrypt_block(padded[i:i + BLOCK_SIZE], rk)
    return bytes(ciphertext)


def decrypt_message(ciphertext: bytes, master_key: bytes) -> bytes:
    rk = key_schedule(master_key, rounds=ROUNDS)
    plaintext_padded = bytearray()
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        plaintext_padded += decrypt_block(ciphertext[i:i + BLOCK_SIZE], rk)
    return unpad_pkcs7(bytes(plaintext_padded))


# ===============================================================
# Interactive demo
# ===============================================================
if __name__ == "__main__":
    print("=== DeMorgan–Feistel Block Cipher (Enhanced Key Schedule) ===")
    plaintext = input("Enter plaintext message: ").encode()
    key_input = input("Enter 8-character key: ")

    while len(key_input.encode()) != 8:
        key_input = input("Key must be exactly 8 characters. Try again: ")

    master_key = key_input.encode()

    # Encryption
    ciphertext = encrypt_message(plaintext, master_key)
    print("\nCiphertext (hex):", ciphertext.hex())

    # Decryption
    recovered = decrypt_message(ciphertext, master_key)
    print("Decrypted message:", recovered.decode())

    if recovered == plaintext:
        print("Encryption & Decryption successful!")
    else:
        print("Decryption failed!")
