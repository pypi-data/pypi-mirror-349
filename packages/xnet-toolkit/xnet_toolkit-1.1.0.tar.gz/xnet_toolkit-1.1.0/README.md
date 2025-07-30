<!-- Copyright (c) 2025 StasX (Kozosvyst Stas). All rights reserved. -->

# XNET – Professional Network Administration & Security Toolkit

![GitHub](https://img.shields.io/badge/GitHub-StasX--Official/xnet-blue?logo=github)
![Release](https://img.shields.io/badge/release-1.1.0-green)
![Python](https://img.shields.io/badge/python-3.6%2B-blue?logo=python)
![License](https://img.shields.io/badge/license-MIT-blue)

**XNET** is a comprehensive, extensible CLI suite for network diagnostics, security auditing, traffic analysis, and administration. Designed for system administrators, DevOps, security professionals, and network engineers.

---

## 🚀 Quick Start

1. Clone repository  
   ```bash
   git clone https://github.com/StasX-Official/xnet.git
   cd xnet
   ```

2. (Optional) Create a Python virtual environment  
   ```bash
   python3 -m venv venv
   source venv/bin/activate    # Linux / macOS
   venv\Scripts\activate.bat   # Windows
   ```

3. Install dependencies  
   ```bash
   pip install -r requirements.txt
   pip install cryptography requests dnspython scapy netifaces python-iptables graphviz weasyprint
   ```

4. Install XNET CLI  
   ```bash
   pip install .
   ```

5. Verify installation  
   ```bash
   xnet --help
   ```

---

## 🔧 Features

### Core Network Tools
- `ping` – Host reachability  
- `traceroute` – Path discovery  
- `latency` – Average round-trip time  
- `ipsweep` – Ping sweep IP ranges  
- `netmap` – ARP-based network mapping  

### Port & Service Scanning
- `portscan` – TCP port scan (async, rate-limited)  
- `multiscan` – Multi-host port scan via CSV or CIDR  
- `lanscan` – ARP scan for LAN hosts  
- `serviceenum` – Banner grabbing on multiple ports  
- `dnsscan` – Enumerate DNS record types  

### Traffic Analysis & Monitoring
- `sniff` – Live packet capture (Scapy)  
- `arpwatch` – Detect ARP spoofing  
- `netflow` – UDP NetFlow/sFlow listener  
- `dashboard` – Quick summary of devices & ports  

### Security & Audit
- `cvescan` – Query NVD for CVEs on open ports  
- `sslscan` – TLS version, cipher suite & certificate PEM  
- `sslcert` – X.509 certificate details  
- `sslinfo` – Fingerprint, issuer, validity & public key info  

### HTTP & API
- `httpget` – HTTP(S) GET with header/body preview  
- `apirequest` – Generic REST client with JSON payload  

### Packet & Firewall Management
- `packet` – Craft & send custom TCP/UDP/ICMP packets  
- `knock` – Port knocking listener & sender  
- `serve` – Simple HTTP fileserver  

### Configuration & Extensibility
- `cfg` – Show, get or set values in `config.json`  
- `cfgdrift` – Monitor or check config file drift  
- `report` – Generate HTML or PDF report from logs  
- `plugin` – List, install or run external plugins  

---

## 📖 Command Reference

```bash
# Diagnose connectivity
xnet ping <host>
xnet traceroute <host>
xnet latency <host> [count]

# Port scans
xnet portscan <host> [start] [end]
xnet multiscan <hosts> [ports]

# LAN and DNS
xnet lanscan [network/CIDR]
xnet dnsscan <domain>
xnet lookup <hostname>

# Packet capture & ARP monitoring
xnet sniff [iface] [filter] [count]
xnet arpwatch [iface] [duration]

# Security checks
xnet cvescan <host> [start] [end]
xnet sslscan <host> [port]
xnet sslcert <host> [port]
xnet sslinfo <host> [port]

# HTTP & API
xnet httpget <url>
xnet apirequest <METHOD> <url> [json_data]

# Custom packets & firewall
xnet packet <tcp|udp|icmp> <target> [port] [flags] [payload]
xnet knock <start|list|send> [sequence]
xnet serve <dir> [host] [port]

# Configuration & Logs
xnet cfg show|get|set [key] [value]
xnet cfgdrift monitor|status
xnet report <html|pdf> [basename]
xnet log view|clear

# Plugin system
xnet plugin list|install|run [name] [args...]

# Help & interactive
xnet help
xnet interactive
```

---

## 💡 Examples

- **Scan localhost TCP ports 1–100**  
  `xnet portscan 127.0.0.1 1 100`

- **Sweep an IP range**  
  `xnet ipsweep 192.168.1.1 192.168.1.254`

- **Capture 500 packets on eth0**  
  `xnet sniff eth0 "" 500`

- **Detect ARP spoof attempts for 5 minutes**  
  `xnet arpwatch eth0 300`

- **Query HTTP headers and body**  
  `xnet httpget https://example.com`

- **Send custom TCP SYN to port 22**  
  `xnet packet tcp 192.168.1.100 22 S "Hello"`

- **Generate PDF report from logs**  
  `xnet report pdf my-report`

---

## ⚙️ Configuration

All settings stored in `xnet_system/config.json`:

```json
{
  "version": "1.1.0",
  "max_ports": 500,
  "async_threads": 50,
  "security": { ... },
  "advanced_features": {
    "packet_sniffer": { "max_capture_time": 60, "max_packets": 1000 },
    "arp_watch":     { "monitoring_time": 300 },
    "port_knock":    { "sequences": { ... }, "open_port": 22 },
    "packet_sender": { "default_ttl": 64, "max_payload_size": 1024 }
  }
}
```

Use `xnet cfg` to view or update values without editing manually.

---

## 🧩 Plugins

1. Place your plugin Python file under  
   `xnet_system/plugins/<name>.py`

2. Implement a `main(*args)` function.

3. List available plugins:  
   `xnet plugin list`

4. Run a plugin:  
   `xnet plugin run <name> [args...]`

---

## 🛠 Interactive Mode & Autocomplete

Enable shell completion in **bash**:
```bash
source bash_completion.sh
```
Start interactive session:
```bash
xnet interactive
```
Use **Tab** for commands and parameters, **Ctrl+C** to exit.

---

## 🆘 Troubleshooting & Support

- Check logs at `~/.xnet/logs/xnet.log`
- Common issues: missing privileges, firewall blocking, module imports

**Email**: xnet@sxservisecli.tech  
**GitHub Issues**: https://github.com/StasX-Official/xnet/issues

---

## 📜 License

This project is released under the [MIT License](LICENSE).  
© 2025 StasX (Kozosvyst Stas). All rights reserved.
