#!/usr/bin/env python3
# ============================================================================
#               WIFICRACY: AUTONOMOUS ZERO-INTERACTION COMMAND ENGINE
# ============================================================================
import sys
import os
import time
import subprocess

def display_engine_banner():
    print("====================================================")
    print("          WIFICRACY: AUTOMATED MULTI-ENGINE SYSTEM   ")
    print("====================================================")

def enforce_managed_mode(interface):
    print(f"[*] Cycling driver logic to Managed Mode for {interface}...")
    subprocess.run(["sudo", "ip", "link", "set", interface, "down"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["sudo", "iw", "dev", interface, "set", "type", "managed"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", interface, "up"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def execute_automated_pipeline(interface):
    display_engine_banner()
    
    print("[*] Flushing local socket workspaces and background caches...")
    subprocess.run(["sudo", "pkill", "-f", "dns_server.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["sudo", "pkill", "-f", "server.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    target_ssid = "Starbucks_WiFi"
    target_template = "starbucks"
    print(f"[+] Autopilot Target Active -> SSID: {target_ssid} | Portal: {target_template}")
    
    enforce_managed_mode(interface)
    
    print("\n[+] Initializing Independent Custom Server Daemons...")
    time.sleep(1)
    
    dns_proc = subprocess.Popen(["sudo", "python3", "/home/kali/wificracy/dns_server.py"],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                                
    web_proc = subprocess.Popen(["sudo", "python3", "/home/kali/wificracy/server.py"],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                                
    print("[+] Py_DNS Interceptor running in background (UDP 53)")
    print("[+] Web Portal Server running in background (TCP 80)")
    print("\n[!] Pipeline established completely on autopilot. Press Ctrl+C to stop.\n")
    
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n[*] Intercepted Break. Flushing custom local servers...")
            dns_proc.terminate()
            web_proc.terminate()
            subprocess.run(["sudo", "pkill", "-f", "dns_server.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["sudo", "pkill", "-f", "server.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["sudo", "systemctl", "start", "NetworkManager"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("[+] System environment sanitized successfully.")
            break

if __name__ == "__main__":
    if os.getuid() != 0:
        print("[-] Critical Privilege Error: Root privileges required (sudo).")
        sys.exit(1)
    if len(sys.argv) < 2:
        print("Usage: sudo wificracy <interface>")
        sys.exit(1)
    
    execute_automated_pipeline(sys.argv[1])
  
