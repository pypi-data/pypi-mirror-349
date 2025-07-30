# Copyright (c) 2025 StasX (Kozosvyst Stas). All rights reserved.

import sys
import os
import time
import re
from typing import List, Dict, Any, Optional
from xnet_system.tools import managers, utils
from xnet_system.security import (
    sanitize_input, confirm_action, validate_ip, validate_port,
    validate_hostname, validate_domain
)

class XNET:
    def __init__(self, command: str, args: Optional[List[str]] = None):
        self.command = command
        self.args = args if args else []
        self.logger = managers.loggining()
        self.config_manager = managers.config()
        self.execution_start_time = time.time()
        self.session_id = os.urandom(8).hex()
        
        try:
            self.config = self.config_manager.load_config()
            self.logger.save_log(f"Session {self.session_id} started with command: {command}")
        except Exception as e:
            self.logger.save_log(f"Failed to load configuration: {str(e)}", "error")
            self.config = {}
            
    def execute(self) -> None:
        try:
            self.args = [sanitize_input(arg) for arg in self.args]
            
            session_timeout = self.config.get("security", {}).get("session_timeout", 1800)
            if time.time() - self.execution_start_time > session_timeout:
                print("Error: Session timeout exceeded")
                self.logger.save_log(f"Session {self.session_id} timeout", "warning")
                return
            
            if self.command == "help":
                self._show_help()
                return
                
            elif self.command == "ping":
                self._validate_args(1, "Usage: xnet ping <hostname/IP>")
                if not validate_ip(self.args[0]) and not validate_hostname(self.args[0]):
                    print(f"Error: Invalid hostname or IP format")
                    return
                utils.ping().execute(self.args[0])
                
            elif self.command == "traceroute":
                self._validate_args(1, "Usage: xnet traceroute <hostname/IP>")
                if not validate_ip(self.args[0]) and not validate_hostname(self.args[0]):
                    print(f"Error: Invalid hostname or IP format")
                    return
                utils.traceroute().execute(self.args[0])
                
            elif self.command == "lookup":
                self._validate_args(1, "Usage: xnet lookup <hostname>")
                if not validate_hostname(self.args[0]):
                    print(f"Error: Invalid hostname format")
                    return
                utils.lookup().execute(self.args[0])
                
            elif self.command == "portscan":
                self._validate_args(1, "Usage: xnet portscan <hostname/IP> [start_port] [end_port]")
                
                if not validate_ip(self.args[0]) and not validate_hostname(self.args[0]):
                    print("Error: Invalid host format")
                    return
                    
                try:
                    if len(self.args) > 1:
                        start_port = int(self.args[1])
                        if not validate_port(start_port):
                            print("Error: Start port must be between 1-65535")
                            return
                    else:
                        start_port = 1
                        
                    if len(self.args) > 2:
                        end_port = int(self.args[2])
                        if not validate_port(end_port):
                            print("Error: End port must be between 1-65535")
                            return
                    else:
                        end_port = 1024
                except ValueError:
                    print("Error: Ports must be valid integers")
                    return
                
                utils.portscan().execute(self.args[0], start_port, end_port)
                
            elif self.command == "whois":
                self._validate_args(1, "Usage: xnet whois <domain>")
                if not validate_domain(self.args[0]):
                    print("Error: Invalid domain format")
                    return
                utils.dnsscan().execute(self.args[0])

            elif self.command == "ipgeo":
                self._validate_args(1, "Usage: xnet ipgeo <IP>")
                if not validate_ip(self.args[0]):
                    print("Error: Invalid IP address format")
                    return
                utils.geoip().execute(self.args[0])

            elif self.command == "macscan":
                self._validate_args(0, "Usage: xnet macscan [network]")
                network = self.args[0] if self.args else "192.168.1.0/24"
                utils.lanscan().execute(network)

            elif self.command == "log":
                if not self.args:
                    print("Available log commands: view, clear")
                    return
                    
                if self.args[0] == "view":
                    logs = self.logger.read_log()
                    for log in logs:
                        if isinstance(log, bytes):
                            continue
                        if isinstance(log, str):
                            printable_log = ''.join(c if c.isprintable() or c in '\n\r\t' else ' ' for c in log)
                            print(printable_log.strip())
                            
                elif self.args[0] == "clear":
                    if confirm_action("clear all logs"):
                        if self.logger.clear_log():
                            print("Logs cleared successfully")
                        else:
                            print("Error: Failed to clear logs")
                    else:
                        print("Log clearing canceled.")
                else:
                    print(f"Error: Unknown log command: {self.args[0]}")
                    
            elif self.command == "update":
                update_manager = managers.update()
                if update_manager.check_update():
                    print("Update available. Installing...")
                    update_manager.update()
                    print("Update completed successfully.")
                else:
                    print("No updates available.")
                    
            elif self.command == "sniff":
                interface = self.args[0] if len(self.args)>0 else ""
                flt = self.args[1] if len(self.args)>1 else ""
                cnt = self.args[2] if len(self.args)>2 else 0
                utils.sniffer().execute(interface, flt, cnt)

            elif self.command == "interfaces":
                utils.sniffer().list_interfaces()

            elif self.command == "arpwatch":
                interface = self.args[0] if len(self.args)>0 else ""
                dur = self.args[1] if len(self.args)>1 else 0
                utils.arpwatch().execute(interface, dur)

            elif self.command == "knock":
                action = self.args[0]
                seq = self.args[1] if len(self.args)>1 else "default"
                utils.portknock().execute(action, seq)

            elif self.command == "packet":
                protocol = self.args[0]
                target = self.args[1]
                port = int(self.args[2]) if len(self.args)>2 else 0
                flags = self.args[3] if len(self.args)>3 else ""
                payload = self.args[4] if len(self.args)>4 else ""
                utils.packetsender().execute(protocol, target, port, flags, payload)

            elif self.command == "wifi":
                iface = self.args[0] if len(self.args)>0 else "wlan0"
                utils.wifiscanner().execute(iface)

            elif self.command == "netmap":
                net = self.args[0] if len(self.args)>0 else "192.168.1.0/24"
                utils.netmap().execute(net)

            elif self.command == "dashboard":
                utils.dashboard().execute()

            elif self.command == "analyze":
                utils.loganalyzer().execute()

            elif self.command == "geoip":
                self._validate_args(1, "Usage: xnet geoip <IP>")
                utils.geoip().execute(self.args[0])

            elif self.command == "banner":
                self._validate_args(1, "Usage: xnet banner <host> [port]")
                port = int(self.args[1]) if len(self.args)>1 else 80
                utils.bannergrab().execute(self.args[0], port)

            elif self.command == "dnsscan":
                self._validate_args(1, "Usage: xnet dnsscan <domain>")
                utils.dnsscan().execute(self.args[0])

            elif self.command == "macvendor":
                self._validate_args(1, "Usage: xnet macvendor <MAC>")
                utils.macvendor().execute(self.args[0])

            elif self.command == "lanscan":
                net = self.args[0] if self.args else "192.168.1.0/24"
                utils.lanscan().execute(net)

            elif self.command == "ipsweep":
                self._validate_args(1, "Usage: xnet ipsweep <start_ip> [end_ip]")
                end_ip = self.args[1] if len(self.args)>1 else None
                utils.ipsweep().execute(self.args[0], end_ip)

            elif self.command == "latency":
                self._validate_args(1, "Usage: xnet latency <host> [count]")
                cnt = int(self.args[1]) if len(self.args)>1 else 5
                utils.latencytest().execute(self.args[0], cnt)

            elif self.command == "serviceenum":
                self._validate_args(1, "Usage: xnet serviceenum <host> [ports]")
                ports = self.args[1] if len(self.args)>1 else "21,22,80,443"
                utils.serviceenum().execute(self.args[0], ports)

            elif self.command == "sslcert":
                self._validate_args(1, "Usage: xnet sslcert <host> [port]")
                port = int(self.args[1]) if len(self.args)>1 else 443
                utils.sslcert().execute(self.args[0], port)

            elif self.command == "nbtscan":
                self._validate_args(1, "Usage: xnet nbtscan <ip>")
                utils.nbtscan().execute(self.args[0])

            elif self.command == "snmpwalk":
                self._validate_args(1, "Usage: xnet snmpwalk <host> [community]")
                comm = self.args[1] if len(self.args)>1 else "public"
                utils.snmpwalk().execute(self.args[0], comm)

            elif self.command == "multiscan":
                self._validate_args(1, "Usage: xnet multiscan <hosts> [ports]")
                ports = self.args[1] if len(self.args)>1 else "1-1024"
                utils.multiscan().execute(self.args[0], ports)

            elif self.command == "httpget":
                self._validate_args(1, "Usage: xnet httpget <url>")
                utils.httpget().execute(self.args[0])

            elif self.command == "apirequest":
                self._validate_args(2, "Usage: xnet apirequest <method> <url> [json_data]")
                data = self.args[2] if len(self.args)>2 else ""
                utils.apirequest().execute(self.args[0], self.args[1], data)

            elif self.command == "sslscan":
                self._validate_args(1, "Usage: xnet sslscan <host> [port]")
                port = int(self.args[1]) if len(self.args)>1 else 443
                utils.sslscan().execute(self.args[0], port)

            elif self.command == "sslgen":
                self._validate_args(1, "Usage: xnet sslgen <common_name> [days]")
                days = int(self.args[1]) if len(self.args)>1 else 365
                utils.sslgen().execute(self.args[0], days)

            elif self.command == "serve":
                self._validate_args(1, "Usage: xnet serve <directory> [host] [port]")
                host = self.args[1] if len(self.args)>1 else "0.0.0.0"
                port = int(self.args[2]) if len(self.args)>2 else 8000
                utils.fileserver().execute(self.args[0], host, port)

            elif self.command == "sslinfo":
                self._validate_args(1, "Usage: xnet sslinfo <host> [port]")
                port = int(self.args[1]) if len(self.args)>1 else 443
                utils.sslinfo().execute(self.args[0], port)

            elif self.command == "cfg":
                self._validate_args(1, "Usage: xnet cfg <show|get|set> [key] [value]")
                action = self.args[0]
                key = self.args[1] if len(self.args)>1 else ""
                val = self.args[2] if len(self.args)>2 else ""
                utils.configtool().execute(action, key, val)

            elif self.command == "cvescan":
                self._validate_args(1, "Usage: xnet cvescan <host> [start_port] [end_port]")
                sp = int(self.args[1]) if len(self.args)>1 else 1
                ep = int(self.args[2]) if len(self.args)>2 else 1024
                utils.cvescan().execute(self.args[0], sp, ep)

            elif self.command == "netflow":
                iface = self.args[0] if self.args else ""
                utils.netflow().execute(iface)

            elif self.command == "topo":
                self._validate_args(1, "Usage: xnet topo <network/CIDR>")
                utils.topo().execute(self.args[0])

            elif self.command == "plugin":
                self._validate_args(1, "Usage: xnet plugin <list|install|run> [plugin] [args...]")
                action = self.args[0]
                name = self.args[1] if len(self.args)>1 else ""
                utils.pluginmgr().execute(action, name, *self.args[2:])

            elif self.command == "cfgdrift":
                self._validate_args(1, "Usage: xnet cfgdrift <monitor|status>")
                if self.args[0] == "monitor":
                    utils.configdrift().monitor()
                else:
                    utils.configdrift().status()

            elif self.command == "report":
                self._validate_args(1, "Usage: xnet report <html|pdf> [basename]")
                fmt = self.args[0]
                base = self.args[1] if len(self.args) > 1 else "xnet_report"
                utils.reportgen().execute(fmt, base)

            else:
                print(f"Error: Unknown command: {self.command}")
                print("Use 'xnet help' to see available commands")

            self.logger.save_log(f"Command executed: {self.command} {self.args}")
            
        except Exception as e:
            print(f"Error: {str(e)}")
            self.logger.save_log(f"Error executing command {self.command}: {str(e)}", "error")
            
    def _validate_args(self, min_args: int, usage: str) -> None:
        if len(self.args) < min_args:
            print(usage)
            raise SystemExit(1)
            
    def _show_help(self) -> None:
        help_text = """
XNET - Professional Network Toolkit

Available commands:
- help: Show this help message
- ping <hostname/IP>: Check the reachability of a host
- traceroute <hostname/IP>: Trace the route to a host
- lookup <hostname>: DNS lookup for a hostname
- portscan <hostname/IP> [start_port] [end_port]: Scan for open ports
- whois <domain>: Perform a whois lookup on a domain
- ipgeo <IP>: Get geolocation information for an IP address
- macscan [network]: Scan for devices on your network (MAC addresses)
- subnetcalc <network/CIDR>: Calculate subnet information
- speedtest: Test your network speed
- log <view|clear>: View or clear the log file
- update: Check for and install updates
- sniff [interface] [filter] [count]: Sniff network packets
- interfaces: List available network interfaces
- arpwatch [interface] [duration]: Watch for ARP spoofing
- knock <action> [sequence]: Port knocking action
- packet <protocol> <target> [port] [flags] [payload]: Send a custom packet
- wifi [interface]: Scan for WiFi networks
- netmap <network>: Map out a network range
- dashboard: Show network dashboard
- analyze: Analyze logs for insights
- geoip <IP>                       - Lookup geolocation of an IP
- banner <host> [port]             - Grab service banner
- dnsscan <domain>                 - Enumerate DNS records

Professional Network Tools:
  macvendor <MAC>                  - Lookup vendor for MAC address
  lanscan [network/CIDR]           - ARP scan your LAN
  ipsweep <start_ip> [end_ip]      - Ping sweep IP range
  latency <host> [count]           - Measure average latency

Advanced White-Hat Utilities:
- serviceenum <host> [ports]      - Enumerate service banners on ports
- sslcert <host> [port]           - Retrieve SSL certificate details
- nbtscan <ip>                    - NetBIOS name enumeration
- snmpwalk <host> [community]     - SNMP walk OIDs on target

Network & SSL Tools:
- multiscan <hosts> [ports]        - Scan targets (CSV or CIDR) by port range
- httpget <url>                    - HTTP GET with headers/body preview
- apirequest <method> <url> [json] - Generic API call with JSON payload
- sslscan <host> [port]            - Fetch cert, TLS version & cipher
- sslgen <common_name> [days]      - Generate self-signed SSL certificate

Local Hosting & Config:
- serve <dir> [host] [port]    - Serve files from directory
- cfg <show|get|set> [k] [v]   - Show or modify configuration

SSL & Analysis:
- sslinfo <host> [port]        - Detailed cert info & fingerprint

Use 'xnet <command> -h' for details.
"""
        print(help_text)
        self.logger.save_log(f"Help requested for command: {self.command}")
        
    def _exit(self, code: int = 0) -> None:
        self.logger.save_log(f"Session {self.session_id} ended")
        sys.exit(code)
        
def main():
    if len(sys.argv) < 2:
        print("Error: No command provided. Use 'xnet help' for usage.")
        return
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    xnet = XNET(command, args)
    xnet.execute()
    
if __name__ == "__main__":
    main()

