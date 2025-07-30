# Copyright (c) 2024 StasX (Kozosvyst Stas). All rights reserved.

import os
import base64
import re
import secrets
import shutil
import ipaddress
import socket
import subprocess
from typing import Dict, Any, List, Optional, Union, Tuple, Set
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hashlib
import hmac

class SecurityManager:
    def __init__(self):
        self._key_dir = os.path.join(os.path.dirname(__file__), ".security")
        self._key_file = os.path.join(self._key_dir, ".key")
        self._salt_file = os.path.join(self._key_dir, ".salt")
        self._master_key = None
        self._initialize_security()
    
    def _initialize_security(self) -> None:
        try:
            os.makedirs(self._key_dir, exist_ok=True)
            os.chmod(self._key_dir, 0o700)
            
            if not os.path.exists(self._key_file) or not os.path.exists(self._salt_file):
                self._generate_new_key()
            else:
                self._load_key()
        except Exception as e:
            self._master_key = Fernet.generate_key()
    
    def _generate_new_key(self) -> None:
        try:
            salt = secrets.token_bytes(16)
            password = secrets.token_bytes(32)
            
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password))
            
            with open(self._salt_file, "wb") as f:
                f.write(salt)
            os.chmod(self._salt_file, 0o600)
            
            with open(self._key_file, "wb") as f:
                f.write(key)
            os.chmod(self._key_file, 0o600)
            
            self._master_key = key
        except Exception:
            self._master_key = Fernet.generate_key()
    
    def _load_key(self) -> None:
        try:
            if not self._verify_file_permissions():
                self._generate_new_key()
                return
                
            with open(self._key_file, "rb") as f:
                self._master_key = f.read()
                
            try:
                Fernet(self._master_key)
            except Exception:
                self._generate_new_key()
        except Exception:
            self._master_key = Fernet.generate_key()
    
    def _verify_file_permissions(self) -> bool:
        try:
            if os.name != 'nt':
                key_stat = os.stat(self._key_file)
                salt_stat = os.stat(self._salt_file)
                dir_stat = os.stat(self._key_dir)
                
                if key_stat.st_mode & 0o077 or salt_stat.st_mode & 0o077 or dir_stat.st_mode & 0o077:
                    return False
            return True
        except Exception:
            return False
    
    def encrypt(self, data: Union[str, bytes]) -> bytes:
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            fernet = Fernet(self._master_key)
            return fernet.encrypt(data)
        except Exception:
            return b''
    
    def decrypt(self, data: bytes) -> bytes:
        try:
            fernet = Fernet(self._master_key)
            return fernet.decrypt(data)
        except InvalidToken:
            return b'[Encrypted data - decryption failed]'
        except Exception:
            return b'[Error: Could not decrypt data]'
    
    def secure_hash(self, data: str) -> str:
        try:
            h = hmac.new(self._master_key, data.encode(), hashlib.sha256)
            return h.hexdigest()
        except Exception:
            return hashlib.sha256(data.encode()).hexdigest()

def confirm_action(action_description: str) -> bool:
    response = input(f"\nWARNING: You are about to {action_description}.\n"
                    "This action may have security implications.\n"
                    "Type 'YES' (all caps) to confirm: ").strip()
    return response == 'YES'

def sanitize_input(input_str: str) -> str:
    if not input_str:
        return ""
        
    allowed_pattern = re.compile(r'^[a-zA-Z0-9_\-\.:/]+$')
    if not allowed_pattern.match(input_str):
        return re.sub(r'[^a-zA-Z0-9_\-\.:/]', '', input_str)
    
    return input_str

def validate_ip(ip: str) -> bool:
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def validate_port(port: Union[int, str]) -> bool:
    try:
        port_num = int(port)
        return 1 <= port_num <= 65535
    except (ValueError, TypeError):
        return False

def validate_hostname(hostname: str) -> bool:
    if not hostname or len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1]
    allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

def validate_domain(domain: str) -> bool:
    domain_pattern = re.compile(
        r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    )
    return bool(domain_pattern.match(domain))

class SafeSubprocessRunner:
    ALLOWED_COMMANDS = {
        'ping': {
            'params': ['-c', '-n', '-w', '-t'],
            'validate': lambda args: len(args) > 1 and (validate_ip(args[-1]) or validate_hostname(args[-1]))
        },
        'tracert': {
            'params': ['-d', '-h', '-w', '-R'],
            'validate': lambda args: len(args) > 1 and (validate_ip(args[-1]) or validate_hostname(args[-1]))
        },
        'traceroute': {
            'params': ['-m', '-n', '-p', '-w', '-q'],
            'validate': lambda args: len(args) > 1 and (validate_ip(args[-1]) or validate_hostname(args[-1]))
        },
        'whois': {
            'params': [],
            'validate': lambda args: len(args) > 1 and validate_domain(args[1])
        },
        'arp': {
            'params': ['-a', '-v', '-n'],
            'validate': lambda args: True
        }
    }
    
    @classmethod
    def run(cls, command: List[str]) -> subprocess.CompletedProcess:
        if not command:
            raise ValueError("No command specified")
            
        base_cmd = os.path.basename(command[0])
        
        if base_cmd not in cls.ALLOWED_COMMANDS:
            raise ValueError(f"Command not allowed: {base_cmd}")
        
        cmd_rules = cls.ALLOWED_COMMANDS[base_cmd]
        
        for param in command[1:-1]:
            if param.startswith('-') and param not in cmd_rules['params']:
                raise ValueError(f"Parameter not allowed: {param}")
        
        if not cmd_rules['validate'](command):
            raise ValueError(f"Invalid command parameters: {' '.join(command)}")
        
        return subprocess.run(command, capture_output=True, text=True)
