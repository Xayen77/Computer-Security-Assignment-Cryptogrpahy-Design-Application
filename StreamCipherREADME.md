# VishStream-24X Stream Cipher

A custom stream cipher implementation using dual Linear Feedback Shift Registers (LFSRs) with non-linear combination for educational purposes.

## 📋 Project Information

**Course:** Computer Security Assignment  
**Institution:** [Your Institution Name]

### Group Members
- Vishall A/L Mahadevan (22007347)
- Ahmad Ashraf Bin Abdul Aziz (21001218)
- Muhammad Idlan Bin Idris (21001226)
- Mohammad Eizwan Eizaidie Bin Matheus (22003905)

## 🔐 Overview

VishStream-24X is a stream cipher that combines two 16-bit Linear Feedback Shift Registers (LFSRs) with a non-linear combining function to generate pseudorandom keystreams for encryption and decryption operations.

### Key Features

- **Dual LFSR Architecture**: Uses two independent 16-bit LFSRs for enhanced randomness
- **Non-linear Combination**: Implements `(bit1 ⊕ bit2) ⊕ (bit1 ∧ bit2)` for increased security
- **SHA-256 Key Derivation**: Converts user passwords into deterministic LFSR seeds
- **XOR-based Encryption**: Symmetric encryption allowing same function for encrypt/decrypt
- **Customizable Tap Positions**: Configurable feedback polynomials for both LFSRs

## 🛠️ Technical Specifications

### LFSR Configuration

| Component | Size | Tap Positions |
|-----------|------|---------------|
| LFSR 1 | 16 bits | [0, 2, 3, 5] |
| LFSR 2 | 16 bits | [1, 4, 6, 9] |

### Architecture
```
User Key → SHA-256 Hash → Split Seeds → LFSR1 + LFSR2
                                           ↓
                                    Non-linear Combiner
                                           ↓
                                      Keystream
                                           ↓
                              Plaintext ⊕ Keystream = Ciphertext
```

## 📦 Installation

### Prerequisites

- Python 3.6 or higher
- No external dependencies required (uses standard library only)

### Setup

1. Clone or download the repository
2. Navigate to the project directory
3. Run the script directly:
```bash
python vishstream24x.py
```

## 💻 Usage

### Basic Example
```python
from vishstream24x import VishStream24X

# Initialize cipher with a secret key
cipher = VishStream24X("my_secret_password")

# Encrypt a message
plaintext = b"HELLO WORLD"
ciphertext = cipher.encrypt(plaintext)
print(f"Encrypted: {ciphertext.hex()}")

# Decrypt the message (reinitialize cipher first!)
cipher = VishStream24X("my_secret_password")
decrypted = cipher.decrypt(ciphertext)
print(f"Decrypted: {decrypted}")
```

### Interactive Demo

Run the script directly for an interactive demonstration:
```bash
python vishstream24x.py
```

Example session:
```
=== VishStream-24X Encryption Demo ===
Enter secret key: SecurePassword123
Plaintext : b'HELLO WORLD'
Ciphertext (hex): a3f5b2c8d4e1f7a9b3c5
Decrypted : b'HELLO WORLD'
```

## 🔧 API Reference

### Classes

#### `LFSR`
Linear Feedback Shift Register implementation.

**Parameters:**
- `seed_bits` (list): Initial state as list of bits
- `tap_positions` (list): Positions for feedback XOR operation

**Methods:**
- `step()`: Advances LFSR one step, returns output bit

#### `VishStream24X`
Main cipher class.

**Parameters:**
- `key` (str): Secret key for encryption/decryption

**Methods:**
- `generate_keystream(num_bytes)`: Generates pseudorandom keystream
- `encrypt(plaintext)`: Encrypts data (bytes)
- `decrypt(ciphertext)`: Decrypts data (bytes)

### Helper Functions

- `text_to_bits_from_key(key, length)`: Converts key to bit array using SHA-256
- `bits_to_bytes(bit_list)`: Converts bit list to bytes
- `xor_bytes(data, keystream)`: XORs two byte sequences

## ⚠️ Important Notes

### Cipher Reinitialization

**Critical:** You must reinitialize the cipher with the same key before decryption:
```python
# ✅ CORRECT
cipher = VishStream24X(key)
ciphertext = cipher.encrypt(plaintext)

cipher = VishStream24X(key)  # Reinitialize!
decrypted = cipher.decrypt(ciphertext)

# ❌ WRONG
cipher = VishStream24X(key)
ciphertext = cipher.encrypt(plaintext)
decrypted = cipher.decrypt(ciphertext)  # Will produce garbage!
```

This is required because the LFSR state changes during encryption and must be reset to the initial state for decryption.

## 🔒 Security Considerations

### Educational Purpose Only

**This cipher is designed for educational purposes and should NOT be used in production environments.**

### Known Limitations

1. **Small State Space**: 16-bit LFSRs provide only 2^16 possible states each
2. **Known Plaintext Attacks**: Vulnerable if attacker knows plaintext-ciphertext pairs
3. **Algebraic Attacks**: Linear structure can be exploited mathematically
4. **No Authentication**: Provides no integrity or authenticity guarantees
5. **Short Period**: Maximum period is limited by LFSR size

### Recommendations for Real-World Use

For actual security applications, use established standards:
- **AES-GCM** for authenticated encryption
- **ChaCha20-Poly1305** for stream cipher needs
- **TLS 1.3** for network communications

## 📚 Educational Value

This implementation demonstrates:

- Stream cipher principles
- LFSR operation and feedback polynomials
- Non-linear combining functions
- Key derivation from passwords
- XOR-based encryption symmetry

## 🧪 Testing

Run basic tests:
```python
# Test encryption/decryption cycle
def test_encryption_cycle():
    key = "test_key"
    plaintext = b"Test message 123"
    
    cipher1 = VishStream24X(key)
    ciphertext = cipher1.encrypt(plaintext)
    
    cipher2 = VishStream24X(key)
    decrypted = cipher2.decrypt(ciphertext)
    
    assert plaintext == decrypted, "Decryption failed!"
    print("✓ Encryption cycle test passed")

test_encryption_cycle()
```

## 📄 License

This project is created for academic purposes. Please check with your institution regarding usage and distribution policies.

## 🤝 Contributing

This is an academic assignment. For educational improvements or bug fixes, please contact the group members.

## 📧 Contact

For questions regarding this implementation, please contact any of the group members listed above.

---

**Disclaimer:** This is a student project for educational purposes. Do not use this cipher for protecting sensitive or real-world data. Always use industry-standard, peer-reviewed cryptographic libraries for production applications.
