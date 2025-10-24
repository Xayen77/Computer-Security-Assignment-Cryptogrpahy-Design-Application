# =========================================================
# VishStream-5: Simple Educational Stream Cipher
# =========================================================

class LFSR:
    def __init__(self, seed_bits, tap_positions):
        """
        seed_bits: list representing initial key as bits (e.g. [1,0,1,1,0])
        tap_positions: positions used to generate new bit through XOR
        """
        self.register = seed_bits
        self.taps = tap_positions

    def step(self):
        """
        Perform one LFSR step:
        1. XOR tap bits to compute new bit.
        2. Shift right.
        3. Return the output bit (used as part of keystream).
        """
        new_bit = 0
        for t in self.taps:
            new_bit ^= self.register[-1 - t]  # XOR tap bits from right
        
        # Output bit is the rightmost bit before shifting
        output_bit = self.register[-1]
        
        # Shift register right and insert new_bit at left
        self.register = [new_bit] + self.register[:-1]
        
        return output_bit

    def generate_keystream(self, length):
        """
        Generate keystream bits of specified length
        """
        return [self.step() for _ in range(length)]


def bits_to_bytes(bit_list):
    """
    Convert list of bits (0/1) to actual bytes
    """
    result = bytearray()
    for i in range(0, len(bit_list), 8):
        byte = 0
        for bit in bit_list[i:i+8]:
            byte = (byte << 1) | bit
        result.append(byte)
    return bytes(result)


def xor_bytes(data, keystream):
    """
    XOR two byte arrays
    """
    return bytes([d ^ k for d, k in zip(data, keystream)])


# ========================== DEMO =========================

# 1. Key (seed) and tap selection
seed = [1, 0, 1, 1, 0]  # 5-bit key
taps = [0, 2]           # XOR tap positions
lfsr = LFSR(seed, taps)

# 2. Message to encrypt
plaintext = b"HELLO"

# 3. Generate keystream of same length as plaintext (in bits)
keystream_bits = lfsr.generate_keystream(len(plaintext) * 8)

# 4. Convert keystream bits to bytes
keystream = bits_to_bytes(keystream_bits)

print("Plaintext :", plaintext)
print("Keystream :", keystream.hex())

# 5. Encrypt
ciphertext = xor_bytes(plaintext, keystream)
print("Ciphertext:", ciphertext.hex())

# 6. Decrypt (same process: XOR again)
# Need to reinitialize LFSR to the same state
lfsr = LFSR(seed, taps)
keystream_bits = lfsr.generate_keystream(len(ciphertext) * 8)
keystream = bits_to_bytes(keystream_bits)
decrypted = xor_bytes(ciphertext, keystream)

print("Decrypted :", decrypted)
