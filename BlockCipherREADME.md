DeMorganBlock Cipher
====================================================

Overview
--------
The DeMorganBlock Cipher is a custom symmetric block cipher designed for educational purposes.
It combines a Feistel structure with a De Morgan–based round function to demonstrate cryptographic concepts 
such as confusion, diffusion, and key sensitivity.

The enhanced key schedule introduces additional variability to the round keys for improved security while 
keeping the implementation lightweight.

Features
--------
- Feistel network with 4 rounds
- De Morgan–based round function for nonlinearity and bit-level complexity
- Enhanced key schedule with rotation, mixing, and XOR
- PKCS#7 padding to handle variable-length plaintext
- Interactive user input for plaintext and 8-character keys
- Python implementation suitable for educational demonstration

Cipher Details
--------------
- Block Size: 64 bits (8 bytes)
- Half-block Size: 32 bits
- Number of Rounds: 4
- Key Size: 64 bits (8 characters)
- Padding Scheme: PKCS#7

Round Function Highlights:
- XOR input with round key
- Multiply by a constant for diffusion
- Apply AND/OR logic along with De Morgan transformations
- Rotate and mix bits with key-dependent shifts
- Output modifies the opposite half of the block in Feistel structure

Key Schedule Highlights:
- Master key rotated left by 8 bits per round
- Nonlinear mixing via shifts and XOR
- Round number incorporated for extra variation
- Produces 32-bit round keys for each round

Usage
-----
Requirements:
- Python 3.x

Run the Program:
1. Clone or download the repository.
2. Navigate to the folder containing `DeMorganBlock.py`.
3. Run the script:
   python DeMorganBlock.py
4. Enter a plaintext message.
5. Enter an 8-character key (exactly 8 characters).
6. The program outputs:
   - Ciphertext in hexadecimal
   - Decrypted message

Example:
--------
Enter plaintext message: I love computer security
Enter 8-character key: 88992211

Ciphertext (hex): fd85ca0af041c1d30246c8cc44afec2d49ba828d146331b800453b80b6080a8a
Decrypted message: I love computer security
Encryption & Decryption successful!

Design Justification
--------------------
- Feistel Structure: Simplifies decryption; same process as encryption with reversed round keys
- De Morgan Round Function: Introduces nonlinear transformations for strong confusion and diffusion
- Enhanced Key Schedule: Produces unique round keys per round to improve security
- Lightweight Operations: Bitwise logic, rotations, and XOR keep it efficient and suitable for low-power devices

Applications
------------
- Educational demonstration of block cipher design
- Small-scale secure messaging or IoT communication
- Illustrates effects of round functions, key schedules, and Feistel structures

Strengths
---------
- Symmetric encryption and decryption use the same logic
- Lightweight and efficient for demonstration
- Nonlinear round function ensures strong diffusion and key sensitivity

Limitations
-----------
- Limited to 4 rounds, providing moderate security; not suitable for high-security use
- Custom design is primarily educational; not widely analyzed for attacks
- Fixed 8-character key may limit key space

Repository Contents
-------------------
- DeMorganBlock.py — Python script for encryption and decryption
- README.txt — Documentation and usage instructions

