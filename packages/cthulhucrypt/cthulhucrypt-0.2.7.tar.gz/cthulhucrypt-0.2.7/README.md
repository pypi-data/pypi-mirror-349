# CthulhuCrypt 

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](https://opensource.org/licenses/MIT)

A Python package featuring **multi-layered, non-linear encryption** combining:
- Bitwise XOR with golden ratio constants
- Dynamic substitution tables  
- Chaotic math (primes, Collatz conjecture, trig functions)
- Recursive encryption pipelines

# Features
**Brute-force resistant:** 10+ transformation layers

**Position-dependent ops:** Identical chars → different outputs

**Zero dependencies:** Pure Python (math only)

**CLI support:** Encrypt/hash text or files from terminal

# Quick Start

`pip install cthulhucrypt`

```python
from cthulhucrypt import ultra_encrypt

encrypted = ultra_encrypt("hello", iterations=7)
print(encrypted)  # Output: Ý°FtÔÖr&¥[8ª...
```

# CLI Usage

## See all commands
`cthulhucrypt --help`

## Encrypt or hash a string
```
cthulhucrypt encrypt "hello world"
cthulhucrypt medhash "hello world"
cthulhucrypt highhash "hello world" --iterations 10
cthulhucrypt hash2 "hello world" --iterations 10
cthulhucrypt hash2-high "hello world" --iterations 10
```

## Encrypt or hash a file
```
cthulhucrypt encrypt --file input.txt --output encrypted.txt
cthulhucrypt medhash --file input.txt --output hash.txt
cthulhucrypt highhash --file input.txt --iterations 10 --output hash.txt
cthulhucrypt hash2 --file input.txt --iterations 10 --output hash.txt
cthulhucrypt hash2-high --file input.txt --iterations 10 --output hash.txt
```

## Decrypt a file or string
```
# If you have the output in the form ENCRYPTED;TABLE_IDX
cthulhucrypt decrypt "a1b2c3d4;5" --output decrypted.txt
# Or, if you have the encrypted text and table index separately
cthulhucrypt decrypt "a1b2c3d4" 5 --output decrypted.txt
# Or, from a file
cthulhucrypt decrypt --file encrypted.txt 5 --output decrypted.txt
```

# Algorithm Breakdown

## Character Pairing:
`('h','e') → 104*101 = 10504 → [1,0,5,0,4]`

## Dynamic Substitution:
9 rotating substitution tables selected via `sqrt(ascii_sum)*π + log(len)`

## Bitwise Chaos:
`((char ^ position ^ 1618) << (i%3)) & 0xFF`

## Math Destruction:
Collatz conjecture + prime-modulated trig functions

# Warning
**Not for passwords:** No salting/key stretching