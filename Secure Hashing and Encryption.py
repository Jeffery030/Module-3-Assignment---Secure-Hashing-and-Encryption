import hashlib
import sys
from pathlib import Path
from typing import Tuple

# --- Utilities ---
def sha256_str(s: str) -> str:
    """Return the SHA256 hash of a string."""
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def ensure_dir(path: Path):
    """Ensure a directory exists."""
    if not path.exists():
        path.mkdir(parents=True)
        print(f"Created directory: {path}")

# --- User Database ---
USERS = {
    "admin": {"password": sha256_str("adminpass"), "role": "admin"},
    "user": {"password": sha256_str("userpass"), "role": "user"}
}

# --- Login ---
def login() -> Tuple[str, str]:
    """Prompt for username and password, return role if valid."""
    username = input("Username: ")
    password = input("Password: ")  # <-- visible input
    if username in USERS and sha256_str(password) == USERS[username]["password"]:
        print("Login successful")
        return username, USERS[username]["role"]
    else:
        print("Invalid credentials")
        sys.exit(1)

# --- Crypto Tools ---
def make_hash():
    text = input("Enter text to hash (leave empty to hash a file): ")
    if text.strip() != "":
        h = hashlib.sha256(text.encode()).hexdigest()
        print("SHA-256:", h)
    else:
        filename = input("Enter file name: ")
        try:
            with open(filename, "rb") as f:
                data = f.read()
                h = hashlib.sha256(data).hexdigest()
            print("SHA-256:", h)
        except FileNotFoundError:
            print("File not found.")

def caesar_cipher():
    text = input("Enter text: ")
    shift = int(input("Enter shift number: "))
    mode = input("Encrypt (e) or Decrypt (d)? ")

    result = ""
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            if mode.lower() == "e":
                result += chr((ord(ch) - base + shift) % 26 + base)
            else:
                result += chr((ord(ch) - base - shift) % 26 + base)
        else:
            result += ch
    print("Result:", result)

# --- Simulated Digital Signature ---
SECRET_KEY = "mysecretkey"  # pretend private key

def digital_signature():
    choice = input("Sign (s) or Verify (v)? ")
    if choice.lower() == "s":
        message = input("Enter message to sign: ")
        sig = hashlib.sha256((message + SECRET_KEY).encode()).hexdigest()
        print("Message:", message)
        print("Signature:", sig)
    else:
        message = input("Enter message to verify: ")
        given_sig = input("Enter signature: ")
        sig = hashlib.sha256((message + SECRET_KEY).encode()).hexdigest()
        if sig == given_sig:
            print("Signature is VALID")
        else:
            print("Signature is NOT valid")

# --- Main Program ---
if __name__ == "__main__":
    username, role = login()
    print(f"Welcome, {username}! Role: {role}")

    # create per-user directory
    data_dir = Path(f"./data/{username}")
    ensure_dir(data_dir)

    while True:
        print("\n--- Crypto Toolkit ---")
        print("1. SHA-256 Hash")
        print("2. Caesar Cipher")
        if role == "admin":
            print("3. Digital Signature (Simulated)")
        print("4. Quit")

        choice = input("Choose: ")

        if choice == "1":
            make_hash()
        elif choice == "2":
            caesar_cipher()
        elif choice == "3" and role == "admin":
            digital_signature()
        elif choice == "4":
            break
        else:
            print("Invalid choice or not allowed for your role.")
