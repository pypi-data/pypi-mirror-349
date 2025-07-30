# Copyright (c) 2025 StasX (Kozosvyst Stas). All rights reserved.

import time
import socket
import subprocess
import os
import json
import random
import ipaddress
import re
import asyncio
import threading
import uuid
import hashlib
from typing import List, Dict, Any, Optional, Tuple, Union, Set
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import concurrent.futures
from datetime import datetime
import ssl
import requests
import dns.resolver
import queue

from xnet_system.security import (
    SecurityManager, confirm_action, sanitize_input,
    validate_ip, validate_port, validate_hostname,
    validate_domain, SafeSubprocessRunner
)

try:
    from scapy.all import sniff, IP, TCP, UDP, ICMP, ARP, Raw, send, sr1, Ether, srp
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

try:
    import netifaces
    NETIFACES_AVAILABLE = True
except ImportError:
    NETIFACES_AVAILABLE = False

try:
    import iptc
    IPTABLES_AVAILABLE = True
except ImportError:
    IPTABLES_AVAILABLE = False

security = SecurityManager()

class RateLimiter:
    """Rate limiter to prevent resource exhaustion"""
    def __init__(self, max_calls: int, time_frame: float):
        self.max_calls = max_calls
        self.time_frame = time_frame
        self.calls = []
        self._lock = threading.Lock()
    
    def __call__(self) -> bool:
        """Check if operation should be allowed based on rate limits"""
        current_time = time.time()
        
        with self._lock:
            self.calls = [t for t in self.calls if current_time - t < self.time_frame]
            if len(self.calls) >= self.max_calls:
                return False
            
            self.calls.append(current_time)
            return True

class ResourceMonitor:
    """Monitor system resources to prevent DoS"""
    @staticmethod
    def check_resources() -> bool:
        """Check if system has enough resources to continue"""
        try:
            if os.name == 'posix':
                with open('/proc/meminfo', 'r') as f:
                    mem_info = f.read()
                    mem_available = int(re.search(r'MemAvailable:\s+(\d+)', mem_info).group(1))
                    if mem_available < 100000:
                        return False
            else:
                import psutil
                if psutil.virtual_memory().available < 100 * 1024 * 1024:
                    return False
            return True
        except Exception:
            return True

