# =========================================================
# VishStream-24X: COMPUTER SECURITY ASSIGNMENT 
#GROUP MEMBERS : VISHALL A/L MAHADEVAN (22007347), AHMAD ASHRAF BIN ABDUL AZIZ (21001218), MUHAMMAD IDLAN BIN IDRIS (21001226), MOHAMMAD EIZWAN EIZAIDIE BIN MATHEUS (22003905)
# =========================================================

import hashlib

class LFSR:
    def __init__(self, seed_bits, tap_positions):
        self.register = seed_bits[:]  # Make a copy to avoid mutation issues
        self.taps = tap_positions

    def step(self):
        # XOR the tap positions (feedback)
        
        new_bit = 0
        for t in self.taps:
            new_bit ^= self.register[-1 - t]
        output_bit = self.register[-1]  # Last bit before shifting
        self.register = [new_bit] + self.register[:-1]
        return output_bit

# ======== Helper Functions ========
def text_to_bits_from_key(key, length):
    """
    Converts a user key into a bit array using SHA-256 and truncating to match length.
    """
    hashed = hashlib.sha256(key.encode()).hexdigest()  # 256-bit hash in hex
    bits = bin(int(hashed, 16))[2:].zfill(256)  # Convert to binary, padded
    return [int(b) for b in bits[:length]]


def bits_to_bytes(bit_list):
    result = bytearray()
    for i in range(0, len(bit_list), 8):
        byte = 0
        for bit in bit_list[i:i+8]:
            byte = (byte << 1) | bit
        result.append(byte)
    return bytes(result)


def xor_bytes(data, keystream):
    return bytes([d ^ k for d, k in zip(data, keystream)])


# ======== VishStream-24X Core ========
class VishStream24X:
    def __init__(self, key):
        # Convert key to bits
        seed1 = text_to_bits_from_key(key + "A", 16)  # LFSR1 16-bit
        seed2 = text_to_bits_from_key(key + "B", 16)  # LFSR2 16-bit

        # Define taps (chosen for good randomness)
        taps1 = [0, 2, 3, 5]   # Feedback for first LFSR
        taps2 = [1, 4, 6, 9]   # Feedback for second LFSR
        
        # Initialize LFSRs
        self.lfsr1 = LFSR(seed1, taps1)
        self.lfsr2 = LFSR(seed2, taps2)

    def generate_keystream(self, num_bytes):
        keystream_bits = []
        for _ in range(num_bytes * 8):  # 8 bits per byte
            bit1 = self.lfsr1.step()
            bit2 = self.lfsr2.step()
            # Non-linear combination (Originality Feature)
            combined_bit = (bit1 ^ bit2) ^ (bit1 & bit2)
            keystream_bits.append(combined_bit)
        return bits_to_bytes(keystream_bits)

    def encrypt(self, plaintext):
        ks = self.generate_keystream(len(plaintext))
        return xor_bytes(plaintext, ks)

    def decrypt(self, ciphertext):
        # Same function as encrypt since XOR is reversible
        return self.encrypt(ciphertext)

# ========================== DEMO =========================
if __name__ == "__main__":
    print("=== VishStream-24X Encryption Demo ===")
    key = input("Enter secret key: ")
    
    cipher = VishStream24X(key)
    plaintext = b"HELLO WORLD"
    
    print("Plaintext :", plaintext)
    
    ciphertext = cipher.encrypt(plaintext)
    print("Ciphertext (hex):", ciphertext.hex())
    
    # Reinitialize cipher (important for decryption)
    cipher = VishStream24X(key)
    decrypted = cipher.decrypt(ciphertext)
    print("Decrypted :", decrypted)
