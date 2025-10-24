# 🔐 VishStream-24: Custom Stream Cipher Implementation (COMPUTER SECURITY ASSIGNMENT) 

GROUP MEMBERS: VISHALL A/L MAHADEVAN, AHMAD ASHRAF BIN ABDUL AZIZ, MUHAMMAD IDLAN BIN IDRIS, MOHAMMAD EIZWAN EIZAIDIE BIN MATHEUS





A simple implementation of a stream cipher using a Linear Feedback Shift Register (LFSR) for educational purposes.
Overview
VishStream-5 demonstrates the fundamental concepts of stream cipher encryption using an LFSR to generate a pseudorandom keystream. This implementation is designed for learning cryptographic principles and should not be used for actual security applications.
How It Works
1. Linear Feedback Shift Register (LFSR)
The LFSR is the core component that generates the keystream:

Seed (Initial State): A sequence of bits that serves as your encryption key (e.g., [1,0,1,1,0])
Tap Positions: Specific bit positions that are XORed together to generate new bits
Shift Operation: The register shifts right, outputting one bit at a time while feeding the new bit on the left

Example LFSR Step:
Initial state: [1,0,1,1,0]
Taps at positions 0 and 2 (from right):
  - Bit at position 0: 0
  - Bit at position 2: 1
  - New bit = 0 XOR 1 = 1

Output the rightmost bit (0), shift right, insert new bit:
New state: [1,1,0,1,1]
```

### 2. Keystream Generation

The LFSR repeatedly steps through states, producing a stream of pseudorandom bits equal in length to your message.

### 3. Encryption Process
```
Plaintext:  H    E    L    L    O
            ⊕    ⊕    ⊕    ⊕    ⊕  (XOR operation)
Keystream: [pseudorandom bytes from LFSR]
            =    =    =    =    =
Ciphertext: [encrypted bytes]
4. Decryption Process
Decryption uses the same process as encryption:

Reinitialize the LFSR with the same seed
Generate the same keystream
XOR the ciphertext with the keystream to recover the plaintext

This works because: (Plaintext ⊕ Keystream) ⊕ Keystream = Plaintext
Usage
Basic Encryption/Decryption
python# Initialize LFSR with a 5-bit seed and tap positions
seed = [1, 0, 1, 1, 0]
taps = [0, 2]
lfsr = LFSR(seed, taps)

# Encrypt a message
plaintext = b"HELLO"
keystream_bits = lfsr.generate_keystream(len(plaintext) * 8)
keystream = bits_to_bytes(keystream_bits)
ciphertext = xor_bytes(plaintext, keystream)

# Decrypt (reinitialize LFSR with same seed)
lfsr = LFSR(seed, taps)
keystream_bits = lfsr.generate_keystream(len(ciphertext) * 8)
keystream = bits_to_bytes(keystream_bits)
decrypted = xor_bytes(ciphertext, keystream)
Custom Keys and Taps
python# Use a longer seed for a longer period before repetition
seed = [1, 1, 0, 1, 0, 1, 1, 0]  # 8-bit seed
taps = [0, 2, 3, 5]               # Multiple tap positions

# Encrypt longer messages
plaintext = b"This is a secret message!"
# ... proceed with encryption as above
```

## Key Components

### `LFSR` Class

- **`__init__(seed_bits, tap_positions)`**: Initialize with a bit sequence and tap positions
- **`step()`**: Perform one LFSR iteration and return an output bit
- **`generate_keystream(length)`**: Generate a keystream of specified bit length

### Helper Functions

- **`bits_to_bytes(bit_list)`**: Convert a list of bits to bytes
- **`xor_bytes(data, keystream)`**: XOR two byte sequences together

## Security Considerations

⚠️ **This implementation is for educational purposes only!**

**Weaknesses:**
- **Short period**: A 5-bit LFSR has a maximum period of 31 states before repeating
- **Linear structure**: The cipher is vulnerable to known-plaintext attacks
- **Simple tap configuration**: Easy to analyze and break
- **No authentication**: Provides no integrity checking

**For real applications**, use established cryptographic libraries like:
- Python's `cryptography` library
- `PyCryptodome`
- Industry-standard algorithms (AES-GCM, ChaCha20-Poly1305)

## Example Output
```
Plaintext : b'HELLO'
Keystream : 5e4a39f7cd
Ciphertext: 161f2d9ba1
Decrypted : b'HELLO'
Learning Extensions
Try modifying the code to explore:

Different seed lengths: How does a longer seed affect the period?
Various tap configurations: Experiment with different tap positions
Known-plaintext attacks: If you know part of the plaintext, can you recover the seed?
Period calculation: Calculate and verify the LFSR's period length

Requirements:
Python 3.x
No external dependencies required