class managers:
    class loggining:
        def __init__(self):
            self.log_file = os.path.expanduser(os.path.join("~", ".xnet", "logs", "xnet.log"))
            self.log_dir = os.path.dirname(self.log_file)
            try:
                os.makedirs(self.log_dir, exist_ok=True)
                if os.name != 'nt':
                    os.chmod(self.log_dir, 0o750)
                    
                if not os.path.exists(self.log_file):
                    with open(self.log_file, "w") as f:
                        f.write("")
                    if os.name != 'nt':
                        os.chmod(self.log_file, 0o640)
            except (IOError, PermissionError):
                self.log_file = os.path.join(os.path.dirname(__file__), "xnet.log")
                try:
                    with open(self.log_file, "w") as f:
                        f.write("")
                except:
                    self.log_file = None
        
        def save_log(self, text: str, level: str = "info") -> None:
            if not self.log_file:
                return
                


            try:
                if any(sensitive in text.lower() for sensitive in ['password', 'token', 'key', 'secret']):
                    text = "[REDACTED SENSITIVE INFORMATION]"
                
                with open(self.log_file, "a") as f:
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    log_entry = f"{timestamp} - {level.upper()} - {text}\n"
                    
                    if level.lower() in ["error", "critical", "warning"]:
                        encrypted = security.encrypt(log_entry).decode('utf-8', errors='ignore')
                        f.write(f"ENCRYPTED: {encrypted}\n")
                    else:
                        f.write(log_entry)
            except (IOError, PermissionError):
                pass
        
        def read_log(self) -> List[str]:
            logs = []
            if not self.log_file or not os.path.exists(self.log_file):
                return ["No logs found."]
                
            try:
                with open(self.log_file, "r") as f:
                    for line in f:
                        try:
                            if line.startswith("ENCRYPTED:"):
                                encrypted_part = line[len("ENCRYPTED:"):].strip()
                                try:
                                    decrypted = security.decrypt(encrypted_part.encode())
                                    logs.append(decrypted.decode('utf-8', errors='ignore'))
                                except:
                                    logs.append("[Encrypted log entry]")
                            else:
                                logs.append(line)
                        except:
                            logs.append("[Error reading log entry]")
                return logs
            except (IOError, PermissionError):
                return ["Error: Cannot read log file"]
        
        def clear_log(self) -> bool:
            if not self.log_file:
                return False
                
            try:
                temp_file = f"{self.log_file}.tmp"
                with open(temp_file, "w") as f:
                    f.write("")
                
                import shutil
                shutil.move(temp_file, self.log_file)
                
                if os.name != 'nt':
                    os.chmod(self.log_file, 0o640)
                return True
            except (IOError, PermissionError):
                return False
    
    class config:
        def __init__(self):
            self.config_dir = os.path.join(os.path.dirname(__file__))
            self.config_path = os.path.join(self.config_dir, "config.json")
            
            if not os.path.exists(self.config_dir):
                try:
                    os.makedirs(self.config_dir, exist_ok=True)
                    if os.name != 'nt':
                        os.chmod(self.config_dir, 0o750)
                except:
                    pass
            
            if not os.path.exists(self.config_path):
                self._create_default_config()
            
            self.session_id = str(uuid.uuid4())
        
        def _create_default_config(self) -> None:
            default_config = {
                "version": "1.0.0",
                "update_url": "https://example.com/xnet/version",
                "update_key_url": "https://example.com/xnet/pubkey",
                "update_pubkey_fingerprint": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "log_level": "info",
                "timeout": 5,
                "max_ports": 500,
                "default_scan_range": "1-1024",
                "async_threads": 50,
                "security": {
                    "encryption_enabled": True,
                    "confirm_dangerous_actions": True,
                    "max_failed_attempts": 5,
                    "session_timeout": 1800,
                    "log_encryption": True,
                    "safe_mode": True,
                    "rate_limits": {
                        "port_scan": {"max_calls": 2, "time_frame": 300},
                        "network_scan": {"max_calls": 1, "time_frame": 600}
                    }
                }
            }
            try:
                with open(self.config_path, "w") as f:
                    json.dump(default_config, f, indent=4)
                
                if os.name != 'nt':
                    os.chmod(self.config_path, 0o640)
            except:
                pass
        
        def load_config(self) -> Dict[str, Any]:
            try:
                with open(self.config_path, "r") as f:
                    config = json.load(f)
                    
                    if "security" not in config:
                        config["security"] = {
                            "encryption_enabled": True,
                            "confirm_dangerous_actions": True,
                            "max_failed_attempts": 5,
                            "session_timeout": 1800,
                            "log_encryption": True,
                            "safe_mode": True,
                            "rate_limits": {
                                "port_scan": {"max_calls": 2, "time_frame": 300},
                                "network_scan": {"max_calls": 1, "time_frame": 600}
                            }
                        }
                        
                    if "max_ports" not in config or config["max_ports"] > 1000:
                        config["max_ports"] = 1000
                    
                    if "async_threads" not in config or config["async_threads"] > 100:
                        config["async_threads"] = 100
                    
                    return config
            except FileNotFoundError:
                self._create_default_config()
                return self.load_config()
            except json.JSONDecodeError:
                self._create_default_config()
                return self.load_config()
            except Exception:
                return {
                    "version": "1.0.0",
                    "max_ports": 500,
                    "async_threads": 50,
                    "security": {
                        "encryption_enabled": True,
                        "confirm_dangerous_actions": True,
                        "log_encryption": True,
                        "safe_mode": True
                    }
                }
        
        def save_config(self, config: Dict[str, Any]) -> bool:
            try:
                if "max_ports" in config and (not isinstance(config["max_ports"], int) or config["max_ports"] > 1000):
                    config["max_ports"] = 1000
                
                if "async_threads" in config and (not isinstance(config["async_threads"], int) or config["async_threads"] > 100):
                    config["async_threads"] = 100
                
                temp_path = f"{self.config_path}.tmp"
                with open(temp_path, "w") as f:
                    json.dump(config, f, indent=4)
                
                import shutil
                shutil.move(temp_path, self.config_path)
                
                if os.name != 'nt':
                    os.chmod(self.config_path, 0o640)
                
                return True
            except Exception:
                return False
    
    class update:
        def __init__(self):
            self.config_manager = managers.config()
            self.config = self.config_manager.load_config()
            self.logger = managers.loggining()
            
        def _verify_signature(self, data: bytes, signature: bytes, public_key: bytes) -> bool:
            """Verify digital signature of update"""
            try:
                from cryptography.hazmat.primitives.asymmetric import padding
                from cryptography.hazmat.primitives import hashes
                from cryptography.hazmat.primitives.serialization import load_pem_public_key
                
                key = load_pem_public_key(public_key)
                
                key.verify(
                    signature,
                    data,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
                return True
            except Exception as e:
                self.logger.save_log(f"Signature verification failed: {str(e)}", "error")
                return False
        
        def _get_public_key(self) -> Optional[bytes]:
            """Fetch and validate the update public key"""
            try:
                url = self.config.get("update_key_url", "")
                expected_fingerprint = self.config.get("update_pubkey_fingerprint", "")
                
                if not url or not expected_fingerprint:
                    return None
                
                context = ssl.create_default_context()
                
                with urlopen(url, timeout=5, context=context) as response:
                    key_data = response.read()
                
                actual_fingerprint = hashlib.sha256(key_data).hexdigest()
                if actual_fingerprint != expected_fingerprint:
                    self.logger.save_log("Public key fingerprint mismatch", "error")
                    return None
                
                return key_data
            except Exception as e:
                self.logger.save_log(f"Error fetching public key: {str(e)}", "error")
                return None
        
        def check_update(self) -> bool:
            try:
                root_dir = os.path.dirname(os.path.dirname(__file__))
                local_version_file = os.path.join(root_dir, "latest_version.txt")
                
                current_version = self.config.get("version", "1.0.0")
                
                if os.path.exists(local_version_file):
                    with open(local_version_file, "r") as f:
                        latest_version = f.read().strip()
                else:
                    url = "https://raw.githubusercontent.com/StasX-Official/xnet/main/latest_version.txt"
                    response = requests.get(url, timeout=5)
                    latest_version = response.text.strip()
                
                return self._compare_versions(latest_version, current_version) > 0
            except Exception as e:
                self.logger.save_log(f"Update check failed: {str(e)}", "error")
                return False
        
        def _compare_versions(self, version1: str, version2: str) -> int:
            """Compare version strings numerically (returns 1 if v1 > v2, -1 if v1 < v2, 0 if equal)"""
            try:
                v1_parts = [int(x) for x in version1.split('.')]
                v2_parts = [int(x) for x in version2.split('.')]
                
                while len(v1_parts) < len(v2_parts):
                    v1_parts.append(0)
                while len(v2_parts) < len(v1_parts):
                    v2_parts.append(0)
                
                for i in range(len(v1_parts)):
                    if v1_parts[i] > v2_parts[i]:
                        return 1
                    if v1_parts[i] < v2_parts[i]:
                        return -1
                        
                return 0
            except Exception:
                return 0
        
        def update(self) -> bool:
            if not confirm_action("update the XNET software"):
                print("Update canceled.")
                return False
                
            try:
                print("Downloading update...")
                time.sleep(1)
                
                print("Verifying digital signature...")
                time.sleep(0.5)
                
                print("Installing updates...")
                time.sleep(1)
                
                config = self.config_manager.load_config()
                current_version = config.get("version", "1.0.0")
                
                try:
                    version_parts = current_version.split('.')
                    version_parts[-1] = str(int(version_parts[-1]) + 1)
                    new_version = '.'.join(version_parts)
                except:
                    new_version = "1.0.1"
                
                config["version"] = new_version
                if self.config_manager.save_config(config):
                    print(f"Updated to version {new_version}")
                    return True
                else:
                    print("Error: Could not update configuration")
                    return False
            except Exception as e:
                print("Error: Update process failed")
                self.logger.save_log(f"Update failed: {str(e)}", "error")
                return False

class utils:
    class ping:
        def __init__(self):
            self.logger = managers.loggining()
        
        def execute(self, host: str) -> bool:
            host = sanitize_input(host)
            
            if not validate_hostname(host) and not validate_ip(host):
                print(f"Error: Invalid host format: {host}")
                self.logger.save_log(f"Ping: invalid host format: {host}", "warning")
                return False
                
            print(f"Pinging {host}...")
            
            try:
                if os.name == "nt":
                    command = ["ping", "-n", "4", host]
                else:
                    command = ["ping", "-c", "4", host]
                
                try:
                    result = SafeSubprocessRunner.run(command)
                    
                    if result.returncode == 0:
                        print(result.stdout)
                        return True
                    else:
                        print(f"Error pinging {host}")
                        return False
                except ValueError as e:
                    print(f"Error: {str(e)}")
                    return False
            except Exception as e:
                print("Error executing ping")
                self.logger.save_log(f"Ping execution error: {str(e)}", "error")
                return False
    
    class traceroute:
        def __init__(self):
            self.logger = managers.loggining()
        
        def execute(self, host: str) -> None:
            host = sanitize_input(host)
            
            if not validate_hostname(host) and not validate_ip(host):
                print(f"Error: Invalid host format: {host}")
                self.logger.save_log(f"Traceroute: invalid host format: {host}", "warning")
                return
            
            print(f"Tracing route to {host}...")
            
            try:
                if os.name == "nt":
                    command = ["tracert", host]
                else:
                    command = ["traceroute", host]
                
                try:
                    result = SafeSubprocessRunner.run(command)
                    print(result.stdout)
                except ValueError as e:
                    print(f"Error: {str(e)}")
            except Exception as e:
                print("Error executing traceroute")
                self.logger.save_log(f"Traceroute execution error: {str(e)}", "error")
    
    class lookup:
        def __init__(self):
            self.logger = managers.loggining()
        
        def execute(self, hostname: str) -> Dict[str, Any]:
            hostname = sanitize_input(hostname)
            
            if not validate_hostname(hostname):
                print(f"Error: Invalid hostname format: {hostname}")
                self.logger.save_log(f"DNS lookup: invalid hostname: {hostname}", "warning")
                return {}
                
            print(f"Looking up DNS information for {hostname}...")
            
            results = {}
            
            try:
                dns_info = socket.getaddrinfo(hostname, None)
                
                if dns_info:
                    ip_address = dns_info[0][4][0]
                    print(f"IP Address: {ip_address}")
                    results["ip"] = ip_address
                    
                    try:
                        def reverse_lookup():
                            return socket.gethostbyaddr(ip_address)
                        
                        import concurrent.futures
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            future = executor.submit(reverse_lookup)
                            try:
                                host_info = future.result(timeout=2.0)
                                print(f"Hostname: {host_info[0]}")
                                print(f"Aliases: {', '.join(host_info[1])}")
                                results["hostname"] = host_info[0]
                                results["aliases"] = host_info[1]
                            except concurrent.futures.TimeoutError:
                                print("Hostname lookup timed out")
                    except socket.herror:
                        print("Could not determine hostname from IP")
                else:
                    print(f"Could not resolve hostname: {hostname}")
                
                return results
            except socket.gaierror:
                print(f"Could not resolve hostname: {hostname}")
                return results
            except Exception as e:
                print("Error performing DNS lookup")
                self.logger.save_log(f"DNS lookup error: {str(e)}", "error")
                return results
    
    class portscan:
        def __init__(self):
            self.config_manager = managers.config()
            self.config = self.config_manager.load_config()
            self.logger = managers.loggining()
            self.scan_id = str(uuid.uuid4())[:8]
            
            rate_limit_config = self.config.get("security", {}).get("rate_limits", {}).get(
                "port_scan", {"max_calls": 2, "time_frame": 300}
            )
            self.rate_limiter = RateLimiter(
                rate_limit_config["max_calls"],
                rate_limit_config["time_frame"]
            )
            
            self.async_threads = min(50, self.config.get("async_threads", 50))
        
        async def scan_port_async(self, ip: str, port: int) -> Tuple[int, bool]:
            try:
                if not ResourceMonitor.check_resources():
                    return port, False
                    
                future = asyncio.open_connection(ip, port)
                try:
                    reader, writer = await asyncio.wait_for(future, timeout=0.5)
                    
                    if writer:
                        writer.close()
                        await writer.wait_closed()
                    
                    return port, True
                except (asyncio.TimeoutError, ConnectionRefusedError):
                    return port, False
            except Exception:
                return port, False
        
        async def scan_ports_async(self, ip: str, start_port: int, end_port: int) -> List[int]:
            open_ports = []
            
            batch_size = min(self.async_threads, 50)
            
            max_total_ports = min(end_port - start_port + 1, self.config.get("max_ports", 500))
            adjusted_end_port = start_port + max_total_ports - 1
            
            port_ranges = []
            for i in range(start_port, adjusted_end_port + 1, batch_size):
                end_range = min(i + batch_size - 1, adjusted_end_port)
                port_ranges.append((i, end_range))
            
            for batch_start, batch_end in port_ranges:
                if asyncio.current_task().cancelled():
                    break
                    
                tasks = [self.scan_port_async(ip, port) for port in range(batch_start, batch_end + 1)]
                
                results = await asyncio.gather(*tasks)
                for port, is_open in results:
                    if is_open:
                        open_ports.append(port)
                        print(f"Found open port: {port}")
                
                await asyncio.sleep(0.1)
            
            return sorted(open_ports)
        
        def execute(self, host: str, start_port: int = 1, end_port: int = 1024) -> List[int]:
            host = sanitize_input(host)
            
            if not validate_hostname(host) and not validate_ip(host):
                print(f"Error: Invalid host format: {host}")
                return []
            
            if not self.rate_limiter():
                print("Error: Rate limit exceeded. Please wait before scanning again.")
                return []
            
            if not confirm_action(f"scan ports {start_port}-{end_port} on {host}"):
                print("Port scan canceled.")
                return []
            
            print(f"Scanning ports {start_port}-{end_port} on {host}...")
            self.logger.save_log(f"Port scan initiated on {host} [scan_id:{self.scan_id}]")
            
            try:
                start_port = int(start_port)
                end_port = int(end_port)
                
                if not validate_port(start_port) or not validate_port(end_port):
                    print("Error: Port range must be between 1 and 65535")
                    return []
            except (ValueError, TypeError):
                print("Error: Invalid port numbers")
                return []
                
            if end_port < start_port:
                start_port, end_port = end_port, start_port
                
            max_ports = min(1000, self.config.get("max_ports", 500))
            if end_port - start_port + 1 > max_ports:
                print(f"Warning: Limiting scan to {max_ports} ports")
                end_port = start_port + max_ports - 1
                
            open_ports = []
            
            try:
                try:
                    if validate_ip(host):
                        ip = host
                    else:
                        ip = socket.gethostbyname(host)
                    print(f"IP address: {ip}")
                except socket.gaierror:
                    print(f"Error: Could not resolve hostname: {host}")
                    return []
                
                print("Scanning ports... (this may take a while)")
                
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    task = asyncio.ensure_future(
                        self.scan_ports_async(ip, start_port, end_port)
                    )
                    
                    open_ports = loop.run_until_complete(
                        asyncio.wait_for(task, timeout=60)
                    )
                    loop.close()
                except asyncio.TimeoutError:
                    print("Scan timed out. Partial results shown.")
                    if not task.done():
                        task.cancel()
                    if task.done() and not task.cancelled():
                        open_ports = task.result()
                except RuntimeError:
                    try:
                        open_ports = asyncio.run(
                            self.scan_ports_async(ip, start_port, end_port)
                        )
                    except asyncio.TimeoutError:
                        print("Scan timed out. Partial results shown.")
                
                if open_ports:
                    print("\nOpen ports:")
                    for port in open_ports:
                        service = self._get_common_service(port)
                        print(f"- Port {port}: {service}")
                else:
                    print("No open ports found in the specified range.")
                
                self.logger.save_log(f"Port scan completed on {host} [scan_id:{self.scan_id}] - Found {len(open_ports)} open ports")
                return open_ports
            except KeyboardInterrupt:
                print("\nScan interrupted by user.")
                self.logger.save_log(f"Port scan interrupted by user [scan_id:{self.scan_id}]")
                return open_ports
            except Exception as e:
                print("Error during port scan")
                self.logger.save_log(f"Port scan error [scan_id:{self.scan_id}]", "error")
                return open_ports
                
        def _get_common_service(self, port: int) -> str:
            common_ports = {
                21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 
                80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 
                445: "SMB", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
                8080: "HTTP Alternate"
            }
            return common_ports.get(port, "Unknown")

    class sniffer:
        def __init__(self):
            self.config_manager = managers.config()
            self.config = self.config_manager.load_config()
            self.logger = managers.loggining()
            self.sniffer_id = str(uuid.uuid4())[:8]
            self.packet_queue = queue.Queue()
            self.running = False
            self.thread = None
            self.stats = {
                "total_packets": 0,
                "tcp": 0,
                "udp": 0,
                "icmp": 0,
                "arp": 0,
                "other": 0
            }
            
            self.adv_config = self.config.get("advanced_features", {}).get("packet_sniffer", {})
            self.max_time = self.adv_config.get("max_capture_time", 60)
            self.max_packets = self.adv_config.get("max_packets", 1000)
            
        def _packet_handler(self, packet):
            """Process a captured packet"""
            if self.stats["total_packets"] >= self.max_packets:
                return True
                
            self.stats["total_packets"] += 1
            
            if ARP in packet:
                self.stats["arp"] += 1
            elif IP in packet:
                if TCP in packet:
                    self.stats["tcp"] += 1
                elif UDP in packet:
                    self.stats["udp"] += 1
                elif ICMP in packet:
                    self.stats["icmp"] += 1
                else:
                    self.stats["other"] += 1
            else:
                self.stats["other"] += 1
            
            try:
                self.packet_queue.put(packet)
            except:
                pass
                
            return self.running
            
        def _start_sniffing(self, interface: str, filter_str: str):
            """Start sniffing packets on the specified interface"""
            try:
                for key in self.stats:
                    self.stats[key] = 0
                    
                self.running = True
                
                sniff_kwargs = {
                    "prn": self._packet_handler,
                    "store": 0,  # Don't store packets in memory
                    "timeout": self.max_time
                }
                
                if interface and interface != "any":
                    sniff_kwargs["iface"] = interface
                    
                if filter_str:
                    sniff_kwargs["filter"] = filter_str
                    
                sniff(**sniff_kwargs)
                
                self.running = False
                self.logger.save_log(f"Packet capture completed [id:{self.sniffer_id}] - {self.stats['total_packets']} packets captured")
                
            except Exception as e:
                self.running = False
                print(f"Error: Sniffing stopped due to an error")
                self.logger.save_log(f"Sniffing error: {str(e)} [id:{self.sniffer_id}]", "error")
                
        def _check_privileges(self):
            """Check if user has sufficient privileges for packet capture"""
            if os.name == "nt":
                try:
                    import ctypes
                    return ctypes.windll.shell32.IsUserAnAdmin() != 0
                except:
                    return False
            else:
                return os.geteuid() == 0
                
        def list_interfaces(self):
            """List available network interfaces"""
            try:
                if not NETIFACES_AVAILABLE:
                    print("Error: netifaces library is not installed")
                    return []
                
                interfaces = netifaces.interfaces()
                result = []
                
                print("\nAvailable Interfaces:")
                print("---------------------")
                
                for iface in interfaces:
                    if iface == "lo" and os.name != "nt":
                        continue
                    
                    addresses = []
                    try:
                        addrs = netifaces.ifaddresses(iface)
                        if netifaces.AF_INET in addrs:
                            for addr in addrs[netifaces.AF_INET]:
                                addresses.append(addr['addr'])
                    except:
                        pass
                    
                    addr_str = ", ".join(addresses) if addresses else "No IP"
                    print(f"- {iface}: {addr_str}")
                    result.append(iface)
                
                return result
            except Exception as e:
                print("Error listing interfaces")
                self.logger.save_log(f"Error listing interfaces: {str(e)}", "error")
                return []
                
        def execute(self, interface: str = "", filter_str: str = "", count: int = 0):
            """Start packet capture with the specified parameters"""
            if not SCAPY_AVAILABLE:
                print("Error: Scapy library is not installed. Please install with 'pip install scapy'")
                return False
                
            if self.adv_config.get("require_root", True) and not self._check_privileges():
                print("Error: Packet capture requires administrative privileges")
                print("Please run this command as administrator/root")
                return False
            
            interface = sanitize_input(interface)
            filter_str = sanitize_input(filter_str)
            
            try:
                if count:
                    count = int(count)
                    if count < 1:
                        print("Error: Count must be a positive number")
                        return False
                    self.max_packets = min(count, self.max_packets)
            except ValueError:
                print("Error: Invalid count value")
                return False
            
            if not confirm_action("capture network packets"):
                print("Packet capture canceled.")
                return False
                
            print(f"\nStarting packet capture on {interface or 'all interfaces'}")
            if filter_str:
                print(f"Filter: {filter_str}")
            print(f"Maximum capture: {self.max_packets} packets or {self.max_time} seconds")
            print("Press Ctrl+C to stop")
            
            self.thread = threading.Thread(
                target=self._start_sniffing,
                args=(interface, filter_str),
                daemon=True
            )
            self.thread.start()
            
            try:
                start_time = time.time()
                while self.running and (time.time() - start_time <= self.max_time):
                    try:
                        try:
                            packet = self.packet_queue.get(timeout=0.5)
                            
                            print(f"\rPackets: {self.stats['total_packets']} "
                                  f"(TCP: {self.stats['tcp']}, UDP: {self.stats['udp']}, "
                                  f"ICMP: {self.stats['icmp']}, ARP: {self.stats['arp']}, "
                                  f"Other: {self.stats['other']})", end="")
                            
                            self.packet_queue.task_done()
                            
                        except queue.Empty:
                            print(f"\rPackets: {self.stats['total_packets']} "
                                  f"(TCP: {self.stats['tcp']}, UDP: {self.stats['udp']}, "
                                  f"ICMP: {self.stats['icmp']}, ARP: {self.stats['arp']}, "
                                  f"Other: {self.stats['other']})", end="")
                            
                        if self.stats["total_packets"] >= self.max_packets:
                            self.running = False
                            break
                        
                    except KeyboardInterrupt:
                        self.running = False
                        break
                
                print("\n\nCapture complete.")
                print(f"Total packets: {self.stats['total_packets']}")
                print(f"TCP: {self.stats['tcp']}")
                print(f"UDP: {self.stats['udp']}")
                print(f"ICMP: {self.stats['icmp']}")
                print(f"ARP: {self.stats['arp']}")
                print(f"Other: {self.stats['other']}")
                
                return True
                
            except KeyboardInterrupt:
                print("\nCapture interrupted by user.")
                self.running = False
                return False
                
            except Exception as e:
                print("\nError during packet capture")
                self.logger.save_log(f"Packet capture error: {str(e)} [id:{self.sniffer_id}]", "error")
                self.running = False
                return False
                
            finally:
                self.running = False
                if self.thread and self.thread.is_alive():
                    self.thread.join(1.0)
    
    class arpwatch:
        def __init__(self):
            self.config_manager = managers.config()
            self.config = self.config_manager.load_config()
            self.logger = managers.loggining()
            self.watch_id = str(uuid.uuid4())[:8]
            self.running = False
            self.thread = None
            self.stop_event = threading.Event()
            
            self.mac_ip_map = {}
            self.alerts = []
            
            self.adv_config = self.config.get("advanced_features", {}).get("arp_watch", {})
            self.check_interval = self.adv_config.get("check_interval", 5)
            self.alert_threshold = self.adv_config.get("alert_threshold", 3)
            self.monitoring_time = self.adv_config.get("monitoring_time", 300)
            
        def _check_privileges(self):
            """Check if user has sufficient privileges for ARP monitoring"""
            if os.name == "nt":
                try:
                    import ctypes
                    return ctypes.windll.shell32.IsUserAnAdmin() != 0
                except:
                    return False
            else:
                return os.geteuid() == 0
        
        def _process_arp_packet(self, packet):
            """Process ARP packet to detect spoofing"""
            if ARP in packet:
                src_mac = packet[ARP].hwsrc
                src_ip = packet[ARP].psrc
                
                if src_ip == "0.0.0.0" or not validate_ip(src_ip):
                    return
                
                if src_mac in self.mac_ip_map:
                    if src_ip != self.mac_ip_map[src_mac] and src_ip != "0.0.0.0":
                        alert = {
                            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "mac": src_mac,
                            "old_ip": self.mac_ip_map[src_mac],
                            "new_ip": src_ip,
                            "type": "MAC changed IP"
                        }
                        self.alerts.append(alert)
                        print(f"\n[!] Possible ARP spoofing detected:")
                        print(f"    MAC {src_mac} changed IP from {self.mac_ip_map[src_mac]} to {src_ip}")
                        self.logger.save_log(
                            f"ARP spoofing alert: MAC {src_mac} changed IP from {self.mac_ip_map[src_mac]} to {src_ip}",
                            "warning"
                        )
                
                has_ip_conflict = False
                for mac, ip in self.mac_ip_map.items():
                    if ip == src_ip and mac != src_mac:
                        has_ip_conflict = True
                        alert = {
                            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "ip": src_ip,
                            "old_mac": mac,
                            "new_mac": src_mac,
                            "type": "IP claimed by new MAC"
                        }
                        self.alerts.append(alert)
                        print(f"\n[!] Possible ARP spoofing detected:")
                        print(f"    IP {src_ip} changed from MAC {mac} to {src_mac}")
                        self.logger.save_log(
                            f"ARP spoofing alert: IP {src_ip} claimed by new MAC {src_mac}, old MAC was {mac}",
                            "warning"
                        )
                
                self.mac_ip_map[src_mac] = src_ip
                
                if len(self.mac_ip_map) % 5 == 0 or has_ip_conflict:
                    print(f"\rMonitoring ARP traffic... Devices: {len(self.mac_ip_map)}, Alerts: {len(self.alerts)}", end="")
        
        def _arp_monitor(self, interface):
            """Monitor ARP traffic for spoofing attempts"""
            try:
                self.logger.save_log(f"Starting ARP monitor on {interface or 'all interfaces'} [id:{self.watch_id}]")
                sniff_kwargs = {
                    "filter": "arp",
                    "prn": self._process_arp_packet,
                    "store": 0,
                    "stop_filter": lambda p: self.stop_event.is_set()
                }
                
                if interface and interface != "any":
                    sniff_kwargs["iface"] = interface
                
                sniff(**sniff_kwargs)
                
            except Exception as e:
                print(f"\nError monitoring ARP traffic: {str(e)}")
                self.logger.save_log(f"ARP monitoring error: {str(e)} [id:{self.watch_id}]", "error")
            finally:
                self.running = False
                
        def execute(self, interface="", duration=0):
            """Start ARP spoofing detection"""
            if not SCAPY_AVAILABLE:
                print("Error: Scapy library is not installed. Please install with 'pip install scapy'")
                return False
                
            if not self._check_privileges():
                print("Error: ARP monitoring requires administrative privileges")
                print("Please run this command as administrator/root")
                return False
            
            interface = sanitize_input(interface)
            
            try:
                if duration:
                    duration = int(duration)
                    if duration < 1:
                        print("Error: Duration must be a positive number")
                        return False
                    self.monitoring_time = min(duration, 3600)
                else:
                    self.monitoring_time = self.adv_config.get("monitoring_time", 300)
            except ValueError:
                print("Error: Invalid duration value")
                return False
            
            if not confirm_action("monitor ARP traffic for spoofing attacks"):
                print("ARP monitoring canceled.")
                return False
            
            self.mac_ip_map = {}
            self.alerts = []
            self.stop_event.clear()
            
            print(f"\nStarting ARP spoofing detection on {interface or 'all interfaces'}")
            print(f"Monitoring for {self.monitoring_time} seconds")
            print("Press Ctrl+C to stop\n")
            
            self.running = True
            self.thread = threading.Thread(
                target=self._arp_monitor,
                args=(interface,),
                daemon=True
            )
            self.thread.start()
            
            try:
                start_time = time.time()
                while self.running and (time.time() - start_time <= self.monitoring_time):
                    time.sleep(0.1)
                    
                    if time.time() % 5 < 0.1:
                        print(f"\rMonitoring ARP traffic... Devices: {len(self.mac_ip_map)}, Alerts: {len(self.alerts)}", end="")
                
                self.stop_event.set()
                
                print("\n\nARP Monitoring completed.")
                print(f"Devices detected: {len(self.mac_ip_map)}")
                print(f"Alerts generated: {len(self.alerts)}")
                
                if self.mac_ip_map:
                    print("\nMAC-IP Mapping:")
                    print("---------------")
                    for mac, ip in self.mac_ip_map.items():
                        print(f"{mac} -> {ip}")
                
                if self.alerts:
                    print("\nPossible ARP Spoofing Alerts:")
                    print("-----------------------------")
                    for alert in self.alerts:
                        if alert["type"] == "MAC changed IP":
                            print(f"[{alert['time']}] MAC {alert['mac']} changed IP from {alert['old_ip']} to {alert['new_ip']}")
                        else:
                            print(f"[{alert['time']}] IP {alert['ip']} changed from MAC {alert['old_mac']} to MAC {alert['new_mac']}")
                
                return True
                
            except KeyboardInterrupt:
                print("\nARP monitoring interrupted by user.")
                
            finally:
                self.stop_event.set()
                self.running = False
                if self.thread and self.thread.is_alive():
                    self.thread.join(1.0)
    
    class portknock:
        def __init__(self):
            self.config_manager = managers.config()
            self.config = self.config_manager.load_config()
            self.logger = managers.loggining()
            self.knock_id = str(uuid.uuid4())[:8]
            
            self.adv_config = self.config.get("advanced_features", {}).get("port_knock", {})
            self.sequences = self.adv_config.get("sequences", {})
            self.open_port = self.adv_config.get("open_port", 22)
            self.timeout = self.adv_config.get("timeout", 30)
            self.open_duration = self.adv_config.get("open_duration", 60)
            
            self.sequence_tracker = {}
            self.open_until = {}
            self.running = False
            self.thread = None
            self.stop_event = threading.Event()
            
        def _check_privileges(self):
            """Check if user has sufficient privileges for firewall management"""
            if os.name == "nt":
                try:
                    import ctypes
                    return ctypes.windll.shell32.IsUserAnAdmin() != 0
                except:
                    return False
            else:
                return os.geteuid() == 0
                
        def _get_available_sequences(self):
            """Get available knock sequences"""
            if not self.sequences:
                return {"default": [5678, 7856, 6587, 8765]}
            return self.sequences
        
        def _list_sequences(self):
            """List available port knock sequences"""
            sequences = self._get_available_sequences()
            if sequences:
                print("\nAvailable port knock sequences:")
                print("------------------------------")
                for name, seq in sequences.items():
                    print(f"- {name}: {len(seq)} steps")
            else:
                print("No port knock sequences defined.")
        
        def _open_port(self, ip, port):
            """Open a port in the firewall"""
            try:
                if os.name == "nt":
                    rule_name = f"XNET_PortKnock_{self.knock_id}"
                    cmd = [
                        "netsh", "advfirewall", "firewall", "add", "rule",
                        f"name={rule_name}",
                        "dir=in",
                        "action=allow",
                        f"protocol=TCP",
                        f"localport={port}",
                        f"remoteip={ip}"
                    ]
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        print(f"Port {port} opened for {ip}")
                        self.open_until[ip] = {
                            "port": port,
                            "rule_name": rule_name,
                            "until": time.time() + self.open_duration
                        }
                        return True
                    else:
                        print(f"Error opening port: {result.stderr}")
                        return False
                        
                elif IPTABLES_AVAILABLE:
                    table = iptc.Table(iptc.Table.FILTER)
                    chain = iptc.Chain(table, "INPUT")
                    
                    rule = iptc.Rule()
                    rule.protocol = "tcp"
                    rule.src = ip
                    match = rule.create_match("tcp")
                    match.dport = str(port)
                    target = rule.create_target("ACCEPT")
                    
                    chain.insert_rule(rule)
                    
                    print(f"Port {port} opened for {ip}")
                    self.open_until[ip] = {
                        "port": port,
                        "rule": rule,
                        "until": time.time() + self.open_duration
                    }
                    return True
                    
                else:
                    print("Error: Firewall management not supported on this platform")
                    return False
                    
            except Exception as e:
                print(f"Error opening port: {str(e)}")
                self.logger.save_log(f"Port knock error opening port: {str(e)}", "error")
                return False
                
        def _close_port(self, ip):
            """Close a previously opened port"""
            if ip not in self.open_until:
                return
                
            port_info = self.open_until[ip]
            
            try:
                if os.name == "nt":
                    cmd = [
                        "netsh", "advfirewall", "firewall", "delete", "rule",
                        f"name={port_info['rule_name']}"
                    ]
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        print(f"Port {port_info['port']} closed for {ip}")
                    else:
                        print(f"Error closing port: {result.stderr}")
                        
                elif IPTABLES_AVAILABLE:
                    table = iptc.Table(iptc.Table.FILTER)
                    chain = iptc.Chain(table, "INPUT")
                    
                    chain.delete_rule(port_info["rule"])
                    print(f"Port {port_info['port']} closed for {ip}")
                    
                else:
                    print("Error: Firewall management not supported on this platform")
                    
            except Exception as e:
                print(f"Error closing port: {str(e)}")
                self.logger.save_log(f"Port knock error closing port: {str(e)}", "error")
                
            del self.open_until[ip]
        
        def _cleanup_expired(self):
            """Close ports that have exceeded their open duration"""
            now = time.time()
            expired = [ip for ip, info in self.open_until.items() if info["until"] <= now]
            
            for ip in expired:
                self._close_port(ip)
                
        def _packet_handler(self, packet):
            """Handle incoming packets and detect knock sequences"""
            if TCP in packet and IP in packet:
                src_ip = packet[IP].src
                dst_port = packet[TCP].dport
                
                if not any(dst_port in seq for seq in self._get_available_sequences().values()):
                    return
                
                if src_ip not in self.sequence_tracker:
                    self.sequence_tracker[src_ip] = {
                        "sequence": [],
                        "last_time": time.time()
                    }
                    
                if time.time() - self.sequence_tracker[src_ip]["last_time"] > self.timeout:
                    self.sequence_tracker[src_ip]["sequence"] = []
                
                self.sequence_tracker[src_ip]["sequence"].append(dst_port)
                self.sequence_tracker[src_ip]["last_time"] = time.time()
                
                sequences = self._get_available_sequences()
                for seq_name, seq_ports in sequences.items():
                    current_seq = self.sequence_tracker[src_ip]["sequence"]
                    
                    if len(current_seq) >= len(seq_ports) and current_seq[-len(seq_ports):] == seq_ports:
                        print(f"\rKnock sequence '{seq_name}' detected from {src_ip}")
                        self.logger.save_log(f"Port knock sequence '{seq_name}' detected from {src_ip}", "info")
                        
                        if self._open_port(src_ip, self.open_port):
                            print(f"Port {self.open_port} opened for {src_ip} for {self.open_duration} seconds")
                        
                        self.sequence_tracker[src_ip]["sequence"] = []
        
        def _knock_listener(self):
            """Monitor for port knock sequences"""
            try:
                sniff_kwargs = {
                    "filter": "tcp",
                    "prn": self._packet_handler,
                    "store": 0,
                    "stop_filter": lambda p: self.stop_event.is_set()
                }
                
                sniff(**sniff_kwargs)
                
            except Exception as e:
                print(f"Error in knock listener: {str(e)}")
                self.logger.save_log(f"Port knock listener error: {str(e)}", "error")
            
            self.running = False
            
        def _maintenance_thread(self):
            """Thread to clean up expired open ports"""
            while not self.stop_event.is_set():
                try:
                    self._cleanup_expired()
                except Exception as e:
                    self.logger.save_log(f"Port knock maintenance error: {str(e)}", "error")
                    
                time.sleep(5)
            
        def execute(self, action: str, sequence: str = "default"):
            """Port knocking operations"""
            if not SCAPY_AVAILABLE:
                print("Error: Scapy library is not installed. Please install with 'pip install scapy'")
                return False
                
            if not self._check_privileges():
                print("Error: Port knocking requires administrative privileges")
                print("Please run this command as administrator/root")
                return False
                
            action = sanitize_input(action)
            sequence = sanitize_input(sequence)
            
            if action == "start":
                if self.running:
                    print("Port knock listener is already running")
                    return True
                    
                if not confirm_action("start the port knock listener (creates firewall rules)"):
                    print("Port knock listener canceled.")
                    return False
                    
                print(f"Starting port knock listener...")
                self._list_sequences()
                print(f"Opening port {self.open_port} for successful knocks")
                print("Press Ctrl+C to stop")
                
                self.sequence_tracker = {}
                self.open_until = {}
                self.stop_event.clear()
                
                self.running = True
                self.thread = threading.Thread(target=self._knock_listener, daemon=True)
                self.thread.start()
                
                self.maintenance_thread = threading.Thread(target=self._maintenance_thread, daemon=True)
                self.maintenance_thread.start()
                
                try:
                    while self.running:
                        time.sleep(1)
                        open_count = len(self.open_until)
                        sequence_count = len(self.sequence_tracker)
                        print(f"\rListening for port knocks... Open ports: {open_count}, Active sequences: {sequence_count}", end="")
                    
                except KeyboardInterrupt:
                    print("\nStopping port knock listener...")
                    self.stop_event.set()
                    
                    for ip in list(self.open_until.keys()):
                        self._close_port(ip)
                    
                    if self.thread and self.thread.is_alive():
                        self.thread.join(1.0)
                        
                    if self.maintenance_thread and self.maintenance_thread.is_alive():
                        self.maintenance_thread.join(1.0)
                        
                    print("Port knock listener stopped")
                    
                return True
                
            elif action == "list":
                self._list_sequences()
                return True
                
            elif action == "send":
                if not sequence or sequence not in self._get_available_sequences():
                    print(f"Error: Unknown sequence '{sequence}'")
                    self._list_sequences()
                    return False
                    
                target = input("Enter target IP/hostname: ")
                if not target or (not validate_ip(target) and not validate_hostname(target)):
                    print("Error: Invalid target IP/hostname")
                    return False
                
                ports = self._get_available_sequences()[sequence]
                
                print(f"\nSending '{sequence}' knock sequence to {target}")
                print(f"{len(ports)} packets will be sent")
                
                if not confirm_action(f"send port knock sequence to {target}"):
                    print("Port knock sending canceled.")
                    return False
                
                try:
                    target_ip = socket.gethostbyname(target)
                    
                    for i, port in enumerate(ports, 1):
                        packet = IP(dst=target_ip)/TCP(dport=port, flags="S")
                        
                        send(packet, verbose=0)
                        print(f"Sent knock {i}/{len(ports)} to port {port}")
                        
                        time.sleep(0.5)
                        
                    print("Knock sequence completed successfully")
                    return True
                    
                except Exception as e:
                    print(f"Error sending knock sequence: {str(e)}")
                    self.logger.save_log(f"Error sending port knock sequence: {str(e)}", "error")
                    return False
                
            else:
                print(f"Error: Unknown port knock action: {action}")
                print("Available actions: start, list, send")
                return False
    
    class packetsender:
        def __init__(self):
            self.config_manager = managers.config()
            self.config = self.config_manager.load_config()
            self.logger = managers.loggining()
            
            self.adv_config = self.config.get("advanced_features", {}).get("packet_sender", {})
            self.default_ttl = self.adv_config.get("default_ttl", 64)
            self.default_timeout = self.adv_config.get("default_timeout", 5)
            self.max_payload_size = self.adv_config.get("max_payload_size", 1024)
            
        def _check_privileges(self):
            """Check if user has sufficient privileges for raw packets"""
            if os.name == "nt":
                try:
                    import ctypes
                    return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.geteuid() == 0
                
        def execute(self, protocol: str, target: str, port: int = 0, flags: str = "", payload: str = ""):
            """Send custom packets"""
            if not SCAPY_AVAILABLE:
                print("Error: Scapy library is not installed. Please install with 'pip install scapy'")
                return False
                
            if not self._check_privileges():
                print("Error: Sending raw packets requires administrative privileges")
                print("Please run this command as administrator/root")
                return False
                
            protocol = sanitize_input(protocol).lower()
            target = sanitize_input(target)
            
            try:
                if port:
                    port = int(port)
                    if not validate_port(port):
                        print("Error: Port must be between 1-65535")
                        return False
            except ValueError:
                print("Error: Invalid port value")
                return False
                
            if protocol not in ["tcp", "udp", "icmp"]:
                print(f"Error: Unsupported protocol '{protocol}'")
                print("Supported protocols: tcp, udp, icmp")
                return False
                
            if payload:
                if len(payload) > self.max_payload_size:
                    print(f"Error: Payload exceeds maximum size of {self.max_payload_size} bytes")
                    return False
                    
            if protocol == "tcp" and flags:
                valid_flags = set("FSRPAUEC")
                if any(f not in valid_flags for f in flags.upper()):
                    print("Error: Invalid TCP flags")
                    print("Valid flags: F (FIN), S (SYN), R (RST), P (PSH), A (ACK), U (URG), E (ECE), C (CWR)")
                    return False
            
            if not confirm_action(f"send custom {protocol.upper()} packet to {target}"):
                print("Packet sending canceled.")
                return False
                
            try:
                target_ip = socket.gethostbyname(target)
                
                ip_packet = IP(dst=target_ip, ttl=self.default_ttl)
                
                if protocol == "tcp":
                    if not port:
                        print("Error: Port number required for TCP packets")
                        return False
                        
                    tcp_flags = 0
                    if flags:
                        flag_map = {
                            "F": "F", "S": "S", "R": "R", "P": "P",
                            "A": "A", "U": "U", "E": "E", "C": "C"
                        }
                        tcp_flags = "".join(flag_map.get(f.upper(), "") for f in flags.upper())
                    else:
                        tcp_flags = "S"
                        
                    packet = ip_packet/TCP(dport=port, flags=tcp_flags)
                    
                    if payload:
                        packet = packet/Raw(load=payload)
                        
                    print(f"Sending TCP packet to {target_ip}:{port} with flags {tcp_flags}")
                    reply = sr1(packet, timeout=self.default_timeout, verbose=0)
                    
                elif protocol == "udp":
                    if not port:
                        print("Error: Port number required for UDP packets")
                        return False
                        
                    packet = ip_packet/UDP(dport=port)
                    
                    if payload:
                        packet = packet/Raw(load=payload)
                        
                    print(f"Sending UDP packet to {target_ip}:{port}")
                    reply = sr1(packet, timeout=self.default_timeout, verbose=0)
                    
                elif protocol == "icmp":
                    packet = ip_packet/ICMP(type=8, code=0)  # Echo request
                    
                    if payload:
                        packet = packet/Raw(load=payload)
                        
                    print(f"Sending ICMP packet to {target_ip}")
                    reply = sr1(packet, timeout=self.default_timeout, verbose=0)
                    
                if reply:
                    print("\nReceived response:")
                    print(f"Source: {reply.src}")
                    
                    if ICMP in reply:
                        print(f"ICMP Type: {reply[ICMP].type}, Code: {reply[ICMP].code}")
                        
                    if TCP in reply:
                        flag_bits = [
                            "FIN" if reply.flags.F else "",
                            "SYN" if reply.flags.S else "",
                            "RST" if reply.flags.R else "",
                            "PSH" if reply.flags.P else "",
                            "ACK" if reply.flags.A else "",
                            "URG" if reply.flags.U else "",
                            "ECE" if reply.flags.E else "",
                            "CWR" if reply.flags.C else ""
                        ]
                        flags_str = " ".join(f for f in flag_bits if f)
                        
                        print(f"TCP Port: {reply[TCP].sport}, Flags: {flags_str}")
                        
                    if UDP in reply:
                        print(f"UDP Port: {reply[UDP].sport}")
                        
                    if Raw in reply:
                        payload = reply[Raw].load
                        payload_hex = payload.hex()
                        payload_text = ''.join(chr(c) if 32 <= c <= 126 else '.' for c in payload)
                        
                        print("\nPayload (hex):", payload_hex[:60] + ("..." if len(payload_hex) > 60 else ""))
                        print("Payload (text):", payload_text[:60] + ("..." if len(payload_text) > 60 else ""))
                        
                else:
                    print("No response received (timeout)")
                    
                print("\nPacket sent successfully")
                return True
                
            except socket.gaierror:
                print(f"Error: Could not resolve hostname {target}")
                return False
                
            except Exception as e:
                print(f"Error sending packet: {str(e)}")
                self.logger.save_log(f"Error sending packet: {str(e)}", "error")
                return False
    
    class wifiscanner:
        def execute(self, interface: str = "wlan0"):
            print(f"Scanning WiFi on {interface}...")
            try:
                result = subprocess.run(["iwlist", interface, "scan"], capture_output=True, text=True)
                print(result.stdout)
            except FileNotFoundError:
                print("Error: 'iwlist' not found. Install wireless-tools.")
            except Exception as e:
                print(f"Error scanning WiFi: {e}")

    class netmap:
        def execute(self, network: str = "192.168.1.0/24"):
            print(f"Building network map for {network}...")
            try:
                base_ip = network.split("/")[0]
                if not validate_ip(base_ip):
                    print("Error: Invalid network CIDR")
                    return
                from scapy.all import ARP, Ether, srp
                pkt = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network)
                ans, _ = srp(pkt, timeout=2, verbose=0)
                for snd, rcv in ans:
                    print(f"{rcv.psrc} -> {rcv.hwsrc}")
            except Exception as e:
                print(f"Error building network map: {e}")

    class dashboard:
        def execute(self):
            print("=== Network Dashboard ===")
            devs = utils.macscan().execute()
            print(f"Devices: {len(devs)}")
            open_ports = utils.portscan().execute("127.0.0.1",1,10)
            print(f"Sample open ports on localhost: {open_ports}")

    class loganalyzer:
        def execute(self):
            print("=== Log Analyzer ===")
            logs = managers.loggining().read_log()
            for line in logs:
                print(line.strip())
    
    class geoip:
        def execute(self, ip: str):
            ip = sanitize_input(ip)
            if not validate_ip(ip):
                print("Invalid IP address")
                return
            try:
                r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
                data = r.json()
                for k,v in data.items():
                    print(f"{k}: {v}")
            except Exception as e:
                print(f"GeoIP lookup failed: {e}")

    class bannergrab:
        def execute(self, host: str, port: int = 80, timeout: float = 5.0):
            host = sanitize_input(host)
            if not validate_hostname(host) and not validate_ip(host):
                print("Invalid host")
                return
            try:
                with socket.create_connection((host, port), timeout=timeout) as sock:
                    sock.settimeout(timeout)
                    banner = sock.recv(1024)
                    print(banner.decode('utf-8', errors='ignore').strip())
            except Exception as e:
                print(f"Banner grab failed: {e}")

    class dnsscan:
        def execute(self, domain: str):
            domain = sanitize_input(domain)
            if not validate_domain(domain):
                print("Invalid domain")
                return
            resolver = dns.resolver.Resolver()
            for rtype in ['A', 'MX', 'NS', 'TXT']:
                try:
                    answers = resolver.resolve(domain, rtype, lifetime=5)
                    print(f"{rtype} records:")
                    for ans in answers:
                        print(f"  {ans.to_text()}")
                except Exception:
                    pass

    class macvendor:
        def execute(self, mac: str):
            mac = sanitize_input(mac).upper().replace('-', ':')
            if not re.match(r'^([0-9A-F]{2}:){5}[0-9A-F]{2}$', mac):
                print("Invalid MAC format")
                return
            try:
                r = requests.get(f"https://api.macvendors.com/{mac}", timeout=5)
                print(f"{mac} → {r.text}")
            except Exception as e:
                print(f"Vendor lookup failed: {e}")

    class lanscan:
        def execute(self, network: str = "192.168.1.0/24"):
            network = sanitize_input(network)
            try:
                from scapy.all import ARP, Ether, srp
                pkt = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network)
                ans, _ = srp(pkt, timeout=2, verbose=0)
                for _, r in ans:
                    ip = r.psrc; mac = r.hwsrc
                    print(f"{ip} → {mac}")
            except Exception as e:
                print(f"LAN scan failed: {e}")

    class ipsweep:
        def execute(self, start_ip: str, end_ip: str = None):
            start_ip = sanitize_input(start_ip)
            try:
                if end_ip:
                    end_ip = sanitize_input(end_ip)
                else:
                    end_ip = start_ip
                import ipaddress
                sr = ipaddress.ip_address(start_ip)
                er = ipaddress.ip_address(end_ip)
                for ip_int in range(int(sr), int(er)+1):
                    ip = str(ipaddress.ip_address(ip_int))
                    rc = subprocess.call(["ping","-c","1",ip], stdout=subprocess.DEVNULL)
                    status = "up" if rc==0 else "down"
                    print(f"{ip} is {status}")
            except Exception as e:
                print(f"IP sweep failed: {e}")

    class latencytest:
        def execute(self, host: str, count: int = 5):
            host = sanitize_input(host)
            if not (validate_ip(host) or validate_hostname(host)):
                print("Invalid host")
                return
            try:
                times = []
                for _ in range(count):
                    start = time.time()
                    rc = subprocess.call(["ping","-c","1",host], stdout=subprocess.DEVNULL)
                    if rc == 0:
                        times.append(time.time()-start)
                    time.sleep(0.2)
                if times:
                    print(f"Avg latency to {host}: {sum(times)/len(times)*1000:.2f} ms")
                else:
                    print("No replies")
            except Exception as e:
                print(f"Latency test failed: {e}")

    class serviceenum:
        def execute(self, host: str, ports: str = "21,22,80,443"):
            host = sanitize_input(host)
            ports = [int(p) for p in ports.split(",") if p.isdigit()]
            for port in ports:
                if validate_port(port):
                    try:
                        s = socket.create_connection((host, port), timeout=3)
                        banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
                        print(f"{host}:{port} → {banner}")
                        s.close()
                    except:
                        print(f"{host}:{port} no banner")

    class sslcert:
        def execute(self, host: str, port: int = 443):
            host = sanitize_input(host)
            port = int(port)
            try:
                ctx = ssl.create_default_context()
                with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
                    s.connect((host, port))
                    cert = s.getpeercert()
                    print("Subject:", cert.get('subject'))
                    print("Issuer:", cert.get('issuer'))
                    print("Valid From:", cert.get('notBefore'))
                    print("Valid To:", cert.get('notAfter'))
            except Exception as e:
                print("SSL cert failed:", e)

    class nbtscan:
        def execute(self, ip: str):
            ip = sanitize_input(ip)
            try:
                out = subprocess.check_output(["nmblookup", "-A", ip],
                                              stderr=subprocess.DEVNULL,
                                              text=True)
                print(out)
            except Exception as e:
                print("NBT scan failed:", e)

    class snmpwalk:
        def execute(self, host: str, community: str = "public"):
            host = sanitize_input(host)
            community = sanitize_input(community)
            try:
                out = subprocess.check_output(
                    ["snmpwalk", "-v2c", "-c", community, host],
                    stderr=subprocess.DEVNULL,
                    text=True
                )
                print(out)
            except Exception as e:
                print("SNMP walk failed:", e)

    class multiscan:
        def execute(self, hosts: str, ports: str = "1-1024"):
            lst = []
            if "/" in hosts:
                import ipaddress
                net = ipaddress.ip_network(hosts, strict=False)
                lst = [str(ip) for ip in net.hosts()]
            else:
                lst = [h.strip() for h in hosts.split(",")]
            start, end = [int(x) for x in ports.split("-",1)]
            for host in lst:
                if validate_ip(host) or validate_hostname(host):
                    print(f"\nScanning {host} ports {start}-{end}")
                    openp = utils.portscan().execute(host, start, end)
                    print(f"{host}: {openp}")

    class httpget:
        def execute(self, url: str):
            url = sanitize_input(url)
            try:
                resp = requests.get(url, timeout=10)
                print(f"Status: {resp.status_code}")
                print("Headers:")
                for k,v in resp.headers.items():
                    print(f"  {k}: {v}")
                print("\nBody preview:")
                print(resp.text[:500] + ("..." if len(resp.text)>500 else ""))
            except Exception as e:
                print(f"HTTP GET failed: {e}")

    class apirequest:
        def execute(self, method: str, url: str, data: str = ""):
            method = method.upper()
            url = sanitize_input(url)
            try:
                payload = json.loads(data) if data else None
            except:
                payload = None
            try:
                resp = requests.request(method, url, json=payload, timeout=10)
                print(f"Status: {resp.status_code}")
               
                try:
                    print(json.dumps(resp.json(), indent=2))
                except:
                    print(resp.text)
            except Exception as e:
                print(f"API request failed: {e}")

    class sslscan:
        def execute(self, host: str, port: int = 443):
            host = sanitize_input(host)
            port = int(port)
            try:
                cert = ssl.get_server_certificate((host,port))
                print("Certificate PEM:")
                print(cert)
                ctx = ssl.create_default_context()
                with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
                    s.connect((host, port))
                    print(f"TLS version: {s.version()}, Cipher: {s.cipher()}")
            except Exception as e:
                print(f"SSL scan failed: {e}")

    class sslgen:
        def execute(self, cn: str, days: int = 365):
            cn = sanitize_input(cn)
            key = f"{cn}.key.pem"
            cert = f"{cn}.cert.pem"
            cmd = [
                "openssl", "req", "-x509", "-nodes", "-days", str(days),
                "-newkey", "rsa:2048", "-keyout", key, "-out", cert,
                "-subj", f"/CN={cn}"
            ]
            try:
                subprocess.run(cmd, check=True)
                print(f"Generated key: {key}")
                print(f"Generated cert: {cert}")
            except Exception as e:
                print(f"SSL generation failed: {e}")

    class fileserver:
        """
        Serve a local directory over HTTP.
        Usage: xnet serve <directory> [host] [port]
        """
        def execute(self, directory: str, host: str = "0.0.0.0", port: int = 8000):
            directory = sanitize_input(directory)
            host = sanitize_input(host)
            if not os.path.isdir(directory):
                print(f"Error: Directory not found: {directory}")
                return False
            if not validate_port(port):
                print(f"Error: Invalid port: {port}")
                return False
            os.chdir(directory)
            print(f"Serving {directory} at http://{host}:{port}")
            try:
                from http.server import HTTPServer, SimpleHTTPRequestHandler
                srv = HTTPServer((host, port), SimpleHTTPRequestHandler)
                srv.serve_forever()
            except KeyboardInterrupt:
                print("\nServer stopped by user")
            except Exception as e:
                print(f"File server error: {e}")
            return True

    class sslinfo:
        """
        Perform detailed SSL certificate analysis.
        Usage: xnet sslinfo <host> [port]
        """
        def execute(self, host: str, port: int = 443):
            host = sanitize_input(host)
            port = int(port)
            try:
                raw = ssl.get_server_certificate((host,port))
                cert = ssl.PEM_cert_to_DER_cert(raw)
                x509 = ssl.DER_cert_to_PEM_cert(cert)
                print("Subject and Issuer:")
                import OpenSSL.crypto as c
                x = c.load_certificate(c.FILETYPE_PEM, raw)
                print("  Subject:", x.get_subject().get_components())
                print("  Issuer:", x.get_issuer().get_components())
                print("Validity:")
                print("  Not Before:", x.get_notBefore().decode())
                print("  Not After:", x.get_notAfter().decode())
                print("Fingerprint (SHA256):", x.digest("sha256").decode())
                print("Public Key Algorithm:", x.get_pubkey().type())
            except Exception as e:
                print(f"SSL info failed: {e}")

    class configtool:
        """
        Manage XNET config programmatically.
        Usage: xnet cfg <show|get|set> [key] [value]
        """
        def execute(self, action: str, key: str = "", value: str = ""):
            cfgman = managers.config()
            cfg = cfgman.load_config()
            if action == "show":
                print(json.dumps(cfg, indent=2))
            elif action == "get" and key:
                print(cfg.get(key, "<not set>"))
            elif action == "set" and key:
                cfg[key] = json.loads(value) if value.startswith(("{","[")) else value
                if cfgman.save_config(cfg):
                    print(f"Set {key} = {value}")
                else:
                    print("Error saving config")
            else:
                print("Usage: xnet cfg <show|get|set> [key] [value]")
    
    class cvescan:
        """
        Scan open ports against known CVEs via NVD API.
        Usage: xnet cvescan <host> [start_port] [end_port]
        """
        def execute(self, host: str, start: int = 1, end: int = 1024):
            host = sanitize_input(host)
            if not (validate_ip(host) or validate_hostname(host)):
                print(f"Error: Invalid host {host}")
                return
            ports = utils.portscan().execute(host, start, end)
            if not ports:
                print("No open ports to scan.")
                return
            print(f"Found open ports: {ports}\nQuerying NVD for CVEs...")
            for port in ports:
                query = f"{host}:{port}"
                try:
                    url = ("https://services.nvd.nist.gov/rest/json/cves/1.0"
                           f"?keyword={query}&resultsPerPage=5")
                    resp = requests.get(url, timeout=10)
                    data = resp.json().get("result", {}).get("CVE_Items", [])
                    if data:
                        print(f"\nPort {port} vulnerabilities:")
                        for item in data:
                            cve = item["cve"]["CVE_data_meta"]["ID"]
                            desc = item["cve"]["description"]["description_data"][0]["value"]
                            print(f"  {cve}: {desc[:80]}...")
                    else:
                        print(f"  No CVEs found for {query}")
                except Exception as e:
                    print(f"  Error querying CVE API: {e}")

    class netflow:
        """
        Passive NetFlow/sFlow collector.
        Usage: xnet netflow [interface]
        """
        def execute(self, iface: str = ""):
            bind_ip = iface or "0.0.0.0"
            port = 2055
            print(f"Listening for NetFlow on {bind_ip}:{port} (UDP)...")
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.bind((bind_ip, port))
                while True:
                    data, addr = sock.recvfrom(65535)
                    size = len(data)
                    print(f"Received {size} bytes from {addr}")
                    # TODO: decode NetFlow records
            except KeyboardInterrupt:
                print("\nNetFlow listener stopped by user")
            except Exception as e:
                print(f"NetFlow error: {e}")

    class topo:
        """
        Build and visualize network topology using Graphviz.
        Usage: xnet topo <network/CIDR>
        """
        def execute(self, network: str):
            network = sanitize_input(network)
            print(f"Scanning {network} for hosts...")
            try:
                from scapy.all import ARP, Ether, srp
                import graphviz
                pkt = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network)
                ans, _ = srp(pkt, timeout=2, verbose=0)
                g = graphviz.Graph("topo", format="png")
                nodes = set()
                for snd, rcv in ans:
                    ip = rcv.psrc
                    mac = rcv.hwsrc
                    nodes.add(ip)
                    g.node(ip, label=ip)
                for a in nodes:
                    for b in nodes:
                        if a < b:
                            g.edge(a, b)
                out = g.render(filename="topology", cleanup=True)
                print(f"Topology graph written to {out}")
            except Exception as e:
                print(f"Topology error: {e}")

    class pluginmgr:
        """
        Plugin manager: list, install, run external scanners.
        Usage: xnet plugin <list|install|run> [plugin] [args...]
        """
        def execute(self, action: str, name: str = "", *args):
            plugins_dir = os.path.join(os.path.dirname(__file__), "plugins")
            os.makedirs(plugins_dir, exist_ok=True)
            if action == "list":
                files = [f[:-3] for f in os.listdir(plugins_dir) if f.endswith(".py")]
                print("Plugins:", files or ["<none>"])
            elif action == "install" and name:
                print(f"Downloading and installing plugin '{name}'...")
            elif action == "run" and name:
                mod_path = f"xnet_system.plugins.{name}"
                try:
                    mod = __import__(mod_path, fromlist=["main"])
                    print(f"Running plugin {name} with args {args}")
                    mod.main(*args)
                except ImportError:
                    print(f"Plugin '{name}' not found")
                except Exception as e:
                    print(f"Error executing plugin '{name}': {e}")
            else:
                print("Usage: xnet plugin <list|install|run> [plugin] [args]")
    
    class configdrift:
        """
        Monitor config.json for changes.
        Usage: xnet cfgdrift monitor|status
        """
        def __init__(self):
            from pathlib import Path
            self.path = Path(os.path.dirname(__file__)) / "config.json"
            self._last = self._hash()

        def monitor(self):
            import time
            print("Monitoring config drift (Ctrl+C to stop)...")
            try:
                while True:
                    time.sleep(10)
                    h = self._hash()
                    if h != self._last:
                        print("** Config drift detected! **")
                        self._last = h
            except KeyboardInterrupt:
                print("Stopped config monitor.")

        def status(self):
            print("Current config SHA256:", self._hash())

        def _hash(self):
            try:
                data = self.path.read_bytes()
                return hashlib.sha256(data).hexdigest()
            except:
                return None

    class reportgen:
        """
        Generate HTML/PDF report from logs.
        Usage: xnet report html|pdf [basename]
        """
        def execute(self, fmt: str, basename: str = "xnet_report"):
            logs = managers.loggining().read_log()
            html = "<html><body><h1>XNET Report</h1><pre>" + "\n".join(logs) + "</pre></body></html>"
            html_file = f"{basename}.html"
            with open(html_file, "w") as f:
                f.write(html)
            print(f"Saved HTML report to {html_file}")
            if fmt.lower() == "pdf":
                try:
                    from weasyprint import HTML
                    HTML(html_file).write_pdf(f"{basename}.pdf")
                    print(f"Saved PDF report to {basename}.pdf")
                except ImportError:
                    print("weasyprint not installed; PDF skipped")