# Copyright (c) 2025 StasX (Kozosvyst Stas). All rights reserved.

#!/usr/bin/env python3
import sys
import os
import signal
import ssl
import readline
import rlcompleter
from typing import List, Optional, Dict, Any
from xnet_system.main import XNET
from xnet_system.tools import managers
from xnet_system.security import sanitize_input
import tkinter as _tk
from tkinter import filedialog as _fd

VERSION = "1.0.0"

def signal_handler(sig, frame):
    print("\nOperation cancelled by user.")
    sys.exit(0)

def setup_ssl_context():
    try:
        context = ssl.create_default_context()
        
        context.options |= ssl.OP_NO_SSLv2
        context.options |= ssl.OP_NO_SSLv3
        context.options |= ssl.OP_NO_TLSv1
        context.options |= ssl.OP_NO_TLSv1_1
        
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        
        ssl._create_default_https_context = lambda: context
    except Exception:
        pass

def validate_environment() -> bool:
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        if os.name != 'nt':
            dir_stat = os.stat(current_dir)
            if dir_stat.st_mode & 0o007:
                print("Warning: Running from an insecure directory")
                return False
            
        suspicious_vars = ['LD_PRELOAD', 'LD_LIBRARY_PATH', 'PYTHONPATH']
        for var in suspicious_vars:
            if var in os.environ:
                print(f"Warning: Potentially unsafe environment variable set: {var}")
                return False
        
        return True
    except Exception:
        return True

def interactive_mode():
    cmds = ['help','ping','traceroute','lookup','portscan','whois','ipgeo',
            'macscan','subnetcalc','speedtest','log','update','sniff',
            'interfaces','arpwatch','knock','packet','wifi','netmap',
            'dashboard','analyze','geoip','banner','dnsscan','macvendor',
            'lanscan','ipsweep','latency','serviceenum','sslcert','nbtscan',
            'snmpwalk','multiscan','httpget','apirequest','sslscan','sslgen',
            'serve','sslinfo','cfg','cvescan','netflow','topo','plugin',
            'cfgdrift','report','exit','quit']
    def completer(text, state):
        options = [c for c in cmds if c.startswith(text)]
        return options[state] if state < len(options) else None

    readline.set_completer(completer)
    readline.parse_and_bind('tab: complete')
    while True:
        try:
            line = input('xnet> ').strip()
            if not line: continue
            if line in ('exit','quit'): break
            parts = line.split()
            XNET(parts[0], parts[1:]).execute()
        except (EOFError, KeyboardInterrupt):
            print()
            break

def main() -> None:
    signal.signal(signal.SIGINT, signal_handler)
    setup_ssl_context()
    validate_environment()
    
    logger = None
    
    try:
        export_flag = False
        if "--export" in sys.argv:
            export_flag = True
            sys.argv.remove("--export")
            
        command = sys.argv[1].lower() if len(sys.argv) > 1 else "help"
        advanced_commands = ["sniff", "arpwatch", "knock", "packet"]
        
        if command in advanced_commands and not _check_admin():
            print("Warning: Advanced network features require administrative privileges.")
            print("Some functionality may be limited.")
            
        config_manager = managers.config()
        config = config_manager.load_config()
        logger = managers.loggining()
        
        if len(sys.argv) == 1:
            print(f"XNET v{VERSION} (Stable)")
            print("© 2025 StasX (Kozosvyst Stas). All rights reserved.")
            return
        
        if len(sys.argv) > 1:
            command = sanitize_input(sys.argv[1].lower())
        else:
            command = "help"
            
        args = []
        if len(sys.argv) > 2:
            args = [sanitize_input(arg) for arg in sys.argv[2:]]
        
        logger.save_log(f"Command executed: {command}")
        
        xnet = XNET(command, args)
        xnet.execute()
        
        if export_flag and logger:
            _export_logs(logger)

    except KeyboardInterrupt:
        print("\nOperation canceled by user")
        if logger:
            logger.save_log("Operation canceled by user", "warning")
        sys.exit(1)
    except SystemExit:
        raise
    except Exception as e:
        print(f"Error: An unexpected error occurred")
        if logger:
            logger.save_log(f"Unhandled error: {str(e)}", "error")
        sys.exit(1)
    finally:
        pass

def _export_logs(logger):
    root = _tk.Tk(); root.withdraw()
    path = _fd.asksaveasfilename(
        title="Export Logs",
        defaultextension=".txt",
        filetypes=[("Text","*.txt"), ("HTML","*.html")]
    )
    if not path: 
        return
    logs = logger.read_log()
    if path.lower().endswith('.html'):
        html = "<html><body><h1>XNET Logs</h1><pre>" + "\n".join(logs) + "</pre></body></html>"
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(logs))
    print(f"Exported logs to {path}")

def _check_admin():
    try:
        if os.name == 'nt':
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.geteuid() == 0
    except:
        return False

if __name__ == "__main__":
    main()
